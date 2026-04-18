"""
pbir_utils.py — shared helpers for PBIR report scripts.

Used by finalize_pbir.py, design_quality_check.py, and pbir_gate.py.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

# ── Windows UTF-8 console fix ──────────────────────────────────
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass


# ── Shared constants ───────────────────────────────────────────

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

# Size tolerance: if a font size is within ±TOLERANCE of a standard size, snap it.
FONT_SIZE_TOLERANCE = 2

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")

# Non-data "primitive" visual types — used for visual-count exclusions and alt-text skipping.
PRIMITIVE_VTYPES = frozenset({
    "slicer", "button", "actionbutton", "image",
    "textbox", "shape", "basicshape",
})

# Performance budget (shared-standards.md §8)
REPORT_VISUAL_BUDGET = 60


# ── JSON I/O ──────────────────────────────────────────────────

def read_json(path: Path) -> dict:
    """Read and parse a JSON file. Returns {} on decode error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def read_json_strict(path: Path) -> dict:
    """Read and parse a JSON file. Raises on decode error."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    """Write a dict as pretty-printed JSON."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ── Visual introspection ──────────────────────────────────────

def visual_type(data: dict) -> str | None:
    """Extract the visual type string from a visual.json dict."""
    v = data.get("visual") or data.get("visualContainer", {}).get("visual", {})
    if isinstance(v, dict):
        return v.get("visualType") or v.get("type")
    return None


def get_visual_title(data: dict) -> str | None:
    """Extract the visual's display title (Literal expression style)."""
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


def get_alt_text(data: dict) -> str | None:
    """Extract the visual's alt-text string (returns None if absent or blank)."""
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


def set_alt_text(data: dict, text: str) -> bool:
    """Set alt text on a visual.json dict. Returns True if the path existed to write into."""
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


def get_position(data: dict) -> dict | None:
    """Extract the position dict from a visual.json dict."""
    if isinstance(data.get("position"), dict):
        return data["position"]
    vc = data.get("visualContainer")
    if isinstance(vc, dict) and isinstance(vc.get("position"), dict):
        return vc["position"]
    return None


def normalize_hex(h: str) -> str:
    """Uppercase hex string without leading #."""
    return h.upper().lstrip("#")


def is_drillthrough(page_data: dict) -> bool:
    """Return True if page_data represents a drillthrough page."""
    if page_data.get("type") == 2:
        return True
    return "filterConfig" in page_data and "type" in page_data.get("filterConfig", {})


def is_back_button(visual_data: dict) -> bool:
    """Return True if visual_data represents a back-navigation button."""
    v = visual_data.get("visual") or visual_data.get("visualContainer", {}).get("visual", {})
    vtype = (v.get("visualType") or v.get("type") or "").lower()
    if vtype not in ("actionbutton", "button"):
        return False
    raw = json.dumps(visual_data).lower()
    return '"back"' in raw or ("shapetype" in raw and "back" in raw)


# ── WCAG contrast helpers ──────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert '#RRGGBB' to (r, g, b) ints."""
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG 2.1 relative luminance (0.0–1.0)."""
    def _lin(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(hex1: str, hex2: str) -> float:
    """WCAG 2.1 contrast ratio between two hex colors (range 1.0–21.0)."""
    l1 = relative_luminance(*hex_to_rgb(hex1))
    l2 = relative_luminance(*hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ── Logging setup ──────────────────────────────────────────────
import logging  # noqa: E402 — intentionally at bottom to avoid circular issues


def setup_logging(name: str, *, verbose: bool = False, quiet: bool = False) -> logging.Logger:
    """Configure and return a logger for CLI scripts.

    --verbose → DEBUG, --quiet → WARNING, default → INFO.
    """
    level = logging.DEBUG if verbose else (logging.WARNING if quiet else logging.INFO)
    log = logging.getLogger(name)
    log.setLevel(level)
    if not log.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)-5s %(message)s"))
        log.addHandler(handler)
    return log
