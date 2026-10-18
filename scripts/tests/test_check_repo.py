"""Tests for scripts/check_repo.py."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


cr = _load("check_repo", "check_repo.py")


def test_mirror_integrity_passes_on_repo():
    status, detail = cr.check_mirror_integrity()
    assert status == "ok", detail


def test_mirror_paths_resolve_for_every_locked_key():
    keys = json.loads(cr.LOCK.read_text(encoding="utf-8"))["files"]
    unresolved = [k for k in keys if cr._mirror_path(k) is None or not cr._mirror_path(k).is_file()]
    assert unresolved == []


def test_mirror_mapping_matches_sync_official():
    so = _load("sync_official_cmp", "sync-official.py")
    if not so.AGENTS.is_dir():
        pytest.skip("no local .agents install")
    for key, (_src, dst) in so.mapping().items():
        assert cr._mirror_path(key) == dst, key


def test_integrity_flags_edit_and_missing(tmp_path, monkeypatch):
    lock = tmp_path / "lock.json"
    target = tmp_path / "skills" / "power-bi-report-authoring" / "references"
    target.mkdir(parents=True)
    f = target / "authoring.md"
    f.write_text("a", encoding="utf-8")
    lock.write_text(json.dumps({"files": {
        "powerbi-report-cli/authoring.md": {"upstream": "x", "mirror": cr._sha(f)},
        "powerbi-report-cli/authoring-part-02.md": {"upstream": "x", "mirror": "y"},
    }}), encoding="utf-8")
    monkeypatch.setattr(cr, "ROOT", tmp_path)
    monkeypatch.setattr(cr, "LOCK", lock)
    status, detail = cr.check_mirror_integrity()
    assert status == "fail" and "1 missing" in detail
    (target / "authoring-part-02.md").write_text("b", encoding="utf-8")
    status, detail = cr.check_mirror_integrity()
    assert status == "fail" and "edited since lock" in detail
