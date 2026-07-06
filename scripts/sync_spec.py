#!/usr/bin/env python3
"""Copy the PostZen OpenAPI spec into this SDK repo."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    default_source = project_root.parent / "postzen" / "apps" / "docs" / "openapi.json"
    source = Path(os.environ.get("POSTZEN_SPEC_PATH", default_source))
    destination = project_root / "openapi.json"

    if not source.exists():
        print(f"OpenAPI spec not found: {source}")
        return 1

    shutil.copyfile(source, destination)
    print(f"Synced {source} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
