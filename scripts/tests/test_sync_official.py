"""Tests for the three-way merge in scripts/sync-official.py (real `git merge-file`, synthetic files)."""
from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("sync_official", Path(__file__).resolve().parent.parent / "sync-official.py")
so = importlib.util.module_from_spec(SPEC)
sys.modules["sync_official"] = so
SPEC.loader.exec_module(so)

pytestmark = pytest.mark.skipif(not shutil.which("git"), reason="git required")

BASE = "# Title\nline one\nline two\nline three\nlink: ../../common/COMMON-CLI.md\nend\n"


def _w(p: Path, text: str) -> Path:
    p.write_text(text, encoding="utf-8")
    return p


def test_local_patch_and_upstream_edit_merge_cleanly(tmp_path):
    baseline = _w(tmp_path / "base.md", BASE)
    mirror = _w(tmp_path / "mirror.md", BASE.replace("../../common/COMMON-CLI.md", "fabric-common-cli.md"))
    upstream = _w(tmp_path / "up.md", BASE.replace("line one", "line ONE (upstream edit)"))
    text, conflicts = so.merge_three_way(mirror, baseline, upstream)
    assert conflicts == 0
    assert "fabric-common-cli.md" in text and "line ONE (upstream edit)" in text
    assert "COMMON-CLI.md" not in text.replace("fabric-common-cli.md", "")


def test_overlapping_edits_conflict(tmp_path):
    baseline = _w(tmp_path / "base.md", BASE)
    mirror = _w(tmp_path / "mirror.md", BASE.replace("line two", "line two (local)"))
    upstream = _w(tmp_path / "up.md", BASE.replace("line two", "line two (upstream)"))
    text, conflicts = so.merge_three_way(mirror, baseline, upstream)
    assert conflicts >= 1 and "<<<<<<<" in text


def _setup(tmp_path, monkeypatch, upstream_text, mirror_text, baseline_text):
    root = tmp_path
    (root / ".agents" / "skills" / "powerbi-report-cli" / "references").mkdir(parents=True)
    (root / ".agents" / "skills" / "powerbi-report-cli" / "SKILL.md").write_text("version: 1.0.0\n", encoding="utf-8")
    owner = root / "skills" / "power-bi-report-authoring" / "references"
    owner.mkdir(parents=True)
    up = root / ".agents" / "skills" / "powerbi-report-cli" / "references" / "authoring.md"
    up.write_text(upstream_text, encoding="utf-8")
    mirror = owner / "authoring.md"
    mirror.write_text(mirror_text, encoding="utf-8")
    (root / "scripts" / "official-baseline" / "powerbi-report-cli").mkdir(parents=True)
    (root / "scripts" / "official-baseline" / "powerbi-report-cli" / "authoring.md").write_text(baseline_text, encoding="utf-8")
    for name, val in {
        "ROOT": root, "AGENTS": root / ".agents" / "skills", "SKILLS": root / "skills",
        "LOCK": root / "official-sync.lock.json", "BASELINE": root / "scripts" / "official-baseline",
        "CLI": root / ".agents" / "skills" / "powerbi-report-cli", "SMA": root / ".agents" / "skills" / "semantic-model-authoring",
    }.items():
        monkeypatch.setattr(so, name, val)
    return up, mirror


def test_sync_merges_patched_file_and_lock_records_baseline(tmp_path, monkeypatch, capsys):
    base = BASE
    mirror_text = BASE.replace("../../common/COMMON-CLI.md", "fabric-common-cli.md")
    up, mirror = _setup(tmp_path, monkeypatch, base, mirror_text, base)
    assert so.cmd_lock() == 0
    assert (tmp_path / "scripts" / "official-baseline" / "powerbi-report-cli" / "authoring.md").read_text(encoding="utf-8") == base

    up.write_text(base.replace("line one", "line ONE"), encoding="utf-8")  # upstream moves on (not adjacent to the patch)
    assert so.cmd_check() == 1
    assert so.cmd_sync(force=False) == 0
    merged = mirror.read_text(encoding="utf-8")
    assert "line ONE" in merged and "fabric-common-cli.md" in merged
    so.cmd_lock()
    assert so.cmd_check() == 0


def test_sync_conflict_leaves_mirror_untouched(tmp_path, monkeypatch, capsys):
    base = BASE
    mirror_text = BASE.replace("line two", "line two (local)")
    up, mirror = _setup(tmp_path, monkeypatch, base, mirror_text, base)
    so.cmd_lock()
    up.write_text(base.replace("line two", "line two (upstream)"), encoding="utf-8")
    assert so.cmd_sync(force=False) == 1
    assert mirror.read_text(encoding="utf-8") == mirror_text
    assert (mirror.with_name("authoring.md.conflict")).is_file()
