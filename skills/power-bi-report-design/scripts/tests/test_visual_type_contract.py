"""Tests for the visual-type contract checker."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import check_visual_type_contract as contract  # noqa: E402

_REAL_DESIGN_ROOT = Path(__file__).resolve().parents[2]


def _write_recipe(root: Path, name: str, visual_type: str) -> None:
    templates = root / "references" / "chart-templates"
    templates.mkdir(parents=True, exist_ok=True)
    (templates / name).write_text(
        f"# Recipe\n\n- **id:** `x`\n- **Visual type:** {visual_type}\n",
        encoding="utf-8",
    )


def _write_policy(root: Path) -> None:
    refs = root / "references"
    refs.mkdir(parents=True, exist_ok=True)
    (refs / "visual-type-policy.json").write_text(
        json.dumps({"prohibited_generate": ["card", "multiRowCard", "map", "filledMap", "table", "matrix"]}),
        encoding="utf-8",
    )


class ContractCheckerTests(unittest.TestCase):
    def test_real_design_root_is_clean(self):
        # The shipped recipes and index must satisfy the contract.
        self.assertEqual(contract.run(_REAL_DESIGN_ROOT), [])

    def test_detects_prohibited_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_policy(root)
            _write_recipe(root, "bad.md", "`card` (single value)")
            problems = contract.run(root, root / "references" / "visual-type-policy.json")
            self.assertTrue(any("card" in p for p in problems))

    def test_allows_modern_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_policy(root)
            _write_recipe(root, "good.md", "`cardVisual` (single value)")
            _write_recipe(root, "map.md", "`azureMap` OR `shapeMap`")
            _write_recipe(root, "tbl.md", "`tableEx` / `pivotTable`")
            self.assertEqual(
                contract.run(root, root / "references" / "visual-type-policy.json"),
                [],
            )


if __name__ == "__main__":
    unittest.main()
