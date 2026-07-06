#!/usr/bin/env python3
"""Generate pydantic models with datamodel-code-generator."""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path


def validate_imports(output_file: Path, parent_init: Path) -> int:
    tree = ast.parse(output_file.read_text())
    generated_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    init_source = parent_init.read_text()
    import_names: list[str] = []
    for match in re.finditer(r"from \._generated\.models import \((.*?)\)", init_source, re.DOTALL):
        import_names.extend(re.findall(r"\b([A-Z]\w+)\b", match.group(1)))
    missing = sorted(set(import_names) - generated_names)
    if missing:
        print("models/__init__.py imports names that do not exist in generated models:")
        for name in missing:
            print(f"  - {name}")
        return 1
    print(f"Validated {len(import_names)} explicit model imports.")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    spec_path = root / "openapi.json"
    output_dir = root / "src" / "postzen" / "models" / "_generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "models.py"

    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input",
        str(spec_path),
        "--input-file-type",
        "openapi",
        "--output",
        str(output_file),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--use-annotated",
        "--field-constraints",
        "--collapse-root-models",
        "--use-union-operator",
        "--target-python-version",
        "3.10",
        # Drop the header timestamp so regeneration is byte-for-byte idempotent.
        "--disable-timestamp",
        # Restore the intended model contract that the raw generator drops:
        # populate_by_name + extra="ignore" (parity with the old _PostZenModel base).
        "--allow-population-by-field-name",
        "--extra-fields",
        "ignore",
        # Keep `format: uri` fields as plain str (authUrl/uploadUrl/publicUrl/...)
        # so they compare/serialize as strings instead of pydantic AnyUrl.
        "--type-mappings",
        "string+uri=string",
        # Plain datetime (not AwareDatetime) to match resource signatures.
        "--output-datetime-class",
        "datetime",
        # Emit enum-typed fields as Literal[...] of their string values instead of
        # Enum classes. Keeps string-equality ergonomics (status == "connected") on
        # the py310 target, where StrEnum/--use-specialized-enum is unavailable, and
        # avoids leaking numerically-suffixed enum class names (Status1, Type, ...).
        "--enum-field-as-literal",
        "all",
        # Pin external formatters so datamodel-code-generator's FutureWarning about
        # default formatters going opt-in cannot change output across versions.
        "--formatters",
        "black",
        "isort",
    ]
    print("Generating models:")
    print(" ".join(cmd))
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        print(exc.stdout)
        print(exc.stderr)
        return exc.returncode
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    (output_dir / "__init__.py").write_text(
        '"""Auto-generated PostZen models."""\n\n'
        "from __future__ import annotations\n\n"
        "from .models import *  # noqa: F401, F403\n"
    )
    return validate_imports(output_file, output_dir.parent / "__init__.py")


if __name__ == "__main__":
    raise SystemExit(main())
