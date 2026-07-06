#!/usr/bin/env python3
"""Generate the README SDK Reference section from openapi.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RESOURCE_ORDER = ["profiles", "accounts", "connect", "media", "posts"]
DISPLAY_NAMES = {
    "profiles": "Profiles",
    "accounts": "Accounts",
    "connect": "Connect (OAuth)",
    "media": "Media",
    "posts": "Posts",
}
TAG_TO_RESOURCE = {
    "Profiles": "profiles",
    "Accounts": "accounts",
    "Connect": "connect",
    "Media": "media",
    "Posts": "posts",
}


def camel_to_snake(name: str) -> str:
    name = name.replace("-", "_")
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    return name.lower()


def method_sort_key(name: str) -> tuple[int, str]:
    lower = name.lower()
    if lower.startswith("list"):
        return (0, name)
    if lower.startswith("create"):
        return (1, name)
    if lower.startswith("get"):
        return (2, name)
    if lower.startswith("update"):
        return (3, name)
    if lower.startswith("delete"):
        return (4, name)
    return (5, name)


def generate_reference(spec: dict) -> str:
    resources: dict[str, list[tuple[str, str]]] = {name: [] for name in RESOURCE_ORDER}
    for path_item in spec.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for http_method, operation in path_item.items():
            if http_method not in {"get", "post", "put", "patch", "delete"} or not isinstance(operation, dict):
                continue
            tag = operation.get("tags", [""])[0]
            resource = TAG_TO_RESOURCE.get(tag)
            operation_id = operation.get("operationId")
            if resource and operation_id:
                resources[resource].append(
                    (camel_to_snake(operation_id), operation.get("summary") or operation_id)
                )

    lines = ["## SDK Reference", ""]
    for resource in RESOURCE_ORDER:
        methods = sorted(resources[resource], key=lambda item: method_sort_key(item[0]))
        if not methods:
            continue
        lines.append(f"### {DISPLAY_NAMES[resource]}")
        lines.append("| Method | Description |")
        lines.append("|--------|-------------|")
        for method, description in methods:
            lines.append(f"| `{resource}.{method}()` | {description} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    reference = generate_reference(json.loads((root / "openapi.json").read_text()))
    if "--print" in sys.argv:
        print(reference)
        return 0

    readme_path = root / "README.md"
    content = readme_path.read_text()
    pattern = r"## SDK Reference\n.*?(?=## Requirements)"
    new_content = re.sub(pattern, reference + "\n", content, flags=re.DOTALL)
    if new_content == content:
        print("No README changes needed.")
    else:
        readme_path.write_text(new_content)
        print("Updated README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
