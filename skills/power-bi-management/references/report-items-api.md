# Fabric Report Items REST API (reference)

Raw endpoint detail behind the `power-bi-management` skill. The skill drives
these through the tested helper in `scripts/power_bi_management.py`; author code
against the CLI, not against these endpoints directly. This file exists so an
agent can verify behavior, not to encourage hand-rolled `az rest` calls.

> **Attribution.** Endpoint semantics adapted from
> [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
> (`powerbi-report-management`, MIT) and the official
> [Fabric REST API](https://learn.microsoft.com/rest/api/fabric/report/items).

## Audience

Every call targets the Fabric audience `https://api.fabric.microsoft.com`. A
wrong or missing audience returns `401`. The helper always passes
`--resource "https://api.fabric.microsoft.com"`.

## Operations

| Operation | HTTP | Endpoint | LRO |
|---|---|---|---|
| List reports | GET | `/v1/workspaces/{workspaceId}/reports` | no |
| Get report | GET | `/v1/workspaces/{workspaceId}/reports/{reportId}` | no |
| Get definition | POST | `/v1/workspaces/{workspaceId}/reports/{reportId}/getDefinition?format=PBIR` | maybe |
| Create report | POST | `/v1/workspaces/{workspaceId}/reports` | maybe |
| Update definition | POST | `/v1/workspaces/{workspaceId}/reports/{reportId}/updateDefinition` | maybe |
| Update properties | PATCH | `/v1/workspaces/{workspaceId}/reports/{reportId}` | no |
| Delete (soft) | DELETE | `/v1/workspaces/{workspaceId}/reports/{reportId}` | no |

- **`?format=PBIR` is mandatory on `getDefinition`.** Without it, older reports
  return PBIR-Legacy (a single `report.json` blob) which this skill does not
  support. The helper stops if `definition.format == "PBIR-Legacy"`.
- **`updateDefinition` replaces the entire definition.** All parts must be sent;
  omitting a part deletes it. The helper always uploads the full allowlisted set.
- **Hard delete is intentionally not exposed** in this release. Soft delete is
  recoverable; permanent deletion will return later behind an explicit flag plus
  exact report-ID confirmation.

## Long-running operations

`create`, `getDefinition`, and `updateDefinition` may answer `202 Accepted`
with an empty body. The LRO contract adds three headers:

- `x-ms-operation-id` — the operation id to poll.
- `Location` — the status/result URL.
- `Retry-After` — seconds to wait before the next poll.

Poll `GET /v1/operations/{operationId}` until `status` is terminal
(`Succeeded`, `Failed`, or cancelled), honoring `Retry-After` and a deadline,
then fetch `GET /v1/operations/{operationId}/result` for operations that produce
a result. The helper implements this in `fabric_rest_client.poll_operation`.

> **Never retry a create POST after a `202`.** The operation is already running
> server-side; retrying risks duplicate reports. If the operation id is lost,
> list reports to find the created item rather than re-posting.

Reference: [Fabric Long-Running Operations](https://learn.microsoft.com/rest/api/fabric/articles/long-running-operation).

## PBIR definition parts

A report definition is a set of base64-encoded parts with
`"payloadType": "InlineBase64"`. Only these public parts are transported:

```text
definition.pbir                      # required — semantic model reference
definition/**                        # required — report.json, version.json, pages, bookmarks
StaticResources/**                   # optional — themes, images
semanticModelDiagramLayout.json      # optional — model diagram
```

Local files that are **never** uploaded: `.pbi/**` (local cache),
`.platform` (Git-integration system file), `.pbip`, dotfiles, and temporary
files. The helper enforces this allowlist in
`report_definition_io.collect_parts`.

### definition.pbir binding

For the API the reference must be `byConnection` (version 2 form):

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byConnection": { "connectionString": "semanticmodelid=<SemanticModelId>" }
  }
}
```

`byPath` is for local/Git scenarios and is rejected by the API. On publish the
helper rewrites `byPath` to `byConnection` **only in a temporary staging copy**,
so the source project keeps its `byPath` reference for local Desktop editing.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Wrong/missing `--resource` audience | Pass `--resource https://api.fabric.microsoft.com` (helper does this) |
| `403 Forbidden` | Insufficient permission | Need Contributor+ workspace role for writes |
| `404 Not Found` | Wrong workspace/report id | Re-resolve by name |
| `CorruptedPayload` | Bad base64 / invalid PBIR | Validate JSON via authoring skill before publishing |
| `202` with no result | LRO not polled | Helper polls automatically; if manual, poll the operation id |
| `OperationNotSupportedForItem` | Encrypted sensitivity label | Cannot get definition for encrypted reports |
| `ItemDisplayNameAlreadyInUse` | Duplicate name in workspace | Use a unique display name |
| `format: "PBIR-Legacy"` | Pre-PBIR report | Not supported |
| Visuals empty after publish | PBIR entity names ≠ model table names | Diff model TMDL; remap refs via authoring skill |
| Duplicate reports after create | Create POST retried after `202` | Never retry after `202`; delete duplicates |
