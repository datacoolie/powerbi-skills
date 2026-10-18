"""Offline tests for fabric_rest_client. No network or Azure CLI required."""

from __future__ import annotations

import os
import sys
import unittest
import unittest.mock
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fabric_rest_client as frc  # noqa: E402


def _completed(stdout: str = "", stderr: str = "", returncode: int = 0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


class FakeRunner:
    """Deterministic ``az rest`` stand-in driven by a queue of responses."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls: list[list[str]] = []

    def __call__(self, args):
        self.calls.append(args)
        if not self._responses:
            raise AssertionError(f"Unexpected extra az call: {args}")
        item = self._responses.pop(0)
        return item(args) if callable(item) else item


class VerboseParseTests(unittest.TestCase):
    def test_extracts_status_and_operation_id(self):
        stderr = (
            "cli.knack: Response status: 202\n"
            "urllib3: 'x-ms-operation-id': 'op-123'\n"
            "urllib3: 'Location': 'https://api.fabric.microsoft.com/v1/operations/op-123'\n"
            "urllib3: 'Retry-After': '5'\n"
        )
        status, headers = frc.parse_verbose(stderr)
        self.assertEqual(status, 202)
        self.assertEqual(headers["x-ms-operation-id"], "op-123")
        self.assertEqual(headers["retry-after"], "5")

    def test_missing_status_fails_closed(self):
        status, headers = frc.parse_verbose("no status here")
        self.assertIsNone(status)
        self.assertEqual(headers, {})


class UrlGuardTests(unittest.TestCase):
    def test_rejects_non_https(self):
        with self.assertRaises(frc.FabricRestError):
            frc._validate_fabric_url("http://api.fabric.microsoft.com/v1/workspaces")

    def test_rejects_foreign_host(self):
        with self.assertRaises(frc.FabricRestError):
            frc._validate_fabric_url("https://evil.example.com/v1/workspaces")


class AzRestTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def test_parses_200_body(self):
        frc._run = FakeRunner([
            _completed(stdout='{"value": [1, 2]}', stderr="Response status: 200"),
        ])
        resp = frc.az_rest("get", f"{frc.FABRIC_BASE}/workspaces")
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.body, {"value": [1, 2]})

    def test_transport_failure_without_status_raises(self):
        frc._run = FakeRunner([_completed(stderr="boom", returncode=1)])
        with self.assertRaises(frc.FabricRestError):
            frc.az_rest("get", f"{frc.FABRIC_BASE}/workspaces")

    def _headers_arg(self, runner):
        args = runner.calls[0]
        start = args.index("--headers") + 1
        end = next((i for i in range(start, len(args)) if args[i].startswith("--")), len(args))
        return args[start:end]

    def test_telemetry_header_sent_by_default(self):
        runner = FakeRunner([_completed(stdout="{}", stderr="Response status: 200")])
        frc._run = runner
        with unittest.mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("POWERBI_SKILLS_TELEMETRY", None)
            frc.az_rest("get", f"{frc.FABRIC_BASE}/workspaces")
        self.assertIn("x-ms-fabric-skill=powerbi-report-cli", self._headers_arg(runner))

    def test_telemetry_header_merged_with_extra_headers_in_one_flag(self):
        runner = FakeRunner([_completed(stdout="{}", stderr="Response status: 200")])
        frc._run = runner
        with unittest.mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("POWERBI_SKILLS_TELEMETRY", None)
            frc.az_rest(
                "post", f"{frc.FABRIC_BASE}/workspaces",
                extra_headers={"Content-Type": "application/json"},
            )
        self.assertEqual(runner.calls[0].count("--headers"), 1)
        headers = self._headers_arg(runner)
        self.assertIn("x-ms-fabric-skill=powerbi-report-cli", headers)
        self.assertIn("Content-Type=application/json", headers)

    def test_telemetry_opt_out(self):
        runner = FakeRunner([_completed(stdout="{}", stderr="Response status: 200")])
        frc._run = runner
        with unittest.mock.patch.dict(os.environ, {"POWERBI_SKILLS_TELEMETRY": "off"}):
            frc.az_rest("get", f"{frc.FABRIC_BASE}/workspaces")
        self.assertNotIn("--headers", runner.calls[0])


class PaginateTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def test_follows_continuation(self):
        page1 = _completed(
            stdout='{"value": [{"id": "a"}], "continuationUri": '
            '"https://api.fabric.microsoft.com/v1/workspaces?tok=2"}',
            stderr="Response status: 200",
        )
        page2 = _completed(
            stdout='{"value": [{"id": "b"}]}',
            stderr="Response status: 200",
        )
        frc._run = FakeRunner([page1, page2])
        items = frc.paginate(f"{frc.FABRIC_BASE}/workspaces")
        self.assertEqual([i["id"] for i in items], ["a", "b"])


class ResolveTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def _single_page(self, value_json: str):
        frc._run = FakeRunner([
            _completed(stdout=value_json, stderr="Response status: 200"),
        ])

    def test_unique_match(self):
        self._single_page('{"value": [{"id": "ws1", "displayName": "Sales"}]}')
        self.assertEqual(frc.resolve_workspace_id("Sales"), "ws1")

    def test_no_match_fails(self):
        self._single_page('{"value": [{"id": "ws1", "displayName": "Other"}]}')
        with self.assertRaises(frc.FabricRestError):
            frc.resolve_workspace_id("Sales")

    def test_duplicate_match_fails(self):
        self._single_page(
            '{"value": [{"id": "ws1", "displayName": "Sales"},'
            ' {"id": "ws2", "displayName": "Sales"}]}'
        )
        with self.assertRaises(frc.FabricRestError) as ctx:
            frc.resolve_workspace_id("Sales")
        self.assertIn("ws1", str(ctx.exception))
        self.assertIn("ws2", str(ctx.exception))


class PollOperationTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def _no_sleep(self, _seconds):
        return None

    def test_running_then_succeeded(self):
        frc._run = FakeRunner([
            _completed(stdout='{"status": "Running"}', stderr="Response status: 200"),
            _completed(stdout='{"status": "Succeeded"}', stderr="Response status: 200"),
        ])
        result = frc.poll_operation("op-1", sleep=self._no_sleep)
        self.assertEqual(result["status"], "Succeeded")

    def test_succeeded_with_result(self):
        frc._run = FakeRunner([
            _completed(stdout='{"status": "Succeeded"}', stderr="Response status: 200"),
            _completed(
                stdout='{"definition": {"parts": []}}',
                stderr="Response status: 200",
            ),
        ])
        result = frc.poll_operation("op-1", get_result=True, sleep=self._no_sleep)
        self.assertEqual(result, {"definition": {"parts": []}})

    def test_failed_raises_with_detail(self):
        frc._run = FakeRunner([
            _completed(
                stdout='{"status": "Failed", "error": {"code": "Bad", "message": "nope"}}',
                stderr="Response status: 200",
            ),
        ])
        with self.assertRaises(frc.FabricRestError) as ctx:
            frc.poll_operation("op-1", sleep=self._no_sleep)
        self.assertEqual(ctx.exception.error_code, "Bad")
        self.assertEqual(ctx.exception.operation_id, "op-1")

    def test_unknown_state_raises(self):
        frc._run = FakeRunner([
            _completed(stdout='{"status": "Weird"}', stderr="Response status: 200"),
        ])
        with self.assertRaises(frc.FabricRestError):
            frc.poll_operation("op-1", sleep=self._no_sleep)

    def test_missing_operation_id_raises(self):
        with self.assertRaises(frc.FabricRestError):
            frc.poll_operation("", sleep=self._no_sleep)

    def test_deadline_timeout_preserves_operation_id(self):
        clock = {"t": 0.0}

        def fake_now():
            return clock["t"]

        def advancing_sleep(_seconds):
            clock["t"] += 5

        frc._run = FakeRunner([
            _completed(stdout='{"status": "Running"}', stderr="Response status: 200")
            for _ in range(10)
        ])
        with self.assertRaises(frc.FabricRestError) as ctx:
            frc.poll_operation(
                "op-1",
                deadline_s=3,
                sleep=advancing_sleep,
                now=fake_now,
            )
        self.assertEqual(ctx.exception.operation_id, "op-1")


class SendDefinitionRequestTests(unittest.TestCase):
    def tearDown(self):
        frc._run = frc._run_subprocess

    def test_sync_200_returns_body(self):
        frc._run = FakeRunner([
            _completed(
                stdout='{"definition": {"parts": [1]}}',
                stderr="Response status: 200",
            ),
        ])
        result = frc.send_definition_request("post", f"{frc.FABRIC_BASE}/x/getDefinition")
        self.assertEqual(result, {"definition": {"parts": [1]}})

    def test_async_202_polls_result(self):
        frc._run = FakeRunner([
            _completed(
                stdout="",
                stderr="Response status: 202\n'x-ms-operation-id': 'op-9'",
            ),
            _completed(stdout='{"status": "Succeeded"}', stderr="Response status: 200"),
            _completed(
                stdout='{"definition": {"parts": [2]}}',
                stderr="Response status: 200",
            ),
        ])
        result = frc.send_definition_request(
            "post",
            f"{frc.FABRIC_BASE}/x/getDefinition",
            get_result=True,
            sleep=lambda _s: None,
        )
        self.assertEqual(result, {"definition": {"parts": [2]}})


if __name__ == "__main__":
    unittest.main()
