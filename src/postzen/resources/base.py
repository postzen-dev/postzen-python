"""Base resource helpers."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from ..client.base import BaseClient

T = TypeVar("T", bound=BaseModel)


def _to_camel_case(snake_str: str) -> str:
    components = snake_str.rstrip("_").split("_")
    return components[0] + "".join(part.title() for part in components[1:])


def _serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {
            _to_camel_case(str(key)) if isinstance(key, str) else key: _serialize_value(item)
            for key, item in value.items()
            if item is not None
        }
    return value


class BaseResource(Generic[T]):
    """Base class for generated API resources."""

    _BASE_PATH = ""

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def _build_params(self, **kwargs: Any) -> dict[str, Any]:
        return {
            _to_camel_case(key): _serialize_value(value)
            for key, value in kwargs.items()
            if value is not None
        }

    def _build_payload(self, **kwargs: Any) -> dict[str, Any]:
        return {
            _to_camel_case(key): _serialize_value(value)
            for key, value in kwargs.items()
            if value is not None
        }

    def _build_headers(self, **kwargs: Any) -> dict[str, str]:
        return {
            key.replace("_", "-"): str(value)
            for key, value in kwargs.items()
            if value is not None
        }

    def _path(self, *parts: str) -> str:
        if parts:
            suffix = "/".join(str(part).strip("/") for part in parts)
            return f"{self._BASE_PATH}/{suffix}"
        return self._BASE_PATH
