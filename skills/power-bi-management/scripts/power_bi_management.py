"""Command-line interface for Power BI report management on Microsoft Fabric.

Tier-2 fallback lane: use only when no exact Fabric MCP capability exists. All
PBIR content authoring stays in ``power-bi-report-authoring``; this CLI only
transports report items to and from a Fabric workspace.

Commands
--------
list                 List reports in a workspace.
get                  Get report properties.
get-definition       Download a report's PBIR definition to a local folder.
create               Create a report from a local definition folder.
update-definition    Overwrite an existing report's definition.
update-properties    Rename or re-describe a report.
delete               Soft-delete a report (recoverable). Hard delete is not
                     available in this release by design.
publish-pbip         Publish a local .pbip report to a workspace without
                     mutating the source project.

Every command resolves ids from names by exact single match, honours
long-running operations, and returns JSON on stdout.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

import fabric_rest_client as frc  # noqa: E402
import report_definition_io as rio  # noqa: E402


def _workspace_id(args: argparse.Namespace) -> str:
    if getattr(args, "workspace_id", None):
        return args.workspace_id
    return frc.resolve_workspace_id(args.workspace_name)


def _report_id(args: argparse.Namespace, workspace_id: str) -> str:
    if getattr(args, "report_id", None):
        return args.report_id
    return frc.resolve_report_id(workspace_id, args.report_name)


def _emit(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_list(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    reports = frc.paginate(f"{frc.FABRIC_BASE}/workspaces/{ws}/reports")
    _emit([
        {"id": r.get("id"), "displayName": r.get("displayName"), "description": r.get("description")}
        for r in reports
    ])
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    report = _report_id(args, ws)
    resp = frc.az_rest("get", f"{frc.FABRIC_BASE}/workspaces/{ws}/reports/{report}")
    frc._require_success(resp, "get report")
    _emit(resp.body)
    return 0


def cmd_get_definition(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    report = _report_id(args, ws)
    url = (
        f"{frc.FABRIC_BASE}/workspaces/{ws}/reports/{report}"
        "/getDefinition?format=PBIR"
    )
    definition = frc.send_definition_request("post", url, get_result=True)
    fmt = (definition or {}).get("definition", {}).get("format")
    if fmt == "PBIR-Legacy":
        raise SystemExit("Report is stored as PBIR-Legacy, which is not supported.")
    written = rio.safe_extract(definition, args.out_dir)
    _emit({"outDir": str(Path(args.out_dir).resolve()), "parts": written})
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    payload = rio.build_upload_payload(args.definition_dir)
    body = {"displayName": args.display_name, "definition": payload["definition"]}
    if args.description:
        body["description"] = args.description
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
        json.dump(body, fh)
        body_file = fh.name
    try:
        result = frc.send_definition_request(
            "post",
            f"{frc.FABRIC_BASE}/workspaces/{ws}/reports",
            body_file=body_file,
            extra_headers={"Content-Type": "application/json"},
        )
    finally:
        Path(body_file).unlink(missing_ok=True)
    _emit(result)
    return 0


def cmd_update_definition(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    report = _report_id(args, ws)
    payload = rio.build_upload_payload(args.definition_dir)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
        json.dump({"definition": payload["definition"]}, fh)
        body_file = fh.name
    try:
        frc.send_definition_request(
            "post",
            f"{frc.FABRIC_BASE}/workspaces/{ws}/reports/{report}/updateDefinition",
            body_file=body_file,
            extra_headers={"Content-Type": "application/json"},
        )
    finally:
        Path(body_file).unlink(missing_ok=True)
    _emit({"updated": report, "workspace": ws})
    return 0


def cmd_update_properties(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    report = _report_id(args, ws)
    body: dict[str, str] = {}
    if args.display_name:
        body["displayName"] = args.display_name
    if args.description is not None:
        body["description"] = args.description
    if not body:
        raise SystemExit("Provide --display-name and/or --description to update.")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
        json.dump(body, fh)
        body_file = fh.name
    try:
        resp = frc.az_rest(
            "patch",
            f"{frc.FABRIC_BASE}/workspaces/{ws}/reports/{report}",
            body_file=body_file,
            extra_headers={"Content-Type": "application/json"},
        )
        frc._require_success(resp, "update report properties")
    finally:
        Path(body_file).unlink(missing_ok=True)
    _emit({"updated": report, "properties": body})
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    report = _report_id(args, ws)
    # Soft delete only. Hard delete is intentionally excluded from this release.
    resp = frc.az_rest("delete", f"{frc.FABRIC_BASE}/workspaces/{ws}/reports/{report}")
    frc._require_success(resp, "delete report")
    _emit({"softDeleted": report, "workspace": ws})
    return 0


def cmd_publish_pbip(args: argparse.Namespace) -> int:
    ws = _workspace_id(args)
    report_dir = Path(args.report_dir).resolve()
    model_id = _resolve_model_id(args, ws)

    before = rio.content_digest(report_dir)
    staging = rio.stage_publish_copy(report_dir, model_id)
    try:
        after = rio.content_digest(report_dir)
        if before != after:
            raise SystemExit("Aborting: source project changed during staging.")
        payload = rio.build_upload_payload(staging)
        display_name = args.display_name or report_dir.stem.replace(".Report", "")
        existing = _find_report(ws, display_name)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            if existing:
                json.dump({"definition": payload["definition"]}, fh)
                url = f"{frc.FABRIC_BASE}/workspaces/{ws}/reports/{existing}/updateDefinition"
            else:
                json.dump(
                    {"displayName": display_name, "definition": payload["definition"]}, fh
                )
                url = f"{frc.FABRIC_BASE}/workspaces/{ws}/reports"
            body_file = fh.name
        try:
            result = frc.send_definition_request(
                "post",
                url,
                body_file=body_file,
                extra_headers={"Content-Type": "application/json"},
            )
        finally:
            Path(body_file).unlink(missing_ok=True)
    finally:
        rio.cleanup(staging)
    _emit({
        "workspace": ws,
        "report": display_name,
        "mode": "updated" if existing else "created",
        "result": result,
    })
    return 0


def _resolve_model_id(args: argparse.Namespace, workspace_id: str) -> str:
    if getattr(args, "semantic_model_id", None):
        return args.semantic_model_id
    if getattr(args, "semantic_model_name", None):
        models = frc.paginate(
            f"{frc.FABRIC_BASE}/workspaces/{workspace_id}/semanticModels"
        )
        return frc._resolve_unique(models, args.semantic_model_name, "semantic model")
    raise SystemExit(
        "publish-pbip needs --semantic-model-id or --semantic-model-name. "
        "Resolve or deploy the model first (power-bi-semantic-model)."
    )


def _find_report(workspace_id: str, display_name: str) -> Optional[str]:
    reports = frc.paginate(f"{frc.FABRIC_BASE}/workspaces/{workspace_id}/reports")
    matches = [r["id"] for r in reports if r.get("displayName") == display_name and r.get("id")]
    if len(matches) > 1:
        raise SystemExit(
            f"{len(matches)} reports named {display_name!r} exist; resolve manually."
        )
    return matches[0] if matches else None


def _add_workspace_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--workspace-id")
    group.add_argument("--workspace-name")


def _add_report_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--report-id")
    group.add_argument("--report-name")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="power_bi_management",
        description="Transport Power BI reports to/from a Fabric workspace (Tier-2).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List reports in a workspace")
    _add_workspace_args(p_list)
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Get report properties")
    _add_workspace_args(p_get)
    _add_report_args(p_get)
    p_get.set_defaults(func=cmd_get)

    p_getdef = sub.add_parser("get-definition", help="Download a report definition")
    _add_workspace_args(p_getdef)
    _add_report_args(p_getdef)
    p_getdef.add_argument("--out-dir", required=True)
    p_getdef.set_defaults(func=cmd_get_definition)

    p_create = sub.add_parser("create", help="Create a report from a definition folder")
    _add_workspace_args(p_create)
    p_create.add_argument("--definition-dir", required=True)
    p_create.add_argument("--display-name", required=True)
    p_create.add_argument("--description")
    p_create.set_defaults(func=cmd_create)

    p_upd = sub.add_parser("update-definition", help="Overwrite a report definition")
    _add_workspace_args(p_upd)
    _add_report_args(p_upd)
    p_upd.add_argument("--definition-dir", required=True)
    p_upd.set_defaults(func=cmd_update_definition)

    p_props = sub.add_parser("update-properties", help="Rename/re-describe a report")
    _add_workspace_args(p_props)
    _add_report_args(p_props)
    p_props.add_argument("--display-name")
    p_props.add_argument("--description")
    p_props.set_defaults(func=cmd_update_properties)

    p_del = sub.add_parser("delete", help="Soft-delete a report (recoverable)")
    _add_workspace_args(p_del)
    _add_report_args(p_del)
    p_del.set_defaults(func=cmd_delete)

    p_pub = sub.add_parser("publish-pbip", help="Publish a local .pbip report")
    _add_workspace_args(p_pub)
    p_pub.add_argument("--report-dir", required=True)
    p_pub.add_argument("--display-name")
    model = p_pub.add_mutually_exclusive_group()
    model.add_argument("--semantic-model-id")
    model.add_argument("--semantic-model-name")
    p_pub.set_defaults(func=cmd_publish_pbip)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except frc.FabricRestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except rio.DefinitionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
