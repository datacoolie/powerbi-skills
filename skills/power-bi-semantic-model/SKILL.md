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
| TMDL syntax | Tables, columns, measures, relationships, roles (references/tmdl-reference.md) |
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

Apply dimensional modeling principles:

#### Identify Tables

```
Table Classification:
┌─────────────────────────────────────────────────────────┐
│ Fact Tables (measurable events)                         │
│ - Contain foreign keys to dimensions                    │
│ - Contain numeric measures for aggregation              │
│ - Typically large and growing                           │
│ - Examples: Sales, Orders, Transactions, Production     │
├─────────────────────────────────────────────────────────┤
│ Dimension Tables (descriptive context)                  │
│ - Contain surrogate key (unique identifier)             │
│ - Contain descriptive attributes for filtering/grouping │
│ - Relatively small and slowly changing                  │
│ - Examples: Date, Product, Customer, Store, Employee    │
├─────────────────────────────────────────────────────────┤
│ Bridge Tables (for many-to-many)                        │
│ - Link two tables with M:N relationship                 │
│ - Contain only key columns                              │
│ - Examples: CustomerProduct, EmployeeProject            │
├─────────────────────────────────────────────────────────┤
│ Measure Tables (DAX measures container)                 │
│ - No data rows, only measures                           │
│ - Organizes measures by business area                   │
│ - Naming: _Measures, _KPIs, _[Domain] KPI              │
└─────────────────────────────────────────────────────────┘
```

#### Design Rules

```
Star Schema Rules:
✅ One relationship path between any two tables
✅ Dimension tables connect directly to fact tables (no snowflaking)
✅ Date dimension is always present (required for time intelligence)
✅ Surrogate keys (integer) preferred over natural keys
✅ Hide foreign key columns from report view
✅ Avoid bi-directional filtering unless explicitly needed
❌ No circular relationships
❌ No fact-to-fact direct relationships (use shared dimensions)
❌ No calculated columns on fact tables (use measures or Power Query)
```

Run the full checklist: read `references/star-schema-checklist.md`.

### Step 3: Configure Storage Modes

Choose the right storage mode for each table. Read `references/storage-mode-decision.md`
for the full decision matrix.

**Quick Decision Guide:**

| Scenario | Recommended Mode |
|---|---|
| Historical data, < 1GB | Import |
| Historical data, > 1GB with Fabric | Direct Lake |
| Direct Lake + external reference data | Composite (DL on OneLake + Import) |
| Real-time operational data | DirectQuery |
| Mix of real-time + historical | Composite (DQ for recent, Import for historical) |
| Dimension tables in composite model | Dual (best of both worlds) |
| Aggregation tables | Import (pre-aggregated summaries) |

### Step 4: Build Relationships

Use `powerbi-modeling-mcp/relationship_operations` to create relationships:

```
Relationship Design Checklist:
□ Cardinality: One-to-Many (dimension → fact) is the standard pattern
□ Cross-filter: Single direction (dimension filters fact) is default
□ Active: Only one active relationship between any two tables
□ Inactive: Use USERELATIONSHIP() in DAX for role-playing dimensions
□ Referential integrity: Enable for Import mode (performance boost)
```

#### Common Relationship Patterns

**Role-Playing Dimensions** (e.g., Date used as Order Date and Ship Date):
```
DimDate ──1:M──► FactSales (OrderDateKey)     [ACTIVE]
DimDate ──1:M──► FactSales (ShipDateKey)       [INACTIVE]
DimDate ──1:M──► FactSales (DueDateKey)        [INACTIVE]

// Access inactive relationships via DAX:
Sales by Ship Date =
CALCULATE([Total Sales], USERELATIONSHIP(FactSales[ShipDateKey], DimDate[DateKey]))
```

**Many-to-Many via Bridge Table**:
```
DimCustomer ──1:M──► BridgeCustomerAccount ◄──M:1── DimAccount
                              │
                          (M:1 to FactTransactions via AccountKey)
```

**Parent-Child Hierarchy** (e.g., Organization chart):
```
DimEmployee [EmployeeKey] ──self-referencing──► DimEmployee [ManagerKey]
// Flatten with PATH() function in DAX
```

For advanced patterns (MMR weak relationships, granularity mismatch detection,
ambiguity resolution, virtual vs physical trade-offs), read
`references/advanced-relationships.md`.

### Step 5: Optimize the Model

#### Column Optimization

VertiPaq stores each column using one of three encodings. The #1 driver of model
size and query speed is **column cardinality** (number of distinct values).

```
Column Cleanup Checklist (in priority order of compression impact):
□ Remove unused columns — every column consumes memory even if hidden
□ Reduce cardinality — bin dates to month/year, round decimals, group rare values
□ Split DateTime into Date + Time columns — DateTime keys have high cardinality
□ Use INT keys, not TEXT — INT uses value encoding (fast), TEXT uses hash encoding (slower)
□ Set correct data types (Int64 for keys, Date for dates, Decimal for amounts)
□ Hide foreign key columns (visible in model, hidden from report)
□ Set Sort By Column for display columns (e.g., MonthName sorted by MonthNumber)
□ Set Data Category for geographic columns (City, State, Country, Latitude, Longitude)
□ Mark key columns for summarization = "None" (prevent accidental aggregation)
□ Consolidate similar columns across tables
```

**VertiPaq Encoding Reference:**

| Column Type | Encoding | Implication |
|---|---|---|
| Low-cardinality integers | Value encoding | Smallest footprint, fastest scans |
| Strings, high-cardinality numbers | Hash encoding | Dictionary + compressed index |
| Any column after sorting | RLE (Run-Length) | Applied on top; benefits from low cardinality |

> **Rule**: Calculated columns on fact tables block optimal RLE compression.
> Always prefer Power Query transformations or DAX measures over calculated columns
> on large tables.

#### Model-Level Optimization

```
Model Optimization Checklist:
□ Date table: Use a dedicated, complete date dimension (no auto date/time)
□ Disable Auto Date/Time at model level (reduces hidden table bloat)
□ Remove unused auto-generated date tables (LocalDateTable_*)
□ Set appropriate Default Summarization per column
□ Create aggregation tables for large fact tables (> 100M rows)
□ Consider partitioning for incremental refresh
□ Review model size: aim for < 1GB for Import mode
□ See references/vertipaq-optimization.md for deep-dive cardinality guidance
```

### Step 6: Implement Security

#### Row-Level Security (RLS)

```
RLS Implementation Steps:
1. Define roles with powerbi-modeling-mcp/security_role_operations
2. Write DAX filter expressions per role
3. Test with powerbi-modeling-mcp/dax_query_operations (EVALUATE with role context)
```

**Static RLS** (fixed filter values):
```dax
// Role: "Europe Sales"
// Table: DimRegion
// Filter: [Region] = "Europe"
[Region] = "Europe"
```

**Dynamic RLS** (user-based):
```dax
// Role: "Regional Manager"
// Table: DimRegion
// Filter: Based on logged-in user
[ManagerEmail] = USERPRINCIPALNAME()
```

**Dynamic RLS with lookup table**:
```dax
// Role: "Data Access"
// Table: SecurityMapping
// Filter: User maps to allowed regions
[UserEmail] = USERPRINCIPALNAME()
// With bridge: SecurityMapping → DimRegion → FactSales (bi-directional on bridge)
```

### Step 7: Validate the Model

Use `powerbi-modeling-mcp/dax_query_operations` to run validation queries:

```dax
// Check relationship integrity — orphaned fact records
EVALUATE
VAR OrphanedSales =
    CALCULATETABLE(
        FactSales,
        ISBLANK(RELATED(DimProduct[ProductName]))
    )
RETURN ROW("Orphaned Records", COUNTROWS(OrphanedSales))

// Verify model info
EVALUATE INFO.VIEW.RELATIONSHIPS()

// Check table row counts
EVALUATE
UNION(
    ROW("Table", "FactSales", "Rows", COUNTROWS(FactSales)),
    ROW("Table", "DimProduct", "Rows", COUNTROWS(DimProduct)),
    ROW("Table", "DimDate", "Rows", COUNTROWS(DimDate))
)

// Test RLS filter propagation
EVALUATE
CALCULATETABLE(
    SUMMARIZE(FactSales, DimRegion[Region], "Sales", [Total Sales]),
    USERPRINCIPALNAME() = "manager@company.com"
)
```

## Common Modeling Scenarios

### Slowly Changing Dimensions (SCD)

**Type 1** (overwrite): Simply update the dimension row. No special modeling needed.

**Type 2** (history tracking):
```
DimCustomer:
- CustomerKey (surrogate key — unique per version)
- CustomerID (natural key — same across versions)
- CustomerName, Address, ...
- ValidFrom, ValidTo
- IsCurrent (boolean)

Relationship: FactSales[CustomerKey] → DimCustomer[CustomerKey] (1:M)
```

### Date Table Requirements

Every model MUST have a proper date table. Time intelligence functions
(TOTALYTD, SAMEPERIODLASTYEAR, etc.) will fail silently or produce wrong
results if these five requirements are not met:

```
5 Non-Negotiable Requirements:
1. Contiguous dates — one row per calendar date, NO gaps
2. Covers the full range of all fact table dates (plus a buffer year)
3. Date column is DATE type — no time component (00:00:00 only)
4. DateKey column is INT (YYYYMMDD format preferred for relationships)
5. Marked as Date Table via powerbi-modeling-mcp/calendar_operations

Required Columns:
- Date (unique, DATE type, no time component)
- DateKey (INT, format YYYYMMDD — use as relationship key)
- Year, Quarter, Month, Day
- MonthName (with Sort By = MonthNumber)
- QuarterLabel (e.g., "Q1 2024")
- FiscalYear, FiscalQuarter (if fiscal calendar differs)
- IsCurrentMonth, IsCurrentYear (for dynamic filtering)
- WeekNumber, DayOfWeek, IsWeekend (for operational reports)
```

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-business-analysis` | Upstream (Phase 1) | Requirements doc defines tables, data sources, and RLS needs |
| `power-bi-dax-development` | Downstream (Phase 3) | Model schema feeds into measure creation |
| `power-bi-performance-troubleshooting` | Cross-cutting | VertiPaq optimization, storage mode tuning, cardinality reduction |
| `power-bi-pbip-report` | Downstream (Phase 4b) | Model schema used during PBIR generation for queryState bindings |

> **Why INT key?** Integer DateKey (e.g., 20241231) uses value encoding in
> VertiPaq — much smaller and faster than a text or datetime relationship key.

### Aggregation Tables

For large fact tables (>100M rows), add pre-aggregated summary tables:

```
FactSales_Agg_Monthly:
- DateKey (monthly grain → links to DimDate)
- ProductCategoryKey (rolled up from ProductKey)
- RegionKey
- TotalAmount (pre-aggregated SUM)
- RowCount (pre-aggregated COUNT)

Configure: Set aggregation table priority so Power BI uses it automatically
when queries match the aggregated grain.
```

## TMDL File Structure Reference

When working with PBIP semantic models, the `.SemanticModel/` folder uses TMDL format:

```
<Project>.SemanticModel/
├── definition.pbism              # Semantic model definition (version, settings)
├── diagramLayout.json            # Visual diagram positions
├── .platform                     # Git integration metadata
└── definition/
    ├── database.tmdl             # Compatibility level (1600)
    ├── model.tmdl               # Model config, culture, annotations
    ├── relationships.tmdl        # All relationship definitions
    ├── cultures/
    │   └── en-US.tmdl           # Localization
    └── tables/
        ├── DimDate.tmdl         # Each table = one .tmdl file
        ├── DimProduct.tmdl      # Contains columns, measures, partitions
        ├── FactSales.tmdl       # Contains M expressions or source queries
        └── _Measures.tmdl       # Dedicated measure table
```

### TMDL Syntax Basics

```tmdl
/// Table definition
table DimProduct
    lineageTag: abc123-def456

    /// Column definition
    column ProductKey
        dataType: int64
        isHidden
        isKey
        lineageTag: col-001
        summarizeBy: none
        sourceColumn: ProductKey

    /// Measure definition
    measure 'Total Revenue' =
        SUM(FactSales[Revenue])
        formatString: $#,##0
        lineageTag: msr-001

    /// Partition (data source)
    partition DimProduct = m
        mode: import
        source =
            let
                Source = Sql.Database("server", "database"),
                Result = Source{[Schema="dbo",Item="DimProduct"]}[Data]
            in
                Result
```
