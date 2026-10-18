#!/usr/bin/env python3
"""Detect drift between the approved layout and the built report.

`build_report_from_layout.py` records every generated visual's slot rectangle in a manifest
(`_brief/layout-manifest.json`). This check re-reads the report and compares:

  moved/resized  a manifest visual whose position differs from its slot (beyond --tolerance px)  → ERROR
  missing        a manifest visual whose folder/visual.json no longer exists                       → ERROR
  out of canvas  any visual extending past the page width/height                                   → ERROR
  overlap        two visuals overlapping that were not overlapping in the manifest (new overlap)   → WARN
  extra          visuals on a managed page that are not in the manifest (e.g. narrative-pass
                 buttons/annotations)                                                              → INFO

Usage:
    python check_layout_drift.py --report <path>.Report [--manifest <file>] [--tolerance 0] [--json out.json]

Exit codes: 0 no errors, 1 input error, 2 drift errors found.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def _rect(visual_json: Path) -> Optional[tuple[int, int, int, int]]:
    try:
        pos = json.loads(visual_json.read_text(encoding="utf-8")).get("position") or {}
        return int(pos["x"]), int(pos["y"]), int(pos["width"]), int(pos["height"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def check(report: Path, manifest: dict, tolerance: int = 0) -> list[dict]:
    findings: list[dict] = []
    for page_name, page in manifest.get("pages", {}).items():
        page_dir = report / "definition" / "pages" / page_name
        if not page_dir.is_dir():
            findings.append({"level": "error", "kind": "missing-page", "page": page_name,
                             "message": f"page folder {page_name!r} no longer exists"})
            continue
        canvas = page.get("canvas", {})
        actual: dict[str, tuple[int, int, int, int]] = {}
        for vdir in sorted((page_dir / "visuals").glob("*")) if (page_dir / "visuals").is_dir() else []:
            vj = vdir / "visual.json"
            r = _rect(vj) if vj.is_file() else None
            if r:
                actual[vdir.name] = r
        expected = {v["visual"]: (v["x"], v["y"], v["w"], v["h"]) for v in page.get("visuals", [])}
        for name, want in expected.items():
            got = actual.get(name)
            if got is None:
                findings.append({"level": "error", "kind": "missing", "page": page_name, "visual": name,
                                 "message": "visual from the approved layout is missing"})
            elif any(abs(g - w) > tolerance for g, w in zip(got, want)):
                findings.append({"level": "error", "kind": "moved", "page": page_name, "visual": name,
                                 "expected": list(want), "actual": list(got),
                                 "message": f"x,y,w,h {list(got)} differs from layout {list(want)}"})
        for name in sorted(set(actual) - set(expected)):
            findings.append({"level": "info", "kind": "extra", "page": page_name, "visual": name,
                             "message": "not in the layout manifest (added after generation)"})
        width, height = canvas.get("width"), canvas.get("height")
        if width and height:
            for name, (x, y, w, h) in actual.items():
                if x < 0 or y < 0 or x + w > width or y + h > height:
                    findings.append({"level": "error", "kind": "out-of-canvas", "page": page_name, "visual": name,
                                     "message": f"extends past the {width}x{height} page"})
        baseline = {tuple(sorted((a, b))) for a in expected for b in expected
                    if a < b and _overlap(expected[a], expected[b])}
        names = sorted(actual)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if _overlap(actual[a], actual[b]) and (a, b) not in baseline:
                    findings.append({"level": "warn", "kind": "overlap", "page": page_name, "visual": f"{a} / {b}",
                                     "message": "new overlap (not in the approved layout)"})
    return findings


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=None,
                        help="default: <project>/_brief/layout-manifest.json next to the .Report folder")
    parser.add_argument("--tolerance", type=int, default=0, help="allowed per-edge difference in px (default 0)")
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)
    manifest_path = args.manifest or args.report.resolve().parent / "_brief" / "layout-manifest.json"
    if not (args.report / "definition").is_dir() or not manifest_path.is_file():
        print(f"error: need a .Report folder and a manifest ({manifest_path})", file=sys.stderr)
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"error: unreadable manifest: {exc}", file=sys.stderr)
        return 1
    findings = check(args.report, manifest, args.tolerance)
    errors = [f for f in findings if f["level"] == "error"]
    for f in findings:
        print(f"[{f['level'].upper():5}] {f['page']}/{f.get('visual', '')}: {f['message']}")
    print(f"layout drift: {len(errors)} error(s), {sum(f['level'] == 'warn' for f in findings)} warning(s), "
          f"{sum(f['level'] == 'info' for f in findings)} extra")
    if args.json:
        args.json.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
