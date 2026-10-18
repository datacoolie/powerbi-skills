"""Tests for rescale_layout.py."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS))

import rescale_layout as r  # noqa: E402

_INDEX = json.loads(r._INDEX.read_text(encoding="utf-8"))
_LANDSCAPE = [
    l for l in _INDEX["layouts"]
    if abs(l["canvas"]["width"] / l["canvas"]["height"] - 16 / 9) <= r.ASPECT_TOLERANCE
]


def test_parse_canvas():
    assert r.parse_canvas("1920x1080") == (1920, 1080)
    assert r.parse_canvas("1280×720") == (1280, 720)
    with pytest.raises(r.RescaleError):
        r.parse_canvas("wide")


def test_edges_snap_to_grid_and_stay_flush():
    zones = [
        {"name": "a", "x": 16, "y": 16, "w": 400, "h": 100},
        {"name": "b", "x": 416, "y": 16, "w": 400, "h": 100},  # flush with a
    ]
    out = r.rescale_zones(zones, (1664, 936), (1920, 1080))
    assert all(v % r.GRID == 0 for z in out for v in (z["x"], z["y"], z["w"], z["h"]))
    assert out[0]["x"] + out[0]["w"] == out[1]["x"]


def test_aspect_mismatch_rejected():
    with pytest.raises(r.RescaleError):
        r.rescale_zones([{"name": "a", "x": 0, "y": 0, "w": 8, "h": 8}], (1664, 936), (1200, 900))


def test_unknown_layout():
    with pytest.raises(r.RescaleError):
        r.rescale_layout("does-not-exist", (1920, 1080))


def test_intentional_source_overlap_not_reported():
    zones = [
        {"name": "title", "x": 16, "y": 16, "w": 800, "h": 64},
        {"name": "back", "x": 16, "y": 16, "w": 64, "h": 64},  # intentional overlap in the recipe
    ]
    scaled = r.rescale_zones(zones, (1664, 936), (1920, 1080))
    assert r.problems(scaled, (1920, 1080), zones) == []
    assert r.problems(scaled, (1920, 1080)) != []


@pytest.mark.parametrize("canvas", [(1920, 1080), (1280, 720), (2560, 1440)])
def test_every_16x9_layout_rescales_cleanly(canvas):
    for layout in _LANDSCAPE:
        result = r.rescale_layout(layout["id"], canvas)
        assert result["problems"] == [], layout["id"]


def test_cli_exit_codes(capsys):
    assert r.main(["--layout", "exec-overview-16x9", "--canvas", "1920x1080"]) == 0
    assert r.main(["--layout", "nope", "--canvas", "1920x1080"]) == 1
    assert r.main(["--layout", "exec-overview-16x9", "--canvas", "1200x900"]) == 1


def test_auto_prefers_recipe_slot_table():
    result = r.rescale_layout("exec-overview-16x9", (1920, 1080))
    assert result["source"] == "md"
    assert {z["name"] for z in result["zones"]} >= {"Page title", "KPI 1", "Hero visual"}
    assert all(v % r.GRID == 0 for z in result["zones"] for v in (z["x"], z["y"], z["w"], z["h"]))


def test_index_source_and_missing_table():
    assert r.rescale_layout("exec-overview-16x9", (1920, 1080), source="index")["source"] == "index"
    no_table = next(
        l["id"] for l in _LANDSCAPE
        if not r.parse_slot_tables((r._INDEX.parent / l["file"]).read_text(encoding="utf-8"))
    )
    assert r.rescale_layout(no_table, (1920, 1080))["source"] == "index"
    with pytest.raises(r.RescaleError):
        r.rescale_layout(no_table, (1920, 1080), source="md")


def test_md_format_output(capsys):
    assert r.main(["--layout", "exec-overview-16x9", "--canvas", "1280x720", "--format", "md"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("| Slot | x | y | w | h |")
    assert "| Page title |" in out


def test_same_canvas_is_identity():
    own = r.parse_slot_tables((r._INDEX.parent / "exec-overview-16x9.md").read_text(encoding="utf-8"))[0]["rows"]
    again = r.rescale_layout("exec-overview-16x9", (1920, 1080))["zones"]
    assert [(z["x"], z["y"], z["w"], z["h"]) for z in again] == [(z["x"], z["y"], z["w"], z["h"]) for z in own]


def test_library_is_fhd_native_and_clean():
    """Guards the FHD migration: no landscape recipe may keep the legacy canvas."""
    for layout in _LANDSCAPE:
        assert (layout["canvas"]["width"], layout["canvas"]["height"]) in {(1920, 1080)}, layout["id"]
        assert "canvas-1664x936" not in layout["tags"], layout["id"]
        text = (r._INDEX.parent / layout["file"]).read_text(encoding="utf-8")
        assert "1664" not in text, layout["id"]
        assert not r.check_recipe(r._INDEX.parent / layout["file"], (1920, 1080)), layout["id"]


def test_visual_budgets_in_index():
    budget = {"executive": 6, "analytical": 12, "operational": 14}
    over = [
        l["id"] for l in _LANDSCAPE
        if l["canvas_class"] == "landscape-16x9" and l["visual_count"] > budget[l["style"]]
    ]
    # Known dense catalog entries (KPI grids/scorecards) and navigation hubs (tiles are buttons, not
    # data visuals); each documents its density in its own recipe.
    assert set(over) <= {"scorecard-kpi-grid", "kpi-donut-row", "advanced-kpi-card-grid",
                         "ultra-dense-kpi-scorecard", "pl-statement-grid", "hr-dei-scorecard",
                         "dimension-nav-hub", "landing-navigation"}


def test_scale_rect_and_table_cli(capsys):
    assert r.scale_rect((40, 16, 1840, 64), (1920, 1080), (1280, 720)) == (24, 8, 1232, 48)
    assert r.main(["--canvas", "1280x720", "--rect", "40,16,1840,64", "--from-canvas", "1920x1080"]) == 0
    assert capsys.readouterr().out.strip() == "24,8,1232,48"
    assert r.main(["--canvas", "1280x720", "--rect", "1,2,3"]) == 1


def test_parse_slot_tables_ignores_other_tables():
    text = "| A | B |\n|---|---|\n| 1 | 2 |\n\n| Slot | x | y | w | h | Notes |\n|---|---|---|---|---|---|\n| s | 8 | 8 | 16 | 16 | n |\n"
    tables = r.parse_slot_tables(text)
    assert len(tables) == 1 and tables[0]["rows"][0]["extra"] == ["n"]


_HDR = "| Slot | x | y | w | h | Notes |\n|---|---|---|---|---|---|\n"


def test_repeated_rows_expand_from_lists_and_affine_expressions():
    text = _HDR + (
        "| KPI 1–4 | 24 / 496 / 968 / 1440 | 168 | 456 | 120 | n |\n"
        "| Trend 1-3 | 32+(i×472) | 784 | 448 | 264 | n |\n"
        "| Slicer 1–3 | 40 | 104, 248, 392 | 296 | 128 | n |\n")
    rows = {z["name"]: z for z in r.parse_slot_tables(text)[0]["rows"]}
    assert [rows[f"KPI {i}"]["x"] for i in range(1, 5)] == [24, 496, 968, 1440]
    assert [rows[f"Trend {i}"]["x"] for i in range(1, 4)] == [32, 504, 976]
    assert [rows[f"Slicer {i}"]["y"] for i in range(1, 4)] == [104, 248, 392]
    assert rows["Slicer 2"]["x"] == 40 and rows["KPI 1"]["w"] == 456


def test_group_row_with_single_numbers_is_not_expanded():
    text = _HDR + "| Gauge 1–4 | 32 | 96 | 1856 | 240 | one box for the whole band |\n"
    rows = r.parse_slot_tables(text)[0]["rows"]
    assert len(rows) == 1 and rows[0]["name"] == "Gauge 1–4" and rows[0]["w"] == 1856


def test_unexpressible_rows_are_reported_not_dropped_silently():
    text = _HDR + "| Line cells | 160…1584 | 152…816 | 344×4 | 56 per row | n |\n| Real | 8 | 8 | 16 | 16 | n |\n"
    table = r.parse_slot_tables(text)[0]
    assert table["unparsed"] == ["Line cells"] and [z["name"] for z in table["rows"]] == ["Real"]


def test_recipes_never_name_legacy_visual_types():
    """Official guardrail: multiRowCard / filledMap / map / matrix / table must not be created
    (use cardVisual / azureMap / pivotTable / tableEx). A bare `card` / `slicer` / `line` is the generic
    recipe word for the category and is allowed."""
    banned = re.compile(r"(?<![A-Za-z])(multiRowCard|filledMap|map|matrix|table)(?![A-Za-z])")
    offenders = []
    for layout in _LANDSCAPE:
        text = (r._INDEX.parent / layout["file"]).read_text(encoding="utf-8")
        for t in r.parse_slot_tables(text):
            if len(t["header"]) < 6 or t["header"][5].lower() != "visual type":
                continue
            for row in t["rows"]:
                if banned.search(row["extra"][0]):
                    offenders.append((layout["id"], row["name"], row["extra"][0]))
    assert offenders == [], offenders


def test_recipe_tables_have_no_silent_gaps():
    """Every landscape recipe's slot rows are fully parsed except the documented range rows."""
    allowed = {"pl-statement-grid": {"Line cells (value, plan, Δ, YoY)", "Sparkline cells", "Variance mini-bar col"}}
    for layout in _LANDSCAPE:
        text = (r._INDEX.parent / layout["file"]).read_text(encoding="utf-8")
        for t in r.parse_slot_tables(text):
            extra = set(t["unparsed"]) - allowed.get(layout["id"], set())
            assert not extra, f"{layout['id']}: rows not parsed: {sorted(extra)}"
