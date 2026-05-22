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
  report generation (use power-bi-pbip-report).
---

# Power BI Semantic Model Builder

Design and build Power BI semantic models following star schema best practices,
using PowerBI Modeling MCP tools for all model operations.

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
the latest modeling guidance before making design decisions.

**Use PowerBI Modeling MCP** (`powerbi-modeling-mcp/*`) for all model operations —
exploring tables, creating relationships, configuring columns, testing queries.
Read `references/mcp-tool-reference.md` for the complete tool mapping.

## Quick Reference

| Task | Approach |
|---|---|
| Explore existing model | `model_operations` → get model info, `table_operations` → list tables |
| Connect to gold layer | `connection_operations` → configure data source |
| Design star schema | Run Star Schema Checklist (references/star-schema-checklist.md) |
| Choose storage mode | Use Decision Matrix (references/storage-mode-decision.md) |
| Direct Lake guide | Framing, guardrails, fallback, composite (references/directlake-guide.md) |
| Build relationships | `relationship_operations` → create with proper cardinality |
| Advanced relationships | M:M, weak, role-playing, ambiguity (references/advanced-relationships.md) |
| Optimize columns | `column_operations` → set data types, remove unused, hide keys |
| Power Query / ETL | M language, query folding, transformations (references/power-query-reference.md) |
| Implement RLS | Dynamic RLS, OLS, DirectLake RLS patterns (references/rls-patterns.md) |
| TMDL / PBIP structure | Tables, columns, measures, relationships, roles (references/tmdl-reference.md) |
| Deploy to workspace | Git integration, CI/CD, Fabric pipelines (references/deployment-alm-guide.md) |
| Gateway & refresh | On-prem gateway, scheduled/incremental refresh (references/gateway-refresh-guide.md) |
| Test the model | `dax_query_operations` → run EVALUATE queries |

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
Data Source Exploration:
□ Use fabric-notebook-mcp/list_artifacts to find available tables
□ Use fabric-notebook-mcp/get_lakehouse_detail for lakehouse schema
□ Use fabric-notebook-mcp/preview_lakehouse_table to inspect data
□ Use fabric-notebook-mcp/get_table_column_stats for column statistics
□ Use ms-mssql.mssql tools to query SQL-based gold layers
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
read `references/tmdl-reference.md`.

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-business-analysis` | Upstream (Phase 1) | Requirements doc defines tables, data sources, and RLS needs |
| `power-bi-dax-development` | Downstream (Phase 3) | Model schema feeds into measure creation |
| `power-bi-performance-troubleshooting` | Cross-cutting | VertiPaq optimization, storage mode tuning, cardinality reduction |
| `power-bi-pbip-report` | Downstream (Phase 4b) | Model schema used during PBIR generation for queryState bindings |
