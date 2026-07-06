"""Error mapping and retry tests."""

from __future__ import annotations

import httpx
import pytest
import respx

from postzen.client.exceptions import (
    PostZenAPIError,
    PostZenAuthenticationError,
    PostZenForbiddenError,
    PostZenNotFoundError,
    PostZenPaymentRequiredError,
    PostZenRateLimitError,
    PostZenTimeoutError,
)


@pytest.mark.parametrize(
    ("status_code", "exception_type"),
    [
        (401, PostZenAuthenticationError),
        (402, PostZenPaymentRequiredError),
        (403, PostZenForbiddenError),
        (404, PostZenNotFoundError),
        (429, PostZenRateLimitError),
        (500, PostZenAPIError),
    ],
)
@respx.mock
def test_http_errors_map_to_exceptions(client, base_url: str, status_code: int, exception_type: type[Exception]) -> None:
    headers = {
        "X-RateLimit-Limit": "100",
        "X-RateLimit-Remaining": "0",
        "X-RateLimit-Reset": "1767225600",
    }
    route = respx.get(f"{base_url}/v1/profiles").mock(
        return_value=httpx.Response(
            status_code,
            json={"error": "Nope", "code": "testCode"},
            headers=headers,
        )
    )

    with pytest.raises(exception_type) as exc_info:
        client.profiles.list_profiles()

    assert route.call_count == 1
    if status_code == 429:
        exc = exc_info.value
        assert isinstance(exc, PostZenRateLimitError)
        assert exc.limit == 100
        assert exc.remaining == 0
        assert exc.reset_time is not None
        assert client.rate_limit_info["limit"] == 100
        assert client.rate_limit_info["remaining"] == 0


@respx.mock
def test_timeout_retries_then_raises(base_url: str) -> None:
    from postzen import PostZen

    client = PostZen(api_key="x", base_url=base_url, max_retries=3)
    route = respx.get(f"{base_url}/v1/profiles").mock(
        side_effect=httpx.TimeoutException("timed out")
    )

    with pytest.raises(PostZenTimeoutError):
        client.profiles.list_profiles()

    assert route.call_count == 3


@respx.mock
def test_post_read_timeout_is_not_retried(base_url: str) -> None:
    """A read-timeout on POST may have already created the resource server-side,
    so it must surface immediately rather than auto-retry and risk a duplicate."""
    from postzen import PostZen

    client = PostZen(api_key="x", base_url=base_url, max_retries=3)
    route = respx.post(f"{base_url}/v1/posts").mock(
        side_effect=httpx.ReadTimeout("read timed out")
    )

    with pytest.raises(PostZenTimeoutError):
        client.posts.create_post(content="Hello", publish_now=True)

    assert route.call_count == 1


@respx.mock
def test_post_connect_timeout_still_retries(base_url: str) -> None:
    """A ConnectTimeout is pre-send (no request reached the server), so it is safe
    to retry even for POST — the request is exhausted across max_retries attempts."""
    from postzen import PostZen

    client = PostZen(api_key="x", base_url=base_url, max_retries=3)
    route = respx.post(f"{base_url}/v1/posts").mock(
        side_effect=httpx.ConnectTimeout("connect timed out")
    )

    with pytest.raises(PostZenTimeoutError):
        client.posts.create_post(content="Hello", publish_now=True)

    assert route.call_count == 3


@respx.mock
def test_authentication_error_is_not_retried(client, base_url: str) -> None:
    route = respx.get(f"{base_url}/v1/profiles").mock(
        return_value=httpx.Response(401, json={"error": "Invalid API key"})
    )

    with pytest.raises(PostZenAuthenticationError):
        client.profiles.list_profiles()

    assert route.call_count == 1
