#!/usr/bin/env python3
"""
finalize_pbir.py — deterministic mechanical polish for PBIR reports.

Runs as Phase 4c Step 1 (Polisher role).

Sub-modules (all on by default, order matters):
  1. snap_grid           — round x/y/width/height to 8px grid
  2. align_kpi_row       — equalize top + height + width of card visuals in a horizontal band
  3. apply_theme_tokens  — replace hard-coded #RRGGBB with nearest theme token
  4. normalize_fonts     — enforce Segoe UI + size scale from shared-standards.md
  5. ensure_alt_text     — derive alt text from visual title where missing

Usage:
    python finalize_pbir.py --report <path-to-.Report>
    python finalize_pbir.py --report <path-to-.Report> --skip ensure_alt_text,normalize_fonts
    python finalize_pbir.py --report <path-to-.Report> --dry-run

Exit codes:
    0 — success (changes made or no-op)
    1 — input error (path invalid, not a PBIR report, etc.)
    2 — processing error (malformed JSON, schema violation, etc.)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

# Windows default console (cp1252) can't print U+2264/U+2014 etc.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass

GRID = 8

# Canonical font scale from shared-standards.md §4
FONT_FAMILY = "Segoe UI"
FONT_SIZES = {
    "page_title": 24,
    "page_subtitle": 14,
    "visual_title": 14,
    "visual_subtitle": 11,
    "axis_label": 10,
    "data_label": 12,
    "card_value": 32,
    "card_label": 11,
    "button": 12,
    "tooltip": 11,
}

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")


@dataclass
class Report:
    root: Path
    pages: list[Path]
    theme: dict[str, str] | None  # token -> hex

    @classmethod
    def load(cls, root: Path) -> "Report":
        if not (root / "definition").exists():
            raise ValueError(f"{root} does not look like a PBIR report (missing 'definition/')")

        pages_root = root / "definition" / "pages"
        pages = sorted([p for p in pages_root.iterdir() if p.is_dir()]) if pages_root.exists() else []

        theme = _load_theme_tokens(root)
        return cls(root=root, pages=pages, theme=theme)

    def iter_visuals(self):
        for page in self.pages:
            visuals_dir = page / "visuals"
            if not visuals_dir.exists():
                continue
            for vdir in sorted(visuals_dir.iterdir()):
                visual_json = vdir / "visual.json"
                if visual_json.exists():
                    yield page, vdir, visual_json


def _load_theme_tokens(root: Path) -> dict[str, str] | None:
    """Extract token-to-hex map from the report's theme, if any."""
    theme_candidates = list((root / "StaticResources" / "SharedResources" / "BaseThemes").glob("*.json")) \
        if (root / "StaticResources" / "SharedResources" / "BaseThemes").exists() else []
    theme_candidates += list((root / "StaticResources").rglob("*Theme*.json"))

    if not theme_candidates:
        return None

    for p in theme_candidates:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        tokens: dict[str, str] = {}
        for i, color in enumerate(data.get("dataColors", [])):
            tokens[f"data{i}"] = color
        for key in ("foreground", "background", "tableAccent", "good", "bad", "neutral", "maximum", "center", "minimum"):
            if key in data and isinstance(data[key], str):
                tokens[key] = data[key]
        if tokens:
            return tokens
    return None


# ────────────────────────────────────────────────────────────────
# Sub-module 1: snap_grid
# ────────────────────────────────────────────────────────────────

def snap_grid(report: Report, dry_run: bool = False) -> dict[str, int]:
    """Round every x/y/width/height to the 8px grid."""
    changed_visuals = 0
    changed_fields = 0

    for _page, _vdir, visual_json in report.iter_visuals():
        data = _read_json(visual_json)
        pos = data.get("position") or (data.get("visualContainer", {}) if isinstance(data.get("visualContainer"), dict) else {}).get("position")
        if not isinstance(pos, dict):
            continue
        local_changes = 0
        for key in ("x", "y", "width", "height"):
            if key in pos and isinstance(pos[key], (int, float)):
                rounded = round(pos[key] / GRID) * GRID
                if rounded != pos[key]:
                    pos[key] = rounded
                    local_changes += 1
        if local_changes:
            changed_visuals += 1
            changed_fields += local_changes
            if not dry_run:
                _write_json(visual_json, data)

    return {"visuals_changed": changed_visuals, "fields_changed": changed_fields}


# ────────────────────────────────────────────────────────────────
# Sub-module 2: align_kpi_row
# ────────────────────────────────────────────────────────────────

def align_kpi_row(report: Report, dry_run: bool = False) -> dict[str, int]:
    """
    Detect card visuals in a horizontal band (top within 16px of each other)
    and equalize their top + height.
    """
    rows_aligned = 0
    cards_adjusted = 0

    for page in report.pages:
        cards: list[tuple[Path, dict, dict]] = []
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _read_json(vjson)
            if _visual_type(data) in ("card", "multiRowCard"):
                pos = _get_pos(data)
                if pos and all(k in pos for k in ("x", "y", "width", "height")):
                    cards.append((vjson, data, pos))

        # Group cards into horizontal bands (top within 16px tolerance)
        cards.sort(key=lambda t: (t[2]["y"], t[2]["x"]))
        bands: list[list[tuple[Path, dict, dict]]] = []
        for card in cards:
            placed = False
            for band in bands:
                if abs(band[0][2]["y"] - card[2]["y"]) <= 16:
                    band.append(card)
                    placed = True
                    break
            if not placed:
                bands.append([card])

        for band in bands:
            if len(band) < 2:
                continue
            # Canonical top + height = median
            ys = sorted(c[2]["y"] for c in band)
            heights = sorted(c[2]["height"] for c in band)
            canon_y = ys[len(ys) // 2]
            canon_h = heights[len(heights) // 2]
            canon_y = round(canon_y / GRID) * GRID
            canon_h = round(canon_h / GRID) * GRID

            band_changed = False
            for vjson, data, pos in band:
                if pos["y"] != canon_y or pos["height"] != canon_h:
                    pos["y"] = canon_y
                    pos["height"] = canon_h
                    cards_adjusted += 1
                    band_changed = True
                    if not dry_run:
                        _write_json(vjson, data)
            if band_changed:
                rows_aligned += 1

    return {"rows_aligned": rows_aligned, "cards_adjusted": cards_adjusted}


# ────────────────────────────────────────────────────────────────
# Sub-module 3: apply_theme_tokens
# ────────────────────────────────────────────────────────────────

def apply_theme_tokens(report: Report, dry_run: bool = False) -> dict[str, int]:
    """Replace hard-coded #RRGGBB hex values in visual.json with the nearest theme token."""
    if not report.theme:
        return {"visuals_changed": 0, "replacements": 0, "skipped_reason": "no theme found"}

    reverse = {_normalize_hex(v): k for k, v in report.theme.items() if isinstance(v, str)}
    changes_total = 0
    visuals_changed = 0

    for _page, _vdir, visual_json in report.iter_visuals():
        raw = visual_json.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            norm = _normalize_hex(match.group(0))
            token = reverse.get(norm)
            if token:
                # Surround with a marker so future runs don't re-process
                return f'{{"solid":{{"color":{{"expr":{{"ThemeDataColor":{{"ColorId":"{token}"}}}}}}}}}}'
            return match.group(0)

        new_raw, n = HEX_RE.subn(replace, raw)
        if n:
            changes_total += n
            visuals_changed += 1
            if not dry_run:
                visual_json.write_text(new_raw, encoding="utf-8")

    return {"visuals_changed": visuals_changed, "replacements": changes_total}


# ────────────────────────────────────────────────────────────────
# Sub-module 4: normalize_fonts
# ────────────────────────────────────────────────────────────────

def normalize_fonts(report: Report, dry_run: bool = False) -> dict[str, int]:
    """Enforce Segoe UI family everywhere; reset title/label/value sizes where obviously off."""
    visuals_changed = 0
    props_changed = 0

    for _page, _vdir, visual_json in report.iter_visuals():
        data = _read_json(visual_json)
        local = _walk_and_fix_fonts(data)
        if local:
            visuals_changed += 1
            props_changed += local
            if not dry_run:
                _write_json(visual_json, data)

    return {"visuals_changed": visuals_changed, "props_changed": props_changed}


def _walk_and_fix_fonts(node: Any) -> int:
    """Recursively find font-family properties and normalize to Segoe UI."""
    changes = 0
    if isinstance(node, dict):
        # PBIR typically nests like: objects.labels[0].properties.fontFamily.expr.Literal.Value = "'Arial, Helvetica'"
        for key, value in list(node.items()):
            if key.lower() in ("fontfamily", "fontfamilyname"):
                if isinstance(value, dict):
                    # {"expr":{"Literal":{"Value":"'...'"}}} style
                    lit = value.get("expr", {}).get("Literal", {}).get("Value") if isinstance(value.get("expr"), dict) else None
                    if lit and FONT_FAMILY not in lit:
                        value["expr"]["Literal"]["Value"] = f"'{FONT_FAMILY}'"
                        changes += 1
                elif isinstance(value, str) and FONT_FAMILY not in value:
                    node[key] = FONT_FAMILY
                    changes += 1
            else:
                changes += _walk_and_fix_fonts(value)
    elif isinstance(node, list):
        for item in node:
            changes += _walk_and_fix_fonts(item)
    return changes


# ────────────────────────────────────────────────────────────────
# Sub-module 5: ensure_alt_text
# ────────────────────────────────────────────────────────────────

def ensure_alt_text(report: Report, dry_run: bool = False) -> dict[str, int]:
    """Where alt text is missing, derive from visual title + type."""
    added = 0

    for _page, _vdir, visual_json in report.iter_visuals():
        data = _read_json(visual_json)
        alt = _get_alt_text(data)
        if alt:
            continue
        title = _get_visual_title(data) or _visual_type(data) or "visual"
        vtype = _visual_type(data) or "visual"
        derived = f"{vtype} showing {title}".strip()
        if _set_alt_text(data, derived):
            added += 1
            if not dry_run:
                _write_json(visual_json, data)

    return {"alt_text_added": added}


# ────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────

def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _get_pos(data: dict) -> dict | None:
    if isinstance(data.get("position"), dict):
        return data["position"]
    vc = data.get("visualContainer")
    if isinstance(vc, dict) and isinstance(vc.get("position"), dict):
        return vc["position"]
    return None


def _visual_type(data: dict) -> str | None:
    v = data.get("visual") or data.get("visualContainer", {}).get("visual", {})
    if isinstance(v, dict):
        return v.get("visualType") or v.get("type")
    return None


def _get_visual_title(data: dict) -> str | None:
    # Heuristic: look for objects.title[0].properties.text.expr.Literal.Value
    try:
        v = data.get("visual") or data.get("visualContainer", {}).get("visual", {})
        title = v.get("objects", {}).get("title", [{}])[0].get("properties", {}).get("text")
        if isinstance(title, dict):
            return title.get("expr", {}).get("Literal", {}).get("Value", "").strip("'")
        if isinstance(title, str):
            return title
    except (AttributeError, IndexError, KeyError):
        pass
    return None


def _get_alt_text(data: dict) -> str | None:
    try:
        v = data.get("visual") or data.get("visualContainer", {}).get("visual", {})
        alt = v.get("objects", {}).get("general", [{}])[0].get("properties", {}).get("altText")
        if isinstance(alt, dict):
            return alt.get("expr", {}).get("Literal", {}).get("Value", "").strip("'") or None
        if isinstance(alt, str):
            return alt
    except (AttributeError, IndexError, KeyError):
        pass
    return None


def _set_alt_text(data: dict, text: str) -> bool:
    v = data.get("visual") or data.get("visualContainer", {}).get("visual", {})
    if not isinstance(v, dict):
        return False
    objs = v.setdefault("objects", {})
    general = objs.setdefault("general", [{}])
    if not general:
        general.append({})
    props = general[0].setdefault("properties", {})
    props["altText"] = {"expr": {"Literal": {"Value": f"'{text}'"}}}
    return True


def _normalize_hex(h: str) -> str:
    return h.upper().lstrip("#")


# ────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────

MODULES: dict[str, Callable[[Report, bool], dict]] = {
    "snap_grid": snap_grid,
    "align_kpi_row": align_kpi_row,
    "apply_theme_tokens": apply_theme_tokens,
    "normalize_fonts": normalize_fonts,
    "ensure_alt_text": ensure_alt_text,
}
# Order matters: snap_grid before align_kpi_row; fonts before alt text (doesn't matter).
MODULE_ORDER = ["snap_grid", "align_kpi_row", "apply_theme_tokens", "normalize_fonts", "ensure_alt_text"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Mechanical polish for PBIR reports.")
    parser.add_argument("--report", required=True, type=Path, help="Path to the .Report folder")
    parser.add_argument("--skip", default="", help="Comma-separated module names to skip")
    parser.add_argument("--only", default="", help="Comma-separated module names to run (overrides --skip)")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change, don't write")
    args = parser.parse_args()

    if not args.report.exists() or not args.report.is_dir():
        print(f"ERROR: report path invalid: {args.report}", file=sys.stderr)
        return 1

    try:
        report = Report.load(args.report)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    print(f"Report: {args.report}")
    print(f"Pages: {len(report.pages)}")
    print(f"Theme tokens: {len(report.theme) if report.theme else 0}")
    print(f"Dry-run: {args.dry_run}")
    print()

    for module_name in MODULE_ORDER:
        if only and module_name not in only:
            continue
        if module_name in skip:
            print(f"SKIP  {module_name}")
            continue
        fn = MODULES[module_name]
        try:
            result = fn(report, args.dry_run)
        except Exception as e:  # noqa: BLE001
            print(f"ERROR in {module_name}: {e}", file=sys.stderr)
            return 2
        summary = ", ".join(f"{k}={v}" for k, v in result.items())
        print(f"OK    {module_name}: {summary}")

    print()
    print("Done." if not args.dry_run else "Done (dry-run).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
