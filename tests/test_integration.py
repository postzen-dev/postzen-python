"""Mocked integration tests for generated resources."""

from __future__ import annotations

import json

import httpx
import respx


@respx.mock
def test_profiles_crud(client, base_url: str, profile_payload: dict) -> None:
    list_route = respx.get(f"{base_url}/v1/profiles").mock(
        return_value=httpx.Response(200, json={"profiles": [profile_payload]})
    )
    create_route = respx.post(f"{base_url}/v1/profiles").mock(
        return_value=httpx.Response(201, json={"message": "Profile created", "profile": profile_payload})
    )
    get_route = respx.get(f"{base_url}/v1/profiles/prof_123").mock(
        return_value=httpx.Response(200, json={"profile": profile_payload})
    )
    update_route = respx.put(f"{base_url}/v1/profiles/prof_123").mock(
        return_value=httpx.Response(200, json={"message": "Profile updated", "profile": profile_payload})
    )
    delete_route = respx.delete(f"{base_url}/v1/profiles/prof_123").mock(
        return_value=httpx.Response(200, json={"message": "Profile deleted"})
    )

    listed = client.profiles.list_profiles()
    created = client.profiles.create_profile(name="Main", description="Primary", color="#ffeda0")
    fetched = client.profiles.get_profile("prof_123")
    updated = client.profiles.update_profile("prof_123", is_default=True)
    deleted = client.profiles.delete_profile("prof_123")

    assert list_route.called
    assert listed.profiles[0].field_id == "prof_123"
    assert created.profile.field_id == "prof_123"
    assert fetched.profile.field_id == "prof_123"
    assert updated.profile.field_id == "prof_123"
    assert deleted.message == "Profile deleted"
    assert json.loads(create_route.calls[0].request.content)["description"] == "Primary"
    assert json.loads(update_route.calls[0].request.content)["isDefault"] is True
    assert get_route.called
    assert delete_route.called


@respx.mock
def test_accounts_resource(client, base_url: str, account_payload: dict) -> None:
    list_route = respx.get(f"{base_url}/v1/accounts").mock(
        return_value=httpx.Response(
            200,
            json={
                "accounts": [account_payload],
                "pagination": {"page": 1, "limit": 10, "total": 1, "totalPages": 1},
            },
        )
    )
    disconnect_route = respx.delete(f"{base_url}/v1/accounts/acc_123").mock(
        return_value=httpx.Response(200, json={"message": "Account disconnected"})
    )

    accounts = client.accounts.list_accounts(profile_id="prof_123", platform="instagram", page=2)
    disconnected = client.accounts.disconnect_account("acc_123")

    assert accounts.accounts[0].field_id == "acc_123"
    assert disconnected.message == "Account disconnected"
    url = str(list_route.calls[0].request.url)
    assert "profileId=prof_123" in url
    assert "platform=instagram" in url
    assert "page=2" in url
    assert disconnect_route.called


@respx.mock
def test_connect_resource(client, base_url: str, account_payload: dict) -> None:
    start_route = respx.get(f"{base_url}/v1/connect/instagram").mock(
        return_value=httpx.Response(200, json={"authUrl": "https://oauth.example.com", "state": "state_123"})
    )
    complete_route = respx.post(f"{base_url}/v1/connect/instagram").mock(
        return_value=httpx.Response(
            200,
            json={
                "message": "Connected",
                "platform": "instagram",
                "profileId": "prof_123",
                "status": "connected",
                "accounts": [account_payload],
            },
        )
    )

    started = client.connect.create_connect_url("instagram", profile_id="prof_123")
    completed = client.connect.complete_connect(
        "instagram",
        code="code_123",
        state="state_123",
        profile_id="prof_123",
    )

    assert started.state == "state_123"
    assert completed.status == "connected"
    assert "profileId=prof_123" in str(start_route.calls[0].request.url)
    assert json.loads(complete_route.calls[0].request.content)["profileId"] == "prof_123"


@respx.mock
def test_media_resource(client, base_url: str) -> None:
    route = respx.post(f"{base_url}/v1/media/presign").mock(
        return_value=httpx.Response(
            200,
            json={
                "uploadUrl": "https://uploads.example.com/object",
                "publicUrl": "https://cdn.example.com/object",
                "key": "object",
                "type": "image",
            },
        )
    )

    result = client.media.create_media_presign(
        filename="image.png",
        content_type="image/png",
        size=123,
        profile_id="prof_123",
    )

    body = json.loads(route.calls[0].request.content)
    assert body["contentType"] == "image/png"
    assert body["profileId"] == "prof_123"
    assert result.publicUrl == "https://cdn.example.com/object"


@respx.mock
def test_posts_resource(client, base_url: str, api_post_payload: dict) -> None:
    route = respx.post(f"{base_url}/v1/posts").mock(
        return_value=httpx.Response(
            201,
            json={"message": "Post published successfully", "post": api_post_payload},
        )
    )

    result = client.posts.create_post(
        content="Publishing from PostZen",
        platforms=[{"platform": "instagram", "accountId": "acc_123"}],
        publish_now=True,
        x_request_id="request_123",
    )

    body = json.loads(route.calls[0].request.content)
    assert body["publishNow"] is True
    assert route.calls[0].request.headers["x-request-id"] == "request_123"
    assert result.post.field_id == "post_123"


@respx.mock
async def test_async_profiles_and_posts(client, base_url: str, profile_payload: dict, api_post_payload: dict) -> None:
    respx.get(f"{base_url}/v1/profiles").mock(
        return_value=httpx.Response(200, json={"profiles": [profile_payload]})
    )
    respx.post(f"{base_url}/v1/posts").mock(
        return_value=httpx.Response(
            201,
            json={"message": "Post published successfully", "post": api_post_payload},
        )
    )

    profiles = await client.profiles.alist_profiles()
    post = await client.posts.acreate_post(content="Async", publish_now=True)

    assert profiles.profiles[0].field_id == "prof_123"
    assert post.post.field_id == "post_123"
