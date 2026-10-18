"""Tests for build_report_from_layout.py and check_layout_drift.py (CLI-dependent tests skip without the CLI)."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS))

import build_report_from_layout as brl  # noqa: E402
import check_layout_drift as drift  # noqa: E402

CLI = shutil.which("powerbi-report-author")
needs_cli = pytest.mark.skipif(not CLI, reason="powerbi-report-author not installed")
EXAMPLE = _SCRIPTS.parent / "references" / "layout-spec-example.json"


def _scaffold(tmp: Path) -> Path:
    out = subprocess.run([CLI, "scaffold", str(tmp), "--name", "Gen", "--offline"], capture_output=True, text=True)
    if out.returncode != 0:
        pytest.skip("scaffold unavailable in this CLI version")
    return tmp / "Gen.Report"


def test_pure_helpers():
    assert brl.kebab("KPI 1") == "kpi-1"
    assert brl.folder_name("cardVisual", "KPI 1") == "card-kpi-1"
    assert brl.folder_name("clusteredBarChart", "Supporting 1") == "clusteredBarChart-supporting-1"
    p = brl.projection({"table": "_M", "measure": "Total Sales"})
    assert p["field"]["Measure"]["Property"] == "Total Sales"
    assert p["queryRef"] == "_M.Total Sales" and p["nativeQueryRef"] == "Total Sales"
    c = brl.projection({"table": "DimDate", "column": "Date"})
    assert "Column" in c["field"]
    a = brl.projection({"table": "F", "column": "Qty", "aggregation": 0})
    assert a["field"]["Aggregation"]["Function"] == 0
    with pytest.raises(brl.SpecError):
        brl.projection({"table": "T"})


@needs_cli
def test_unknown_role_and_missing_required_role_rejected():
    with pytest.raises(brl.SpecError):
        brl.check_roles("cardVisual", {"Fields": [{"table": "T", "measure": "m"}]})  # legacy role name
    with pytest.raises(brl.SpecError):
        brl.check_roles("cardVisual", {})  # required role Data missing


@needs_cli
def test_build_validates_and_writes_manifest(tmp_path):
    report = _scaffold(tmp_path)
    manifest = tmp_path / "_brief" / "layout-manifest.json"
    result = brl.build(report, json.loads(EXAMPLE.read_text(encoding="utf-8")), manifest)
    assert result["page"] == "overview" and result["canvas"] == {"width": 1920, "height": 1080}
    assert (report / "definition" / "pages" / "overview" / "visuals" / "card-kpi-1" / "visual.json").is_file()
    pages = json.loads((report / "definition" / "pages" / "pages.json").read_text(encoding="utf-8"))
    assert pages["pageOrder"] == ["overview"] and pages["activePageName"] == "overview"
    page = json.loads((report / "definition" / "pages" / "overview" / "page.json").read_text(encoding="utf-8"))
    assert (page["width"], page["height"]) == (1920, 1080) and page["name"] == "overview"
    # every generated position is on the 8-px grid and inside the canvas
    for v in result["visuals"]:
        assert all(n % 8 == 0 for n in (v["x"], v["y"], v["w"], v["h"]))
        assert v["x"] + v["w"] <= 1920 and v["y"] + v["h"] <= 1080
    verdict = json.loads(subprocess.run([CLI, "validate", str(report)], capture_output=True, text=True).stdout)
    assert verdict["data"]["result"] == "succeeded" and verdict["data"]["errorCount"] == 0


@needs_cli
def test_unknown_slot_rejected(tmp_path):
    report = _scaffold(tmp_path)
    spec = {"layout": "exec-overview-16x9", "slots": {"No such slot": {"visualType": "textbox"}}}
    with pytest.raises(brl.SpecError, match="not in layout"):
        brl.build(report, spec, None)


@needs_cli
def test_other_canvas_scales_slots(tmp_path):
    report = _scaffold(tmp_path)
    spec = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    spec["canvas"] = "1280x720"
    result = brl.build(report, spec, None)
    assert result["canvas"] == {"width": 1280, "height": 720}
    assert all(v["x"] + v["w"] <= 1280 and v["y"] + v["h"] <= 720 for v in result["visuals"])


@needs_cli
def test_drift_detects_move_missing_and_new_overlap(tmp_path):
    report = _scaffold(tmp_path)
    manifest_path = tmp_path / "_brief" / "layout-manifest.json"
    brl.build(report, json.loads(EXAMPLE.read_text(encoding="utf-8")), manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert [f for f in drift.check(report, manifest) if f["level"] != "info"] == []

    vdir = report / "definition" / "pages" / "overview" / "visuals"
    moved = vdir / "card-kpi-1" / "visual.json"
    data = json.loads(moved.read_text(encoding="utf-8"))
    data["position"]["x"] += 40
    moved.write_text(json.dumps(data), encoding="utf-8")
    shutil.rmtree(vdir / "textbox-page-title")
    # new overlap: drag the supporting chart up over the hero chart
    sup = vdir / "clusteredBarChart-supporting-1" / "visual.json"
    d2 = json.loads(sup.read_text(encoding="utf-8"))
    d2["position"]["y"] = 300
    sup.write_text(json.dumps(d2), encoding="utf-8")
    kinds = {(f["kind"], f.get("visual", "")) for f in drift.check(report, manifest)}
    assert ("moved", "card-kpi-1") in kinds
    assert ("missing", "textbox-page-title") in kinds
    assert ("moved", "clusteredBarChart-supporting-1") in kinds
    assert any(k == "overlap" for k, _ in kinds)
    assert drift.check(report, manifest, tolerance=400)  # tolerance relaxes moves but not missing visuals


def test_drift_cli_exit_codes(tmp_path):
    assert drift.main(["--report", str(tmp_path), "--manifest", str(tmp_path / "nope.json")]) == 1
