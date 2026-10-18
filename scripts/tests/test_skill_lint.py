"""Tests for scripts/skill_lint.py."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import skill_lint as sl  # noqa: E402


def _skill(root: Path, name: str, skill_md: str, **files: str) -> Path:
    d = root / "skills" / name
    (d / "references").mkdir(parents=True)
    (d / "SKILL.md").write_text(skill_md, encoding="utf-8")
    for rel, text in files.items():
        p = d / rel.replace("__", "/")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return d


GOOD = '---\nname: demo\ndescription: >-\n  Does things. Triggers: "do thing".\n---\n# Demo\nSee `references/a.md`.\n'


def test_frontmatter_folded_description():
    fm = sl.frontmatter(GOOD)
    assert fm["name"] == "demo" and fm["description"].startswith("Does things.")


def test_clean_skill_passes(tmp_path):
    d = _skill(tmp_path, "demo", GOOD, references__a="x")
    (d / "references" / "a.md").write_text("ok", encoding="utf-8")
    assert sl.lint_skill(d, tmp_path) == []


def test_name_mismatch_and_long_description(tmp_path):
    bad = '---\nname: other\ndescription: ' + "x " * 700 + '\n---\n'
    d = _skill(tmp_path, "demo", bad)
    kinds = {f["kind"] for f in sl.lint_skill(d, tmp_path)}
    assert {"name", "description-length", "description-triggers"} <= kinds


def test_broken_reference_detected_but_placeholders_ignored(tmp_path):
    text = GOOD + "Also `references/missing.md`, `references/<x>.md`, and `definition/report.json`.\n"
    d = _skill(tmp_path, "demo", text)
    (d / "references" / "a.md").write_text("ok", encoding="utf-8")
    msgs = [f["message"] for f in sl.lint_skill(d, tmp_path) if f["kind"] == "broken-ref"]
    assert msgs == ["references/missing.md not found"]


def test_code_fence_paths_are_not_checked(tmp_path):
    text = GOOD + "```\nreferences/ghost.md\n```\n"
    d = _skill(tmp_path, "demo", text)
    (d / "references" / "a.md").write_text("ok", encoding="utf-8")
    assert sl.lint_skill(d, tmp_path) == []


def test_repo_skills_are_clean():
    """The real repo must stay lint-clean (this is the guard CI relies on)."""
    root = Path(__file__).resolve().parent.parent.parent
    findings = []
    for s in sorted((root / "skills").iterdir()):
        if s.is_dir():
            findings += sl.lint_skill(s, root)
    assert findings == [], "\n".join(f"{f['file']}: {f['message']}" for f in findings)
