"""Offline tests for power_bi_management CLI wiring. No Azure CLI required."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fabric_rest_client as frc  # noqa: E402
import power_bi_management as cli  # noqa: E402
import report_definition_io as rio  # noqa: E402


def _completed(stdout: str = "", stderr: str = "", returncode: int = 0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


class ScriptedRunner:
    """Maps ``az rest`` calls to canned responses by (method, url-substring)."""

    def __init__(self, rules):
        self._rules = list(rules)
        self.calls = []

    def __call__(self, args):
        method = args[args.index("--method") + 1]
        url = args[args.index("--url") + 1]
        self.calls.append((method, url))
        for rule_method, needle, response in self._rules:
            if rule_method == method and needle in url:
                return response(args) if callable(response) else response
        raise AssertionError(f"No rule for {method} {url}")


def _make_report(root: Path) -> None:
    (root / "definition" / "pages").mkdir(parents=True)
    (root / "definition.pbir").write_text(
        json.dumps({"version": "4.0", "datasetReference": {"byPath": {"path": "../M.SemanticModel"}}}),
        encoding="utf-8",
    )
    (root / "definition" / "report.json").write_text("{}", encoding="utf-8")
    (root / "definition" / "version.json").write_text("{}", encoding="utf-8")
    (root / ".pbi").mkdir()
    (root / ".pbi" / "localSettings.json").write_text("{}", encoding="utf-8")


class ParserTests(unittest.TestCase):
    def test_help_lists_commands(self):
        parser = cli.build_parser()
        text = parser.format_help()
        for cmd in ("list", "get-definition", "publish-pbip", "delete"):
            self.assertIn(cmd, text)

    def test_no_hard_delete_flag(self):
        parser = cli.build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["delete", "--workspace-id", "w", "--report-id", "r", "--hard-delete"])


class SoftDeleteTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def test_soft_delete_only(self):
        frc._run = ScriptedRunner([
            ("delete", "reports/r1", _completed(stderr="Response status: 200")),
        ])
        rc = cli.main(["delete", "--workspace-id", "w1", "--report-id", "r1"])
        self.assertEqual(rc, 0)
        method, url = frc._run.calls[-1]
        self.assertEqual(method, "delete")
        self.assertNotIn("hardDelete", url)


class PublishPbipTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def test_publish_creates_and_leaves_source_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Sales.Report"
            _make_report(root)
            before = rio.content_digest(root)

            frc._run = ScriptedRunner([
                ("get", "/reports", _completed(stdout='{"value": []}', stderr="Response status: 200")),
                ("post", "/reports", _completed(stdout='{"id": "new-report"}', stderr="Response status: 201")),
            ])
            rc = cli.main([
                "publish-pbip",
                "--workspace-id", "w1",
                "--report-dir", str(root),
                "--semantic-model-id", "model-9",
                "--display-name", "Sales",
            ])
            self.assertEqual(rc, 0)
            self.assertEqual(before, rio.content_digest(root))
            # source binding still byPath (never mutated)
            pbir = json.loads((root / "definition.pbir").read_text(encoding="utf-8"))
            self.assertIn("byPath", pbir["datasetReference"])

    def test_publish_requires_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Sales.Report"
            _make_report(root)
            with self.assertRaises(SystemExit):
                cli.main([
                    "publish-pbip",
                    "--workspace-id", "w1",
                    "--report-dir", str(root),
                ])

    def _publish_existing(self, root, *extra):
        frc._run = ScriptedRunner([
            ("get", "/reports", _completed(
                stdout='{"value": [{"id": "r-old", "displayName": "Sales"}]}',
                stderr="Response status: 200")),
            ("post", "updateDefinition", _completed(stdout="{}", stderr="Response status: 200")),
        ])
        return cli.main([
            "publish-pbip", "--workspace-id", "w1", "--report-dir", str(root),
            "--semantic-model-id", "model-9", "--display-name", "Sales", *extra,
        ])

    def test_publish_existing_report_requires_overwrite_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Sales.Report"
            _make_report(root)
            with self.assertRaises(SystemExit) as ctx:
                self._publish_existing(root)
            self.assertIn("--confirm-overwrite", str(ctx.exception))
            self.assertFalse([c for c in frc._run.calls if c[0] == "post"])

    def test_publish_existing_report_with_confirmation_updates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Sales.Report"
            _make_report(root)
            self.assertEqual(self._publish_existing(root, "--confirm-overwrite"), 0)
            self.assertTrue([c for c in frc._run.calls if c[0] == "post" and "updateDefinition" in c[1]])


class UpdateDefinitionGuardTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def test_update_definition_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Sales.Report"
            _make_report(root)
            frc._run = ScriptedRunner([])
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["update-definition", "--workspace-id", "w1", "--report-id", "r1",
                          "--definition-dir", str(root)])
            self.assertIn("--confirm-overwrite", str(ctx.exception))
            self.assertEqual(frc._run.calls, [])


if __name__ == "__main__":
    unittest.main()
