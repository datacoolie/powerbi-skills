# Fabric CLI Common Patterns (az rest)

Shared recipes used by `management.md`, `management-part-02.md`,
`management-part-04.md`, and the planning mode. Everything here is CLI-first:
`az rest` + JMESPath. Use it directly or through the tested helper
`scripts/power_bi_management.py`, which implements the same patterns.

## Telemetry header — MANDATORY

Every `api.fabric.microsoft.com` call (including every LRO poll, `fabric_lro`
call, and retry) carries:

```text
x-ms-fabric-skill: powerbi-report-cli
```

`az rest`: `--headers "x-ms-fabric-skill=powerbi-report-cli"`. The helper adds it
automatically (opt out only with `POWERBI_SKILLS_TELEMETRY=off`). Snippets in
the reference files omit it for brevity — add it anyway.

## Authentication Recipes

All Fabric calls use the audience `https://api.fabric.microsoft.com`
(`--resource`). Wrong or missing audience returns `401`.

| Context | Command |
|---|---|
| Interactive | `az login` |
| Device code (headless shell) | `az login --use-device-code` |
| Service principal + secret | `az login --service-principal -u <appId> --password <secret> --tenant <tenantId>` |
| Service principal + certificate | `az login --service-principal -u <appId> --certificate <path/to/cert.pem> --tenant <tenantId>` |
| Managed identity (Azure host) | `az login --identity` |
| Workload / federated (CI) | `az login --service-principal -u <appId> --federated-token <token> --tenant <tenantId>` |

Verify the session and token audience:

```bash
az account show --query "{user:user.name, tenant:tenantId}" -o json
az account get-access-token --resource https://api.fabric.microsoft.com --query expiresOn -o tsv
```

Never put literal secrets in scripts or shell history; use a secure prompt or a
CI secret store.

## Finding Workspaces and Items in Fabric

Resolve IDs by listing and filtering — never guess identifiers.

```bash
# Workspace ID from workspace name
WS_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --headers "x-ms-fabric-skill=powerbi-report-cli" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='Sales Analytics'] | [0].id" -o tsv)

# Item ID from workspace ID + item type + item name
MODEL_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --headers "x-ms-fabric-skill=powerbi-report-cli" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/semanticModels" \
  --query "value[?displayName=='Sales Model'] | [0].id" -o tsv)
```

Type-specific collections: `/reports`, `/semanticModels`, `/lakehouses`,
`/warehouses`; generic `/items?type=<ItemType>` also works.

Rules:

- Zero matches → stop and report; more than one match → ask which one. Never
  pick the first of several.
- Pagination: if the response has `continuationToken`, repeat the call with
  `?continuationToken=<token>` until it is absent (the helper does this).
- A workspace/report name in the user's request is a lookup key, not proof the
  item exists. Resolve it before any write.

## Long-Running Operations (LRO) Pattern

`202 Accepted` means a long-running operation. The response carries
`x-ms-operation-id`, `Location`, and `Retry-After`.

1. Use `--verbose` and write output to a file to capture `x-ms-operation-id`
   (`az rest` hides response headers otherwise).
2. Poll `GET /v1/operations/{operationId}` every `Retry-After` seconds (default
   5) until `status` is `Succeeded`, `Failed`, or `Cancelled`; set a deadline.
3. On `Succeeded`, fetch `GET /v1/operations/{operationId}/result` for operations
   that produce a body (`getDefinition`).
4. Each poll/result call also carries the telemetry header.

```powershell
az rest --method get --resource "https://api.fabric.microsoft.com" `
  --headers "x-ms-fabric-skill=powerbi-report-cli" `
  --url "https://api.fabric.microsoft.com/v1/operations/$OP_ID"
```

Never retry a create `POST` after `202`; list the workspace reports to find what
was created instead.

## Fabric Control-Plane API via az rest

Generic pattern for any Fabric item (semantic models, lakehouses, …):

```bash
az rest --method <get|post|patch|delete> \
  --resource "https://api.fabric.microsoft.com" \
  --headers "x-ms-fabric-skill=<skill-name>" \
  --url "https://api.fabric.microsoft.com/v1/<path>" \
  [--body @body.json] [--verbose]
```

- Always pass `--resource` (wrong audience → `401`) and `--verbose` for operations that may return `202`.
- `<skill-name>` is `powerbi-report-cli` for report work and `semantic-model-authoring` for semantic-model work.
- Pagination: follow `continuationToken`. LRO: see the pattern above.
- Equivalent with the Fabric CLI: `fab api -X <method> <endpoint> -H "x-ms-fabric-skill=<skill-name>" [--show_headers]`.

**`az rest` vs `fab api` (evaluated).** Read calls through `fab api` work (verified: it returns a
`{status_code, headers, text}` envelope with `--show_headers`; `-q` takes JMESPath over `text`).
The management helper and the official `management` mode stay on `az rest`: that path is the official
contract, its `--verbose` header capture for `202` LROs is tested, and the `fab api` 202/LRO header
behavior has not been verified against a real long-running operation. Use `fab api` for ad-hoc reads and
OneLake/lakehouse discovery; use `az rest` (or the helper) for report create/update/getDefinition.
