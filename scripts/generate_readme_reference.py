#!/usr/bin/env python3
"""Generate the README SDK Reference section from openapi.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from resource_map import camel_to_snake, display_name, operations, resource_order


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
    order = resource_order(spec)
    tag_to_resource = dict(order)
    resources = {key: [] for _, key in order}
    for _, _, _, operation in operations(spec):
        for tag in operation["tags"]:
            resource = tag_to_resource[tag]
            operation_id = operation["operationId"]
            resources[resource].append(
                (camel_to_snake(operation_id), operation.get("summary") or operation_id)
            )

    lines = ["## SDK Reference", ""]
    for tag, resource in order:
        methods = sorted(resources[resource], key=lambda item: method_sort_key(item[0]))
        if not methods:
            continue
        lines.append(f"### {display_name(tag)}")
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
