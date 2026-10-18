"""Tests for scripts/doctor.py (no real CLIs required)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import doctor  # noqa: E402


def _cp(stdout="", stderr="", rc=0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=rc)


def test_parse_version():
    assert doctor.parse_version("v26.1.0") == (26, 1, 0)
    assert doctor.parse_version("fab version 1.7.0") == (1, 7, 0)
    assert doctor.parse_version("0.5.0") == (0, 5, 0)
    assert doctor.parse_version("no version") is None


def test_missing_required_cli_fails(monkeypatch):
    monkeypatch.setattr(doctor, "_which", lambda name: None)
    c = doctor.check_node()
    assert c.status == "fail" and c.required and c.fix


def test_outdated_cli_fails_and_current_passes(monkeypatch):
    monkeypatch.setattr(doctor, "_which", lambda name: name)
    monkeypatch.setattr(doctor, "_run", lambda args, timeout=30: _cp("0.1.1"))
    assert doctor.check_report_author()[0].status == "fail"
    monkeypatch.setattr(doctor, "_run", lambda args, timeout=30: _cp("0.5.0"))
    assert doctor.check_report_author()[0].status == "ok"


def test_optional_missing_is_warn_not_fail(monkeypatch):
    monkeypatch.setattr(doctor, "_which", lambda name: None)
    assert doctor.check_fab().status == "warn"
    assert doctor.check_az()[0].status == "warn"


def test_preview_hosts_parsing(monkeypatch):
    payload = {"data": {"hosts": [
        {"host": "service", "available": True, "availability": {"available": True}},
        {"host": "desktop", "available": False, "availability": {"available": False, "reason": "no instance"}},
    ]}}
    monkeypatch.setattr(doctor, "_which", lambda name: name)
    monkeypatch.setattr(doctor, "_run", lambda args, timeout=30: _cp(json.dumps(payload)))
    c = doctor.check_preview_hosts()
    assert c.status == "ok" and "desktop: no instance" in c.detail and c.extra["hosts"]["service"] is True


def test_mcp_note_mentions_both_server_ids():
    note = doctor.check_mcp_note().detail
    assert "powerbi-modeling-mcp" in note and "powerbi-authoring-local" in note


def test_strict_exit_code(monkeypatch, capsys):
    monkeypatch.setattr(doctor, "run_all", lambda: [doctor.Check("x", "fail", "boom", True)])
    assert doctor.main(["--strict"]) == 1
    assert doctor.main([]) == 0
    monkeypatch.setattr(doctor, "run_all", lambda: [doctor.Check("x", "warn", "meh", False)])
    assert doctor.main(["--strict", "--json"]) == 0
