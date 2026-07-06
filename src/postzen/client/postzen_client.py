"""Main PostZen API client."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ..resources import (
    AccountsResource,
    ConnectResource,
    MediaResource,
    PostsResource,
    ProfilesResource,
)
from .base import BaseClient

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self


class PostZen(BaseClient):
    """PostZen API client."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        resolved = api_key or os.environ.get("POSTZEN_API_KEY")
        if not resolved:
            raise ValueError(
                "API key is required. Pass api_key= or set the POSTZEN_API_KEY environment variable."
            )
        super().__init__(resolved, base_url=base_url, timeout=timeout, max_retries=max_retries)

        # --- auto-registered resources (do not edit) ---
        self.profiles = ProfilesResource(self)
        self.accounts = AccountsResource(self)
        self.connect = ConnectResource(self)
        self.media = MediaResource(self)
        self.posts = PostsResource(self)
        # --- end auto-registered resources ---

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return None
