"""Shared, spec-derived resource names and operation discovery (stdlib only)."""

from __future__ import annotations

import keyword
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
_LEGACY_DESCRIPTIONS = {
    "Profiles": "Manage PostZen profiles",
    "Accounts": "List and disconnect connected social accounts",
    "Connect": "Create and complete OAuth connection flows",
    "Media": "Create presigned media upload URLs",
    "Posts": "Create and publish posts",
}


def camel_to_snake(name: str) -> str:
    name = name.replace("-", "_")
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    result = name.lower()
    if keyword.iskeyword(result):
        result += "_"
    return result


def resource_key(tag: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "_", camel_to_snake(tag)).strip("_") or "resource"
    if result[0].isdigit():
        result = "_" + result
    if keyword.iskeyword(result):
        result += "_"
    return result


def operations(spec: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any], dict[str, Any]]]:
    for path, path_item in spec.get("paths", {}).items():
        if isinstance(path_item, dict):
            for method, operation in path_item.items():
                if method in HTTP_METHODS and isinstance(operation, dict):
                    yield path, method, path_item, operation


def resource_order(spec: dict[str, Any]) -> list[tuple[str, str]]:
    used: dict[str, None] = {}
    untagged = []
    for path, method, _, operation in operations(spec):
        if not operation.get("tags"):
            untagged.append(f"{method.upper()} {path} ({operation.get('operationId', '<missing operationId>')})")
        for tag in operation.get("tags") or []:
            used[tag] = None
    if untagged:
        raise SystemExit("Operations without tags:\n" + "\n".join(untagged))
    tags = dict.fromkeys([*_LEGACY_DESCRIPTIONS, *(item["name"] for item in spec.get("tags", [])), *used])
    result = [(tag, resource_key(tag)) for tag in tags if tag in used]
    keys: dict[str, str] = {}
    for tag, key in result:
        if key in keys:
            raise SystemExit(f"Resource key collision: {keys[key]!r} and {tag!r} both map to {key!r}")
        keys[key] = tag
    return result


def display_name(tag: str) -> str:
    return "Connect (OAuth)" if tag == "Connect" else tag


def description(spec: dict[str, Any], tag: str) -> str:
    for item in spec.get("tags", []):
        if item["name"] == tag and item.get("description", "").strip():
            return re.split(r"(?<=[.!?])\s+", item["description"].strip(), maxsplit=1)[0].rstrip(".")
    return _LEGACY_DESCRIPTIONS.get(tag, tag)
