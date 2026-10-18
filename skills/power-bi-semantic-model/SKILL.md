---
name: power-bi-semantic-model
description: >-
  Design and build Power BI semantic models using star schema principles and the PowerBI
  Modeling MCP tools. Use this skill whenever the user wants to build a semantic model,
  create a data model, design a star schema, add tables or columns, create or modify
  relationships, configure storage modes (Import, DirectQuery, DirectLake, Composite),
  implement RLS (Row-Level Security), optimize model performance, or explore existing
  data sources for modeling. Triggers include: "build semantic model", "create data model",
  "star schema", "add table", "create relationship", "storage mode", "DirectLake",
  "composite model", "RLS", "optimize model", "model review", "explore data",
  "connect to gold layer", "extend model", "add dimension", "add fact table".
  Do NOT use for DAX measure creation (use power-bi-dax-development) or
  report generation (use power-bi-report-authoring).
---

# Power BI Semantic Model Builder

Design and build Power BI semantic models following star schema best practices.
Live model authoring and DAX validation use PowerBI Modeling MCP tools (no CLI
equivalent exists); Fabric item transport uses `az rest` (see Tool Selection below).

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
the latest modeling guidance before making design decisions.

**Use PowerBI Modeling MCP** (`powerbi-modeling-mcp/*` — your host may register the same tool set as
`powerbi-authoring-local`) for live model operations —
exploring tables, creating relationships, configuring columns, testing queries.
Read `references/mcp-tool-reference.md` for the complete tool mapping. Run `python scripts/doctor.py`
at the repo root to check the surrounding CLIs.

## Quick Reference

> **Official workflows.** `references/official-workflows.md` is the verbatim body of Microsoft's
> `semantic-model-authoring` skill (create model, discover metadata, modify, field parameters, DAX perf,
> best-practice analysis, AI readiness, export to PBIP, deploy, refresh, manage in Fabric — data sources,
> permissions, connection binding — plus DENY rules, validation checklist, troubleshooting). Read the matching
> workflow there before acting; the official topic files `modeling-guidelines.md`, `tmdl-guidelines.md`,
> `metadata-discovery.md`, `field-parameters.md`, `direct-lake-guidelines.md` are in `references/`.
> **Telemetry:** semantic-model calls to `api.fabric.microsoft.com` carry
> `x-ms-fabric-skill: semantic-model-authoring` (the report helper uses `powerbi-report-cli`).
> Publishing a PBIP (report + model) belongs to `power-bi-management`.
> For natural-language questions about the data, use `fabriciq` if available.

**Workflow router** (official workflow = section of `references/official-workflows.md`; repo step = section below in this file):

| User wants to… | Do |
|---|---|
| Create a model from scratch / design a star schema | Repo Steps 1–4 (star schema, storage mode, relationships) + official *Create new Semantic Model* |
| Inspect model metadata | Official *Discover Semantic Model Metadata* (`metadata-discovery.md`, DAX INFO functions) + `references/discovery-queries.md` |
| Add/edit tables, columns, measures, relationships; write/refactor DAX | Official *Modify an Existing Model* (+ `modeling-guidelines.md`, `tmdl-guidelines.md`, `dax-guidelines.md`); measures → `power-bi-dax-development` |
| Field parameter | Official *Author a Field Parameter* (`field-parameters.md`) |
| DAX/measure performance | Official *Optimize DAX Performance* (`dax-perf-decision-guide.md` → `dax-perf-patterns.md`); report-level → `power-bi-performance-troubleshooting` |
| Best-practice review | Official *Analyze Best Practices* + repo Step 7 (validate) |
| Copilot / Data Agent readiness | Repo Step 8 + official *Semantic Model AI Readiness* (`semantic-model-ai-readiness.md`) |
| RLS / OLS | Repo Step 6 + `references/rls-patterns.md` |
| Export to PBIP / deploy / refresh / data sources / permissions / connection binding | Official *Export to PBIP*, *Deploy to Fabric*, *Refresh*, *Manage in Fabric*, *Bind to a Connection* (CLI: `az rest`; add the `semantic-model-authoring` telemetry header) |
| Publish a PBIP report + model together | `power-bi-management` (publish-pbip flow) |

**Precedence:** official workflow steps and MUST/AVOID/DENY rules win over repo prose on conflict; the repo's CLI-first Tool Selection Priority below is consistent with the official one (MCP when connected to the target model, otherwise TMDL + `az rest`).

| Task | Approach | Reference |
|---|---|---|
| Explore existing model | `model_operations` → get model info, `table_operations` → list tables | — |
| Discover model metadata | INFO.VIEW.* queries for tables, columns, measures, relationships | `references/discovery-queries.md` |
| Connect to gold layer | `connection_operations` → configure data source | `references/connection-binding.md` |
| Design star schema | Run Star Schema Checklist | `references/star-schema-checklist.md` |
| Naming conventions | Tables, columns, measures, hierarchies naming rules | `references/naming-conventions.md` |
| Choose storage mode | Use Decision Matrix | `references/storage-mode-decision.md` |
| Direct Lake guide | Framing, guardrails, fallback, composite | `references/directlake-guide.md` |
| Build relationships | `relationship_operations` → create with proper cardinality | `references/advanced-relationships.md` |
| Optimize columns | `column_operations` → set data types, remove unused, hide keys | `references/vertipaq-optimization.md` |
| DAX coding standards | Variables, comments, query syntax, best practices | `references/dax-guidelines.md` |
| DAX performance | Optimization framework (21 patterns, tier 1–4) | `references/dax-perf-decision-guide.md` + `references/dax-perf-patterns.md` |
| Power Query / ETL | M language, query folding, transformations | `references/power-query-reference.md` |
| Implement RLS | Dynamic RLS, OLS, DirectLake RLS patterns | `references/rls-patterns.md` |
| TMDL / PBIP structure | Tables, columns, measures, relationships, roles | `references/tmdl-reference.md` + `references/pbip.md` |
| Deploy to workspace | Git integration, CI/CD, Fabric pipelines | `references/deployment-alm-guide.md` |
| Gateway & refresh | On-prem gateway, scheduled/incremental refresh | `references/gateway-refresh-guide.md` |
| Fabric REST API | TMDL CRUD, refresh, data sources, permissions | `references/semantic-model-rest-api.md` |
| Prepare for AI/Copilot | Descriptions, synonyms, AI instructions, verified answers | `references/semantic-model-ai-readiness.md` |
| Test the model | `dax_query_operations` → run EVALUATE queries | `references/discovery-queries.md` |
| Official workflows (create/modify/deploy/refresh/permissions/…) | Follow the matching workflow | `references/official-workflows.md` |
| Official modeling & TMDL guidelines | Read before structural edits | `references/modeling-guidelines.md` + `references/tmdl-guidelines.md` |
| Official metadata discovery, field parameters, Direct Lake | Read for the matching task | `references/metadata-discovery.md`, `references/field-parameters.md`, `references/direct-lake-guidelines.md` |

## Tool Selection Priority (CLI-first, MCP where no CLI exists)

Repo-wide rule: **if a first-party CLI and an MCP tool can both do an operation, use the CLI.**
Assessment for this skill's operations:

| Operation | Tool | Why |
|---|---|---|
| Deploy/refresh/get/update a semantic model **item** in Fabric; resolve workspace/model IDs | `az rest` (Fabric REST — `references/semantic-model-rest-api.md`) | CLI exists → CLI wins over `Fabric-MCP-*` |
| Load changed TMDL into a Desktop preview | `powerbi-report-author preview --reload-with-model` (see `power-bi-report-authoring`) | CLI exists |
| Read-only inventory (tables/columns/measures) from local `.SemanticModel/` TMDL or a downloaded definition | Read the TMDL files directly | Cheapest, no connection; do not also connect MCP when the TMDL is complete and parseable |
| **Live** model authoring (tables, columns, relationships, measures, RLS, calendars, partitions) and **DAX execution/validation** | PowerBI Modeling MCP (`powerbi-modeling-mcp/*`) | No first-party CLI exposes transactions, model mutation, or `EVALUATE` — MCP is the only option, not a tie |
| Same writes while MCP is unavailable | Edit TMDL files, then deploy with `az rest` (`references/tmdl-reference.md`) | Deterministic file path |
| Microsoft Learn docs lookup | `microsoft-learn-mcp` | No CLI equivalent |
| Lakehouse/table inspection for source discovery | `fab` (`fab find`, `fab dir`, `fab get`, `fab table schema`) | CLI exists → CLI wins (row preview / column stats have no `fab` equivalent → MCP) |
| Same, when `fab` is not installed | `fabric-notebook-mcp` | MCP fallback |

**Tier 1 — MCP (powerbi-modeling-mcp)** for live authoring/DAX when connected to the target model.
**Tier 2 — TMDL files + `az rest`** when MCP is unavailable, or for read-only inventory.
**Tier 3 — Fallback**: if neither MCP nor TMDL access is available, guide the user
to save as PBIP or install MCP.

## Must / Prefer / Avoid

### MUST
- Understand data source schema before designing the model
- Follow star schema principles (`references/star-schema-checklist.md`)
- Follow naming conventions (`references/naming-conventions.md`)
- Follow tool selection priority (CLI where one exists → MCP for live model ops → TMDL files)
- Validate model with DAX queries after structural changes

### PREFER
- Star schema over flat/denormalized tables
- Explicit measures over implicit aggregation
- TMDL format for version-controlled model definitions
- INT keys over TEXT keys for relationships

### AVOID
- Hardcoded workspace/item IDs — resolve dynamically
- Opening a live MCP connection just to read names that a complete local/downloaded TMDL already provides
- Calculated columns on fact tables (use measures or Power Query)
- Auto Date/Time (use dedicated date dimension)

## Workflow

### Step 1: Explore Available Data

Before designing, understand what exists:

```
Exploration Checklist:
□ Use powerbi-modeling-mcp/model_operations to get current model state
□ Use powerbi-modeling-mcp/table_operations to list all tables and columns
□ Use powerbi-modeling-mcp/relationship_operations to see existing relationships
□ Identify which tables are facts (transactions, events) vs. dimensions (descriptive)
□ Check column data types and cardinality
□ Note any existing measures (powerbi-modeling-mcp/measure_operations)
□ Check connection/partition info (powerbi-modeling-mcp/partition_operations)
```

If connecting to a gold layer or lakehouse:
```
Data Source Exploration (CLI first — `fab`; MCP only where `fab` has no equivalent):
□ `fab find "<name>"` / `fab dir "<ws>.Workspace/<lh>.Lakehouse/Tables"` to find available tables
□ `fab get "<ws>.Workspace/<lh>.Lakehouse"` and `fab table schema "<path>/Tables/<table>"` for lakehouse schema
□ Use fabric-notebook-mcp/preview_lakehouse_table to inspect data (no `fab` equivalent for row preview)
□ Use fabric-notebook-mcp/get_table_column_stats for column statistics (no `fab` equivalent)
□ Use ms-mssql.mssql tools to query SQL-based gold layers
□ If `fab` is not installed, fall back to fabric-notebook-mcp/list_artifacts and get_lakehouse_detail
```

### Step 2: Design Star Schema

Classify tables then validate with `references/star-schema-checklist.md`:

| Type | Role | Examples |
|---|---|---|
| **Fact** | Measurable events, FK to dims, numeric aggregates | Sales, Orders, Production |
| **Dimension** | Descriptive context, surrogate key, filtering/grouping | Date, Product, Customer |
| **Bridge** | M:N link, key columns only | CustomerProduct, EmployeeProject |
| **Measure Table** | No data rows, organizes DAX measures | _Measures, _KPIs |

Full design rules and validation → `references/star-schema-checklist.md`

### Step 3: Configure Storage Modes

| Scenario | Recommended Mode |
|---|---|
| Historical data, < 1GB | Import |
| Historical data, > 1GB with Fabric | Direct Lake |
| Direct Lake + external reference data | Composite (DL + Import) |
| Real-time operational data | DirectQuery |
| Mix of real-time + historical | Composite (DQ + Import) |
| Dimension tables in composite model | Dual |
| Aggregation tables | Import |

Full decision matrix → `references/storage-mode-decision.md`

### Step 4: Build Relationships

Use `powerbi-modeling-mcp/relationship_operations`:

```
□ Cardinality: One-to-Many (dimension → fact) is standard
□ Cross-filter: Single direction (dimension filters fact) is default
□ Active: Only one active relationship between any two tables
□ Inactive: Use USERELATIONSHIP() for role-playing dimensions
□ Referential integrity: Enable for Import mode (performance boost)
```

Advanced patterns (M:M, weak, role-playing, ambiguity) → `references/advanced-relationships.md`

### Step 5: Optimize the Model

Prioritize in this order (biggest compression impact first):

1. **Remove unused columns** — hidden columns still consume memory
2. **Reduce cardinality** — bin dates, round decimals, group rare values
3. **Use INT keys** over TEXT — value encoding vs hash encoding
4. **No calculated columns on fact tables** — use measures or Power Query

**Model-level:**
- Dedicated date dimension (disable Auto Date/Time)
- Remove auto-generated `LocalDateTable_*` tables
- Aggregation tables for >100M row facts
- Incremental refresh for growing tables
- Target < 1GB model size (Import mode)

Full optimization guide → `references/vertipaq-optimization.md`

### Step 6: Implement Security

```
RLS Implementation Steps:
1. Define roles → powerbi-modeling-mcp/security_role_operations
2. Write DAX filter expressions per role
3. Test with dax_query_operations (EVALUATE with role context)
```

All patterns (static, dynamic, hierarchy, time-based, OLS) → `references/rls-patterns.md`

### Step 7: Validate the Model

Use `powerbi-modeling-mcp/dax_query_operations` to validate:

- `EVALUATE INFO.VIEW.RELATIONSHIPS()` — verify relationship structure
- Orphaned records check — `ISBLANK(RELATED(...))` pattern
- Row count spot-check — `COUNTROWS()` per table
- RLS propagation test — `CALCULATETABLE` with role context

Full discovery query catalog → `references/discovery-queries.md`

### Step 8: Prepare for AI (Copilot Readiness)

Optimize the model for Power BI Copilot and Fabric Data Agent:

```
Prep for AI Checklist:
□ Use descriptive, human-readable names for all tables, columns, measures
□ Add descriptions to tables, columns, and measures (Copilot uses metadata)
□ Hide relationship key columns and unused technical fields
□ Avoid duplicate field names across tables (e.g., "Name" in Customer vs Store)
□ Remove unused objects — fewer objects = less AI ambiguity
□ Configure AI Data Schema (Prep data for AI → Simplify data schema)
□ Add AI Instructions (business context, terminology, domain logic)
□ Set up Verified Answers for common questions
□ Mark model as "Prepped for AI" in semantic model settings
□ Test with Copilot pane → validate responses against expected answers
```

Copilot folder structure in PBIP → `references/tmdl-reference.md` §Copilot Folder
Full AI readiness guide → `references/semantic-model-ai-readiness.md`

## Common Modeling Scenarios

### Slowly Changing Dimensions (SCD)

**Type 1** (overwrite): Update dimension row directly. No special modeling.

**Type 2** (history): Surrogate key per version + ValidFrom/ValidTo/IsCurrent.
Relationship uses surrogate key (not natural key).

### Date Table Requirements

Every model MUST have a proper date table — time intelligence fails without it:

```
5 Non-Negotiable Requirements:
1. Contiguous dates — one row per calendar date, NO gaps
2. Covers full range of all fact table dates (plus buffer year)
3. Date column is DATE type — no time component
4. DateKey column is INT (YYYYMMDD) — use as relationship key
5. Marked as Date Table via powerbi-modeling-mcp/calendar_operations
```

> **Note:** Calendar-based time intelligence (preview, Sep 2025) relaxes the
> contiguity requirement for custom calendars (fiscal, 4-5-4, 13-month, lunar).
> Defines calendars on tables via Column Category mappings. New DAX functions:
> `TOTALWTD`, `PREVIOUSWEEK`, `TOTALYTD('CalendarName')`. Enable via Preview Features.

Full column requirements → `references/star-schema-checklist.md` (Section 3)

## PBIP / TMDL File Structure

For complete PBIP folder layout, file schemas, and TMDL syntax →
read `references/tmdl-reference.md` and `references/pbip.md`.

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-business-analysis` | Upstream (Phase 1) | Requirements doc defines tables, data sources, and RLS needs |
| `power-bi-dax-development` | Downstream (Phase 3) | Model schema feeds into measure creation |
| `power-bi-performance-troubleshooting` | Cross-cutting | VertiPaq optimization, storage mode tuning, cardinality reduction |
| `power-bi-report-authoring` | Downstream (Phase 4b) | Model schema used during PBIR generation for queryState bindings |
