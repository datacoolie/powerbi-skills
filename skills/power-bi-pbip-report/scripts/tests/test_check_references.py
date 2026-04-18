"""Tests for check_references.py."""
from __future__ import annotations

import sys
from pathlib import Path

_AGENTS = Path(__file__).resolve().parent.parent.parent.parent.parent / "agents"
if str(_AGENTS.parent) not in sys.path:
    sys.path.insert(0, str(_AGENTS.parent))

import pytest

# Import from agents/ — add it to path
if str(_AGENTS) not in sys.path:
    sys.path.insert(0, str(_AGENTS))

from check_references import _code_block_lines


# ── _code_block_lines ─────────────────────────────────────────

def test_no_code_blocks():
    lines = ["Hello", "World", "No code here"]
    result = _code_block_lines(lines)
    assert len(result) == 0


def test_basic_fenced_block():
    lines = [
        "Some text",
        "```python",
        "x = 1",
        "y = 2",
        "```",
        "More text",
    ]
    result = _code_block_lines(lines)
    # Lines 2-5 are inside or on the fence
    assert 2 in result
    assert 3 in result
    assert 4 in result
    assert 5 in result
    assert 1 not in result
    assert 6 not in result


def test_nested_fences():
    lines = [
        "text",
        "````",
        "```",
        "inner code",
        "```",
        "still inside",
        "````",
        "outside",
    ]
    result = _code_block_lines(lines)
    # Lines 2-7 should all be in code blocks (4-tick fence)
    for i in range(2, 8):
        assert i in result, f"Line {i} should be in code block"
    assert 1 not in result
    assert 8 not in result


def test_tilde_fences():
    lines = [
        "text",
        "~~~",
        "code",
        "~~~",
        "text",
    ]
    result = _code_block_lines(lines)
    assert 2 in result
    assert 3 in result
    assert 4 in result
    assert 1 not in result
    assert 5 not in result
