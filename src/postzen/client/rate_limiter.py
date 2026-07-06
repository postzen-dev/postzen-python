"""Rate-limit response header parsing."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass
class RateLimitInfo:
    """Rate-limit information from PostZen response headers."""

    limit: int | None = None
    remaining: int | None = None
    reset: datetime | None = None

    @property
    def is_exhausted(self) -> bool:
        return self.remaining is not None and self.remaining <= 0

    @property
    def seconds_until_reset(self) -> float | None:
        if self.reset is None:
            return None
        return max(0.0, (self.reset - datetime.now()).total_seconds())


class RateLimiter:
    """Tracks rate-limit state from API response headers."""

    def __init__(self) -> None:
        self._info = RateLimitInfo()

    @property
    def info(self) -> RateLimitInfo:
        return self._info

    @property
    def limit(self) -> int | None:
        return self._info.limit

    @property
    def remaining(self) -> int | None:
        return self._info.remaining

    @property
    def reset_time(self) -> datetime | None:
        return self._info.reset

    def update_from_headers(self, headers: Mapping[str, str]) -> None:
        limit_str = headers.get("X-RateLimit-Limit")
        remaining_str = headers.get("X-RateLimit-Remaining")
        reset_str = headers.get("X-RateLimit-Reset")

        if limit_str is not None:
            with contextlib.suppress(ValueError):
                self._info.limit = int(limit_str)
        if remaining_str is not None:
            with contextlib.suppress(ValueError):
                self._info.remaining = int(remaining_str)
        if reset_str is not None:
            with contextlib.suppress(OSError, ValueError):
                self._info.reset = datetime.fromtimestamp(int(reset_str))

    def should_wait(self) -> bool:
        return self._info.is_exhausted

    def get_wait_time(self) -> float:
        if not self._info.is_exhausted:
            return 0.0
        seconds = self._info.seconds_until_reset
        return 60.0 if seconds is None else seconds + 1.0
