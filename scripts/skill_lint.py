#!/usr/bin/env python3
"""Lint the skills in this repo: frontmatter, references, and relative links.

Checks every `skills/<name>/SKILL.md` and every `.md` below it (assets excluded):

  SKILL.md frontmatter   `name` equals the folder name; `description` present and <= 1024 chars;
                         description names at least one trigger phrase ("Triggers"/"Use when"/"Use for"/quotes)
  referenced files       every relative path to a .md/.json/.py/.svg file that contains a "/" and starts with
                         references/ scripts/ assets/ ../ ./ skills/ — or is a markdown link target — must exist.
                         Paths in code fences that show *report* structure (definition/, pages/, .pbi/ ...)
                         or contain placeholders (<x>, *, {x}) are ignored. See ALLOW below for known
                         runtime-generated names.

Usage:
    python scripts/skill_lint.py [--root <repo>] [--json out.json] [--warn-only]

Exit codes: 0 clean, 1 findings (unless --warn-only).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAX_DESCRIPTION = 1024
ROOT = Path(__file__).resolve().parent.parent

# Path fragments that are examples of generated/runtime files, not repo files.
ALLOW_SUBSTR = (
    "_brief/", "definition/", "pages/", "visuals/", "bookmarks/", ".pbi/", "StaticResources/",
    "RegisteredResources/", "CustomVisuals/", "SharedResources/", "item/report/", "pbip/pbipProperties",
    "docs/", "agents/", "screenshots/", "/tmp", "node_modules", "SemanticModel/", ".Report/",
    "layouts-index.finance.json", "design_report.md", "unappliedChanges.json", "Copilot/",
)
ALLOW_EXACT = {
    "references/design/assets/base.json",  # lives under the design skill (resolved separately)
    "design/design-brief.md",              # official planning text; the repo path map points it at power-bi-report-design
}
PATH_RE = re.compile(r"(?<![\w./\\-])((?:\.{1,2}/)*(?:[\w.\-]+/)+[\w.\-]+\.(?:md|json|py|svg))(?![\w/])")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
FENCE_RE = re.compile(r"^```")


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            out[key] = "" if val in (">-", ">", "|", "|-") else val.strip("\"'")
        elif key and line.strip():
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def candidates(md: Path, skill_dir: Path, ref: str, repo: Path) -> list[Path]:
    base = [md.parent, skill_dir, skill_dir / "references", repo, repo / "skills"]
    # references pointing at a sibling mode folder of the same skill (authoring/..., design/...)
    return [(b / ref).resolve() for b in base]


def is_allowed(ref: str) -> bool:
    return ref in ALLOW_EXACT or any(s in ref for s in ALLOW_SUBSTR) or any(c in ref for c in "<>*{}$")


def lint_skill(skill_dir: Path, repo: Path) -> list[dict]:
    findings: list[dict] = []
    skill_md = skill_dir / "SKILL.md"
    rel = lambda p: str(p.relative_to(repo)).replace("\\", "/")  # noqa: E731
    if not skill_md.is_file():
        return [{"file": rel(skill_dir), "kind": "missing-skill-md", "message": "no SKILL.md"}]
    fm = frontmatter(skill_md.read_text(encoding="utf-8"))
    if fm.get("name") != skill_dir.name:
        findings.append({"file": rel(skill_md), "kind": "name", "message": f"name {fm.get('name')!r} != folder {skill_dir.name!r}"})
    desc = fm.get("description", "")
    if not desc:
        findings.append({"file": rel(skill_md), "kind": "description", "message": "description missing"})
    else:
        if len(desc) > MAX_DESCRIPTION:
            findings.append({"file": rel(skill_md), "kind": "description-length",
                             "message": f"description is {len(desc)} chars (max {MAX_DESCRIPTION})"})
        if not re.search(r"Triggers?|Use (this )?(skill )?(when|for|whenever)|[\"“]", desc):
            findings.append({"file": rel(skill_md), "kind": "description-triggers",
                             "message": "description names no trigger phrase / 'Use when' clause"})
    for md in sorted(skill_dir.rglob("*.md")):
        if "assets" in md.relative_to(skill_dir).parts or "__pycache__" in md.parts:
            continue
        in_fence = False
        seen: set[str] = set()
        for line in md.read_text(encoding="utf-8").splitlines():
            if FENCE_RE.match(line.strip()):
                in_fence = not in_fence
                continue
            refs = [m.group(1) for m in LINK_RE.finditer(line) if not m.group(1).startswith(("http", "mailto", "#"))]
            if not in_fence:
                refs += [m.group(1) for m in PATH_RE.finditer(line)]
            for ref in refs:
                ref = ref.strip("`'\"")
                if ref in seen or is_allowed(ref) or not re.search(r"\.(md|json|py|svg)$", ref):
                    continue
                seen.add(ref)
                if "/" not in ref and not ref.startswith("."):
                    continue
                if not any(c.exists() for c in candidates(md, skill_dir, ref, repo)):
                    findings.append({"file": rel(md), "kind": "broken-ref", "message": f"{ref} not found"})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args(argv)
    skills = sorted(p for p in (args.root / "skills").iterdir() if p.is_dir())
    findings: list[dict] = []
    for s in skills:
        findings += lint_skill(s, args.root)
    for f in findings:
        print(f"{f['file']}: [{f['kind']}] {f['message']}")
    print(f"skill-lint: {len(skills)} skill(s), {len(findings)} finding(s)")
    if args.json:
        args.json.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    return 0 if (not findings or args.warn_only) else 1


if __name__ == "__main__":
    sys.exit(main())
