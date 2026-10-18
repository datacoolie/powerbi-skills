"""Opt-in live Fabric lifecycle smoke test.

Runs create -> get-definition -> update-definition -> soft-delete against a
throwaway sandbox workspace. Skipped unless BOTH environment variables are set:

    FABRIC_SANDBOX_SMOKE=1
    FABRIC_WORKSPACE_ID=<sandbox-workspace-guid>

This test performs real Azure CLI calls and requires an authenticated `az`
session with Contributor on the sandbox workspace. It never runs in the default
offline suite and never performs a hard delete.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import power_bi_management as cli  # noqa: E402

_ENABLED = os.environ.get("FABRIC_SANDBOX_SMOKE") == "1"
_WORKSPACE = os.environ.get("FABRIC_WORKSPACE_ID", "")
_MODEL = os.environ.get("FABRIC_SEMANTIC_MODEL_ID", "")


def _minimal_report(root: Path, model_id: str) -> None:
    (root / "definition" / "pages").mkdir(parents=True)
    (root / "definition.pbir").write_text(
        json.dumps(
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
                "version": "4.0",
                "datasetReference": {
                    "byConnection": {"connectionString": f"semanticmodelid={model_id}"}
                },
            }
        ),
        encoding="utf-8",
    )
    (root / "definition" / "report.json").write_text(
        json.dumps({"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/2.0.0/schema.json"}),
        encoding="utf-8",
    )
    (root / "definition" / "version.json").write_text(
        json.dumps({"version": "2.0.0"}), encoding="utf-8"
    )
    (root / "definition" / "pages" / "pages.json").write_text(
        json.dumps({"pageOrder": [], "activePageName": ""}), encoding="utf-8"
    )


@unittest.skipUnless(_ENABLED and _WORKSPACE and _MODEL,
                     "set FABRIC_SANDBOX_SMOKE=1, FABRIC_WORKSPACE_ID, FABRIC_SEMANTIC_MODEL_ID")
class SandboxLifecycleTest(unittest.TestCase):
    def test_create_download_update_softdelete(self):
        name = f"pbi-skills-smoke-{int(time.time())}"
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / f"{name}.Report"
            _minimal_report(src, _MODEL)
            out = Path(tmp) / "downloaded"
            try:
                self.assertEqual(
                    cli.main([
                        "create", "--workspace-id", _WORKSPACE,
                        "--definition-dir", str(src), "--display-name", name,
                    ]),
                    0,
                )
                self.assertEqual(
                    cli.main([
                        "get-definition", "--workspace-id", _WORKSPACE,
                        "--report-name", name, "--out-dir", str(out),
                    ]),
                    0,
                )
                self.assertTrue((out / "definition.pbir").is_file())
                self.assertEqual(
                    cli.main([
                        "update-definition", "--workspace-id", _WORKSPACE,
                        "--report-name", name, "--definition-dir", str(out),
                    ]),
                    0,
                )
            finally:
                # Always attempt soft delete; print id on failure for cleanup.
                rc = cli.main([
                    "delete", "--workspace-id", _WORKSPACE, "--report-name", name,
                ])
                if rc != 0:
                    print(f"MANUAL CLEANUP NEEDED: report {name!r} in {_WORKSPACE}")


if __name__ == "__main__":
    unittest.main()
