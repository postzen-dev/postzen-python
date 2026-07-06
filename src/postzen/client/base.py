"""Base HTTP client with sync and async request support."""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager, contextmanager
from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING, Any

import httpx

from .exceptions import (
    PostZenAPIError,
    PostZenAuthenticationError,
    PostZenConnectionError,
    PostZenForbiddenError,
    PostZenNotFoundError,
    PostZenPaymentRequiredError,
    PostZenRateLimitError,
    PostZenTimeoutError,
)
from .rate_limiter import RateLimiter

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator, Mapping


def _resolve_sdk_version() -> str:
    try:
        return version("postzen-sdk")
    except PackageNotFoundError:
        return "0.0.0+unknown"


# Methods safe to retry after a read/write/pool timeout. A timeout on these is
# idempotent: replaying the request cannot create a second server-side resource.
# POST is deliberately excluded — a read-timeout on POST /v1/posts may have already
# created the post, so an automatic retry risks silently double-posting. The SDK
# does not auto-send x-request-id, so POST timeouts surface immediately instead.
_IDEMPOTENT_METHODS = frozenset({"GET", "PUT", "DELETE"})


class BaseClient:
    """Base PostZen HTTP client."""

    DEFAULT_BASE_URL = "https://api.postzen.dev"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3
    SDK_VERSION = _resolve_sdk_version()

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._rate_limiter = RateLimiter()
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"postzen-python-sdk/{self.SDK_VERSION}",
        }

    @property
    def rate_limit_info(self) -> dict[str, Any]:
        info = self._rate_limiter.info
        return {
            "limit": info.limit,
            "remaining": info.remaining,
            "reset": info.reset.isoformat() if info.reset else None,
        }

    @contextmanager
    def _sync_client(self) -> Iterator[httpx.Client]:
        client = httpx.Client(
            base_url=self.base_url,
            headers=self._headers,
            timeout=self.timeout,
        )
        try:
            yield client
        finally:
            client.close()

    @asynccontextmanager
    async def _async_client(self) -> AsyncIterator[httpx.AsyncClient]:
        client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._headers,
            timeout=self.timeout,
        )
        try:
            yield client
        finally:
            await client.aclose()

    def _error_data(self, response: httpx.Response) -> dict[str, Any]:
        if not response.content:
            return {}
        try:
            data = response.json()
        except ValueError:
            return {"error": response.text}
        return data if isinstance(data, dict) else {"error": str(data)}

    def _error_message(self, data: dict[str, Any], fallback: str) -> str:
        value = data.get("error") or data.get("message") or fallback
        return str(value)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        self._rate_limiter.update_from_headers(response.headers)

        if response.status_code < 400:
            if response.content:
                data = response.json()
                return data if isinstance(data, dict) else {"data": data}
            return {}

        error_data = self._error_data(response)
        message = self._error_message(error_data, f"HTTP {response.status_code}")

        if response.status_code == 401:
            raise PostZenAuthenticationError(message, details=error_data)
        if response.status_code == 402:
            raise PostZenPaymentRequiredError(message, details=error_data)
        if response.status_code == 403:
            raise PostZenForbiddenError(message, details=error_data)
        if response.status_code == 404:
            raise PostZenNotFoundError(message, details=error_data)
        if response.status_code == 429:
            raise PostZenRateLimitError(
                message,
                reset_time=self._rate_limiter.reset_time,
                limit=self._rate_limiter.limit,
                remaining=self._rate_limiter.remaining,
                details=error_data,
            )

        raise PostZenAPIError(message, status_code=response.status_code, details=error_data)

    def _request_with_retry(
        self,
        client: httpx.Client,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                response = client.request(method, path, **kwargs)
                return self._handle_response(response)
            except PostZenAPIError:
                raise
            except httpx.ConnectTimeout as exc:
                # Pre-send timeout (connection never established) — safe to retry
                # for any method, including POST.
                last_error = PostZenTimeoutError(f"Request timed out: {exc}")
            except httpx.TimeoutException as exc:
                # Read/write/pool timeout: the request may already have reached the
                # server. Retry only idempotent methods; for POST, surface immediately
                # so an unacknowledged create is not silently duplicated.
                if method.upper() not in _IDEMPOTENT_METHODS:
                    raise PostZenTimeoutError(f"Request timed out: {exc}") from exc
                last_error = PostZenTimeoutError(f"Request timed out: {exc}")
            except httpx.ConnectError as exc:
                # Connection never established — always safe to retry.
                last_error = PostZenConnectionError(f"Connection failed: {exc}")

            if attempt < self.max_retries - 1:
                time.sleep((2**attempt) * 0.5)

        if last_error:
            raise last_error
        raise PostZenAPIError("Request failed after retries")

    async def _arequest_with_retry(
        self,
        client: httpx.AsyncClient,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                response = await client.request(method, path, **kwargs)
                return self._handle_response(response)
            except PostZenAPIError:
                raise
            except httpx.ConnectTimeout as exc:
                # Pre-send timeout (connection never established) — safe to retry
                # for any method, including POST.
                last_error = PostZenTimeoutError(f"Request timed out: {exc}")
            except httpx.TimeoutException as exc:
                # Read/write/pool timeout: the request may already have reached the
                # server. Retry only idempotent methods; for POST, surface immediately
                # so an unacknowledged create is not silently duplicated.
                if method.upper() not in _IDEMPOTENT_METHODS:
                    raise PostZenTimeoutError(f"Request timed out: {exc}") from exc
                last_error = PostZenTimeoutError(f"Request timed out: {exc}")
            except httpx.ConnectError as exc:
                # Connection never established — always safe to retry.
                last_error = PostZenConnectionError(f"Connection failed: {exc}")

            if attempt < self.max_retries - 1:
                await asyncio.sleep((2**attempt) * 0.5)

        if last_error:
            raise last_error
        raise PostZenAPIError("Request failed after retries")

    def _merge_headers(self, headers: Mapping[str, str] | None) -> dict[str, str] | None:
        if not headers:
            return None
        return {**self._headers, **dict(headers)}

    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        with self._sync_client() as client:
            return self._request_with_retry(
                client,
                "GET",
                path,
                params=params,
                headers=self._merge_headers(headers),
            )

    def _post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        with self._sync_client() as client:
            return self._request_with_retry(
                client,
                "POST",
                path,
                json=data,
                params=params,
                headers=self._merge_headers(headers),
            )

    def _put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        with self._sync_client() as client:
            return self._request_with_retry(
                client,
                "PUT",
                path,
                json=data,
                params=params,
                headers=self._merge_headers(headers),
            )

    def _delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        with self._sync_client() as client:
            return self._request_with_retry(
                client,
                "DELETE",
                path,
                params=params,
                headers=self._merge_headers(headers),
            )

    async def _aget(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client,
                "GET",
                path,
                params=params,
                headers=self._merge_headers(headers),
            )

    async def _apost(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client,
                "POST",
                path,
                json=data,
                params=params,
                headers=self._merge_headers(headers),
            )

    async def _aput(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client,
                "PUT",
                path,
                json=data,
                params=params,
                headers=self._merge_headers(headers),
            )

    async def _adelete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        async with self._async_client() as client:
            return await self._arequest_with_retry(
                client,
                "DELETE",
                path,
                params=params,
                headers=self._merge_headers(headers),
            )
