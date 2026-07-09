#!/usr/bin/env python3
"""Generate typed resource classes from openapi.json."""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path
from typing import Any

RESOURCE_ORDER = ["profiles", "accounts", "connect", "media", "posts"]
TAG_TO_RESOURCE = {
    "Profiles": "profiles",
    "Accounts": "accounts",
    "Connect": "connect",
    "Media": "media",
    "Posts": "posts",
}
RESOURCE_DESCRIPTIONS = {
    "profiles": "Manage PostZen profiles",
    "accounts": "List and disconnect connected social accounts",
    "connect": "Create and complete OAuth connection flows",
    "media": "Create presigned media upload URLs",
    "posts": "Create and publish posts",
}
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def camel_to_snake(name: str) -> str:
    name = name.replace("-", "_")
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    result = name.lower()
    if keyword.iskeyword(result):
        result += "_"
    return result


def class_name(resource: str) -> str:
    return "".join(part.title() for part in resource.split("_")) + "Resource"


def model_name_from_ref(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def resolve(spec: dict[str, Any], value: Any) -> Any:
    if isinstance(value, dict) and "$ref" in value:
        current: Any = spec
        for part in value["$ref"].lstrip("#/").split("/"):
            current = current[part]
        return current
    return value


def python_type(spec: dict[str, Any], schema: dict[str, Any], required: bool) -> str:
    if not schema:
        base = "Any"
    elif "$ref" in schema:
        resolved = resolve(spec, schema)
        if resolved.get("type") == "string":
            base = "str"
        elif resolved.get("type") == "integer":
            base = "int"
        elif resolved.get("type") == "number":
            base = "float"
        elif resolved.get("type") == "boolean":
            base = "bool"
        else:
            base = "dict[str, Any]"
    elif "oneOf" in schema or "anyOf" in schema:
        base = "Any"
    else:
        schema = resolve(spec, schema)
        schema_type = schema.get("type")
        if isinstance(schema_type, list):
            nullable = "null" in schema_type
            non_null = [item for item in schema_type if item != "null"]
            schema_type = non_null[0] if non_null else None
            required = required and not nullable
        if schema_type == "string":
            base = "datetime | str" if schema.get("format") == "date-time" else "str"
        elif schema_type == "integer":
            base = "int"
        elif schema_type == "number":
            base = "float"
        elif schema_type == "boolean":
            base = "bool"
        elif schema_type == "array":
            items = schema.get("items", {})
            if "$ref" in items or "oneOf" in items or "anyOf" in items:
                item_type = "dict[str, Any]"
            else:
                item_type = python_type(spec, items, True)
            base = f"list[{item_type}]"
        elif schema_type == "object":
            base = "dict[str, Any]"
        else:
            base = "Any"
    return base if required else f"{base} | None"


def schema_default(schema: dict[str, Any]) -> Any:
    if "default" in schema:
        return schema["default"]
    return None


def extract_response_model(operation: dict[str, Any]) -> str:
    responses = operation.get("responses", {})
    for status_code in ("201", "200"):
        schema = (
            responses.get(status_code, {})
            .get("content", {})
            .get("application/json", {})
            .get("schema", {})
        )
        if "$ref" in schema:
            return model_name_from_ref(schema["$ref"])
    return "dict[str, Any]"


def extract_parameters(spec: dict[str, Any], path_item: dict[str, Any], operation: dict[str, Any]) -> list[dict[str, Any]]:
    params: list[dict[str, Any]] = []
    for raw_param in [*path_item.get("parameters", []), *operation.get("parameters", [])]:
        param = resolve(spec, raw_param)
        if not isinstance(param, dict) or param.get("in") == "cookie":
            continue
        location = param.get("in", "query")
        original_name = param["name"]
        param_name = camel_to_snake(original_name)
        schema = param.get("schema", {})
        required = bool(param.get("required", False))
        params.append(
            {
                "name": param_name,
                "original_name": original_name,
                "location": location,
                "required": required,
                "type": python_type(spec, schema, required),
                "default": schema_default(schema),
                "description": param.get("description", ""),
            }
        )

    request_body = operation.get("requestBody")
    if request_body:
        request_body = resolve(spec, request_body)
        schema = resolve(
            spec,
            request_body.get("content", {})
            .get("application/json", {})
            .get("schema", {}),
        )
        required_props = set(schema.get("required") or [])
        for prop_name, prop_schema in schema.get("properties", {}).items():
            required = prop_name in required_props
            params.append(
                {
                    "name": camel_to_snake(prop_name),
                    "original_name": prop_name,
                    "location": "body",
                    "required": required,
                    "type": python_type(spec, prop_schema, required),
                    "default": schema_default(prop_schema),
                    "description": prop_schema.get("description", ""),
                }
            )
    return params


def default_literal(value: Any) -> str:
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "None"
    return repr(value)


def signature(method_name: str, params: list[dict[str, Any]], response_model: str, *, is_async: bool) -> str:
    pieces = ["self"]
    path_params = [p for p in params if p["location"] == "path"]
    other_params = [p for p in params if p["location"] != "path"]
    for param in path_params:
        pieces.append(f"{param['name']}: {param['type'].replace(' | None', '')}")
    if other_params:
        pieces.append("*")
        required = [p for p in other_params if p["required"]]
        optional = [p for p in other_params if not p["required"]]
        for param in [*required, *optional]:
            if param["required"]:
                pieces.append(f"{param['name']}: {param['type'].replace(' | None', '')}")
            else:
                pieces.append(f"{param['name']}: {param['type']} = {default_literal(param['default'])}")
    prefix = "async " if is_async else ""
    name = f"a{method_name}" if is_async else method_name
    return f"{prefix}def {name}({', '.join(pieces)}) -> {response_model}"


def request_path(path: str, params: list[dict[str, Any]]) -> str:
    path_params = [p for p in params if p["location"] == "path"]
    if not path_params:
        return repr(path)
    formatted = path
    for param in path_params:
        formatted = formatted.replace("{" + param["original_name"] + "}", "{" + param["name"] + "}")
    return f'f"{formatted}"'


def method_body(operation: dict[str, Any], params: list[dict[str, Any]], response_model: str, *, is_async: bool) -> list[str]:
    http_method = operation["http_method"].lower()
    client_method = f"_a{http_method}" if is_async else f"_{http_method}"
    await_prefix = "await " if is_async else ""
    query_params = [p for p in params if p["location"] == "query"]
    header_params = [p for p in params if p["location"] == "header"]
    body_params = [p for p in params if p["location"] == "body"]
    lines: list[str] = []

    if query_params:
        lines.append("        params = self._build_params(")
        for param in query_params:
            lines.append(f"            {param['name']}={param['name']},")
        lines.append("        )")
    if header_params:
        lines.append("        headers = self._build_headers(")
        for param in header_params:
            lines.append(f"            {param['name']}={param['name']},")
        lines.append("        )")
    if body_params:
        lines.append("        payload = self._build_payload(")
        for param in body_params:
            lines.append(f"            {param['name']}={param['name']},")
        lines.append("        )")

    args = [request_path(operation["path"], params)]
    if body_params and http_method in {"post", "put", "patch"}:
        args.append("data=payload")
    if query_params:
        args.append("params=params")
    if header_params:
        args.append("headers=headers")
    lines.append(f"        data = {await_prefix}self._client.{client_method}({', '.join(args)})")
    lines.append(f"        return {response_model}.model_validate(data)")
    return lines


def generate_resource(resource: str, operations: list[dict[str, Any]]) -> str:
    models = sorted({operation["response_model"] for operation in operations if operation["response_model"] != "dict[str, Any]"})
    uses_datetime = any("datetime" in p["type"] for op in operations for p in op["params"])
    lines = [
        '"""',
        f"Auto-generated {resource} resource.",
        "",
        "DO NOT EDIT THIS FILE MANUALLY.",
        "Run `python scripts/generate_resources.py` to regenerate.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Any",
        "",
    ]
    if models:
        lines.append("from ...models import (")
        for model in models:
            lines.append(f"    {model},")
        lines.append(")")
        lines.append("")
    lines.append("from ..base import BaseResource")
    lines.append("")
    lines.append("if TYPE_CHECKING:")
    if uses_datetime:
        lines.append("    from datetime import datetime")
    lines.append("    from ...client.base import BaseClient")
    lines.append("")
    lines.append("")
    lines.append(f"class {class_name(resource)}(BaseResource[Any]):")
    lines.append(f'    """{RESOURCE_DESCRIPTIONS.get(resource, resource.title())}."""')
    lines.append("")
    lines.append("    def __init__(self, client: BaseClient) -> None:")
    lines.append("        super().__init__(client)")

    for operation in operations:
        method_name = camel_to_snake(operation["operationId"])
        summary = (operation.get("summary") or method_name.replace("_", " ").title()).replace('"""', '\\"\\"\\"')
        lines.append("")
        lines.append(f"    {signature(method_name, operation['params'], operation['response_model'], is_async=False)}:")
        lines.append(f'        """{summary}."""')
        lines.extend(method_body(operation, operation["params"], operation["response_model"], is_async=False))
        lines.append("")
        lines.append(f"    {signature(method_name, operation['params'], operation['response_model'], is_async=True)}:")
        lines.append(f'        """{summary} (async)."""')
        lines.extend(method_body(operation, operation["params"], operation["response_model"], is_async=True))

    return "\n".join(lines) + "\n"


def generate_resource_init(generated: list[str], manual: list[str]) -> str:
    all_resources = [r for r in RESOURCE_ORDER if r in set(generated) | set(manual)]
    lines = [
        '"""API resources.',
        "",
        "This file is regenerated by `python scripts/generate_resources.py`.",
        "Manual resource modules in this package take precedence over generated modules.",
        '"""',
        "",
    ]
    # Sort by module path (not class name) so the block satisfies ruff's isort
    # rule: `._generated.*` modules sort before manual `.<resource>` overrides.
    imports = sorted(
        (f".{resource}" if resource in manual else f"._generated.{resource}", class_name(resource))
        for resource in all_resources
    )
    for module, cls in imports:
        lines.append(f"from {module} import {cls}")
    lines.append("")
    lines.append("__all__ = [")
    for resource in all_resources:
        lines.append(f'    "{class_name(resource)}",')
    lines.append("]")
    return "\n".join(lines) + "\n"


def update_client(client_path: Path, resources: list[str]) -> None:
    content = client_path.read_text()
    import_block = "from ..resources import (\n"
    for resource_class in sorted(class_name(resource) for resource in resources):
        import_block += f"    {resource_class},\n"
    import_block += ")"
    content = re.sub(r"from \.\.resources import \(\n(?:.*?\n)*?\)", import_block, content)

    registration = "\n".join(
        f"        self.{resource} = {class_name(resource)}(self)" for resource in resources
    )
    content = re.sub(
        r"(        # --- auto-registered resources \(do not edit\) ---\n).*?(        # --- end auto-registered resources ---)",
        r"\1" + registration + "\n" + r"\2",
        content,
        flags=re.DOTALL,
    )
    client_path.write_text(content)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    spec_path = root / "openapi.json"
    spec = json.loads(spec_path.read_text())
    resources: dict[str, list[dict[str, Any]]] = {name: [] for name in RESOURCE_ORDER}

    for path, path_item in spec.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for http_method, operation in path_item.items():
            if http_method not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            tag = operation.get("tags", ["Other"])[0]
            resource = TAG_TO_RESOURCE.get(tag)
            if resource is None:
                continue
            operation = dict(operation)
            operation["http_method"] = http_method
            operation["path"] = path
            operation["params"] = extract_parameters(spec, path_item, operation)
            operation["response_model"] = extract_response_model(operation)
            resources[resource].append(operation)

    resources_dir = root / "src" / "postzen" / "resources"
    generated_dir = resources_dir / "_generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    generated_resources = [name for name in RESOURCE_ORDER if resources[name]]

    for resource in generated_resources:
        (generated_dir / f"{resource}.py").write_text(generate_resource(resource, resources[resource]))
        print(f"Generated {resource}.py")

    init_lines = ['"""Auto-generated resources."""', "", "from __future__ import annotations", ""]
    for resource in generated_resources:
        init_lines.append(f"from .{resource} import {class_name(resource)}")
    init_lines.append("")
    init_lines.append("__all__ = [")
    for resource in generated_resources:
        init_lines.append(f'    "{class_name(resource)}",')
    init_lines.append("]")
    (generated_dir / "__init__.py").write_text("\n".join(init_lines) + "\n")

    manual = [
        path.stem
        for path in resources_dir.glob("*.py")
        if path.stem not in {"__init__", "base"} and path.stem in generated_resources
    ]
    (resources_dir / "__init__.py").write_text(generate_resource_init(generated_resources, manual))
    update_client(root / "src" / "postzen" / "client" / "postzen_client.py", generated_resources)
    print(f"Generated {len(generated_resources)} resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
