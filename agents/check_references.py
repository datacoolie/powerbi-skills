#!/usr/bin/env python3
"""Cross-reference checker for skills/ and agents/ markdown files.

Scans every .md file under skills/ and agents/ for workspace file
references (reference docs, scripts, assets) and verifies each target
exists on disk.

Deliberately ignores PBIR format file names (report.json, visual.json,
page.json, …) and PBIR directory paths (pages/, StaticResources/, …)
that appear as documentation about the file format rather than actual
links to workspace files.

Exit codes:
    0 — all references valid
    1 — one or more broken references found
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

# Backtick-wrapped paths: `path/to/file.ext` or `path/to/dir/`
_RE_BACKTICK = re.compile(r"`([^`\n]+?\.(?:md|json|py|js|ts|pbir|pbip|tmdl|bim|csv|txt|svg|png|yaml|yml))`"
                          r"|`([^`\n]+?/)`")

# Markdown links: [text](path)
_RE_MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Template placeholders like <slug>, <name>, <style-from-design-spec>
_RE_PLACEHOLDER = re.compile(r"<[a-zA-Z][a-zA-Z0-9_-]*>")

# Glob-like patterns
_RE_GLOB = re.compile(r"[*?]")

# Paths that are clearly URLs, anchors, or schema refs — skip them
_RE_SKIP = re.compile(r"^(https?://|#|mailto:|data:|\.schema|/)")

# PBIR format file names — documentation about Power BI file structures,
# NOT references to workspace files.
_PBIR_NAMES = {
    "report.json", "visual.json", "page.json", "pages.json",
    "pages/pages.json", "definition.pbir", "version.json", "mobile.json",
    "bookmarks.json", "reportExtensions.json", "definition/reportExtensions.json",
}

# PBIR directory prefixes — references to PBIR project paths
_PBIR_DIR_PREFIXES = (
    "pages/", "StaticResources/", "RegisteredResources/",
    "definition/", ".Report/", ".SemanticModel/",
    "StaticResources/RegisteredResources/",
)

# Workspace reference prefixes — paths that are actual workspace refs
_WORKSPACE_PREFIXES = (
    "references/", "scripts/", "assets/", "agents/", "skills/",
    "../",  # cross-skill references
)


def _extract_paths(text: str) -> list[str]:
    """Return candidate file-path strings from markdown text."""
    paths: list[str] = []
    for m in _RE_BACKTICK.finditer(text):
        paths.append(m.group(1) or m.group(2))
    for m in _RE_MD_LINK.finditer(text):
        paths.append(m.group(1))
    return paths


def _is_workspace_ref(ref: str) -> bool:
    """Return True if *ref* looks like an actual workspace file reference."""
    # Explicit workspace prefixes
    if any(ref.startswith(p) for p in _WORKSPACE_PREFIXES):
        return True
    # Skill-qualified paths: power-bi-*/references/... or power-bi-*/scripts/...
    if re.match(r"power-bi-[^/]+/(?:references|scripts|assets)/", ref):
        return True
    return False


def _should_skip(ref: str) -> bool:
    """Return True if the reference should be skipped."""
    if _RE_SKIP.search(ref):
        return True
    if _RE_PLACEHOLDER.search(ref):
        return True
    if _RE_GLOB.search(ref):
        return True
    if ref.startswith("-") or ref.startswith("$"):
        return True
    # Skip well-known PBIR format names
    if ref in _PBIR_NAMES:
        return True
    # Skip PBIR directory structure paths
    if any(ref.startswith(p) for p in _PBIR_DIR_PREFIXES):
        return True
    # Skip bare file names (no directory component) — usually format docs
    if "/" not in ref and "\\" not in ref:
        return True
    # Only check things that look like actual workspace references
    if not _is_workspace_ref(ref):
        return True
    return False


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

def _resolve_path(ref: str, md_file: Path, workspace: Path) -> Path | None:
    """Attempt to resolve *ref* to an absolute Path.

    Strategy:
    1. Relative to the .md file's parent directory.
    2. For agent files: try relative to each skill folder.
    3. Relative to workspace root.
    """
    # Strip markdown anchor fragments  (e.g.  file.md#section)
    ref = ref.split("#")[0]
    if not ref:
        return None

    # Normalise separators
    ref = ref.replace("\\", "/")

    candidates: list[Path] = []

    # 1. Relative to the .md file's directory
    candidates.append(md_file.parent / ref)

    # 2. For agent files: try relative to each skill folder
    if "agents" in md_file.parts:
        skills_dir = workspace / "skills"
        if skills_dir.is_dir():
            # Try skills/ root
            candidates.append(skills_dir / ref)
            # Try each individual skill folder
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    candidates.append(skill_dir / ref)

    # 3. Relative to workspace root
    candidates.append(workspace / ref)

    for c in candidates:
        resolved = c.resolve()
        if resolved.exists():
            return resolved

    return None


# ---------------------------------------------------------------------------
# Markdown code-block tracking
# ---------------------------------------------------------------------------

_RE_FENCE = re.compile(r"^(`{3,}|~{3,})")


def _code_block_lines(lines: list[str]) -> frozenset[int]:
    """Return the set of 1-based line numbers that fall inside fenced code blocks.

    Single O(n) pass instead of per-reference O(n) rescans.
    """
    inside = False
    fence_char = ""
    fence_len = 0
    result: set[int] = set()
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        m = _RE_FENCE.match(stripped)
        if m:
            ch = m.group(1)[0]
            ln = len(m.group(1))
            if not inside:
                inside = True
                fence_char = ch
                fence_len = ln
                result.add(i)
            elif ch == fence_char and ln >= fence_len:
                inside = False
                result.add(i)  # closing fence line itself
            else:
                if inside:
                    result.add(i)
        elif inside:
            result.add(i)
    return frozenset(result)


# ---------------------------------------------------------------------------
# Main scanner
# ---------------------------------------------------------------------------

def scan_workspace(workspace: Path) -> list[tuple[Path, int, str, str]]:
    """Scan all .md files and return broken references.

    Returns list of (file, line_number, raw_reference, reason).
    """
    broken: list[tuple[Path, int, str, str]] = []

    md_files: list[Path] = []
    for folder in ("skills", "agents"):
        folder_path = workspace / folder
        if folder_path.is_dir():
            md_files.extend(folder_path.rglob("*.md"))

    for md_file in sorted(md_files):
        try:
            lines = md_file.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        code_lines = _code_block_lines(lines)

        for lineno, line in enumerate(lines, start=1):
            refs = _extract_paths(line)
            for ref in refs:
                if _should_skip(ref):
                    continue
                # Skip references inside code blocks (PBIR examples, commands)
                if lineno in code_lines:
                    continue
                resolved = _resolve_path(ref, md_file, workspace)
                if resolved is None:
                    rel = md_file.relative_to(workspace)
                    broken.append((rel, lineno, ref, "not found"))

    return broken


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check file-path references in skills/ and agents/ markdown files."
    )
    parser.add_argument(
        "--workspace", "-w",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Workspace root (default: two levels up from this script).",
    )
    args = parser.parse_args()
    workspace = args.workspace.resolve()

    broken = scan_workspace(workspace)

    if not broken:
        print("OK — all file references are valid.")
        return 0

    print(f"Found {len(broken)} broken reference(s):\n")
    for file, lineno, ref, reason in broken:
        print(f"  {file}:{lineno}  →  {ref}  ({reason})")
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
