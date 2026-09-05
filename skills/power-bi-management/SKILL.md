---
name: power-bi-management
description: >-
  Manage and deploy Power BI report items in Microsoft Fabric workspaces via a
  tested Fabric REST helper (`az rest`). Use this skill for CLOUD TRANSPORT and
  lifecycle operations — NOT for authoring local content. Triggers:
  publish/upload/push/deploy a report to Fabric, download/get a report definition
  from Fabric, list workspace reports, update report properties, delete a report,
  publish a local `.pbip` to a workspace. For editing local PBIR content (pages,
  visuals, filters, themes, formatting) use `power-bi-report-authoring`. For
  building/deploying the semantic model use `power-bi-semantic-model`. This is the
  `az rest` Tier-2 lane: Power BI authoring stays MCP/local-first; only cloud
  transport (which has no MCP path) lives here.
---

# Power BI Management

Transport Power BI report items to and from Microsoft Fabric workspaces. This
skill owns the **cloud transport / lifecycle** concern only: list, create, get,
update, delete report items, and download/upload their PBIR definitions.

All operations run through a **tested Python helper** (standard library +
Azure CLI) so the risky parts — allowlisting uploads, immutable publish staging,
safe path extraction, and long-running-operation handling — are deterministic
and verifiable rather than copy-pasted shell.

> **Attribution.** Adapted from
> [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
> (`powerbi-report-management`, MIT), rewritten for this repo's MCP-first,
> local-PBIP conventions and made self-contained and testable.

## Routing — MCP first, this skill second

Power BI work in this repo is **MCP-first / local-PBIP**. Use this skill only
when **no exact Fabric MCP capability exists** for the requested operation:

1. If a Fabric MCP tool performs the exact operation (e.g. a native publish or
   item-CRUD capability), use it.
2. Otherwise use this skill's helper as the **`az rest` Tier-2 fallback**.
3. Never author PBIR content here — that is `power-bi-report-authoring`.
4. Never build or edit the semantic model here — that is `power-bi-semantic-model`.

> **Telemetry (off by default).** No telemetry header is sent. To opt in, pass
> `--headers "x-ms-fabric-skill=power-bi-management"` on your own `az rest`
> calls; it does not affect functionality.

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

This skill implements the **publish step of Phase 6 (Release)** in `AGENTS.md`,
and only after an exact Fabric MCP publish capability has been ruled out. Local
authoring (Phases 1–4c) produces a validated `.pbip`; this skill pushes it to a
workspace when the user explicitly asks to publish.

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

# Overwrite an existing report's definition (uploads ALL parts)
python $mgmt update-definition --workspace-name "Sales Analytics" `
  --report-name "Sales Report" --definition-dir ./report-definition

# Rename / re-describe
python $mgmt update-properties --workspace-name "Sales Analytics" `
  --report-name "Sales Report" --display-name "Sales Report (2026)"

# Soft delete (recoverable). Hard delete is not available in this release.
python $mgmt delete --workspace-name "Sales Analytics" --report-name "Old Report"

# Publish a local .pbip without mutating the source project
python $mgmt publish-pbip --workspace-name "Sales Analytics" `
  --report-dir "./Sales.Report" --semantic-model-name "Sales Model"
```

The helper handles auth audience, pagination, `202`/LRO polling with
`Retry-After` and a deadline, forward-slash part paths, base64, and cleanup.
Endpoint detail lives in [references/report-items-api.md](references/report-items-api.md).

## Publishing a local `.pbip` (workflow)

`publish-pbip` is the primary entry point when a user asks to publish/upload a
local `.pbip` (report + sibling `.SemanticModel`).

1. **Rule out an exact Fabric MCP publish capability first.** Use it if present.
2. **Confirm the target workspace once** (name → id, reused for model + report).
3. **Resolve the semantic model** (a concrete `semanticModelId` is mandatory):
   - **Branch A — publish local model:** hand off to `power-bi-semantic-model`
     (pass workspace + `.SemanticModel` path), then read back the model id.
   - **Branch B — connect existing:** pass `--semantic-model-name` and the helper
     resolves the id from the workspace (exact single match).
   - If neither yields an id, the helper stops — it never guesses a binding.
4. **Verify bindings** before publish: confirm PBIR `Entity`/`queryRef`/filter
   references match the target model's tables; on drift, remap via
   `power-bi-report-authoring` and re-validate.
5. **Immutable staging (automatic).** The helper copies only the allowlisted
   parts to a temp folder, rewrites `byPath` → `byConnection` there, and asserts
   the source digest is unchanged before and after. Your `.pbip` keeps `byPath`.
6. **Create vs update.** Default `displayName` to the `.Report` folder name; the
   helper creates when absent and updates when a single match exists.
7. **Verify render in a browser.** No reliable programmatic render check exists;
   surface the workspace/report URL for the user to confirm.

## Modifying an existing report in Fabric

1. Rule out an exact MCP capability → 2. `get-definition ... --out-dir` →
3. **author changes via `power-bi-report-authoring`** (validate with its CLI) →
4. `update-definition` (uploads all parts).

## Must / Prefer / Avoid

### MUST
- Route PBIR authoring to `power-bi-report-authoring`; model work to `power-bi-semantic-model`.
- Pass `?format=PBIR` on `getDefinition`; stop on `PBIR-Legacy`.
- Upload ALL parts on `updateDefinition` (missing parts are deleted).
- Keep local edits local by default — publish only when explicitly asked.
- Obtain a concrete `semanticModelId` before publishing.

### PREFER
- An exact Fabric MCP capability over this Tier-2 helper.
- Soft delete over hard delete (hard delete is not exposed in this release).
- Resolving by name (exact single match) or explicit id over hardcoded ids.
- Certificate / managed-identity auth over command-line secrets.

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
