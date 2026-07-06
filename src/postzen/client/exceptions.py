"""Custom exceptions for the PostZen SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


class PostZenError(Exception):
    """Base exception for PostZen SDK errors."""


class PostZenAPIError(PostZenError):
    """Exception raised for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        prefix = f"[{self.status_code}] " if self.status_code else ""
        code = self.details.get("code") if self.details else None
        suffix = f" (code: {code})" if code else ""
        return f"{prefix}{self.message}{suffix}"


class PostZenAuthenticationError(PostZenAPIError):
    """Exception raised for authentication errors (401)."""

    def __init__(self, message: str = "Authentication failed", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=401, details=details)


class PostZenPaymentRequiredError(PostZenAPIError):
    """Exception raised when payment is required (402)."""

    def __init__(self, message: str = "Payment required", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=402, details=details)


class PostZenForbiddenError(PostZenAPIError):
    """Exception raised for forbidden access (403)."""

    def __init__(self, message: str = "Access forbidden", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=403, details=details)


class PostZenNotFoundError(PostZenAPIError):
    """Exception raised when a resource is not found (404)."""

    def __init__(self, message: str = "Resource not found", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=404, details=details)


class PostZenRateLimitError(PostZenAPIError):
    """Exception raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        reset_time: datetime | None = None,
        limit: int | None = None,
        remaining: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=429, details=details)
        self.reset_time = reset_time
        self.limit = limit
        self.remaining = remaining

    def __str__(self) -> str:
        base = f"[429] {self.message}"
        if self.reset_time:
            base += f" (resets at {self.reset_time.isoformat()})"
        return base


class PostZenConnectionError(PostZenError):
    """Exception raised for connection errors."""


class PostZenTimeoutError(PostZenError):
    """Exception raised when a request times out."""


class PostZenValidationError(PostZenError):
    """Exception raised for client-side validation errors."""
