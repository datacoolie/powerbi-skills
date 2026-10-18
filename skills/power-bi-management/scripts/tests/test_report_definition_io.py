"""Offline tests for report_definition_io: allowlist, staging, safe extraction."""

from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import report_definition_io as rio  # noqa: E402


def _make_report(root: Path, *, with_noise: bool = True) -> None:
    (root / "definition" / "pages").mkdir(parents=True)
    (root / "StaticResources").mkdir(parents=True)
    (root / "definition.pbir").write_text(
        json.dumps({"version": "4.0", "datasetReference": {"byPath": {"path": "../M.SemanticModel"}}}),
        encoding="utf-8",
    )
    (root / "definition" / "report.json").write_text("{}", encoding="utf-8")
    (root / "definition" / "version.json").write_text("{}", encoding="utf-8")
    (root / "definition" / "pages" / "pages.json").write_text("{}", encoding="utf-8")
    (root / "StaticResources" / "theme.json").write_text("{}", encoding="utf-8")
    if with_noise:
        (root / ".pbi").mkdir()
        (root / ".pbi" / "localSettings.json").write_text(
            json.dumps({"reportId": "local-guid"}), encoding="utf-8"
        )
        (root / ".platform").write_text("{}", encoding="utf-8")
        (root / "Report.pbip").write_text("{}", encoding="utf-8")


class PackParityTests(unittest.TestCase):
    """Helper payload must match `powerbi-report-author pack` (official transport) part-for-part.

    The only intentional difference: the helper never uploads `.platform`
    (Git-integration system file), while `pack` includes it.
    """

    def test_helper_payload_matches_official_pack(self):
        import shutil
        import subprocess

        cli = shutil.which("powerbi-report-author")
        if not cli:
            self.skipTest("powerbi-report-author CLI not installed")
        with tempfile.TemporaryDirectory() as tmp:
            scaffold = subprocess.run(
                [cli, "scaffold", tmp, "--name", "Parity", "--offline"],
                capture_output=True, text=True,
            )
            if scaffold.returncode != 0:
                self.skipTest("scaffold unavailable in this CLI version")
            report_dir = Path(tmp) / "Parity.Report"
            packed = subprocess.run(
                [cli, "pack", str(report_dir), "--raw"], capture_output=True, text=True,
            )
            if packed.returncode != 0:
                self.skipTest("pack unavailable in this CLI version")
            official = {p["path"]: p["payload"] for p in json.loads(packed.stdout)["definition"]["parts"]}
            ours = {p["path"]: p["payload"]
                    for p in rio.build_upload_payload(report_dir)["definition"]["parts"]}
            official.pop(".platform", None)
            self.assertEqual(official, ours)


class CollectPartsTests(unittest.TestCase):
    def test_excludes_local_noise(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "R.Report"
            _make_report(root)
            paths = {p.path for p in rio.collect_parts(root)}
            self.assertIn("definition.pbir", paths)
            self.assertIn("definition/report.json", paths)
            self.assertIn("StaticResources/theme.json", paths)
            self.assertNotIn(".platform", paths)
            self.assertFalse(any(".pbi/" in p for p in paths))
            self.assertFalse(any(p.endswith(".pbip") for p in paths))

    def test_missing_pbir_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "R.Report"
            (root / "definition").mkdir(parents=True)
            with self.assertRaises(rio.DefinitionError):
                rio.collect_parts(root)

    def test_unexpected_root_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "R.Report"
            _make_report(root, with_noise=False)
            (root / "rogue.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(rio.DefinitionError):
                rio.collect_parts(root)


class UploadPayloadTests(unittest.TestCase):
    def test_payload_is_base64(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "R.Report"
            _make_report(root, with_noise=False)
            payload = rio.build_upload_payload(root)
            parts = payload["definition"]["parts"]
            self.assertTrue(all(p["payloadType"] == "InlineBase64" for p in parts))
            for p in parts:
                base64.b64decode(p["payload"], validate=True)


class StagingImmutabilityTests(unittest.TestCase):
    def test_source_unchanged_and_binding_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "R.Report"
            _make_report(root)
            before = rio.content_digest(root)
            staging = rio.stage_publish_copy(root, "model-123")
            try:
                after = rio.content_digest(root)
                self.assertEqual(before, after, "source must not change")
                staged_pbir = json.loads(
                    (Path(staging) / "definition.pbir").read_text(encoding="utf-8")
                )
                self.assertIn("byConnection", staged_pbir["datasetReference"])
                self.assertEqual(
                    staged_pbir["datasetReference"]["byConnection"]["connectionString"],
                    "semanticmodelid=model-123",
                )
                self.assertFalse((Path(staging) / ".platform").exists())
                self.assertFalse((Path(staging) / ".pbi").exists())
            finally:
                rio.cleanup(staging)

    def test_empty_model_id_fails(self):
        with self.assertRaises(rio.DefinitionError):
            rio.rewrite_binding({"datasetReference": {}}, "")


class SafeExtractTests(unittest.TestCase):
    def _definition(self, path: str, data: bytes = b"{}"):
        return {
            "definition": {
                "parts": [
                    {
                        "path": path,
                        "payload": base64.b64encode(data).decode("ascii"),
                        "payloadType": "InlineBase64",
                    }
                ]
            }
        }

    def test_writes_valid_parts(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            rio.safe_extract(self._definition("definition/report.json"), out)
            self.assertTrue((out / "definition" / "report.json").is_file())

    def test_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(rio.DefinitionError):
                rio.safe_extract(self._definition("../escape.json"), Path(tmp) / "out")

    def test_rejects_absolute(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(rio.DefinitionError):
                rio.safe_extract(self._definition("/etc/passwd"), Path(tmp) / "out")

    def test_rejects_backslash(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(rio.DefinitionError):
                rio.safe_extract(self._definition("definition\\x.json"), Path(tmp) / "out")

    def test_rejects_duplicate_case_collision(self):
        payload = base64.b64encode(b"{}").decode("ascii")
        definition = {
            "definition": {
                "parts": [
                    {"path": "definition/A.json", "payload": payload, "payloadType": "InlineBase64"},
                    {"path": "definition/a.json", "payload": payload, "payloadType": "InlineBase64"},
                ]
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(rio.DefinitionError):
                rio.safe_extract(definition, Path(tmp) / "out")

    def test_rejects_invalid_base64(self):
        bad = {
            "definition": {
                "parts": [
                    {"path": "definition/x.json", "payload": "!!!notb64!!!", "payloadType": "InlineBase64"}
                ]
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(rio.DefinitionError):
                rio.safe_extract(bad, Path(tmp) / "out")

    def test_no_parts_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(rio.DefinitionError):
                rio.safe_extract({"definition": {"parts": []}}, Path(tmp) / "out")


if __name__ == "__main__":
    unittest.main()
