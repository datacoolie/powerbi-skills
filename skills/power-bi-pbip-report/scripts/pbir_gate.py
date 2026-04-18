#!/usr/bin/env python3
"""
pbir_gate.py — single-command Phase 4c gate for PBIR reports.

Runs the full polish + lint + schema chain and returns ONE pass/fail verdict:

    1. finalize_pbir.py      (mechanical polish — grid, KPI row, theme tokens, fonts, alt text)
    2. design_quality_check.py  (8 design lint rules, style-aware)
    3. validate_report.js    (Microsoft JSON-schema validation)  — if Node.js present
       OR validate_report.py                                     — fallback

Emits a JSON verdict object to stdout and (optionally) writes it to a file.

Usage:
    python pbir_gate.py --report <path-to-.Report>
    python pbir_gate.py --report <path-to-.Report> --style executive
    python pbir_gate.py --report <path-to-.Report> --dry-run
    python pbir_gate.py --report <path-to-.Report> --json verdict.json
    python pbir_gate.py --report <path-to-.Report> --skip-finalize
    python pbir_gate.py --report <path-to-.Report> --allow-warnings  # pass with warnings

Exit codes:
    0 — gate PASSED (no errors; warnings allowed if --allow-warnings)
    1 — input error (path invalid, not a PBIR report)
    2 — gate FAILED (errors in any stage, or warnings when not allowed)
    3 — tool error (a stage crashed unexpectedly)
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# Windows default console (cp1252) can't print U+2264/U+2014 etc.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass


SCRIPTS_DIR = Path(__file__).resolve().parent


@dataclass
class StageResult:
    name: str
    ok: bool
    exit_code: int
    summary: str = ""
    skipped: bool = False


@dataclass
class GateVerdict:
    report: str
    style: str
    passed: bool
    stages: list[StageResult] = field(default_factory=list)
    errors: int = 0
    warnings: int = 0


def _run(cmd: list[str]) -> tuple[int, str, str]:
    """Run a subprocess; return (exit_code, stdout, stderr)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except FileNotFoundError as exc:
        return 127, "", f"command not found: {exc}"
    except Exception as exc:  # noqa: BLE001
        return 3, "", f"{type(exc).__name__}: {exc}"


def _count_findings(stdout: str) -> tuple[int, int]:
    """Parse 'Errors: N, Warnings: M' line from design_quality_check.py output."""
    import re
    m = re.search(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", stdout)
    if not m:
        return 0, 0
    return int(m.group(1)), int(m.group(2))


def stage_finalize(report: Path, dry_run: bool, skip: bool) -> StageResult:
    if skip:
        return StageResult(name="finalize_pbir", ok=True, exit_code=0, skipped=True, summary="skipped by flag")
    cmd = [sys.executable, str(SCRIPTS_DIR / "finalize_pbir.py"), "--report", str(report)]
    if dry_run:
        cmd.append("--dry-run")
    code, out, err = _run(cmd)
    summary = (out.strip().splitlines() or [""])[-1] if code == 0 else (err.strip() or out.strip())[:400]
    return StageResult(name="finalize_pbir", ok=(code == 0), exit_code=code, summary=summary)


def stage_lint(report: Path, style: str, skip: bool) -> tuple[StageResult, int, int]:
    if skip:
        return StageResult(name="design_quality_check", ok=True, exit_code=0, skipped=True, summary="skipped by flag"), 0, 0
    cmd = [sys.executable, str(SCRIPTS_DIR / "design_quality_check.py"),
           "--report", str(report), "--style", style, "--write-report"]
    code, out, err = _run(cmd)
    errs, warns = _count_findings(out)
    ok = code in (0, 2)  # 2 = errors found, but not a tool crash
    summary = f"errors={errs}, warnings={warns}"
    return StageResult(name="design_quality_check", ok=ok, exit_code=code, summary=summary), errs, warns


def stage_validate(report: Path, skip: bool) -> StageResult:
    if skip:
        return StageResult(name="validate_report", ok=True, exit_code=0, skipped=True, summary="skipped by flag")

    node_script = SCRIPTS_DIR / "validate_report.js"
    py_fallback = SCRIPTS_DIR / "validate_report.py"

    if shutil.which("node") and node_script.exists():
        code, out, err = _run(["node", str(node_script), str(report)])
        tool = "validate_report.js (schema)"
    elif py_fallback.exists():
        code, out, err = _run([sys.executable, str(py_fallback), str(report)])
        tool = "validate_report.py (syntax)"
    else:
        return StageResult(name="validate_report", ok=False, exit_code=3, summary="no validator available")

    summary = f"{tool}; exit={code}"
    return StageResult(name="validate_report", ok=(code == 0), exit_code=code, summary=summary)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Single-command Phase 4c gate: finalize + lint + schema-validate.",
        epilog=(
            "Examples:\n"
            "  python pbir_gate.py --report ./MyReport.Report\n"
            "  python pbir_gate.py --report ./MyReport.Report --style executive --allow-warnings\n"
            "  python pbir_gate.py --report ./MyReport.Report --dry-run --json verdict.json\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--report", required=True, type=Path, help="Path to the .Report folder")
    parser.add_argument("--style", default="analytical", choices=["executive", "analytical", "operational"])
    parser.add_argument("--dry-run", action="store_true", help="Run finalize without writing changes")
    parser.add_argument("--skip-finalize", action="store_true", help="Skip finalize_pbir stage")
    parser.add_argument("--skip-lint", action="store_true", help="Skip design_quality_check stage")
    parser.add_argument("--skip-validate", action="store_true", help="Skip schema-validate stage")
    parser.add_argument("--allow-warnings", action="store_true", help="Gate passes even with lint warnings")
    parser.add_argument("--json", type=Path, default=None, help="Write JSON verdict to this path")
    args = parser.parse_args()

    if not args.report.exists() or not args.report.is_dir():
        print(f"ERROR: report path invalid: {args.report}", file=sys.stderr)
        return 1
    if not (args.report / "definition").exists():
        print(f"ERROR: {args.report} is not a PBIR report (missing 'definition/')", file=sys.stderr)
        return 1

    verdict = GateVerdict(report=str(args.report), style=args.style, passed=False)

    # ── Stage 1: finalize ──
    s1 = stage_finalize(args.report, args.dry_run, args.skip_finalize)
    verdict.stages.append(s1)

    # ── Stage 2: lint ──
    s2, errs, warns = stage_lint(args.report, args.style, args.skip_lint)
    verdict.stages.append(s2)
    verdict.errors = errs
    verdict.warnings = warns

    # ── Stage 3: validate ──
    s3 = stage_validate(args.report, args.skip_validate)
    verdict.stages.append(s3)

    # ── Verdict ──
    any_stage_crashed = any(not s.ok and not s.skipped for s in verdict.stages)
    has_errors = errs > 0 or s3.exit_code not in (0,) and not s3.skipped
    has_warnings = warns > 0

    if any_stage_crashed:
        verdict.passed = False
        exit_code = 3
    elif has_errors:
        verdict.passed = False
        exit_code = 2
    elif has_warnings and not args.allow_warnings:
        verdict.passed = False
        exit_code = 2
    else:
        verdict.passed = True
        exit_code = 0

    # ── Output ──
    payload: dict[str, Any] = asdict(verdict)
    out_text = json.dumps(payload, indent=2)
    print(out_text)

    if args.json:
        args.json.write_text(out_text, encoding="utf-8")

    print("", file=sys.stderr)
    print(f"PBIR gate: {'PASSED' if verdict.passed else 'FAILED'}", file=sys.stderr)
    print(f"  errors={errs} warnings={warns} allow_warnings={args.allow_warnings}", file=sys.stderr)
    for s in verdict.stages:
        tag = "skip" if s.skipped else ("ok  " if s.ok else "FAIL")
        print(f"  [{tag}] {s.name}: {s.summary}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
