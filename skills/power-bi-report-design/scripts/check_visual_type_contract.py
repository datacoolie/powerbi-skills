"""Enforce the design-to-authoring visual generation contract.

Scans chart-template recipes and the recipe index for generation targets that
report authoring prohibits (legacy `card`/`multiRowCard`/`map`/`filledMap`/
`table`/`matrix`). Fails with a non-zero exit if any recipe would emit a
prohibited type, so Phase 4a cannot produce a Design Spec that Phase 4b rejects.

Usage:
    python check_visual_type_contract.py [--design-root <dir>]

Legacy type names appearing in prose are ignored; only the recipe generation
target (the ``**Visual type:**`` line and the index ``visual_type`` field) is
checked.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_DESIGN_ROOT = _SCRIPT_DIR.parent
_POLICY = _DESIGN_ROOT / "references" / "visual-type-policy.json"

_VISUAL_TYPE_LINE = re.compile(r"^-?\s*\*\*Visual type:\*\*\s*(.+)$", re.IGNORECASE)
_TOKEN = re.compile(r"[A-Za-z0-9]+")


def load_policy(policy_path: Path | None = None) -> dict:
    return json.loads((policy_path or _POLICY).read_text(encoding="utf-8"))


def _tokens(text: str) -> set[str]:
    return set(_TOKEN.findall(text))


def _violations_in_text(text: str, prohibited: set[str]) -> set[str]:
    return _tokens(text) & prohibited


def check_recipes(design_root: Path, prohibited: set[str]) -> list[str]:
    problems: list[str] = []
    templates = design_root / "references" / "chart-templates"
    for recipe in sorted(templates.glob("*.md")):
        for line in recipe.read_text(encoding="utf-8").splitlines():
            match = _VISUAL_TYPE_LINE.match(line.strip())
            if not match:
                continue
            hit = _violations_in_text(match.group(1), prohibited)
            if hit:
                problems.append(
                    f"{recipe.relative_to(design_root)}: Visual type emits "
                    f"prohibited {sorted(hit)} -> {line.strip()}"
                )
            break
    return problems


def check_index(design_root: Path, prohibited: set[str]) -> list[str]:
    index = design_root / "references" / "chart-templates" / "chart-templates-index.json"
    if not index.is_file():
        return []
    data = json.loads(index.read_text(encoding="utf-8"))
    problems: list[str] = []
    for recipe in data.get("recipes", []):
        visual_type = recipe.get("visual_type", "")
        hit = _violations_in_text(visual_type, prohibited)
        if hit:
            problems.append(
                f"chart-templates-index.json [{recipe.get('id')}]: "
                f"visual_type emits prohibited {sorted(hit)} -> {visual_type!r}"
            )
    return problems


def run(design_root: Path, policy_path: Path | None = None) -> list[str]:
    policy = load_policy(policy_path)
    prohibited = set(policy["prohibited_generate"])
    return check_recipes(design_root, prohibited) + check_index(design_root, prohibited)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design-root", default=str(_DESIGN_ROOT))
    args = parser.parse_args(argv)
    problems = run(Path(args.design_root))
    if problems:
        print("Visual-type contract violations:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Visual-type contract OK: no recipe emits a prohibited legacy type.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
