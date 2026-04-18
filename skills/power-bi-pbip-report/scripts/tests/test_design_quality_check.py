"""Tests for design_quality_check.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import pytest
from design_quality_check import (
    LintReport,
    check_default_page_names,
    check_orphan_pages,
    check_contrast,
    _extract_color_props,
)


# ── LintReport ────────────────────────────────────────────────

def test_lint_report_add_and_filter():
    lint = LintReport()
    lint.add("error", "E1", "bad contrast", "page/vis")
    lint.add("warning", "W1", "too many visuals", "page")
    lint.add("info", "I1", "consider labels")

    assert len(lint.errors()) == 1
    assert len(lint.warnings()) == 1
    assert len(lint.infos()) == 1
    assert lint.findings[0].code == "E1"


# ── check_default_page_names ──────────────────────────────────

def test_check_default_page_names(tmp_path):
    """Detects 'Page 1'-style default names."""
    report = _make_report(tmp_path, pages=[
        ("page1", {"displayName": "Page 1"}),
        ("page2", {"displayName": "Sales Overview"}),
    ])
    lint = LintReport()
    check_default_page_names(report, lint)
    assert len(lint.warnings()) == 1
    assert "Page 1" in lint.warnings()[0].message


# ── check_orphan_pages ────────────────────────────────────────

def test_check_orphan_pages_mismatch(tmp_path):
    """Detects page folders not in pageOrder."""
    report = _make_report(tmp_path, pages=[
        ("page1", {"displayName": "P1"}),
        ("orphan_page", {"displayName": "Orphan"}),
    ], page_order=["page1"])
    lint = LintReport()
    check_orphan_pages(report, lint)
    assert len(lint.errors()) >= 1
    assert any("orphan_page" in e.message for e in lint.errors())


# ── _extract_color_props ──────────────────────────────────────

def test_extract_color_props_solid():
    data = {
        "visual": {
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "fontColor": {"solid": {"color": "#000000"}},
                            "backgroundColor": {"solid": {"color": "#FFFFFF"}},
                        }
                    }
                ]
            }
        }
    }
    pairs = _extract_color_props(data)
    assert len(pairs) == 1
    assert pairs[0] == ("#000000", "#FFFFFF")


def test_extract_color_props_no_colors():
    data = {"visual": {"objects": {}}}
    pairs = _extract_color_props(data)
    assert pairs == []


# ── check_contrast ────────────────────────────────────────────

def test_check_contrast_good(tmp_path):
    """Black on white should pass."""
    visual_data = {
        "visual": {
            "visualType": "card",
            "objects": {
                "labels": [{
                    "properties": {
                        "fontColor": {"solid": {"color": "#000000"}},
                        "backgroundColor": {"solid": {"color": "#FFFFFF"}},
                    }
                }]
            }
        }
    }
    report = _make_report(tmp_path, pages=[("p1", {"displayName": "P1"})], visuals={"p1": [visual_data]})
    lint = LintReport()
    check_contrast(report, lint)
    assert len(lint.errors()) == 0


def test_check_contrast_bad(tmp_path):
    """Light gray on white should fail."""
    visual_data = {
        "visual": {
            "visualType": "card",
            "objects": {
                "labels": [{
                    "properties": {
                        "fontColor": {"solid": {"color": "#CCCCCC"}},
                        "backgroundColor": {"solid": {"color": "#FFFFFF"}},
                    }
                }]
            }
        }
    }
    report = _make_report(tmp_path, pages=[("p1", {"displayName": "P1"})], visuals={"p1": [visual_data]})
    lint = LintReport()
    check_contrast(report, lint)
    assert len(lint.errors()) >= 1
    assert "E1" in lint.errors()[0].code


# ── Fixture helper ────────────────────────────────────────────

def _make_report(
    tmp_path: Path,
    pages: list[tuple[str, dict]] | None = None,
    page_order: list[str] | None = None,
    visuals: dict[str, list[dict]] | None = None,
) -> Path:
    """Build a minimal .Report folder structure and return its path."""
    report = tmp_path / "Test.Report"
    defn = report / "definition"
    pages_dir = defn / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    if pages is None:
        pages = []

    names = []
    for page_name, page_data in pages:
        names.append(page_name)
        pdir = pages_dir / page_name
        pdir.mkdir(exist_ok=True)
        (pdir / "page.json").write_text(json.dumps(page_data), encoding="utf-8")

        # Add visuals if provided
        if visuals and page_name in visuals:
            vdir_parent = pdir / "visuals"
            vdir_parent.mkdir(exist_ok=True)
            for i, vdata in enumerate(visuals[page_name]):
                vdir = vdir_parent / f"vis{i}"
                vdir.mkdir(exist_ok=True)
                (vdir / "visual.json").write_text(json.dumps(vdata), encoding="utf-8")

    if page_order is None:
        page_order = names
    # pages.json lives at definition/pages.json (not inside pages/)
    (defn / "pages.json").write_text(json.dumps({"pageOrder": page_order}), encoding="utf-8")

    return report
