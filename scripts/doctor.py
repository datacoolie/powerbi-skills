#!/usr/bin/env python3
"""Environment preflight for the Power BI skills pipeline.

Checks the CLIs and servers the skills rely on and prints a verdict per tool:

  node >= 20 · powerbi-report-author >= 0.5.0 (+ its own `doctor`) · az (+ login) ·
  fab (optional) · python >= 3.10 · preview hosts (desktop/service) · MCP server ids.

Usage:
    python scripts/doctor.py            # human-readable table
    python scripts/doctor.py --json     # machine-readable (for agents / CI)
    python scripts/doctor.py --strict   # exit 1 if any REQUIRED check fails

Statuses: ok, warn (optional / degraded), fail (required and missing/outdated), skip.
Exit codes: 0 no required failure, 1 a required check failed (only with --strict).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from typing import Callable, Optional

MIN_NODE = (20, 0, 0)
MIN_REPORT_AUTHOR = (0, 5, 0)
MIN_PYTHON = (3, 10, 0)

# Both ids expose the same Power BI modeling tool set (measure_operations, dax_query_operations, ...).
MODELING_MCP_ALIASES = ("powerbi-modeling-mcp", "powerbi-authoring-local")


@dataclass
class Check:
    name: str
    status: str  # ok | warn | fail | skip
    detail: str
    required: bool = True
    fix: str = ""
    extra: dict = field(default_factory=dict)


# Injection seam for tests.
def _run(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)


_which: Callable[[str], Optional[str]] = shutil.which


def parse_version(text: str) -> Optional[tuple[int, int, int]]:
    match = re.search(r"v?(\d+)\.(\d+)(?:\.(\d+))?", text or "")
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3) or 0)


def fmt(version: tuple[int, int, int]) -> str:
    return ".".join(str(p) for p in version)


def _version_check(name: str, cmd: str, minimum: tuple[int, int, int], fix: str,
                   required: bool = True, flag: str = "--version") -> Check:
    path = _which(cmd)
    if not path:
        return Check(name, "fail" if required else "warn", f"{cmd} not found on PATH", required, fix)
    try:
        out = _run([path, flag])
    except (OSError, subprocess.SubprocessError) as exc:
        return Check(name, "fail" if required else "warn", f"{cmd} failed to run: {exc}", required, fix)
    version = parse_version((out.stdout or "") + (out.stderr or ""))
    if version is None:
        return Check(name, "warn", f"could not parse version from {cmd} {flag}", required, fix)
    if version < minimum:
        return Check(name, "fail" if required else "warn",
                     f"{fmt(version)} < required {fmt(minimum)}", required, fix, {"version": fmt(version)})
    return Check(name, "ok", f"{fmt(version)}", required, extra={"version": fmt(version)})


def check_node() -> Check:
    return _version_check("node", "node", MIN_NODE, "Install Node.js LTS: winget install OpenJS.NodeJS.LTS")


def check_report_author() -> list[Check]:
    fix = "npm install -g @microsoft/powerbi-report-authoring-cli@latest"
    base = _version_check("powerbi-report-author", "powerbi-report-author", MIN_REPORT_AUTHOR, fix)
    checks = [base]
    if base.status == "ok":
        try:
            out = _run([_which("powerbi-report-author") or "powerbi-report-author", "doctor"], timeout=60)
            data = json.loads(out.stdout or "{}").get("data", {})
            failed = [c["name"] for c in data.get("checks", []) if not c.get("ok")]
            checks.append(Check("powerbi-report-author doctor", "ok" if not failed else "fail",
                                "all self-checks pass" if not failed else f"failed: {', '.join(failed)}",
                                True, fix if failed else ""))
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            checks.append(Check("powerbi-report-author doctor", "warn", f"could not run: {exc}", False))
    return checks


def check_preview_hosts() -> Check:
    path = _which("powerbi-report-author")
    if not path:
        return Check("preview hosts", "skip", "powerbi-report-author missing", False)
    try:
        out = _run([path, "preview", "--list-hosts"])
        hosts = {h["host"]: h for h in json.loads(out.stdout).get("data", {}).get("hosts", [])}
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        return Check("preview hosts", "warn", f"could not list hosts: {exc}", False)
    parts = []
    for name in ("desktop", "service"):
        info = hosts.get(name)
        if info is None:
            parts.append(f"{name}: unknown")
        elif info.get("available"):
            parts.append(f"{name}: available")
        else:
            reason = (info.get("availability") or {}).get("reason", "unavailable")
            parts.append(f"{name}: {reason}")
    any_up = any(h.get("available") for h in hosts.values())
    return Check("preview hosts", "ok" if any_up else "warn", "; ".join(parts), False,
                 "Open the report's .pbip in Power BI Desktop (enable 'external tool access through secure local "
                 "APIs' in Options > Preview features), or use --host service with --group/--dataset",
                 {"hosts": {k: bool(v.get("available")) for k, v in hosts.items()}})


def check_az() -> list[Check]:
    base = _version_check("az", "az", (2, 0, 0), "Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli",
                          required=False, flag="version")
    checks = [base]
    if base.status == "ok":
        try:
            out = _run([_which("az") or "az", "account", "show", "--query", "user.name", "-o", "tsv"], timeout=45)
            if out.returncode == 0 and (out.stdout or "").strip():
                checks.append(Check("az login", "ok", f"signed in as {out.stdout.strip()}", False))
            else:
                checks.append(Check("az login", "warn", "not signed in", False, "az login"))
        except (OSError, subprocess.SubprocessError) as exc:
            checks.append(Check("az login", "warn", f"could not check: {exc}", False))
    return checks


def check_fab() -> Check:
    path = _which("fab")
    if not path:
        return Check("fab", "warn", "not installed (optional; OneLake/lakehouse discovery falls back to MCP)",
                     False, "pip install ms-fabric-cli")
    try:
        out = _run([path, "--version"])
        version = parse_version((out.stdout or "") + (out.stderr or ""))
        return Check("fab", "ok", fmt(version) if version else "installed", False,
                     extra={"version": fmt(version) if version else ""})
    except (OSError, subprocess.SubprocessError) as exc:
        return Check("fab", "warn", f"failed to run: {exc}", False)


def check_python() -> Check:
    version = sys.version_info[:3]
    if version < MIN_PYTHON:
        return Check("python", "fail", f"{fmt(version)} < required {fmt(MIN_PYTHON)}", True,
                     "Install Python 3.10+")
    return Check("python", "ok", fmt(version))


def check_mcp_note() -> Check:
    names = " or ".join(f"`{n}`" for n in MODELING_MCP_ALIASES)
    return Check(
        "modeling MCP", "skip",
        f"cannot be probed from a script. The Power BI Modeling MCP may be registered as {names}; "
        "both expose measure_operations / dax_query_operations / table_operations. If neither is "
        "connected, model edits fall back to TMDL files.",
        False,
    )


def run_all() -> list[Check]:
    checks = [check_python(), check_node()]
    checks += check_report_author()
    checks.append(check_preview_hosts())
    checks += check_az()
    checks.append(check_fab())
    checks.append(check_mcp_note())
    return checks


def render(checks: list[Check]) -> str:
    icon = {"ok": "OK  ", "warn": "WARN", "fail": "FAIL", "skip": "SKIP"}
    lines = []
    for c in checks:
        req = "" if c.required else " (optional)"
        lines.append(f"[{icon[c.status]}] {c.name}{req}: {c.detail}")
        if c.status in ("warn", "fail") and c.fix:
            lines.append(f"       fix: {c.fix}")
    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a required check fails")
    args = parser.parse_args(argv)
    checks = run_all()
    if args.json:
        print(json.dumps([asdict(c) for c in checks], indent=2))
    else:
        print(render(checks))
    failed = [c for c in checks if c.status == "fail" and c.required]
    return 1 if (args.strict and failed) else 0


if __name__ == "__main__":
    sys.exit(main())
