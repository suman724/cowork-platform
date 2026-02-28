#!/usr/bin/env python3
"""Generate Pydantic v2 models from JSON Schema contract files.

Reads all schemas from contracts/schemas/ and generates Python modules
in generated/python/cowork_platform/.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
OUTPUT_DIR = ROOT / "generated" / "python" / "cowork_platform"


def main() -> int:
    """Run datamodel-code-generator on all schema files."""
    # Collect all schema files
    schema_files = sorted(SCHEMAS_DIR.glob("*.json"))
    if not schema_files:
        print("ERROR: No schema files found in", SCHEMAS_DIR)
        return 1

    print(f"Generating Pydantic models from {len(schema_files)} schemas...")

    # Clean output directory (preserve __init__.py pattern)
    for f in OUTPUT_DIR.glob("*.py"):
        if f.name != "__init__.py":
            f.unlink()

    # Generate models from each schema file individually to avoid $ref issues
    # Process schemas without $ref first, then schemas with $ref
    no_ref_schemas = []
    ref_schemas = []

    for sf in schema_files:
        content = sf.read_text()
        if '"$ref"' in content:
            ref_schemas.append(sf)
        else:
            no_ref_schemas.append(sf)

    all_modules: list[str] = []

    for sf in no_ref_schemas + ref_schemas:
        module_name = sf.stem.replace("-", "_")
        output_file = OUTPUT_DIR / f"{module_name}.py"

        cmd = [
            sys.executable,
            "-m",
            "datamodel_code_generator",
            "--input", str(sf),
            "--input-file-type", "jsonschema",
            "--output", str(output_file),
            "--output-model-type", "pydantic_v2.BaseModel",
            "--target-python-version", "3.12",
            "--use-standard-collections",
            "--use-union-operator",
            "--use-annotated",
            "--field-constraints",
            "--collapse-root-models",
            "--use-title-as-name",
            "--enum-field-as-literal", "all",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # If $ref resolution fails, try without collapse-root-models
            cmd_retry = [c for c in cmd if c != "--collapse-root-models"]
            result = subprocess.run(cmd_retry, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"WARNING: Failed to generate {sf.name}, skipping:")
                stderr_lines = result.stderr.strip().split("\n")
                # Print only non-deprecation warnings
                for line in stderr_lines:
                    if "DeprecationWarning" not in line and "FutureWarning" not in line:
                        print(f"  {line}")
                continue

        # Strip the timestamp comment so regeneration doesn't produce diffs
        content = output_file.read_text()
        content = re.sub(r"#   timestamp:.*\n", "", content)
        output_file.write_text(content)

        all_modules.append(module_name)
        print(f"  ✓ {sf.name} → {module_name}.py")

    # Generate __init__.py that re-exports all models
    init_lines = [
        "# Auto-generated Pydantic models from JSON Schema contracts.",
        "# DO NOT EDIT — run `make codegen-python` to regenerate.",
        "",
    ]
    for module in sorted(all_modules):
        init_lines.append(f"from cowork_platform.{module} import *  # noqa: F403")

    init_lines.append("")
    (OUTPUT_DIR / "__init__.py").write_text("\n".join(init_lines))

    # Format generated files with ruff
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", str(OUTPUT_DIR)],
        check=True,
    )

    print(f"\nGenerated {len(all_modules)} modules in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
