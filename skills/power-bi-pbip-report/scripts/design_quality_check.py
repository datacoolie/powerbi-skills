#!/usr/bin/env python3
"""
design_quality_check.py — lint a PBIR report against shared-standards.md.

Runs as Phase 4c Step 2 (Polisher role), AFTER finalize_pbir.py.

Checks (error / warning / info):
  1. E1: Contrast < 4.5:1 on any text vs background                     (ERROR — not yet implemented)
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
from pathlib import Path
from typing import Literal

# Windows default console (cp1252) can't print U+2264/U+2014 etc.
# Force UTF-8 on stdout/stderr so messages containing ≤, —, … render cleanly.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
DEFAULT_PAGE_NAMES = re.compile(r"^(Page \d+|Copy of .*|Untitled.*)$", re.IGNORECASE)
BAD_TITLE_RE = re.compile(r"^(sum of|count of|average of|first|last|min of|max of)\s", re.IGNORECASE)

Severity = Literal["error", "warning", "info"]


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
            data = _read_json(vjson)
            vtype = _visual_type(data) or ""
            if vtype.lower() in ("slicer", "button", "actionbutton", "image", "textbox", "shape"):
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
        data = _read_json(page_json)
        if not _is_drillthrough(data):
            continue

        has_back = False
        visuals_dir = page / "visuals"
        if visuals_dir.exists():
            for vdir in visuals_dir.iterdir():
                vjson = vdir / "visual.json"
                if not vjson.exists():
                    continue
                vdata = _read_json(vjson)
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
            data = _read_json(vjson)
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
            data = _read_json(vjson)
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
        data = _read_json(page_json)
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
            data = _read_json(vjson)
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
            raw = vjson.read_text(encoding="utf-8")
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
            raw = vjson.read_text(encoding="utf-8")
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

def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _visual_type(data: dict) -> str | None:
    v = data.get("visual") or data.get("visualContainer", {}).get("visual", {})
    if isinstance(v, dict):
        return v.get("visualType") or v.get("type")
    return None


def _get_visual_title(data: dict) -> str | None:
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
            return alt.strip() or None
    except (AttributeError, IndexError, KeyError):
        pass
    return None


def _is_drillthrough(page_data: dict) -> bool:
    # PBIR page.json typically has "filterConfig" or "pageBinding" indicating drillthrough
    raw = json.dumps(page_data).lower()
    return "drillthrough" in raw or "pagebinding" in raw


def _is_back_button(visual_data: dict) -> bool:
    v = visual_data.get("visual") or visual_data.get("visualContainer", {}).get("visual", {})
    vtype = (v.get("visualType") or v.get("type") or "").lower()
    if vtype not in ("actionbutton", "button"):
        return False
    raw = json.dumps(visual_data).lower()
    # action is "back" OR shapeType is "back"
    return '"back"' in raw or "shapetype" in raw and "back" in raw


# ────────────────────────────────────────────────────────────────
# Additional checks (W7-W10, E4)
# ────────────────────────────────────────────────────────────────

REPORT_VISUAL_BUDGET = 60  # shared-standards.md §8
PRIMITIVE_VTYPES = {"slicer", "button", "actionbutton", "image", "textbox", "shape", "basicshape"}
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
            raw = vjson.read_text(encoding="utf-8")
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
            raw = vjson.read_text(encoding="utf-8")
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
            data = _read_json(vjson)
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
            data = _read_json(vjson)
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

    meta = _read_json(pages_meta)
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


# ────────────────────────────────────────────────────────────────
# Report writer
# ────────────────────────────────────────────────────────────────

def write_report(lint: LintReport, out_path: Path, style: str) -> None:
    lines = [
        "# Design Quality Report",
        "",
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
    args = parser.parse_args()

    if not args.report.exists() or not args.report.is_dir():
        print(f"ERROR: report path invalid: {args.report}", file=sys.stderr)
        return 1

    if not (args.report / "definition").exists():
        print(f"ERROR: {args.report} is not a PBIR report (missing 'definition/')", file=sys.stderr)
        return 1

    lint = LintReport()

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

    # Print summary grouped by severity
    for severity, label in (("error", "ERRORS"), ("warning", "WARNINGS"), ("info", "INFO")):
        findings = [f for f in lint.findings if f.severity == severity]
        if not findings:
            continue
        print(f"\n=== {label} ({len(findings)}) ===")
        for f in findings:
            loc = f" [{f.location}]" if f.location else ""
            print(f"  [{f.code}]{loc} {f.message}")

    print()
    print(f"Errors: {len(lint.errors())}, Warnings: {len(lint.warnings())}, Info: {len(lint.infos())}")

    if args.write_report:
        report_path = args.report / "design_report.md"
        write_report(lint, report_path, args.style)
        print(f"Wrote: {report_path}")

    return 2 if lint.errors() else 0


if __name__ == "__main__":
    sys.exit(main())
