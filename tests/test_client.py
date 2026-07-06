"""Client behavior tests."""

from __future__ import annotations

import httpx
import pytest
import respx

from postzen import PostZen
from postzen.client.base import BaseClient


def test_missing_api_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("POSTZEN_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key is required"):
        PostZen()


def test_env_api_key_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("POSTZEN_API_KEY", "env_key")
    client = PostZen()
    assert client.api_key == "env_key"


def test_explicit_arg_wins_over_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("POSTZEN_API_KEY", "env_key")
    client = PostZen(api_key="explicit_key")
    assert client.api_key == "explicit_key"


def test_user_agent_header_contains_sdk_name(api_key: str) -> None:
    client = BaseClient(api_key)
    assert "postzen-python-sdk/" in client._headers["User-Agent"]


@respx.mock
def test_authorization_header_sent(client: PostZen, base_url: str) -> None:
    route = respx.get(f"{base_url}/v1/profiles").mock(
        return_value=httpx.Response(200, json={"profiles": []})
    )
    client.profiles.list_profiles()
    assert route.calls[0].request.headers["Authorization"] == "Bearer postzen_test_key"
    assert "postzen-python-sdk/" in route.calls[0].request.headers["User-Agent"]


def test_base_url_override(api_key: str) -> None:
    client = PostZen(api_key=api_key, base_url="https://custom.example.com/")
    assert client.base_url == "https://custom.example.com"


@respx.mock
def test_two_client_isolation(profile_payload: dict) -> None:
    first = PostZen(api_key="first", base_url="https://first.example.com")
    second = PostZen(api_key="second", base_url="https://second.example.com")
    first_route = respx.get("https://first.example.com/v1/profiles").mock(
        return_value=httpx.Response(200, json={"profiles": [profile_payload]})
    )
    second_route = respx.get("https://second.example.com/v1/profiles").mock(
        return_value=httpx.Response(200, json={"profiles": []})
    )

    first.profiles.list_profiles()
    second.profiles.list_profiles()

    assert first_route.calls[0].request.headers["Authorization"] == "Bearer first"
    assert second_route.calls[0].request.headers["Authorization"] == "Bearer second"


def test_sync_context_manager(api_key: str) -> None:
    with PostZen(api_key=api_key) as client:
        assert callable(client.profiles.list_profiles)


async def test_async_context_manager(api_key: str) -> None:
    async with PostZen(api_key=api_key) as client:
        assert callable(client.posts.acreate_post)
