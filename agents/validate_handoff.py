#!/usr/bin/env python3
"""
validate_handoff.py — validate a handoff JSON file against handoff.schema.json.

Usage:
    python validate_handoff.py handoff.json
    python validate_handoff.py handoff.json --schema path/to/handoff.schema.json
    python validate_handoff.py handoff.json --quiet

Exit codes:
    0 — valid
    1 — validation errors (printed to stderr)
    2 — file not found or JSON parse error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema  # type: ignore[import-untyped]
    from jsonschema import Draft202012Validator
except ImportError:
    jsonschema = None  # type: ignore[assignment]
    Draft202012Validator = None  # type: ignore[assignment,misc]

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SCHEMA = SCRIPT_DIR / "handoff.schema.json"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB — reasonable limit for handoff JSON


def _load_json(path: Path) -> dict:
    # Guard against unexpectedly large files
    size = path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large ({size:,} bytes, max {MAX_FILE_SIZE:,})")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _fallback_validate(instance: dict, schema: dict) -> list[str]:
    """Minimal structural validation when jsonschema is not installed."""
    errors: list[str] = []
    for field in schema.get("required", []):
        if field not in instance:
            errors.append(f"Missing required field: '{field}'")
    from_phase = instance.get("from_phase", "")
    artifacts = instance.get("artifacts", {})
    if isinstance(artifacts, dict) and from_phase:
        if from_phase not in artifacts:
            errors.append(
                f"'artifacts' must contain key '{from_phase}' (matching from_phase)"
            )
    return errors


def validate(handoff_path: Path, schema_path: Path) -> list[str]:
    """Return a list of error messages (empty = valid)."""
    schema = _load_json(schema_path)
    instance = _load_json(handoff_path)

    if Draft202012Validator is not None:
        validator = Draft202012Validator(schema)
        return [e.message for e in sorted(validator.iter_errors(instance), key=str)]
    else:
        return _fallback_validate(instance, schema)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a phase-handoff JSON file against handoff.schema.json."
    )
    parser.add_argument("handoff", type=Path, help="Path to the handoff JSON file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help=f"Path to the JSON Schema (default: {DEFAULT_SCHEMA})",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress output on success"
    )
    args = parser.parse_args()

    if not args.handoff.exists():
        print(f"Error: file not found: {args.handoff}", file=sys.stderr)
        return 2
    if not args.schema.exists():
        print(f"Error: schema not found: {args.schema}", file=sys.stderr)
        return 2

    try:
        errors = validate(args.handoff, args.schema)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {args.handoff}: {exc}", file=sys.stderr)
        return 2
    except (PermissionError, IsADirectoryError, OSError) as exc:
        print(f"Error: cannot read {args.handoff}: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"FAIL — {len(errors)} validation error(s):", file=sys.stderr)
        for i, msg in enumerate(errors, 1):
            print(f"  {i}. {msg}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"OK — {args.handoff} is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
