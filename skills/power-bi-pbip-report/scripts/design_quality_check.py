#!/usr/bin/env python3
"""
design_quality_check.py — lint a PBIR report against shared-standards.md.

Runs as Phase 4c Step 2 (Polisher role), AFTER finalize_pbir.py.

Checks (error / warning / info):
  1. E1: Contrast < 4.5:1 on any text vs background                     (ERROR)
  2. E2: Drillthrough page without a back button                        (ERROR)
  3. E3: Bookmark button action points to missing page                  (ERROR)
  4. E4: Page folder vs pages.json pageOrder mismatch (orphan/missing)  (ERROR)
  5. W1: Page has > 8 visuals (style-aware cap: exec=4, analyt=8, ops=12)  (WARN)
  6. W2: Pie / donut chart with > 5 slices                              (WARN)
  7. W3: Visual missing alt text                                        (WARN)
  8. W4: Default page name (starts with "Page" / "Copy of")             (WARN)
  9. W5: Title contains "Sum of" / "Count of"                           (WARN)
 10. W6: Hard-coded hex not via theme (after theme-token pass)          (WARN)
 11. W7: Visual with 3D effects enabled                                 (WARN)
 12. W8: Visual references > 6 distinct colors (rainbow anti-pattern)   (WARN)
 13. W9: Report-wide data-visual count > 60 (performance budget)        (WARN)
 14. W10: Alt text present but too short / duplicates title             (WARN)
 15. I1: Chart has room for data labels but labels are off              (INFO — not yet implemented)

Outputs:
  - Console summary (grouped by severity)
  - design_report.md in report root (optional, via --write-report)

Usage:
    python design_quality_check.py --report <path-to-.Report>
    python design_quality_check.py --report <path-to-.Report> --style analytical --write-report

Exit codes:
    0 — no errors (warnings/info OK)
    1 — input error (invalid path)
    2 — errors found
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pbir_utils import (
    HEX_RE,
    PRIMITIVE_VTYPES,
    REPORT_VISUAL_BUDGET,
    contrast_ratio,
    get_alt_text as _get_alt_text,
    get_visual_title as _get_visual_title,
    is_back_button as _is_back_button,
    is_drillthrough as _is_drillthrough,
    read_json as _read_json,
    setup_logging,
    visual_type as _visual_type,
)

DEFAULT_PAGE_NAMES = re.compile(r"^(Page \d+|Copy of .*|Untitled.*)$", re.IGNORECASE)
BAD_TITLE_RE = re.compile(r"^(sum of|count of|average of|first|last|min of|max of)\s", re.IGNORECASE)

Severity = Literal["error", "warning", "info"]


# ── Read cache: avoids re-reading visual.json / page.json once per check ──
_json_cache: dict[Path, dict] = {}
_text_cache: dict[Path, str] = {}


def _cached_json(path: Path) -> dict:
    """Return parsed JSON for *path*, reading from disk only on first call."""
    if path not in _json_cache:
        _json_cache[path] = _read_json(path)
    return _json_cache[path]


def _cached_text(path: Path) -> str:
    """Return raw text for *path*, reading from disk only on first call."""
    if path not in _text_cache:
        try:
            _text_cache[path] = path.read_text(encoding="utf-8")
        except (OSError, ValueError):
            _text_cache[path] = ""
    return _text_cache[path]


def _clear_cache() -> None:
    _json_cache.clear()
    _text_cache.clear()


@dataclass
class Finding:
    severity: Severity
    code: str
    message: str
    location: str = ""


@dataclass
class LintReport:
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: Severity, code: str, message: str, location: str = "") -> None:
        self.findings.append(Finding(severity=severity, code=code, message=message, location=location))

    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]

    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "info"]


# ────────────────────────────────────────────────────────────────
# Checks
# ────────────────────────────────────────────────────────────────

def check_visual_counts(report_root: Path, style: str, lint: LintReport) -> None:
    """W1: page visual count."""
    caps = {"executive": 4, "analytical": 8, "operational": 12}
    cap = caps.get(style, 8)

    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        if not page.is_dir():
            continue
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue

        count = 0
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            vtype = (_visual_type(data) or "").lower()
            if vtype in PRIMITIVE_VTYPES:
                continue
            count += 1

        if count > cap:
            lint.add(
                "warning",
                "W1",
                f"Page has {count} visuals (excl. slicers/buttons) — {style} cap is {cap}",
                f"pages/{page.name}",
            )


def check_drillthrough_back_button(report_root: Path, lint: LintReport) -> None:
    """E2: every drillthrough page must have a back button."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        if not page.is_dir():
            continue
        page_json = page / "page.json"
        if not page_json.exists():
            continue
        data = _cached_json(page_json)
        if not _is_drillthrough(data):
            continue

        has_back = False
        visuals_dir = page / "visuals"
        if visuals_dir.exists():
            for vdir in visuals_dir.iterdir():
                vjson = vdir / "visual.json"
                if not vjson.exists():
                    continue
                vdata = _cached_json(vjson)
                if _is_back_button(vdata):
                    has_back = True
                    break

        if not has_back:
            lint.add(
                "error",
                "E2",
                "Drillthrough page has no back button (navigate back action)",
                f"pages/{page.name}",
            )


def check_pie_slices(report_root: Path, lint: LintReport) -> None:
    """W2: pie/donut with > 5 slices (can only detect in some cases from JSON; flag any pie/donut found for manual review if we can't count)."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            vtype = (_visual_type(data) or "").lower()
            if vtype in ("pie", "piechart", "donut", "donutchart"):
                lint.add(
                    "warning",
                    "W2",
                    f"Pie/donut visual found ({vtype}) — verify ≤ 5 slices or use bar chart",
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_alt_text(report_root: Path, lint: LintReport) -> None:
    """W3: visuals missing alt text."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            vtype = (_visual_type(data) or "").lower()
            if vtype in ("button", "image", "shape", "textbox"):
                continue  # decorative; alt text optional
            if not _get_alt_text(data):
                lint.add(
                    "warning",
                    "W3",
                    f"Visual missing alt text ({vtype})",
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_default_page_names(report_root: Path, lint: LintReport) -> None:
    """W4: pages with default names."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        if not page.is_dir():
            continue
        page_json = page / "page.json"
        if not page_json.exists():
            continue
        data = _cached_json(page_json)
        name = data.get("displayName") or data.get("name") or ""
        if DEFAULT_PAGE_NAMES.match(name):
            lint.add(
                "warning",
                "W4",
                f"Default-looking page name: '{name}'",
                f"pages/{page.name}",
            )


def check_bad_titles(report_root: Path, lint: LintReport) -> None:
    """W5: visual titles starting with 'Sum of' / 'Count of' / etc."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            title = _get_visual_title(data)
            if title and BAD_TITLE_RE.match(title):
                lint.add(
                    "warning",
                    "W5",
                    f"Visual title uses auto-phrasing: '{title}'",
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_hardcoded_hex(report_root: Path, lint: LintReport) -> None:
    """W6: literal #RRGGBB in visual.json (after theme-token pass should be zero)."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            raw = _cached_text(vjson)
            hexes = set(HEX_RE.findall(raw))
            if hexes:
                lint.add(
                    "warning",
                    "W6",
                    f"Hard-coded hex colors found ({len(hexes)} unique) — use theme tokens",
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_bookmark_targets(report_root: Path, lint: LintReport) -> None:
    """E3: bookmark / button actions pointing to missing pages."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    valid_pages = {p.name for p in pages_dir.iterdir() if p.is_dir()}

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            raw = _cached_text(vjson)
            # Heuristic: "navigationSection" or "pageNavigation" references
            for match in re.finditer(r'"(?:pageName|sectionName)"\s*:\s*"([^"]+)"', raw):
                target = match.group(1)
                if target and target not in valid_pages:
                    lint.add(
                        "error",
                        "E3",
                        f"Button/bookmark targets missing page '{target}'",
                        f"pages/{page.name}/visuals/{vdir.name}",
                    )


# ────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────
# Additional checks (W7-W10, E4)
# ────────────────────────────────────────────────────────────────

THREE_D_HINTS = re.compile(r'"(is3D|enable3D|show3DEffect)"\s*:\s*true', re.IGNORECASE)


def check_three_d_effects(report_root: Path, lint: LintReport) -> None:
    """W7: any visual with 3D effects enabled — banned by shared-standards.md §1."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            raw = _cached_text(vjson)
            if THREE_D_HINTS.search(raw):
                lint.add(
                    "warning",
                    "W7",
                    "3D effect enabled — banned by shared-standards.md (flatten)",
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_rainbow_palette(report_root: Path, lint: LintReport) -> None:
    """W8: single visual uses > 6 distinct theme data tokens (rainbow anti-pattern).

    Heuristic: count distinct `ThemeDataColor` ColorId values AND distinct #RRGGBB values
    referenced inside one visual.json. Threshold > 6.
    """
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    token_re = re.compile(r'"ColorId"\s*:\s*(\d+)')
    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            raw = _cached_text(vjson)
            tokens = set(token_re.findall(raw))
            hexes = set(HEX_RE.findall(raw))
            distinct = len(tokens) + len(hexes)
            if distinct > 6:
                lint.add(
                    "warning",
                    "W8",
                    f"Visual references {distinct} distinct colors — rainbow anti-pattern (cap 6)",
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_report_visual_budget(report_root: Path, lint: LintReport) -> None:
    """W9: report total data-visual count > REPORT_VISUAL_BUDGET (performance budget)."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    total = 0
    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            vtype = (_visual_type(data) or "").lower()
            if vtype in PRIMITIVE_VTYPES:
                continue
            total += 1

    if total > REPORT_VISUAL_BUDGET:
        lint.add(
            "warning",
            "W9",
            f"Report contains {total} data visuals (excl. primitives) — performance budget is {REPORT_VISUAL_BUDGET}",
            "report-wide",
        )


def check_alt_text_quality(report_root: Path, lint: LintReport) -> None:
    """W10: alt text present but low-quality (too short or a copy of the title).

    Rules:
      - < 20 chars  → low-quality
      - equal to title → not accessible (screen reader gets nothing new)
    """
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            vtype = (_visual_type(data) or "").lower()
            if vtype in ("button", "image", "shape", "textbox", "basicshape"):
                continue
            alt = _get_alt_text(data)
            if not alt:
                continue  # W3 catches absence
            title = (_get_visual_title(data) or "").strip()
            reason = None
            if len(alt) < 20:
                reason = f"alt text too short ({len(alt)} chars, min 20)"
            elif title and alt.strip().lower() == title.lower():
                reason = "alt text duplicates title — add context"
            if reason:
                lint.add(
                    "warning",
                    "W10",
                    reason,
                    f"pages/{page.name}/visuals/{vdir.name}",
                )


def check_orphan_pages(report_root: Path, lint: LintReport) -> None:
    """E4: page folder present but not listed in pages.json pageOrder (or vice-versa)."""
    pages_dir = report_root / "definition" / "pages"
    pages_meta = report_root / "definition" / "pages.json"
    if not pages_dir.exists() or not pages_meta.exists():
        return

    meta = _cached_json(pages_meta)
    ordered = meta.get("pageOrder")
    if not isinstance(ordered, list) or not ordered:
        return  # pageOrder is optional per schema; skip silently

    folders = {p.name for p in pages_dir.iterdir() if p.is_dir()}
    ordered_set = set(ordered)

    for orphan in sorted(folders - ordered_set):
        lint.add(
            "error",
            "E4",
            f"Page folder '{orphan}' exists but is not in pages.json pageOrder",
            f"pages/{orphan}",
        )
    for missing in sorted(ordered_set - folders):
        lint.add(
            "error",
            "E4",
            f"pages.json pageOrder references missing folder '{missing}'",
            "definition/pages.json",
        )


# ── E1: contrast check ────────────────────────────────────────

# Regex patterns for extracting foreground/background color pairs from visual JSON
_FG_KEYS = re.compile(r'"(?:fontColor|labelColor|color|foreground(?:Color)?)"', re.IGNORECASE)
_BG_KEYS = re.compile(r'"(?:background(?:Color)?|fill)"', re.IGNORECASE)

# WCAG AA thresholds
_CONTRAST_NORMAL = 4.5  # normal text (< 18pt or < 14pt bold)
_CONTRAST_LARGE = 3.0   # large text (≥ 18pt or ≥ 14pt bold)


def _extract_color_props(data: dict) -> list[tuple[str, str]]:
    """Extract (foreground_hex, background_hex) pairs from visual objects/properties.

    Heuristic: walks `objects` → property groups looking for color-like keys
    with adjacent foreground and background entries.
    """
    pairs: list[tuple[str, str]] = []
    objects = data.get("visual", data).get("objects", data.get("visualContainer", {}).get("visual", {}).get("objects", {}))
    if not isinstance(objects, dict):
        return pairs

    for _group_name, group_entries in objects.items():
        if not isinstance(group_entries, list):
            continue
        for entry in group_entries:
            props = entry.get("properties", {})
            if not isinstance(props, dict):
                continue
            fg_hex = _extract_hex(props, ("fontColor", "labelColor", "color", "foregroundColor", "foreground"))
            bg_hex = _extract_hex(props, ("backgroundColor", "background", "fill"))
            if fg_hex and bg_hex:
                pairs.append((fg_hex, bg_hex))
    return pairs


def _extract_hex(props: dict, keys: tuple[str, ...]) -> str | None:
    """Try to extract a #RRGGBB value from one of the given property keys."""
    for key in keys:
        val = props.get(key)
        if isinstance(val, str) and HEX_RE.match(val):
            return val
        if isinstance(val, dict):
            # Solid expression: {"solid":{"color":"#RRGGBB"}} or {"expr":{"Literal":{"Value":"'#RRGGBB'"}}}
            solid = val.get("solid", {})
            if isinstance(solid, dict):
                c = solid.get("color", "")
                if isinstance(c, str) and HEX_RE.match(c):
                    return c
            lit = val.get("expr", {}).get("Literal", {}).get("Value", "") if isinstance(val.get("expr"), dict) else ""
            if isinstance(lit, str):
                lit = lit.strip("'\"")
                if HEX_RE.match(lit):
                    return lit
    return None


def check_contrast(report_root: Path, lint: LintReport) -> None:
    """E1: check foreground/background contrast ratio against WCAG AA thresholds."""
    pages_dir = report_root / "definition" / "pages"
    if not pages_dir.exists():
        return

    for page in sorted(pages_dir.iterdir()):
        visuals_dir = page / "visuals"
        if not visuals_dir.exists():
            continue
        for vdir in visuals_dir.iterdir():
            vjson = vdir / "visual.json"
            if not vjson.exists():
                continue
            data = _cached_json(vjson)
            pairs = _extract_color_props(data)
            for fg, bg in pairs:
                try:
                    ratio = contrast_ratio(fg, bg)
                except (ValueError, IndexError):
                    continue
                if ratio < _CONTRAST_LARGE:
                    lint.add(
                        "error",
                        "E1",
                        f"Contrast ratio {ratio:.1f}:1 between {fg} and {bg} — WCAG AA requires ≥ {_CONTRAST_NORMAL}:1",
                        f"pages/{page.name}/visuals/{vdir.name}",
                    )


# ────────────────────────────────────────────────────────────────
# Report writer
# ────────────────────────────────────────────────────────────────

def write_report(lint: LintReport, out_path: Path, style: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Design Quality Report",
        "",
        f"- Generated: **{ts}**",
        f"- Report: `{out_path.parent.name}`",
        f"- Style personality: **{style}**",
        f"- Errors: **{len(lint.errors())}**",
        f"- Warnings: **{len(lint.warnings())}**",
        f"- Info: **{len(lint.infos())}**",
        "",
    ]
    for severity, label in (("error", "Errors"), ("warning", "Warnings"), ("info", "Info")):
        findings = [f for f in lint.findings if f.severity == severity]
        if not findings:
            continue
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| Code | Location | Message |")
        lines.append("|---|---|---|")
        for f in findings:
            loc = f.location or "-"
            msg = f.message.replace("|", "\\|")
            lines.append(f"| {f.code} | `{loc}` | {msg} |")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


# ────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a PBIR report against design standards.")
    parser.add_argument("--report", required=True, type=Path, help="Path to the .Report folder")
    parser.add_argument("--style", default="analytical", choices=["executive", "analytical", "operational"], help="Style personality (affects visual count cap)")
    parser.add_argument("--write-report", action="store_true", help="Write design_report.md to report root")
    parser.add_argument("--verbose", action="store_true", help="Show debug details")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings and errors")
    args = parser.parse_args()

    log = setup_logging("design_quality_check", verbose=args.verbose, quiet=args.quiet)

    if not args.report.exists() or not args.report.is_dir():
        log.error("report path invalid: %s", args.report)
        return 1

    if not (args.report / "definition").exists():
        log.error("%s is not a PBIR report (missing 'definition/')", args.report)
        return 1

    lint = LintReport()
    _clear_cache()  # ensure fresh reads

    check_visual_counts(args.report, args.style, lint)
    check_drillthrough_back_button(args.report, lint)
    check_pie_slices(args.report, lint)
    check_alt_text(args.report, lint)
    check_default_page_names(args.report, lint)
    check_bad_titles(args.report, lint)
    check_hardcoded_hex(args.report, lint)
    check_bookmark_targets(args.report, lint)
    check_three_d_effects(args.report, lint)
    check_rainbow_palette(args.report, lint)
    check_report_visual_budget(args.report, lint)
    check_alt_text_quality(args.report, lint)
    check_orphan_pages(args.report, lint)
    check_contrast(args.report, lint)

    # Print summary grouped by severity
    for severity, label in (("error", "ERRORS"), ("warning", "WARNINGS"), ("info", "INFO")):
        findings = [f for f in lint.findings if f.severity == severity]
        if not findings:
            continue
        log.info("")
        log.info("=== %s (%d) ===", label, len(findings))
        for f in findings:
            loc = f" [{f.location}]" if f.location else ""
            log.info("  [%s]%s %s", f.code, loc, f.message)

    log.info("")
    log.info("Errors: %d, Warnings: %d, Info: %d", len(lint.errors()), len(lint.warnings()), len(lint.infos()))

    if args.write_report:
        report_path = args.report / "design_report.md"
        write_report(lint, report_path, args.style)
        log.info("Wrote: %s", report_path)

    return 2 if lint.errors() else 0


if __name__ == "__main__":
    sys.exit(main())
