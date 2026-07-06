"""Official Python SDK for the PostZen Public API."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .client.exceptions import (
    PostZenAPIError,
    PostZenAuthenticationError,
    PostZenConnectionError,
    PostZenError,
    PostZenForbiddenError,
    PostZenNotFoundError,
    PostZenPaymentRequiredError,
    PostZenRateLimitError,
    PostZenTimeoutError,
    PostZenValidationError,
)
from .client.postzen_client import PostZen
from .models import *  # noqa: F401, F403

try:
    __version__ = version("postzen-sdk")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = [
    "PostZen",
    "__version__",
    "PostZenAPIError",
    "PostZenAuthenticationError",
    "PostZenConnectionError",
    "PostZenError",
    "PostZenForbiddenError",
    "PostZenNotFoundError",
    "PostZenPaymentRequiredError",
    "PostZenRateLimitError",
    "PostZenTimeoutError",
    "PostZenValidationError",
]
