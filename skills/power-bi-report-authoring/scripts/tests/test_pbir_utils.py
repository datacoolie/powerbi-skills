"""Tests for pbir_utils.py shared helpers."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure scripts dir is on path
_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import pytest
from pbir_utils import (
    FONT_FAMILY,
    FONT_SIZES,
    FONT_SIZE_TOLERANCE,
    GRID,
    HEX_RE,
    PRIMITIVE_VTYPES,
    contrast_ratio,
    get_alt_text,
    get_position,
    get_visual_title,
    hex_to_rgb,
    is_back_button,
    is_drillthrough,
    normalize_hex,
    read_json,
    read_json_strict,
    relative_luminance,
    set_alt_text,
    visual_type,
    write_json,
)


# ── Constants ──────────────────────────────────────────────────

def test_grid_is_positive():
    assert GRID > 0


def test_font_sizes_non_empty():
    assert len(FONT_SIZES) > 0
    assert all(isinstance(v, int) for v in FONT_SIZES.values())


def test_primitive_vtypes_contains_slicer():
    assert "slicer" in PRIMITIVE_VTYPES
    assert "basicshape" in PRIMITIVE_VTYPES


# ── normalize_hex ──────────────────────────────────────────────

def test_normalize_hex_lowercase():
    assert normalize_hex("#aaBBcc") == "AABBCC"


def test_normalize_hex_already_upper():
    assert normalize_hex("#FFFFFF") == "FFFFFF"


# ── visual_type ────────────────────────────────────────────────

def test_visual_type_from_top_level():
    data = {"visual": {"visualType": "barChart"}}
    assert visual_type(data) == "barChart"


def test_visual_type_from_container():
    data = {"visualContainer": {"visual": {"visualType": "lineChart"}}}
    assert visual_type(data) == "lineChart"


def test_visual_type_missing():
    assert visual_type({}) is None


# ── get_visual_title ───────────────────────────────────────────

def test_get_visual_title_vcTitle():
    data = {"visual": {"objects": {"title": [{"properties": {"text": {"expr": {"Literal": {"Value": "'Revenue by Region'"}}}}}]}}}
    assert get_visual_title(data) == "Revenue by Region"


def test_get_visual_title_missing():
    assert get_visual_title({}) is None


# ── get / set alt_text ─────────────────────────────────────────

def test_alt_text_roundtrip():
    data = {"visual": {"objects": {}}}
    assert get_alt_text(data) is None
    set_alt_text(data, "Test alt text")
    assert get_alt_text(data) == "Test alt text"


# ── is_drillthrough ───────────────────────────────────────────

def test_is_drillthrough_type_2():
    assert is_drillthrough({"type": 2}) is True


def test_is_drillthrough_normal_page():
    assert is_drillthrough({"type": 0}) is False
    assert is_drillthrough({}) is False


# ── is_back_button ────────────────────────────────────────────

def test_is_back_button_action():
    data = {"visual": {"visualType": "actionButton"}, "actions": [{"type": "Back"}]}
    assert is_back_button(data) is True


def test_is_back_button_bar_chart():
    data = {"visual": {"visualType": "barChart"}}
    assert is_back_button(data) is False


# ── get_position ──────────────────────────────────────────────

def test_get_position_basic():
    data = {"position": {"x": 10, "y": 20, "width": 300, "height": 200}}
    pos = get_position(data)
    assert pos == {"x": 10, "y": 20, "width": 300, "height": 200}


def test_get_position_missing():
    assert get_position({}) is None


# ── read/write json ───────────────────────────────────────────

def test_read_json_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_json(tmp_path / "nonexistent.json")


def test_read_json_strict_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_json_strict(tmp_path / "nonexistent.json")


def test_write_and_read_json(tmp_path):
    path = tmp_path / "test.json"
    data = {"hello": "world", "num": 42}
    write_json(path, data)
    result = read_json(path)
    assert result == data


# ── HEX_RE ────────────────────────────────────────────────────

def test_hex_re_matches():
    assert HEX_RE.search("#AABBCC")
    assert HEX_RE.search("#1a2b3c")
    assert not HEX_RE.search("#GGG")
    assert not HEX_RE.search("#AB")


# ── WCAG contrast helpers ─────────────────────────────────────

def test_hex_to_rgb():
    assert hex_to_rgb("#000000") == (0, 0, 0)
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)
    assert hex_to_rgb("#FF8800") == (255, 136, 0)


def test_relative_luminance_black():
    assert relative_luminance(0, 0, 0) == pytest.approx(0.0)


def test_relative_luminance_white():
    assert relative_luminance(255, 255, 255) == pytest.approx(1.0, abs=0.01)


def test_contrast_ratio_black_white():
    ratio = contrast_ratio("#000000", "#FFFFFF")
    assert ratio == pytest.approx(21.0, abs=0.1)


def test_contrast_ratio_same_color():
    ratio = contrast_ratio("#336699", "#336699")
    assert ratio == pytest.approx(1.0)


def test_contrast_ratio_symmetric():
    r1 = contrast_ratio("#FF0000", "#FFFFFF")
    r2 = contrast_ratio("#FFFFFF", "#FF0000")
    assert r1 == pytest.approx(r2)
