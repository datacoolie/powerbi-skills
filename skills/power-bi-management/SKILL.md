---
name: power-bi-management
description: >-
  Manage and deploy Power BI report items in Microsoft Fabric workspaces via the
  CLI stack (`az rest` + `powerbi-report-author pack/unpack`) and a tested Python
  helper. Covers the `management` mode of Microsoft's `powerbi-report-cli` 1:1.
  Use this skill for CLOUD TRANSPORT and lifecycle operations — NOT for authoring
  local content. Triggers: publish/upload/push/deploy a report to Fabric,
  download/get a report definition from Fabric, list workspace reports, get/update/
  delete a report, rebind a report to a semantic model, publish a local `.pbip` to a
  workspace. For editing local PBIR content (pages, visuals, filters, themes,
  formatting) use `power-bi-report-authoring`. For building/deploying the semantic
  model use `power-bi-semantic-model`. CLI-first: Fabric MCP tools are only a
  fallback when no CLI path exists.
---

# Power BI Management

Transport Power BI report items to and from Microsoft Fabric workspaces. This
skill owns the **cloud transport / lifecycle** concern only: list, create, get,
update, delete report items, rebind, and download/upload their PBIR definitions.

> **Official source.** `references/management.md` (+ `-part-02/03/04`) is the
> official `management` mode of
> [microsoft/skills-for-fabric `powerbi-report-cli`](https://github.com/microsoft/skills-for-fabric)
> (MIT), verbatim apart from repo path fixes. It is the canonical procedure; the
> helper below implements the same flows and adds allowlisting, immutable staging,
> and safe extraction. On conflict, the official file wins.
> Mode → skill map: `authoring` → `power-bi-report-authoring`,
> `semantic-model-authoring` → `power-bi-semantic-model`.

## Telemetry — MANDATORY

Every `api.fabric.microsoft.com` call — including each LRO poll, `fabric_lro`
call and retry — carries `x-ms-fabric-skill: powerbi-report-cli`
(`az rest … --headers "x-ms-fabric-skill=powerbi-report-cli"`). Snippets omit it;
add it anyway. The helper sends it automatically on every request.

## Tool choice — CLI first, MCP only as fallback

| Operation | Use | Why |
|---|---|---|
| List/get/create/update/delete report items, getDefinition, updateDefinition | `az rest` (or `scripts/power_bi_management.py`) | CLI, deterministic, auditable, same in CI |
| PBIR payload ⇄ folder | `powerbi-report-author pack` / `unpack` (≥ 0.3.0) | replaces hand-rolled base64/path walking |
| Workspace/item ID resolution | `az rest` + JMESPath (`references/fabric-common-cli.md`) | never guess IDs |
| Publish local semantic model | hand off to `power-bi-semantic-model` | model transport is not report transport |
| Fabric MCP (`Fabric-MCP-*`) | **fallback only** when no CLI path covers the operation | CLI preferred when both fit |
| OneLake/lakehouse/item discovery beyond reports | `fab` (Microsoft Fabric CLI) before any Fabric MCP tool | CLI exists |

Rules of thumb: if the CLI and an MCP tool both can do it, use the CLI. Never
bypass `pack`/`unpack` with `jq`/`base64`/PowerShell directory walks.

## Permission rules — MUST

- **Local edits stay local.** Publish/upload/push/deploy only when the *current*
  request explicitly asks for it. Approval of design, edits, validation,
  screenshots, preview, or an earlier publish is **not** permission. If unsure,
  stay local, make no remote write, and do not ask to publish.
- **Never overwrite an existing remote report** without explicit confirmation
  that the user agrees to overwrite (before any `updateDefinition`).
- **Definition download invariant:** always
  `…/workspaces/$WS_ID/reports/$REPORT_ID/getDefinition?format=PBIR`; store the
  full URL once and reuse it, including for post-update verification.
- **PBIR only** — stop on `PBIR-Legacy`. Run the *Modern-PBIR preflight*
  (`management.md`: `definition/report.json` present + `powerbi-report-author
  validate` clean) before every `pack`.
- Resolve workspace and item IDs by listing + JMESPath filtering; keep one compact
  run-state (workspace/model/report names + IDs, local/download paths, definition
  URL, active LRO endpoint) across turns.

## Reference map

| File | Read when |
|---|---|
| `references/management.md` | Tool stack, preflight, auth, resolving IDs (entry point) |
| `references/management-part-02.md` | CRUD examples (list/get/getDefinition/create/update/delete), LRO guardrails, `definition.pbir` structure |
| `references/management-part-03.md` | Official Must/Prefer/Avoid, binding-verification rule, publish-permission rules |
| `references/management-part-04.md` | **Agentic workflows**: publish a local `.pbip`, modify an existing report, create a new report; troubleshooting |
| `references/fabric-common-cli.md` | Auth recipes, workspace/item lookup, LRO pattern, telemetry header |
| `references/report-items-api.md` | Endpoint table and behavior reference used by the helper |

## Scope & Boundaries

| This skill owns | This skill does NOT do |
|---|---|
| Report item CRUD in Fabric (list/create/get/update/delete) | Author PBIR content (pages, visuals, filters, themes) |
| Download/upload PBIR definitions (transport) | Build or edit the semantic model |
| Publish a local `.pbip` to a workspace | Validate/lint PBIR JSON |
| Resolve workspace/report IDs, poll LROs | Render/verify visuals |

**Companion skills:**

| Skill | Owns | Use for |
|---|---|---|
| `power-bi-report-authoring` | Local PBIR content (JSON authoring) | Pages, visuals, filters, themes, `definition.pbir`, validation |
| `power-bi-semantic-model` | Semantic model authoring + deploy | Measures/tables/relationships (MCP), TMDL, model deploy + `semanticModelId` |
| `power-bi-management` (this) | Cloud transport to/from Fabric | List/create/get/update/delete report items; up/download PBIR |

> **Boundary rule.** This skill transports PBIR definitions. **All PBIR content
> authoring stays in `power-bi-report-authoring`.** Never construct PBIR JSON
> from memory — not even `definition.pbir` or `version.json`.

## Where this fits the pipeline

This skill implements the **publish step of Phase 6 (Release)** in `AGENTS.md`.
Local authoring (Phases 1–4c) produces a validated `.pbip`; this skill pushes it
to a workspace only when the user explicitly asks to publish.

## Prerequisites

```bash
az version          # install: https://learn.microsoft.com/cli/azure/install-azure-cli
python --version    # 3.10+ ; standard library only, no pip installs
```

## Authentication

Every call targets the Fabric audience `https://api.fabric.microsoft.com`
(the helper passes `--resource` automatically). Choose the login that matches
the context:

| Context | Command |
|---|---|
| Interactive | `az login` |
| Service principal + secret | `az login --service-principal -u <appId> --password <secret> --tenant <tenantId>` |
| Service principal + certificate | `az login --service-principal -u <appId> --certificate <path/to/cert.pem> --tenant <tenantId>` |
| Managed identity (Azure host) | `az login --identity` |
| Workload / federated (CI) | `az login --service-principal -u <appId> --federated-token <token> --tenant <tenantId>` |

> **Certificate uses `--certificate`, never `--password`.** Do not put literal
> secrets in scripts or command history — use a secure prompt or a CI secret
> store. Certificate-based auth is preferred for automation.

## Running the helper

All commands live in `scripts/power_bi_management.py` and print JSON. Resolve by
name (exact single match required) or pass an explicit id. Windows examples;
the same commands work on macOS/Linux with `python3`.

```powershell
$mgmt = "skills/power-bi-management/scripts/power_bi_management.py"

# List reports
python $mgmt list --workspace-name "Sales Analytics"

# Get properties
python $mgmt get --workspace-name "Sales Analytics" --report-name "Sales Report"

# Download a definition (PBIR) to a local folder — safe extraction
python $mgmt get-definition --workspace-name "Sales Analytics" `
  --report-name "Sales Report" --out-dir ./report-definition

# Create from a local, already-authored & validated definition folder
python $mgmt create --workspace-name "Sales Analytics" `
  --definition-dir ./report-definition --display-name "Sales Report"

# Overwrite an existing report's definition (uploads ALL parts).
# --confirm-overwrite is REQUIRED and may only be passed after the user explicitly agreed to overwrite.
python $mgmt update-definition --workspace-name "Sales Analytics" `
  --report-name "Sales Report" --definition-dir ./report-definition --confirm-overwrite

# Rename / re-describe
python $mgmt update-properties --workspace-name "Sales Analytics" `
  --report-name "Sales Report" --display-name "Sales Report (2026)"

# Soft delete (recoverable). Hard delete is not available in this release.
python $mgmt delete --workspace-name "Sales Analytics" --report-name "Old Report"

# Publish a local .pbip without mutating the source project
# (add --confirm-overwrite only if a same-named report exists AND the user agreed to overwrite it)
python $mgmt publish-pbip --workspace-name "Sales Analytics" `
  --report-dir "./Sales.Report" --semantic-model-name "Sales Model"
```

The helper handles auth audience, pagination, `202`/LRO polling with
`Retry-After` and a deadline, forward-slash part paths, base64, cleanup, and the
overwrite guard (no `updateDefinition` without `--confirm-overwrite`). Its upload
payload is verified part-for-part against `powerbi-report-author pack --raw`
(only difference: the helper never uploads `.platform`).
Endpoint detail lives in [references/report-items-api.md](references/report-items-api.md).

## Publishing a local `.pbip` (workflow)

`publish-pbip` is the primary entry point when a user asks to publish/upload a
local `.pbip` (report + sibling `.SemanticModel`).

1. **Check the permission rules above** — an explicit publish request in the
   current turn is required; run `powerbi-report-author validate` (modern-PBIR
   preflight) first.
2. **Confirm the target workspace once** (name → id, reused for model + report).
   Resolve it *before* asking the model question; missing/ambiguous → stop.
3. **Ask the user** whether to publish the local semantic model too or connect to
   an existing workspace model — never choose silently — then resolve the
   semantic model (a concrete `semanticModelId` is mandatory):
   - **Branch A — publish local model:** hand off to `power-bi-semantic-model`
     (pass workspace + `.SemanticModel` path), then read back the model id. If
     that skill is unavailable, say so and degrade to Branch B.
   - **Branch B — connect existing:** pass `--semantic-model-name` and the helper
     resolves the id from the workspace (exact single match).
   - If neither yields an id, the helper stops — it never guesses a binding.
4. **Verify bindings** (both branches): download the deployed model TMDL once, build
   one table/column/measure inventory, and diff all PBIR `Entity`/`queryRef`/
   `nativeQueryRef`/filter references against it. Same structure, different names →
   remap via `power-bi-report-authoring`; structurally different → ask the user
   before re-authoring. Use live-model inspection only if TMDL retrieval fails.
5. **Immutable staging (automatic).** The helper copies only the allowlisted
   parts to a temp folder, rewrites `byPath` → `byConnection` there, and asserts
   the source digest is unchanged before and after. Your `.pbip` keeps `byPath`.
6. **Create vs update.** Default `displayName` to the `.Report` folder name and
   surface it. Creating when absent is fine; if a report with that name exists,
   **get explicit overwrite confirmation before `update-definition`**.
7. **Verify render in a browser.** No reliable programmatic render check exists;
   surface the workspace/report URL for the user to confirm.

## Modifying an existing report in Fabric

1. `get-definition ... --out-dir <fresh-or-emptied dir>` (never reuse a dir that holds a
   previous download) → 2. **author changes via `power-bi-report-authoring`**
   (validate with its CLI) → 3. confirm overwrite → 4. `update-definition`
   (uploads all parts) → 5. clean up temp files.

**Rebinding a report** to another semantic model = set `definition.pbir`
`datasetReference.byConnection.connectionString` to `semanticmodelid=<id>` (see
`../power-bi-report-authoring/references/authoring/model-binding.md`), re-verify
bindings against the target model TMDL, then follow the same modify flow
(download → edit → confirm overwrite → `update-definition`).

## Must / Prefer / Avoid

### MUST
- Route PBIR authoring to `power-bi-report-authoring`; model work to `power-bi-semantic-model`.
- Pass `?format=PBIR` on `getDefinition`; stop on `PBIR-Legacy`.
- Upload ALL parts on `updateDefinition` (missing parts are deleted).
- Keep local edits local by default — publish only when explicitly asked; confirm overwrite.
- Obtain a concrete `semanticModelId` before publishing; convert `byPath` → `byConnection` before `pack`.
- Send the telemetry header on every Fabric call.

### PREFER
- CLI (`az rest`, `pack`/`unpack`, helper) over any Fabric MCP tool.
- Soft delete over hard delete (hard delete is not exposed by the helper in this release).
- Resolving by name (exact single match) or explicit id over hardcoded ids.
- Certificate / managed-identity auth over command-line secrets.
- File-based hand-off (`az rest --output-file`, `pack --raw --out`) over shell pipes.

### AVOID
- Hand-writing PBIR JSON (route to authoring).
- Mutating the source `.pbip` binding on publish (staging handles it).
- Uploading `.pbi/**`, `.platform`, `.pbip`, or dotfiles (the allowlist blocks them).
- Retrying a create POST after `202` (risks duplicate reports).

## Tests

Offline, no Fabric tenant required:

```powershell
python -m unittest discover -s skills/power-bi-management/scripts/tests -p "test_*.py" -v
```

An opt-in live lifecycle test (`test_sandbox_smoke.py`) runs create → download →
update → soft-delete against a throwaway workspace only when
`FABRIC_SANDBOX_SMOKE=1` and `FABRIC_WORKSPACE_ID` are set.

## Troubleshooting

See [references/report-items-api.md](references/report-items-api.md#troubleshooting)
for the full error table (401/403/404, `CorruptedPayload`, PBIR-Legacy, empty
visuals after publish, duplicate reports after `202`).
