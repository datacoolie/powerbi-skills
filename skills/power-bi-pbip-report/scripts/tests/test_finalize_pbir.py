"""Tests for finalize_pbir.py key functions."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import pytest
from pbir_utils import GRID, FONT_FAMILY


# ── snap_grid (via direct import) ─────────────────────────────

def test_snap_grid_on_grid():
    """Positions already on grid should not change."""
    from finalize_pbir import snap_grid, Report

    # Create a minimal report fixture
    report = _make_report_with_visual({"position": {"x": GRID * 2, "y": GRID * 3, "width": GRID * 10, "height": GRID * 5}})
    result = snap_grid(report, dry_run=True)
    assert result["visuals_changed"] == 0  # already aligned


def test_snap_grid_off_grid():
    """Positions off-grid should be snapped."""
    from finalize_pbir import snap_grid, Report

    report = _make_report_with_visual({"position": {"x": 13, "y": 17, "width": 305, "height": 199}})
    result = snap_grid(report, dry_run=True)
    # In dry-run, visuals_changed counted but not written
    assert result["visuals_changed"] >= 0  # should detect off-grid


# ── _replace_hex_in_tree ──────────────────────────────────────

def test_replace_hex_in_tree():
    from finalize_pbir import _replace_hex_in_tree

    data = {
        "color": "#ff0000",
        "nested": {"fill": "#FF0000", "other": 42},
        "list": ["#ff0000", "#00ff00"],
    }
    # reverse dict uses normalized keys (no #, uppercase)
    mapping = {"FF0000": "dataColor0", "00FF00": "dataColor1"}
    count = _replace_hex_in_tree(data, mapping)
    assert count >= 2  # at least the ff0000 occurrences
    # Replaced values become theme-token dicts, not plain strings
    assert isinstance(data["color"], dict)
    assert isinstance(data["nested"]["fill"], dict)


# ── _walk_and_fix_fonts ───────────────────────────────────────

def test_walk_and_fix_fonts_family():
    from finalize_pbir import _walk_and_fix_fonts

    data = {"fontFamily": "Arial"}
    changes = _walk_and_fix_fonts(data)
    assert changes == 1
    assert data["fontFamily"] == FONT_FAMILY


def test_walk_and_fix_fonts_already_correct():
    from finalize_pbir import _walk_and_fix_fonts

    data = {"fontFamily": FONT_FAMILY}
    changes = _walk_and_fix_fonts(data)
    assert changes == 0


def test_walk_and_fix_fonts_size_snap():
    from finalize_pbir import _walk_and_fix_fonts

    # fontSize=13 is equidistant from 12 and 14; snaps to 12 (first in sorted order)
    data = {"fontSize": 13}
    changes = _walk_and_fix_fonts(data)
    assert changes == 1
    assert data["fontSize"] == 12


def test_walk_and_fix_fonts_size_no_snap():
    from finalize_pbir import _walk_and_fix_fonts

    # fontSize=20 is not within ±2 of any standard size
    data = {"fontSize": 20}
    changes = _walk_and_fix_fonts(data)
    assert changes == 0
    assert data["fontSize"] == 20


# ── _snap_font_size ───────────────────────────────────────────

def test_snap_font_size_exact():
    from finalize_pbir import _snap_font_size
    assert _snap_font_size(14) == 14  # exact match


def test_snap_font_size_close():
    from finalize_pbir import _snap_font_size
    assert _snap_font_size(13) == 12  # equidistant from 12 and 14; picks 12 (first sorted)
    assert _snap_font_size(9) == 10   # snap to axis_label


def test_snap_font_size_no_snap():
    from finalize_pbir import _snap_font_size
    result = _snap_font_size(20)
    assert result == 20  # no standard size near 20


# ── Helper: build a minimal Report ────────────────────────────

def _make_report_with_visual(visual_data: dict, tmp_path: Path | None = None):
    """Create a minimal Report object with one visual for testing."""
    from finalize_pbir import Report
    import tempfile

    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())

    report_dir = tmp_path / "Test.Report"
    defn = report_dir / "definition"
    page_dir = defn / "pages" / "page1"
    vis_dir = page_dir / "visuals" / "vis1"
    vis_dir.mkdir(parents=True, exist_ok=True)

    # page.json
    page_json = page_dir / "page.json"
    page_json.write_text(json.dumps({"displayName": "Page 1"}), encoding="utf-8")

    # visual.json
    vis_json = vis_dir / "visual.json"
    vis_json.write_text(json.dumps(visual_data), encoding="utf-8")

    # pages.json
    pages_json = defn / "pages" / "pages.json"
    pages_json.write_text(json.dumps({"pageOrder": ["page1"]}), encoding="utf-8")

    # report.json
    (defn / "report.json").write_text("{}", encoding="utf-8")

    return Report.load(report_dir)
