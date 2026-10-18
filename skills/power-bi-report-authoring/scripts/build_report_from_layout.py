#!/usr/bin/env python3
"""Generate PBIR visuals from a layout recipe + a slot spec (deterministic, no guessing).

The design skill's recipes define *where* visuals go (slot tables, FHD-native, rescalable); the spec says
*what* goes in each slot. This script joins them and writes valid `visual.json` files into an existing
report (create the shell first with `powerbi-report-author scaffold`). It also writes a layout manifest
that `check_layout_drift.py` uses to detect later drift between the approved layout and the report.

Spec (JSON):
{
  "layout": "exec-overview-16x9",            # id from layouts-index.json
  "canvas": "1920x1080",                     # default: the layout's own canvas
  "page": {"name": "overview", "displayName": "Revenue is 4% above plan"},   # name = folder slug
  "slots": {
    "Page title":  {"visualType": "textbox", "text": "Revenue is 4% above plan"},
    "KPI 1":       {"visualType": "cardVisual",
                    "bindings": {"Data": [{"table": "_Measures", "measure": "Total Revenue"}]},
                    "altText": "Total revenue, current period vs plan"},
    "Hero visual": {"visualType": "lineChart",
                    "bindings": {"Category": [{"table": "DimDate", "column": "Date"}],
                                 "Y": [{"table": "_Measures", "measure": "Total Revenue"}]}}
  }
}
Slots of the recipe that are not in the spec are skipped (reported). Spec slots that are not in the recipe
are an error. Roles are checked against `powerbi-report-author catalog describe <visualType>`; the
generated report is validated with `powerbi-report-author validate`.

Usage:
    python build_report_from_layout.py --report <path>.Report --spec spec.json [--manifest <file>] [--no-validate]

Exit codes: 0 ok, 1 input error (bad spec / unknown slot / role), 2 validation failed, 3 tool error.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

_HERE = Path(__file__).resolve().parent
_DESIGN_SCRIPTS = _HERE.parent.parent / "power-bi-report-design" / "scripts"
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_DESIGN_SCRIPTS))

import rescale_layout as rl  # noqa: E402

VISUAL_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json"
PAGE_SCHEMA_FALLBACK = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
LAYOUT_PAGE_SIZE_KEYS = ("width", "height")
# Visuals that carry no data query.
NO_QUERY_TYPES = {"textbox", "shape", "basicShape", "image", "actionButton", "pageNavigator", "bookmarkNavigator"}
# Legacy visual types the official authoring guardrails forbid creating → modern replacement.
LEGACY_TYPES = {"card": "cardVisual", "multiRowCard": "cardVisual", "table": "tableEx",
                "matrix": "pivotTable", "map": "azureMap", "filledMap": "azureMap"}

_CLI = shutil.which("powerbi-report-author")


class SpecError(ValueError):
    """Bad spec or unknown slot/role."""


def kebab(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def folder_name(visual_type: str, slot: str) -> str:
    """Repo convention: `<visualType>-<slot>`, visualType keeps its camelCase (`cardVisual` → `card`)."""
    prefix = "card" if visual_type == "cardVisual" else visual_type
    return f"{prefix}-{kebab(slot)}"


def _cli_json(args: list[str]) -> dict:
    if not _CLI:
        raise SpecError("powerbi-report-author not found on PATH (npm install -g @microsoft/powerbi-report-authoring-cli@latest)")
    out = subprocess.run([_CLI, *args], capture_output=True, text=True, timeout=120)
    try:
        return json.loads(out.stdout)
    except ValueError as exc:
        raise SpecError(f"unreadable CLI output for {' '.join(args)}: {out.stdout[:200] or out.stderr[:200]}") from exc


_catalog_cache: dict[str, dict] = {}


def describe(visual_type: str) -> dict:
    if visual_type not in _catalog_cache:
        data = _cli_json(["catalog", "describe", visual_type])
        if "error" in data:
            raise SpecError(f"unknown visualType {visual_type!r}: {data['error'].get('message', '')}")
        _catalog_cache[visual_type] = data["data"]
    return _catalog_cache[visual_type]


def projection(binding: dict) -> dict:
    """One role projection from {table, column|measure[, aggregation]} (Column/Measure/Aggregation forms)."""
    table = binding.get("table")
    if not table:
        raise SpecError(f"binding needs a 'table': {binding}")
    source = {"SourceRef": {"Entity": table}}
    if "measure" in binding:
        name = binding["measure"]
        field = {"Measure": {"Expression": source, "Property": name}}
    elif "column" in binding and binding.get("aggregation") is not None:
        name = binding["column"]
        field = {"Aggregation": {"Expression": {"Column": {"Expression": source, "Property": name}},
                                 "Function": int(binding["aggregation"])}}
    elif "column" in binding:
        name = binding["column"]
        field = {"Column": {"Expression": source, "Property": name}}
    else:
        raise SpecError(f"binding needs 'measure' or 'column': {binding}")
    return {"field": field, "queryRef": f"{table}.{name}", "nativeQueryRef": name}


def check_roles(visual_type: str, bindings: dict) -> None:
    info = describe(visual_type)
    roles = set(info.get("roles", {}))
    unknown = sorted(set(bindings) - roles)
    if unknown:
        raise SpecError(f"{visual_type}: unknown role(s) {unknown}; valid roles: {sorted(roles)}")
    missing = [r for r in info.get("requiredRoles", []) if not bindings.get(r)]
    if missing:
        raise SpecError(f"{visual_type}: required role(s) missing: {missing}")


def build_visual(slot: str, spec: dict, rect: dict, z: int, tab: int, name: str) -> dict:
    visual_type = spec.get("visualType")
    if not visual_type:
        raise SpecError(f"slot {slot!r}: 'visualType' is required")
    if visual_type in LEGACY_TYPES:
        raise SpecError(f"slot {slot!r}: legacy visualType {visual_type!r} must not be created — "
                        f"use {LEGACY_TYPES[visual_type]!r}")
    visual: dict[str, Any] = {"visualType": visual_type}
    bindings = spec.get("bindings") or {}
    if visual_type in NO_QUERY_TYPES:
        if bindings:
            raise SpecError(f"slot {slot!r}: {visual_type} takes no data bindings")
        describe(visual_type)  # still verifies the type exists in the catalog
    else:
        check_roles(visual_type, bindings)
        visual["query"] = {"queryState": {
            role: {"projections": [projection(b) for b in items]} for role, items in bindings.items()
        }}
        visual["drillFilterOtherVisuals"] = True
    if visual_type == "textbox":
        # Theme owns font/color: only the text is set, never hard-coded styling.
        visual["objects"] = {"general": [{"properties": {"paragraphs": [
            {"textRuns": [{"value": spec.get("text", slot)}], "horizontalTextAlignment": spec.get("align", "left")}
        ]}}]}
    container = {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {"x": rect["x"], "y": rect["y"], "z": z, "height": rect["h"], "width": rect["w"], "tabOrder": tab},
        "visual": visual,
    }
    alt = spec.get("altText") or (spec.get("text") if visual_type == "textbox" else None) or f"{slot}"
    from pbir_utils import set_alt_text  # shared with finalize_pbir (writes visualContainerObjects.general)
    set_alt_text(container, alt)
    return container


def ensure_page(report: Path, page: dict, canvas: tuple[int, int]) -> Path:
    pages_dir = report / "definition" / "pages"
    pages_json = pages_dir / "pages.json"
    if not pages_json.exists():
        raise SpecError(f"{report} has no definition/pages/pages.json — run `powerbi-report-author scaffold` first")
    slug = page.get("name") or "page-1"
    page_dir = pages_dir / slug
    index = json.loads(pages_json.read_text(encoding="utf-8"))
    existing = [d for d in pages_dir.iterdir() if d.is_dir()]
    # First build into a fresh scaffold: the single empty scaffolded page (opaque id) becomes the requested
    # slug. Safe because nothing references it yet; pages.json is updated in the same step.
    if not page_dir.exists() and len(existing) == 1 and not (existing[0] / "visuals").exists():
        old = existing[0]
        old.rename(page_dir)
        index["pageOrder"] = [slug if p == old.name else p for p in index.get("pageOrder", [])]
        if index.get("activePageName") == old.name:
            index["activePageName"] = slug
        pages_json.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        data_path = page_dir / "page.json"
        renamed = json.loads(data_path.read_text(encoding="utf-8"))
        renamed["name"] = slug
        data_path.write_text(json.dumps(renamed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    page_json = page_dir / "page.json"
    if page_json.exists():
        data = json.loads(page_json.read_text(encoding="utf-8"))
    else:
        template = next((json.loads(p.read_text(encoding="utf-8")) for p in pages_dir.glob("*/page.json")), None)
        schema = (template or {}).get("$schema", PAGE_SCHEMA_FALLBACK)
        data = {"$schema": schema, "name": slug, "displayName": page.get("displayName", slug),
                "displayOption": "FitToPage"}
        page_dir.mkdir(parents=True, exist_ok=True)
    data["displayName"] = page.get("displayName", data.get("displayName", slug))
    data["width"], data["height"] = canvas
    page_json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if slug not in index.get("pageOrder", []):
        index.setdefault("pageOrder", []).append(slug)
        index.setdefault("activePageName", slug)
        pages_json.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return page_dir


def build(report: Path, spec: dict, manifest: Optional[Path]) -> dict:
    layout_id = spec.get("layout")
    if not layout_id:
        raise SpecError("spec needs 'layout'")
    layout = rl.load_layout(layout_id)
    own = (layout["canvas"]["width"], layout["canvas"]["height"])
    canvas = rl.parse_canvas(spec["canvas"]) if spec.get("canvas") else own
    result = rl.rescale_layout(layout_id, canvas) if canvas != own else rl.rescale_layout(layout_id, own)
    if result["problems"]:
        raise SpecError(f"layout {layout_id} on {canvas[0]}x{canvas[1]} has problems: {result['problems']}")
    slots = {z["name"]: z for z in result["zones"]}
    slot_specs: dict[str, dict] = spec.get("slots") or {}
    unknown = sorted(set(slot_specs) - set(slots))
    if unknown:
        raise SpecError(f"slot(s) not in layout {layout_id}: {unknown}; available: {sorted(slots)}")
    skipped = sorted(set(slots) - set(slot_specs))

    page_dir = ensure_page(report, spec.get("page") or {}, canvas)
    visuals_dir = page_dir / "visuals"
    visuals_dir.mkdir(exist_ok=True)
    ordered = sorted(slot_specs, key=lambda s: (slots[s]["y"], slots[s]["x"]))
    entries = []
    used: set[str] = set()
    for tab, slot in enumerate(ordered):
        rect = slots[slot]
        name = folder_name(slot_specs[slot].get("visualType", "visual"), slot)
        n = 2
        while name in used:
            name, n = f"{folder_name(slot_specs[slot].get('visualType', 'visual'), slot)}-{n}", n + 1
        used.add(name)
        container = build_visual(slot, slot_specs[slot], rect, 1000 + tab * 100, 1000 + tab * 100, name)
        vdir = visuals_dir / name
        vdir.mkdir(exist_ok=True)
        (vdir / "visual.json").write_text(json.dumps(container, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        entries.append({"slot": slot, "visual": name, "page": page_dir.name,
                        "x": rect["x"], "y": rect["y"], "w": rect["w"], "h": rect["h"]})
    out = {"layout": layout_id, "canvas": {"width": canvas[0], "height": canvas[1]},
           "page": page_dir.name, "visuals": entries, "skipped_slots": skipped}
    if manifest:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        existing = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {"pages": {}}
        existing.setdefault("pages", {})[page_dir.name] = out
        manifest.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def default_manifest(report: Path) -> Path:
    return report.resolve().parent / "_brief" / "layout-manifest.json"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--report", required=True, type=Path, help="the .Report folder (from scaffold)")
    parser.add_argument("--spec", required=True, type=Path, help="slot spec JSON")
    parser.add_argument("--manifest", type=Path, default=None,
                        help="layout manifest to write/update (default: <project>/_brief/layout-manifest.json)")
    parser.add_argument("--no-validate", action="store_true", help="skip powerbi-report-author validate")
    args = parser.parse_args(argv)
    if not (args.report / "definition").is_dir():
        print(f"error: {args.report} is not a PBIR .Report folder", file=sys.stderr)
        return 1
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        result = build(args.report, spec, args.manifest or default_manifest(args.report))
    except (SpecError, rl.RescaleError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    if result["skipped_slots"]:
        print(f"note: {len(result['skipped_slots'])} recipe slot(s) not in the spec were skipped: "
              f"{result['skipped_slots']}", file=sys.stderr)
    if args.no_validate:
        return 0
    try:
        verdict = _cli_json(["validate", str(args.report)])
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    data = verdict.get("data", {})
    print(f"validate: {data.get('result')} (errors={data.get('errorCount')}, warnings={data.get('warningCount')})",
          file=sys.stderr)
    return 0 if data.get("result") in ("succeeded", "succeededWithWarnings") else 2


if __name__ == "__main__":
    sys.exit(main())
