#!/usr/bin/env python3
"""
pbir_gate.py — single-command Phase 4c gate for PBIR reports.

Runs the full polish + lint + schema chain and returns ONE pass/fail verdict:

    1. finalize_pbir.py        (mechanical polish — grid, KPI row, theme tokens, fonts, alt text)
    2. design_quality_check.py (design lint rules, style-aware)
    3. validate_report.py      (structural cross-ref checks + naming conventions)
    4. powerbi-report-author validate  (CLI schema validation)
    5. check_layout_drift.py   (built positions vs the approved layout manifest; skipped when none exists)

Stages 1-3 and 5 are imported directly; stage 4 uses the CLI subprocess.

Emits a JSON verdict object to stdout and (optionally) writes it to a file.

Usage:
    python pbir_gate.py --report <path-to-.Report>            # read-only: lint + validate (default)
    python pbir_gate.py --report <path-to-.Report> --apply    # also let finalize_pbir WRITE polish fixes
    python pbir_gate.py --report <path-to-.Report> --style executive
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
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure the scripts directory is on sys.path for sibling imports
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# pbir_utils handles the Windows UTF-8 console fix on import
import pbir_utils  # noqa: F401 — side-effect: reconfigures console


@dataclass
class StageResult:
    name: str
    ok: bool
    summary: str = ""
    skipped: bool = False
    duration_s: float = 0.0


@dataclass
class GateVerdict:
    report: str
    style: str
    passed: bool
    timestamp: str = ""
    duration_s: float = 0.0
    stages: list[StageResult] = field(default_factory=list)
    errors: int = 0
    warnings: int = 0


# ── Stage runners (direct function calls) ─────────────────────

def stage_finalize(report: Path, dry_run: bool, skip: bool) -> StageResult:
    if skip:
        return StageResult(name="finalize_pbir", ok=True, skipped=True, summary="skipped by flag")

    t0 = time.monotonic()
    try:
        from finalize_pbir import Report, MODULES, MODULE_ORDER

        rpt = Report.load(report)
        summaries = []
        for module_name in MODULE_ORDER:
            fn = MODULES[module_name]
            result = fn(rpt, dry_run)
            summaries.append(f"{module_name}: {', '.join(f'{k}={v}' for k, v in result.items())}")
        elapsed = time.monotonic() - t0
        return StageResult(name="finalize_pbir", ok=True, summary="; ".join(summaries), duration_s=round(elapsed, 2))
    except Exception as exc:
        elapsed = time.monotonic() - t0
        return StageResult(name="finalize_pbir", ok=False, summary=f"{type(exc).__name__}: {exc}"[:400], duration_s=round(elapsed, 2))


def stage_lint(report: Path, style: str, skip: bool, evidence_dir: Path) -> tuple[StageResult, int, int]:
    if skip:
        return StageResult(name="design_quality_check", ok=True, skipped=True, summary="skipped by flag"), 0, 0

    t0 = time.monotonic()
    try:
        from design_quality_check import (
            LintReport,
            _clear_cache,
            check_visual_counts,
            check_drillthrough_back_button,
            check_pie_slices,
            check_alt_text,
            check_default_page_names,
            check_bad_titles,
            check_hardcoded_hex,
            check_bookmark_targets,
            check_three_d_effects,
            check_rainbow_palette,
            check_report_visual_budget,
            check_alt_text_quality,
            check_orphan_pages,
            check_contrast,
            write_report,
        )

        _clear_cache()
        lint = LintReport()
        check_visual_counts(report, style, lint)
        check_drillthrough_back_button(report, lint)
        check_pie_slices(report, lint)
        check_alt_text(report, lint)
        check_default_page_names(report, lint)
        check_bad_titles(report, lint)
        check_hardcoded_hex(report, lint)
        check_bookmark_targets(report, lint)
        check_three_d_effects(report, lint)
        check_rainbow_palette(report, lint)
        check_report_visual_budget(report, lint)
        check_alt_text_quality(report, lint)
        check_orphan_pages(report, lint)
        check_contrast(report, lint)

        evidence_dir.mkdir(parents=True, exist_ok=True)
        write_report(lint, evidence_dir / "design_report.md", style)

        errs = len(lint.errors())
        warns = len(lint.warnings())
        elapsed = time.monotonic() - t0
        ok = errs == 0
        summary = f"errors={errs}, warnings={warns}"
        return StageResult(name="design_quality_check", ok=ok, summary=summary, duration_s=round(elapsed, 2)), errs, warns

    except Exception as exc:
        elapsed = time.monotonic() - t0
        return StageResult(name="design_quality_check", ok=False, summary=f"{type(exc).__name__}: {exc}"[:400], duration_s=round(elapsed, 2)), 0, 0


def stage_validate(report: Path, skip: bool) -> StageResult:
    if skip:
        return StageResult(name="validate_report", ok=True, skipped=True, summary="skipped by flag")

    t0 = time.monotonic()
    try:
        from validate_report import validate_report

        result = validate_report(report)
        elapsed = time.monotonic() - t0
        n_err = len(result.errors)
        n_warn = len(result.warnings)
        ok = n_err == 0
        summary = f"errors={n_err}, warnings={n_warn}"
        return StageResult(name="validate_report", ok=ok, summary=summary, duration_s=round(elapsed, 2))
    except Exception as exc:
        elapsed = time.monotonic() - t0
        return StageResult(name="validate_report", ok=False, summary=f"{type(exc).__name__}: {exc}"[:400], duration_s=round(elapsed, 2))


def stage_schemas(report: Path, skip: bool) -> StageResult:
    """Schema validation via powerbi-report-author CLI."""
    if skip:
        return StageResult(name="cli_validate", ok=True, skipped=True, summary="skipped by flag")

    t0 = time.monotonic()
    try:
        import shutil
        import subprocess

        # Prefer the globally installed CLI; fall back to npx. On Windows both are
        # .cmd shims, so resolve with shutil.which() (PATHEXT-aware) and invoke the
        # resolved path directly without shell=True.
        cli_path = shutil.which("powerbi-report-author")
        if cli_path:
            cmd = [cli_path, "validate", str(report)]
        else:
            npx_path = shutil.which("npx")
            if npx_path is None:
                elapsed = time.monotonic() - t0
                return StageResult(name="cli_validate", ok=True, skipped=True,
                                   summary="powerbi-report-author and npx not found on PATH — skipped",
                                   duration_s=round(elapsed, 2))
            cmd = [npx_path, "powerbi-report-author", "validate", str(report)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        elapsed = time.monotonic() - t0
        ok = result.returncode == 0
        # Parse error/warning counts from CLI output
        output = result.stdout.strip() or result.stderr.strip()
        summary = output[:400] if output else ("passed" if ok else "failed")
        return StageResult(name="cli_validate", ok=ok, summary=summary, duration_s=round(elapsed, 2))
    except FileNotFoundError:
        elapsed = time.monotonic() - t0
        return StageResult(name="cli_validate", ok=True, skipped=True,
                           summary="powerbi-report-author CLI not installed — skipped",
                           duration_s=round(elapsed, 2))
    except Exception as exc:
        elapsed = time.monotonic() - t0
        return StageResult(name="cli_validate", ok=False, summary=f"{type(exc).__name__}: {exc}"[:400], duration_s=round(elapsed, 2))


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess | None:
    import shutil
    git = shutil.which("git")
    if not git:
        return None
    try:
        return subprocess.run([git, *args], cwd=str(cwd), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None


def apply_safety(report: Path, force: bool) -> tuple[bool, str, Path | None]:
    """Gate for --apply: finalize rewrites report files, so make that recoverable.

    Returns (allowed, message, backup_dir).
    - inside a git work tree: refuse when the report folder has uncommitted changes (they would be
      mixed with the polish rewrite and become hard to review/revert) unless ``force``;
    - outside git (or git missing): copy the report to a backup folder before writing.
    """
    inside = _git(["rev-parse", "--is-inside-work-tree"], report)
    if inside is not None and inside.returncode == 0 and inside.stdout.strip() == "true":
        status = _git(["status", "--porcelain", "--", str(report)], report)
        dirty = (status.stdout.strip() if status is not None and status.returncode == 0 else "")
        if dirty and not force:
            return False, (
                "--apply refused: the report folder has uncommitted git changes. Commit or stash them "
                "first (so the polish rewrite is a separate, revertable diff), or pass --force-apply."
            ), None
        return True, "git work tree clean — polish changes can be reviewed/reverted with git", None
    backup = Path(tempfile.gettempdir()) / "pbir-gate-backup" / f"{report.resolve().name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    import shutil
    shutil.copytree(report, backup)
    return True, f"not in a git work tree — backup written to {backup}", backup


def stage_drift(report: Path, manifest: Path | None, tolerance: int) -> StageResult:
    """Layout drift vs the approved layout manifest (only when a manifest exists)."""
    manifest = manifest or report.resolve().parent / "_brief" / "layout-manifest.json"
    if not manifest.is_file():
        return StageResult(name="layout_drift", ok=True, skipped=True,
                           summary=f"no layout manifest at {manifest} — skipped")
    t0 = time.monotonic()
    try:
        from check_layout_drift import check
        findings = check(report, json.loads(manifest.read_text(encoding="utf-8")), tolerance)
        errors = [f for f in findings if f["level"] == "error"]
        summary = (f"errors={len(errors)}, warnings={sum(f['level'] == 'warn' for f in findings)}, "
                   f"extra={sum(f['level'] == 'info' for f in findings)}")
        if errors:
            summary += "; " + "; ".join(f"{f.get('visual', '')}: {f['kind']}" for f in errors[:5])
        return StageResult(name="layout_drift", ok=not errors, summary=summary[:400],
                           duration_s=round(time.monotonic() - t0, 2))
    except Exception as exc:  # noqa: BLE001 — a crashing stage is reported, not raised
        return StageResult(name="layout_drift", ok=False, summary=f"{type(exc).__name__}: {exc}"[:400],
                           duration_s=round(time.monotonic() - t0, 2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Single-command Phase 4c gate: finalize + lint + schema-validate.",
        epilog=(
            "Examples:\n"
            "  python pbir_gate.py --report ./MyReport.Report\n"
            "  python pbir_gate.py --report ./MyReport.Report --apply --style executive --allow-warnings\n"
            "  python pbir_gate.py --report ./MyReport.Report --json verdict.json\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--report", required=True, type=Path, help="Path to the .Report folder")
    parser.add_argument("--style", default="analytical", choices=["executive", "analytical", "operational"])
    parser.add_argument("--apply", action="store_true",
                        help="Let the finalize stage WRITE changes to the report. Without it the gate is "
                             "read-only (finalize runs as a dry run) — use --apply only on reports generated "
                             "in this session, never on a brownfield report whose layout must be preserved")
    parser.add_argument("--manifest", type=Path, default=None,
                        help="layout manifest for the drift stage (default: <project>/_brief/layout-manifest.json; "
                             "the stage is skipped when none exists)")
    parser.add_argument("--drift-tolerance", type=int, default=0, help="allowed per-edge px difference (default 0)")
    parser.add_argument("--skip-drift", action="store_true", help="Skip the layout-drift stage")
    parser.add_argument("--force-apply", action="store_true",
                        help="With --apply: proceed even if the report folder has uncommitted git changes")
    parser.add_argument("--dry-run", action="store_true", help="Deprecated alias: read-only is now the default")
    parser.add_argument("--evidence-dir", type=Path, default=None,
                        help="Where design_report.md is written (default: the report folder with --apply, "
                             "otherwise <temp>/pbir-gate/<report-name>)")
    parser.add_argument("--skip-finalize", action="store_true", help="Skip finalize_pbir stage")
    parser.add_argument("--skip-lint", action="store_true", help="Skip design_quality_check stage")
    parser.add_argument("--skip-validate", action="store_true", help="Skip structural-validate stage")
    parser.add_argument("--skip-schemas", action="store_true", help="Skip CLI schema-validation stage")
    parser.add_argument("--allow-warnings", action="store_true", help="Gate passes even with lint warnings")
    parser.add_argument("--json", type=Path, default=None, help="Write JSON verdict to this path")
    parser.add_argument("--verbose", action="store_true", help="Show debug details")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings and errors")
    args = parser.parse_args()

    from pbir_utils import setup_logging
    log = setup_logging("pbir_gate", verbose=args.verbose, quiet=args.quiet)

    if not args.report.exists() or not args.report.is_dir():
        log.error("report path invalid: %s", args.report)
        return 1
    if not (args.report / "definition").exists():
        log.error("%s is not a PBIR report (missing 'definition/')", args.report)
        return 1

    gate_t0 = time.monotonic()
    verdict = GateVerdict(
        report=str(args.report),
        style=args.style,
        passed=False,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # ── Stage 1: finalize (read-only unless --apply) ──
    dry_run = args.dry_run or not args.apply
    if args.apply and not args.dry_run and not args.skip_finalize:
        allowed, message, _backup = apply_safety(args.report, args.force_apply)
        if not allowed:
            log.error(message)
            return 1
        print(f"pbir_gate: {message}", file=sys.stderr)
    evidence_dir = args.evidence_dir or (
        args.report if args.apply
        else Path(tempfile.gettempdir()) / "pbir-gate" / args.report.resolve().name
    )
    s1 = stage_finalize(args.report, dry_run, args.skip_finalize)
    verdict.stages.append(s1)

    # ── Stage 2: lint ──
    s2, errs, warns = stage_lint(args.report, args.style, args.skip_lint, evidence_dir)
    verdict.stages.append(s2)
    verdict.errors = errs
    verdict.warnings = warns

    # ── Stage 3: validate ──
    s3 = stage_validate(args.report, args.skip_validate)
    verdict.stages.append(s3)

    # ── Stage 4: schema validation ──
    s4 = stage_schemas(args.report, args.skip_schemas)
    verdict.stages.append(s4)

    # ── Stage 5: layout drift (vs the approved layout manifest, when present) ──
    s5 = (StageResult(name="layout_drift", ok=True, skipped=True, summary="skipped by flag")
          if args.skip_drift else stage_drift(args.report, args.manifest, args.drift_tolerance))
    verdict.stages.append(s5)

    verdict.duration_s = round(time.monotonic() - gate_t0, 2)

    # ── Verdict ──
    any_stage_failed = any(not s.ok and not s.skipped for s in verdict.stages)
    has_errors = errs > 0 or (not s3.ok and not s3.skipped) or (not s4.ok and not s4.skipped) \
        or (not s5.ok and not s5.skipped)
    has_warnings = warns > 0

    if any_stage_failed and not has_errors:
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
    print(f"PBIR gate: {'PASSED' if verdict.passed else 'FAILED'} ({verdict.duration_s}s)", file=sys.stderr)
    print(f"  errors={errs} warnings={warns} allow_warnings={args.allow_warnings}", file=sys.stderr)
    for s in verdict.stages:
        tag = "skip" if s.skipped else ("ok  " if s.ok else "FAIL")
        print(f"  [{tag}] {s.name} ({s.duration_s}s): {s.summary}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
