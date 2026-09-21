"""Check the SDK surface directly against the specification."""

from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

import httpx
import pytest
import respx
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from generate_resources import validate_client_resources
from resource_map import camel_to_snake, description, display_name, resource_key, resource_order

ROOT = Path(__file__).resolve().parents[1]


def test_generated_surface(client):
    spec = json.loads((ROOT / "openapi.json").read_text())
    tagged = [
        operation
        for path_item in spec["paths"].values()
        for method, operation in path_item.items()
        if method in {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
        and operation.get("tags")
    ]
    seen = 0
    for operation in tagged:
        for tag in operation["tags"]:
            resource = getattr(client, resource_key(tag))
            name = camel_to_snake(operation["operationId"])
            assert callable(getattr(resource, name))
            assert callable(getattr(resource, "a" + name))
        seen += 1
    assert seen == len(tagged)


@pytest.mark.parametrize("tag, expected", [
    ("Comment Automations", "comment_automations"),
    ("API Keys", "api_keys"),
    ("Profiles", "profiles"),
    ("123 strange--tag!", "_123_strange_tag"),
    ("class", "class_"),
    ("!!!", "resource"),
])
def test_resource_key(tag, expected):
    assert resource_key(tag) == expected
    assert resource_key(tag).isidentifier()


def test_resource_order_and_descriptions():
    spec = {
        "tags": [{"name": "Unused"}, {"name": "New", "description": "First sentence. Second sentence."}],
        "paths": {"/test": {"get": {"tags": ["Undeclared", "New", "Posts", "Profiles"]}}},
    }
    assert resource_order(spec) == [
        ("Profiles", "profiles"), ("Posts", "posts"), ("New", "new"), ("Undeclared", "undeclared"),
    ]
    assert description(spec, "New") == "First sentence"
    assert description(spec, "Profiles") == "Manage PostZen profiles"
    assert description(spec, "Undeclared") == "Undeclared"
    assert display_name("Connect") == "Connect (OAuth)"
    assert camel_to_snake("class") == "class_"
    assert camel_to_snake("getAPIKey") == "get_api_key"


def test_untagged_operations_fail_together():
    spec = {"paths": {
        "/one": {"get": {"operationId": "one"}},
        "/two": {"post": {"operationId": "two", "tags": []}},
    }}
    with pytest.raises(SystemExit) as exc:
        resource_order(spec)
    assert "GET /one (one)" in str(exc.value)
    assert "POST /two (two)" in str(exc.value)


def test_resource_key_collisions_fail():
    with pytest.raises(SystemExit, match="Resource key collision"):
        resource_order({"paths": {"/test": {"get": {"tags": ["A B", "A-B"]}}}})


@pytest.mark.parametrize("key", ["timeout", "base_url", "rate_limit_info"])
def test_client_attribute_collisions_fail(key):
    with pytest.raises(SystemExit, match=key):
        validate_client_resources(ROOT, [key])


@respx.mock
@pytest.mark.parametrize("is_async", [False, True])
async def test_generated_patch_with_inline_response(client, base_url, is_async):
    response = {"contact": {"id": "contact_123", "name": "Updated"}}
    route = respx.patch(f"{base_url}/v1/contacts/contact_123").mock(
        return_value=httpx.Response(200, json=response)
    )
    if is_async:
        result = await client.contacts.aupdate_contact("contact_123", name="Updated")
    else:
        result = client.contacts.update_contact("contact_123", name="Updated")
    assert result == response
    assert json.loads(route.calls[0].request.content)["name"] == "Updated"
    assert route.calls[0].request.headers["Authorization"] == "Bearer postzen_test_key"


@respx.mock
@pytest.mark.parametrize("is_async", [False, True])
async def test_get_post_returns_raw_dict(client, base_url, api_post_payload, is_async):
    # Regression: 2.0.0 called dict[str, Any].model_validate() here and raised AttributeError.
    respx.get(f"{base_url}/v1/posts/post_123").mock(
        return_value=httpx.Response(200, json={"post": api_post_payload})
    )
    result = await client.posts.aget_post("post_123") if is_async else client.posts.get_post("post_123")
    assert result == {"post": api_post_payload}


@respx.mock
def test_delete_post_returns_raw_dict(client, base_url):
    respx.delete(f"{base_url}/v1/posts/post_123").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    assert client.posts.delete_post("post_123") == {"success": True}


@respx.mock
@pytest.mark.parametrize(
    "method, path, call, expected",
    [
        ("patch", "/v1/contacts/contact_123", lambda c: c.contacts.update_contact("contact_123", name="Ada"), {"name": "Ada"}),
        ("put", "/v1/posts/post_123", lambda c: c.posts.update_post("post_123", title="Renamed"), {"title": "Renamed"}),
        (
            "patch",
            "/v1/comment-automations/auto_123",
            lambda c: c.comment_automations.update_comment_automation("auto_123", name="Renamed"),
            {"name": "Renamed"},
        ),
    ],
)
def test_partial_updates_send_only_explicit_fields(client, base_url, method, path, call, expected):
    # Regression: spec defaults (isBlocked=false, content="", keywords=[]...) used to be
    # sent on every update, overwriting stored values the caller never mentioned.
    route = getattr(respx, method)(f"{base_url}{path}").mock(return_value=httpx.Response(200, json={}))
    # The empty body fails typed-response validation; only the outgoing payload matters here.
    with contextlib.suppress(ValidationError):
        call(client)
    assert json.loads(route.calls[0].request.content) == expected
