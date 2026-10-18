#!/usr/bin/env python3
"""Track drift between the repo skills and the official Microsoft skills they mirror.

Mirrored (verbatim, apart from repo path fixes):
  .agents/skills/powerbi-report-cli/references/**      -> authoring / design / management / planning skills
  .agents/skills/semantic-model-authoring/{SKILL.md,references/*} -> power-bi-semantic-model/references

`.agents/` is a local, git-ignored install (`npx skills add microsoft/skills-for-fabric`);
refresh it first (`npx skills update`), then run:

  python scripts/sync-official.py check   # report upstream drift / local edits / missing files (default)
  python scripts/sync-official.py sync    # copy upstream files whose mirror is unmodified; list the rest
  python scripts/sync-official.py lock    # record the current state in official-sync.lock.json

Files with intentional local patches (path fixes) are never blindly overwritten: `lock` keeps a baseline copy of
the upstream version in scripts/official-baseline/, and `sync` three-way merges (git merge-file) the new upstream
into the patched mirror — local fixes survive, upstream edits are taken, overlapping edits are written to
`<file>.conflict` for manual resolution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".agents" / "skills"
SKILLS = ROOT / "skills"
LOCK = ROOT / "official-sync.lock.json"
BASELINE = ROOT / "scripts" / "official-baseline"

CLI = AGENTS / "powerbi-report-cli"
SMA = AGENTS / "semantic-model-authoring"

# Official semantic-model references added to the repo skill on top of the ones it already had.
NEW_SM_REFS = {
    "direct-lake-guidelines.md", "field-parameters.md", "metadata-discovery.md",
    "modeling-guidelines.md", "tmdl-guidelines.md",
}


def sha(path: Path) -> str:
    # Normalise line endings so Windows (autocrlf) and Linux checkouts hash identically.
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def mapping() -> dict[str, tuple[Path, Path]]:
    """relative key -> (upstream file, mirror file)."""
    pairs: dict[str, tuple[Path, Path]] = {}
    refs = CLI / "references"
    owners = {
        "authoring": "power-bi-report-authoring",
        "design": "power-bi-report-design",
        "management": "power-bi-management",
        "planning": "power-bi-business-analysis",
    }
    for src in sorted(p for p in refs.rglob("*") if p.is_file()):
        rel = src.relative_to(refs)
        mode = re.split(r"[-./\\]", rel.parts[0])[0]
        owner = owners.get(mode)
        if owner:
            pairs[f"powerbi-report-cli/{rel.as_posix()}"] = (src, SKILLS / owner / "references" / rel)
    sm_refs = SMA / "references"
    sm_dst = SKILLS / "power-bi-semantic-model" / "references"
    if sm_refs.is_dir():
        for src in sorted(sm_refs.glob("*.md")):
            dst = sm_dst / src.name
            # pbip.md carries repo additions; never mirror it.
            if src.name != "pbip.md" and (dst.exists() or src.name in NEW_SM_REFS):
                pairs[f"semantic-model-authoring/references/{src.name}"] = (src, dst)
        pairs["semantic-model-authoring/SKILL.md"] = (SMA / "SKILL.md", sm_dst / "official-workflows.md")
    return pairs


def load_lock() -> dict:
    return json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {"files": {}}


def versions() -> dict[str, str]:
    out = {}
    for name, skill in (("powerbi-report-cli", CLI), ("semantic-model-authoring", SMA)):
        text = (skill / "SKILL.md").read_text(encoding="utf-8") if (skill / "SKILL.md").exists() else ""
        m = re.search(r"^\s*version:\s*([\w.\-]+)", text, re.M)
        out[name] = m.group(1) if m else "unknown"
    return out


def classify(lock: dict) -> dict[str, list[str]]:
    res: dict[str, list[str]] = {
        k: [] for k in ("ok", "upstream_changed", "local_edited", "both", "missing", "new_upstream")
    }
    for key, (src, dst) in mapping().items():
        entry = lock["files"].get(key)
        if not dst.exists():
            res["missing"].append(key)
        elif entry is None:
            res["new_upstream"].append(key)
        else:
            up = sha(src) != entry["upstream"]
            local = sha(dst) != entry["mirror"]
            res["both" if up and local else "upstream_changed" if up else "local_edited" if local else "ok"].append(key)
    return res


def cmd_check() -> int:
    if not AGENTS.is_dir():
        print("No .agents/skills install found; run `npx skills add microsoft/skills-for-fabric` first.")
        return 2
    lock = load_lock()
    res = classify(lock)
    print("versions upstream:", versions(), "| locked:", lock.get("versions"))
    for k, v in res.items():
        print(f"{k:17} {len(v)}")
        if k not in ("ok", "local_edited"):
            for item in v:
                print("   ", item)
    drift = res["upstream_changed"] or res["both"] or res["missing"] or res["new_upstream"]
    return 1 if drift else 0


def baseline_path(key: str) -> Path:
    return BASELINE / key


def merge_three_way(mirror: Path, baseline: Path, upstream: Path) -> tuple[str, int]:
    """`git merge-file -p mirror baseline upstream` → (merged text, number of conflicts).

    mirror = repo file (upstream-at-lock + local path fixes), baseline = upstream-at-lock,
    upstream = new upstream. Local fixes survive; new upstream edits are taken; overlapping edits conflict.
    """
    git = shutil.which("git")
    if not git:
        raise RuntimeError("git is required for the three-way merge")
    out = subprocess.run([git, "merge-file", "-p", "--diff3", str(mirror), str(baseline), str(upstream)],
                         capture_output=True)
    if out.returncode < 0 or out.returncode > 127:
        raise RuntimeError(out.stderr.decode("utf-8", "replace"))
    return out.stdout.decode("utf-8"), out.returncode


def cmd_sync(force: bool) -> int:
    lock = load_lock()
    res = classify(lock)
    pairs = mapping()
    copied, merged, conflicts, skipped = [], [], [], []
    for key in res["upstream_changed"] + res["both"] + res["missing"] + res["new_upstream"]:
        src, dst = pairs[key]
        base = baseline_path(key)
        patched = base.is_file() and dst.exists()
        if patched and key not in res["missing"]:
            text, n = merge_three_way(dst, base, src)
            if n == 0:
                with open(dst, "w", encoding="utf-8", newline="") as fh:
                    fh.write(text)
                merged.append(key)
            else:
                conflict = dst.with_name(dst.name + ".conflict")
                with open(conflict, "w", encoding="utf-8", newline="") as fh:
                    fh.write(text)
                conflicts.append((key, n, conflict))
        elif key in res["both"] and not force:
            skipped.append(key)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            copied.append(key)
    for key in res["local_edited"]:
        pass  # local-only edits: nothing upstream to merge
    print(f"copied {len(copied)} file(s), merged {len(merged)} patched file(s)")
    for key in merged:
        print("   merged (local fixes kept):", key)
    if conflicts:
        print("CONFLICTS — mirror left untouched; resolve in the .conflict file, move it over the mirror, then `lock`:")
        for key, n, path in conflicts:
            print(f"   {key}: {n} conflict(s) -> {path.relative_to(ROOT)}")
    if skipped:
        print("NOT overwritten (changed upstream AND edited locally, no baseline) — merge by hand, then `lock`:")
        for key in skipped:
            print("   ", key)
    print("Next: run `python scripts/check_repo.py`, then `python scripts/sync-official.py lock`.")
    return 1 if (conflicts or skipped) else 0


def cmd_lock() -> int:
    files = {k: {"upstream": sha(src), "mirror": sha(dst)} for k, (src, dst) in mapping().items() if dst.exists()}
    # Keep a baseline copy (upstream at lock time) of every file that carries local patches, so `sync`
    # can three-way merge instead of overwriting or skipping them.
    BASELINE.mkdir(exist_ok=True)
    keep = set()
    for k, (src, dst) in mapping().items():
        if dst.exists() and sha(src) != sha(dst):
            target = baseline_path(k)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
            keep.add(target.resolve())
    for old in BASELINE.rglob("*"):
        if old.is_file() and old.resolve() not in keep:
            old.unlink()
    LOCK.write_text(
        json.dumps({"versions": versions(), "files": files}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"locked {len(files)} file(s) -> {LOCK.name}; {len(keep)} patched file(s) baselined in {BASELINE.name}/")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="check", choices=["check", "sync", "lock"])
    ap.add_argument("--force", action="store_true", help="sync: overwrite files changed both upstream and locally")
    args = ap.parse_args()
    return {"check": cmd_check, "lock": cmd_lock, "sync": lambda: cmd_sync(args.force)}[args.command]()


if __name__ == "__main__":
    sys.exit(main())
