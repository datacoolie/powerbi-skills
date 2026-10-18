#!/usr/bin/env python3
"""Rescale a layout recipe to another canvas of the same aspect ratio.

The layouts library is authored on **1920x1080 (FHD)**, the default report canvas. The same recipe
can serve another 16:9 canvas (1280x720, 2560x1440): every slot is scaled uniformly and its *edges*
are snapped to the 8-px grid (snapping edges, not sizes, keeps adjacent slots flush and gutters
positive). Source of the slots: the recipe's own `| Slot | x | y | w | h |` table when it has one,
else the coarser `zones_detail` in layouts-index.json. The source canvas is read from the layout
(`canvas` in the index); `--from-canvas` applies to `--rect` / `--table` / `--check` only.

Usage:
    python rescale_layout.py --layout exec-overview-16x9 --canvas 1280x720
    python rescale_layout.py --layout exec-overview-16x9 --canvas 2560x1440 --format md
    python rescale_layout.py --canvas 1920x1080 --check references/layouts/exec-overview-16x9.md
    python rescale_layout.py --canvas 1280x720 --rect 32,24,640,128                           # a box from 1920x1080
    python rescale_layout.py --canvas 1920x1080 --table <old.md> --from-canvas 1664x936       # migrate a legacy recipe

Exit codes: 0 ok, 1 input error (unknown layout / bad canvas / aspect mismatch / --source md without
a table), 2 the result introduces overlaps, leaves the canvas, or (--check) breaks the grid/margins.

Typography is NOT scaled here: font sizes come from the theme / Design Brief.
Re-check text-bearing slots (titles, KPI callouts) after rescaling.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GRID = 8
ASPECT_TOLERANCE = 0.01
_INDEX = Path(__file__).resolve().parent.parent / "references" / "layouts" / "layouts-index.json"


class RescaleError(ValueError):
    """Bad input (unknown layout, malformed canvas, aspect mismatch)."""


def parse_canvas(text: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d{3,5})\s*[x×]\s*(\d{3,5})\s*", text)
    if not match:
        raise RescaleError(f"canvas must look like 1920x1080, got {text!r}")
    return int(match.group(1)), int(match.group(2))


def _snap(value: float) -> int:
    return int(round(value / GRID)) * GRID


def rescale_zones(zones: list[dict], src: tuple[int, int], dst: tuple[int, int]) -> list[dict]:
    """Return zones scaled from ``src`` to ``dst`` with edges snapped to the grid."""
    src_w, src_h = src
    dst_w, dst_h = dst
    if abs(src_w / src_h - dst_w / dst_h) > ASPECT_TOLERANCE:
        raise RescaleError(
            f"aspect ratio mismatch: {src_w}x{src_h} -> {dst_w}x{dst_h}. "
            "Rescaling is only defined for the same aspect ratio; pick another layout instead."
        )
    sx, sy = dst_w / src_w, dst_h / src_h
    out = []
    for zone in zones:
        x0, y0 = _snap(zone["x"] * sx), _snap(zone["y"] * sy)
        x1, y1 = _snap((zone["x"] + zone["w"]) * sx), _snap((zone["y"] + zone["h"]) * sy)
        scaled = dict(zone)
        scaled.update(x=x0, y=y0, w=x1 - x0, h=y1 - y0)
        out.append(scaled)
    return out


def _overlaps(zones: list[dict]) -> set[frozenset]:
    pairs = set()
    for i, a in enumerate(zones):
        for b in zones[i + 1:]:
            if a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] \
                    and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]:
                pairs.add(frozenset((a["name"], b["name"])))
    return pairs


def problems(zones: list[dict], canvas: tuple[int, int], source_zones: list[dict] | None = None) -> list[str]:
    """Collapsed/out-of-canvas zones and overlaps *introduced* by rescaling.

    Overlaps already present in the source recipe (e.g. a back button placed on a
    title bar) are intentional and are not reported.
    """
    found = []
    width, height = canvas
    for z in zones:
        if z["w"] <= 0 or z["h"] <= 0:
            found.append(f"{z['name']}: collapsed to {z['w']}x{z['h']}")
        if z["x"] < 0 or z["y"] < 0 or z["x"] + z["w"] > width or z["y"] + z["h"] > height:
            found.append(f"{z['name']}: outside the {width}x{height} canvas")
    known = _overlaps(source_zones) if source_zones else set()
    for pair in sorted(_overlaps(zones) - known, key=sorted):
        found.append(f"{' overlaps '.join(sorted(pair))} (new after rescale)")
    return found


def load_layout(layout_id: str, index_path: Path = _INDEX) -> dict:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    for layout in index["layouts"]:
        if layout["id"] == layout_id:
            return layout
    raise RescaleError(f"unknown layout id {layout_id!r}")


_INT = re.compile(r"-?\d+")
_NAME_RANGE = re.compile(r"^(.*?)(\d+)\s*[–-]\s*(\d+)$")
_AFFINE = re.compile(r"^(-?\d+)\s*\+\s*\(\s*i\s*[×x*]\s*(\d+)\s*\)$")


def _values(cell: str, count: int) -> list[int] | None:
    """One coordinate cell → `count` ints: `N`, `A / B / C`, `A, B, C`, or `A+(i×B)`; None if not expandable."""
    cell = cell.strip()
    if _INT.fullmatch(cell):
        return [int(cell)] * count
    affine = _AFFINE.match(cell)
    if affine:
        return [int(affine.group(1)) + i * int(affine.group(2)) for i in range(count)]
    parts = [p.strip() for p in re.split(r"\s*[/,]\s*", cell)]
    if len(parts) == count and all(_INT.fullmatch(p) for p in parts):
        return [int(p) for p in parts]
    return None


def _expand_row(cells: list[str]) -> list[dict] | None:
    """One markdown row → slot rows.

    A repeated row ("KPI 1–4") expands to N slots only when a coordinate varies per item (`A / B / C / D`
    or `A+(i×B)`). If every coordinate is a single number the row describes the whole group as one box
    (e.g. "Gauge 1–4 | 32 | 96 | 1856 | 240") and stays a single slot.
    """
    name, coords, extra = cells[0], cells[1:5], cells[5:]
    match = _NAME_RANGE.match(name)
    count = (int(match.group(3)) - int(match.group(2)) + 1) if match else 1
    if count < 1:
        return None
    if all(_INT.fullmatch(c.strip()) for c in coords):
        count, match = 1, None
    columns = [_values(c, count) for c in coords]
    if any(c is None for c in columns):
        return None
    rows = []
    for i in range(count):
        label = f"{match.group(1)}{int(match.group(2)) + i}" if match else name
        x, y, w, h = (col[i] for col in columns)
        rows.append({"name": label, "x": x, "y": y, "w": w, "h": h, "extra": extra})
    return rows


def parse_slot_tables(text: str) -> list[dict]:
    """Markdown tables whose header is `| Slot | x | y | w | h | ... |`.

    Numeric rows are returned as slots; repeated rows (`KPI 1–4` with a value list or `A+(i×B)`) are
    expanded; rows that cannot be expressed as integers (e.g. `160…1584`) are listed by name in
    ``table["unparsed"]`` — consumers must treat those slots as not covered.
    """
    tables: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            current = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and [c.lower() for c in cells[1:5]] == ["x", "y", "w", "h"]:
            current = {"header": cells, "rows": [], "unparsed": []}
            tables.append(current)
        elif current is not None and len(cells) >= 5 and all(c.lstrip("-:") == "" for c in cells[:5]):
            continue  # separator row
        elif current is not None and len(cells) >= 5:
            expanded = _expand_row(cells)
            if expanded is None:
                current["unparsed"].append(cells[0])
            else:
                current["rows"].extend(expanded)
        else:
            current = None
    return [t for t in tables if t["rows"] or t["unparsed"]]


def format_slot_table(header: list[str], rows: list[dict]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        cells = [r["name"], str(r["x"]), str(r["y"]), str(r["w"]), str(r["h"]), *r.get("extra", [])]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def rescale_layout(
    layout_id: str, canvas: tuple[int, int], index_path: Path = _INDEX, source: str = "auto"
) -> dict:
    """Rescale a recipe. ``source``: ``md`` (the recipe's slot table), ``index`` (zones), or ``auto``.

    ``auto`` prefers the recipe's own slot table (per-slot coordinates the Executor builds from) and
    falls back to the coarser ``zones_detail`` in the index (the only source for recipes without a table).
    """
    layout = load_layout(layout_id, index_path)
    src = (layout["canvas"]["width"], layout["canvas"]["height"])
    md_path = index_path.parent / layout.get("file", "")
    tables = parse_slot_tables(md_path.read_text(encoding="utf-8")) if source != "index" and md_path.is_file() else []
    if source == "md" and not tables:
        raise RescaleError(f"{layout_id}: no `| Slot | x | y | w | h |` table in {md_path.name}")

    result: dict = {
        "id": layout_id,
        "source_canvas": {"width": src[0], "height": src[1]},
        "canvas": {"width": canvas[0], "height": canvas[1]},
        "grid": GRID,
    }
    if tables:
        scaled_tables = []
        issues: list[str] = []
        for t in tables:
            scaled = rescale_zones(t["rows"], src, canvas)
            issues += problems(scaled, canvas, t["rows"])
            scaled_tables.append({"header": t["header"], "rows": scaled, "unparsed": t.get("unparsed", [])})
        result.update(source="md", zones=scaled_tables[0]["rows"], slot_tables=scaled_tables, problems=issues,
                      unparsed_rows=[name for t in scaled_tables for name in t["unparsed"]])
    else:
        zones = rescale_zones(layout["zones_detail"], src, canvas)
        result.update(source="index", zones=zones, problems=problems(zones, canvas, layout["zones_detail"]))
    return result


def scale_rect(rect: tuple[int, int, int, int], src: tuple[int, int], dst: tuple[int, int]) -> tuple[int, int, int, int]:
    """Scale one x,y,w,h box (edges snapped to the grid) — for converting coordinates quoted in prose."""
    zone = rescale_zones([{"name": "r", "x": rect[0], "y": rect[1], "w": rect[2], "h": rect[3]}], src, dst)[0]
    return zone["x"], zone["y"], zone["w"], zone["h"]


def check_recipe(path: Path, canvas: tuple[int, int]) -> list[str]:
    """Validate a recipe's slot table(s) on ``canvas``: bounds, 8-px grid, new overlaps, edge margins."""
    width, height = canvas
    issues: list[str] = []
    for n, t in enumerate(parse_slot_tables(path.read_text(encoding="utf-8")), 1):
        rows = t["rows"]
        for z in rows:
            if any(z[k] % GRID for k in ("x", "y", "w", "h")):
                issues.append(f"table {n}: {z['name']} is off the {GRID}-px grid ({z['x']},{z['y']},{z['w']},{z['h']})")
        issues += [f"table {n}: {p}" for p in problems(rows, canvas, None)
                   if "overlaps" not in p]
        # Overlaps are allowed only when marked in the Notes column (e.g. "overlay", "behind", "background").
        marked = {z["name"] for z in rows if any(w in " ".join(z.get("extra", [])).lower()
                                                 for w in ("overlay", "behind", "background", "on top", "z-order", "intentional"))}
        for pair in sorted(_overlaps(rows), key=sorted):
            if not (set(pair) & marked):
                issues.append(f"table {n}: {' overlaps '.join(sorted(pair))} (mark the Notes cell 'overlay' if intentional)")
        full_width = [z for z in rows if z["w"] >= width * 0.9]
        for z in rows:
            if z not in full_width and (z["x"] < 24 or z["x"] + z["w"] > width - 24):
                issues.append(f"table {n}: {z['name']} violates the 24-px edge margin")
            if z["y"] < 0 or z["y"] + z["h"] > height:
                issues.append(f"table {n}: {z['name']} leaves the canvas vertically")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--layout", help="layout id from layouts-index.json")
    parser.add_argument("--canvas", required=True, help="target canvas, e.g. 1920x1080")
    parser.add_argument("--check", type=Path,
                        help="validate a (migrated) recipe .md against --canvas: bounds, 8-px grid, unmarked overlaps, edge margins")
    parser.add_argument("--rect", help="scale a single box 'x,y,w,h' (use w,h=0 for a bare point) instead of a layout")
    parser.add_argument("--table", type=Path,
                        help="print the rescaled slot table(s) of a recipe .md file (numbers taken from the file itself, "
                             "scaled from --from-canvas); use while migrating a recipe's own numbers")
    parser.add_argument("--from-canvas", default="1920x1080",
                        help="source canvas for --rect / --table / --check (default: the recipes' authored 1920x1080)")
    parser.add_argument("--source", choices=["auto", "md", "index"], default="auto",
                        help="auto = the recipe's slot table when it has one, else index zones")
    parser.add_argument("--format", choices=["json", "md"], default="json",
                        help="md prints the rescaled slot table(s) ready to paste into a Design Spec")
    parser.add_argument("--index", type=Path, default=_INDEX)
    parser.add_argument("--json", type=Path, default=None, help="also write the JSON result to this file")
    args = parser.parse_args(argv)
    try:
        if args.rect:
            values = [int(v) for v in args.rect.split(",")]
            if len(values) != 4:
                raise RescaleError("--rect needs 4 comma-separated integers: x,y,w,h")
            x, y, w, h = scale_rect(tuple(values), parse_canvas(args.from_canvas), parse_canvas(args.canvas))
            print(f"{x},{y},{w},{h}")
            return 0
        if args.check:
            found = check_recipe(args.check, parse_canvas(args.canvas))
            for line in found:
                print(line)
            unparsed = [n for t in parse_slot_tables(args.check.read_text(encoding="utf-8")) for n in t["unparsed"]]
            if unparsed:
                print(f"note: {len(unparsed)} row(s) not expressible as integers, not checked: {', '.join(unparsed)}")
            print(f"{args.check.name}: {'OK' if not found else str(len(found)) + ' issue(s)'}")
            return 2 if found else 0
        if args.table:
            src, dst = parse_canvas(args.from_canvas), parse_canvas(args.canvas)
            tables = parse_slot_tables(args.table.read_text(encoding="utf-8"))
            if not tables:
                raise RescaleError(f"no `| Slot | x | y | w | h |` table in {args.table}")
            issues: list[str] = []
            blocks = []
            for t in tables:
                scaled = rescale_zones(t["rows"], src, dst)
                issues += problems(scaled, dst, t["rows"])
                blocks.append(format_slot_table(t["header"], scaled))
            print("\n\n".join(blocks))
            if issues:
                print("problems: " + "; ".join(issues), file=sys.stderr)
            return 2 if issues else 0
        if not args.layout:
            raise RescaleError("provide --layout <id> or --rect x,y,w,h")
        result = rescale_layout(args.layout, parse_canvas(args.canvas), args.index, args.source)
    except (RescaleError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, indent=2)
    if args.format == "md":
        tables = result.get("slot_tables") or [{
            "header": ["Slot", "x", "y", "w", "h", "Visual type"],
            "rows": [{**z, "name": z["name"], "extra": [z.get("visual_type", "")]} for z in result["zones"]],
        }]
        print("\n\n".join(format_slot_table(t["header"], t["rows"]) for t in tables))
        if result.get("unparsed_rows"):
            print("\nnote: rows not expressible as integers were left out (place them by hand): "
                  + ", ".join(result["unparsed_rows"]), file=sys.stderr)
        if result["problems"]:
            print("\nproblems: " + "; ".join(result["problems"]), file=sys.stderr)
    else:
        print(text)
    if args.json:
        args.json.write_text(text, encoding="utf-8")
    return 2 if result["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
