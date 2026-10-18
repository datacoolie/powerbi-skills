#!/usr/bin/env python3
"""One command that runs every repository check (used locally and by CI).

  1. mirror-integrity   every file in official-sync.lock.json exists in skills/ and still matches the locked hash
                        (flags unreviewed edits to the verbatim official mirrors; works without .agents/)
  2. skill-lint         frontmatter, description length/triggers, broken relative references
  3. pytest             all script tests (skills/**/scripts/tests, scripts/tests)
  4. official-drift     `sync-official.py check` — only when the local .agents/ install exists (skipped in CI)

Usage:
    python scripts/check_repo.py            # run all
    python scripts/check_repo.py --skip pytest
    python scripts/check_repo.py --json report.json

Exit codes: 0 all passed (skipped checks allowed), 1 a check failed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "official-sync.lock.json"


def _sha(p: Path) -> str:
    # Normalise line endings so Windows (autocrlf) and Linux checkouts hash identically.
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _mirror_path(key: str) -> Path | None:
    """Same mapping as sync-official.py (kept in sync by test_check_repo)."""
    owners = {"authoring": "power-bi-report-authoring", "design": "power-bi-report-design",
              "management": "power-bi-management", "planning": "power-bi-business-analysis"}
    kind, _, rest = key.partition("/")
    if kind == "powerbi-report-cli":
        mode = rest.replace("/", "-").replace(".", "-").split("-")[0]
        owner = owners.get(mode)
        return ROOT / "skills" / owner / "references" / rest if owner else None
    if kind == "semantic-model-authoring":
        base = ROOT / "skills" / "power-bi-semantic-model" / "references"
        return base / "official-workflows.md" if rest == "SKILL.md" else ROOT / "skills" / "power-bi-semantic-model" / rest
    return None


def check_mirror_integrity() -> tuple[str, str]:
    if not LOCK.is_file():
        return "fail", "official-sync.lock.json missing (run scripts/sync-official.py lock)"
    files = json.loads(LOCK.read_text(encoding="utf-8")).get("files", {})
    missing, edited = [], []
    for key, entry in files.items():
        path = _mirror_path(key)
        if path is None or not path.is_file():
            missing.append(key)
        elif _sha(path) != entry["mirror"]:
            edited.append(key)
    if missing or edited:
        parts = []
        if missing:
            parts.append(f"{len(missing)} missing: {', '.join(missing[:5])}")
        if edited:
            parts.append(f"{len(edited)} edited since lock (run sync-official.py lock after reviewing): {', '.join(edited[:5])}")
        return "fail", "; ".join(parts)
    return "ok", f"{len(files)} mirrored file(s) intact"


def run(cmd: list[str]) -> tuple[int, str]:
    out = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return out.returncode, (out.stdout + out.stderr).strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skip", action="append", default=[],
                        choices=["mirror-integrity", "skill-lint", "pytest", "official-drift"])
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)
    results = []

    def record(name: str, status: str, detail: str, seconds: float) -> None:
        results.append({"check": name, "status": status, "detail": detail, "seconds": round(seconds, 2)})
        print(f"[{status.upper():4}] {name} ({seconds:.1f}s): {detail.splitlines()[-1] if detail else ''}")

    if "mirror-integrity" not in args.skip:
        t = time.monotonic()
        status, detail = check_mirror_integrity()
        record("mirror-integrity", status, detail, time.monotonic() - t)
    if "skill-lint" not in args.skip:
        t = time.monotonic()
        rc, out = run([sys.executable, "scripts/skill_lint.py"])
        record("skill-lint", "ok" if rc == 0 else "fail", out, time.monotonic() - t)
        if rc:
            print(out)
    if "pytest" not in args.skip:
        t = time.monotonic()
        rc, out = run([sys.executable, "-m", "pytest", "skills", "scripts", "-q", "-p", "no:cacheprovider"])
        record("pytest", "ok" if rc == 0 else "fail", out, time.monotonic() - t)
        if rc:
            print(out[-4000:])
    if "official-drift" not in args.skip:
        t = time.monotonic()
        if (ROOT / ".agents" / "skills").is_dir():
            rc, out = run([sys.executable, "scripts/sync-official.py", "check"])
            record("official-drift", "ok" if rc == 0 else "fail", out, time.monotonic() - t)
            if rc:
                print(out)
        else:
            record("official-drift", "skip", "no .agents/ install (CI) — run locally after `npx skills update`", 0.0)
    if args.json:
        args.json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 1 if any(r["status"] == "fail" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
