---
name: power-bi-performance-troubleshooting
description: >-
  Diagnose and resolve Power BI performance issues across models, DAX queries,
  report visuals, and data refresh. Use this skill whenever the user reports slow
  report loading, slow visual interactions, long refresh times, high memory usage,
  query timeouts, or capacity bottlenecks. Triggers include: "report is slow",
  "performance issue", "optimize report", "slow loading", "query timeout",
  "refresh takes too long", "high memory", "report performance", "visual is slow",
  "optimize model", "reduce model size", "aggregation table", "incremental refresh",
  "Performance Analyzer", "DAX Studio", "server timings", "capacity metrics".
  Do NOT use for initial model design (use power-bi-semantic-model), initial DAX
  development (use power-bi-dax-development), or report design decisions
  (use power-bi-report-design). This skill is for diagnosing and fixing performance
  problems in existing solutions.
---

# Power BI Performance Troubleshooting

You are a Power BI performance specialist. You systematically diagnose and resolve
performance issues using a layered approach — from quick visual-level fixes to deep
DAX engine analysis and model restructuring.

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
the latest performance guidance before recommending optimizations.

## Reference Files

| Reference | When to Read |
|---|---|
| `references/performance-analyzer-guide.md` | First step: measuring visual-level performance in Power BI Desktop |
| `references/dax-studio-workflow.md` | Deep DAX analysis: Server Timings, query plans, VertiPaq Analyzer |
| `references/report-level-optimization.md` | Visual count, cross-filtering, slicers, query reduction, render vs query |
| `references/aggregation-tables.md` | Speeding up DirectQuery/Composite models with pre-aggregated Import tables |
| `references/incremental-refresh.md` | Reducing refresh time for large Import models, real-time hybrid |
| `../power-bi-dax-development/references/optimization-guide.md` | DAX engine internals: FE/SE, CALCULATE optimization, iterators, composite model patterns, calculated column trade-offs |
| `../power-bi-dax-development/references/anti-patterns.md` | 18 common DAX anti-patterns with fixes and benchmarks |
| `../power-bi-semantic-model/references/vertipaq-optimization.md` | VertiPaq encoding, cardinality reduction, column design, relationship keys |
| `../power-bi-semantic-model/references/storage-mode-decision.md` | Import vs DirectQuery vs DirectLake vs Composite decision matrix |
| `../power-bi-semantic-model/references/directlake-guide.md` | Direct Lake: framing, SKU guardrails, fallback, V-Order, composite patterns, monitoring |

## Performance Targets

| Metric | Target | Concern | Critical |
|---|---|---|---|
| Page load time | < 5s | 5-10s | > 10s |
| Visual interaction response | < 1s | 1-3s | > 3s |
| DAX query execution | < 1s | 1-5s | > 5s |
| Model refresh (full) | < 30 min | 30-120 min | > 2 hours |
| Model size (Pro/PPU) | < 250 MB | 250 MB-1 GB | > 1 GB |
| SE/FE time ratio | SE > 90% | SE 50-90% | FE > 50% |
| Visuals per page | ≤ 8 | 8-12 | > 12 |

## Diagnostic Workflow

### Step 1 — Identify the Symptom

Classify the reported performance issue:

```
Symptom Classification:
┌──────────────────────────┬─────────────────────┬───────────────────────────┐
│ Symptom                  │ Layer               │ Start With                │
├──────────────────────────┼─────────────────────┼───────────────────────────┤
│ Page loads slowly        │ Report + DAX        │ Performance Analyzer      │
│ Visual is slow to update │ DAX + Model         │ Performance Analyzer      │
│ Slicer interaction lag   │ Report + DAX        │ Report-level optimization │
│ Cross-filter is slow     │ Report + Model      │ Report-level optimization │
│ Refresh takes too long   │ Model + Source      │ Incremental refresh       │
│ Model is too large       │ Model               │ VertiPaq Analyzer         │
│ DirectQuery timeout      │ Model + Source      │ Aggregation tables        │
│ Composite model slow     │ Model + DAX         │ Optimization guide        │
│ Multiple reports slow    │ Capacity            │ Capacity metrics          │
│ Direct Lake fallback     │ Model + Lakehouse   │ directlake-guide.md       │
│ DL cold-state slow       │ Model + Lakehouse   │ V-Order + OPTIMIZE        │
│ DL framing failure       │ Lakehouse + SKU     │ Guardrails check          │
└──────────────────────────┴─────────────────────┴───────────────────────────┘
```

### Step 2 — Measure Baseline

Before optimizing, always capture baseline metrics:

1. **Open Performance Analyzer** in Power BI Desktop
   → See `references/performance-analyzer-guide.md`
2. Record for each slow visual:
   - DAX Query time (ms)
   - Visual Display time (ms)
   - Other time (ms)
3. Copy the generated DAX query for deeper analysis
4. Note the total page load time

### Step 3 — Diagnose by Layer

Work through layers from cheapest-to-fix to most-expensive:

```
Layer 1: Report Design (Quick Wins — minutes)
├── Too many visuals? → Reduce to ≤ 8 per page
├── Unnecessary cross-filtering? → Disable on non-interactive visuals
├── High-cardinality slicers? → Switch to dropdown, add search
├── Missing query reduction? → Enable Apply button on slicers
└── Custom visuals slow? → Replace with standard visuals
    → Read: references/report-level-optimization.md

Layer 2: DAX Measures (Medium — hours)
├── High FE time? → Check for anti-patterns (IF in iterators, context transition)
├── Many SE queries? → Excessive CALCULATE calls, consolidate
├── CallbackDataID? → Push logic to SE (split IF into CALCULATE)
├── Large datacache? → Early materialization, reduce columns
└── Complex measures? → Simplify with VAR, break into steps
    → Read: ../power-bi-dax-development/references/optimization-guide.md
    → Read: ../power-bi-dax-development/references/anti-patterns.md

Layer 3: Data Model (Medium — hours to days)
├── High-cardinality columns? → Remove, bin, or move to dimension
├── Calculated columns on facts? → Replace with measures or PQ columns
├── Wrong storage mode? → Import for dims, DQ for large facts
├── Missing referential integrity? → Enable on Import relationships
└── Model too large? → Remove unused columns, optimize data types
    → Read: ../power-bi-semantic-model/references/vertipaq-optimization.md

Layer 4: Architecture (Expensive — days)
├── DirectQuery too slow? → Add aggregation tables
├── Refresh too long? → Implement incremental refresh
├── Composite model cross-engine? → Dual-mode dimensions, TREATAS
└── Need real-time + history? → Hybrid incremental refresh + DQ
    → Read: references/aggregation-tables.md
    → Read: references/incremental-refresh.md
```

### Step 4 — Optimize

Apply fixes in layer order (cheapest first). For each fix:

1. Make ONE change at a time
2. Clear the model cache before re-testing
3. Re-measure with Performance Analyzer or DAX Studio
4. Record the before/after timing
5. If improvement is < 10%, consider reverting (minimal gain, added complexity)

### Step 5 — Validate

After all optimizations:

1. Re-run Performance Analyzer on all affected pages
2. Compare against baseline measurements from Step 2
3. Verify all visuals still display correct data
4. Test with realistic filter combinations (not just default view)
5. Document changes made and their measured impact

## Quick Diagnosis Cheat Sheet

| If you see... | It means... | Fix with... |
|---|---|---|
| DAX Query > 5s in Perf Analyzer | Slow measure or model | Copy query → DAX Studio Server Timings |
| Visual Display > 2s in Perf Analyzer | Too many data points or complex render | Reduce data points, simplify visual |
| FE time > SE time in DAX Studio | Formula Engine bottleneck | Optimize DAX (anti-patterns, split iterators) |
| Many small SE queries (>20) | Excessive context transitions | Reduce iterator scope, use column refs |
| Single large SE query (>1M rows) | Early materialization | Restructure ADDCOLUMNS→SUMMARIZE, reduce columns |
| CallbackDataID in query plan | FE handling SE work | Move IF/SWITCH out of iterators |
| Column > 100 MB in VertiPaq Analyzer | High-cardinality column | Remove, bin, or move to dimension |
| > 8 visuals on a page | Visual overload | Split into multiple pages, use bookmarks |
| Slicer with > 10K items | High-cardinality slicer | Use dropdown mode, add hierarchy |
| Refresh > 2 hours | Full refresh on large table | Implement incremental refresh |
| DQ query timeout | Source too slow for real-time | Add aggregation table |

## MCP Tools for Performance Analysis

Use these PowerBI Modeling MCP tools during diagnosis:

| Tool | Use For |
|---|---|
| `dax_query_operations` | Run test queries, measure execution time |
| `trace_operations` | Capture query traces for timing analysis |
| `model_operations` | Inspect model metadata, storage modes |
| `table_operations` | Check table row counts, partitions, storage mode |
| `column_operations` | Inspect column data types, cardinality |
| `relationship_operations` | Check relationship types, referential integrity |
| `partition_operations` | Inspect/configure incremental refresh partitions |
| `measure_operations` | Review measure expressions for anti-patterns |

### Example: Baseline Test Query

```dax
-- Run via dax_query_operations to measure query time
-- Test the same query that Performance Analyzer generates
DEFINE
    VAR _startTime = NOW()
EVALUATE
SUMMARIZECOLUMNS(
    DimDate[Year],
    DimDate[Month],
    "Sales", [Total Sales],
    "Margin", [% Margin]
)
```

## Common Optimization Scenarios

### Scenario: Slow Dashboard (Multiple KPI Cards + Charts)

1. Performance Analyzer → identify which visuals are slowest
2. If all visuals are slow (similar timing):
   - Problem is likely model-level or shared slicer context
   - Check: cross-filtering chain, slicer cardinality
   - Read: `references/report-level-optimization.md`
3. If one visual is much slower:
   - Problem is that visual's measure
   - Copy DAX query → DAX Studio → Server Timings
   - Read: `references/dax-studio-workflow.md`

### Scenario: Composite Model Slow Queries

1. Check which tables are DirectQuery vs Import
   - `table_operations` → inspect storage modes
2. Ensure all dimension tables are Dual or Import mode
3. Check for cross-engine joins in DAX queries
4. Verify FILTER() never references full remote tables
   - Read: `../power-bi-dax-development/references/optimization-guide.md` (Composite Model section)
5. Add aggregation tables for frequent query patterns
   - Read: `references/aggregation-tables.md`

### Scenario: Model Too Large for Pro License (>1 GB)

1. Run VertiPaq Analyzer in DAX Studio
   - Read: `references/dax-studio-workflow.md` (VertiPaq Analyzer section)
2. Sort columns by size → identify top 10 largest columns
3. For each large column, decide:
   - Remove if unused (check visuals and measures)
   - Move to dimension if it's a text column on a fact table
   - Bin if it's a continuous numeric used for grouping
   - Split if it's a DateTime (separate Date + Time)
4. Read: `../power-bi-semantic-model/references/vertipaq-optimization.md`

### Scenario: Refresh Taking Too Long

1. Check current refresh approach:
   - `partition_operations` → list partitions and their types
2. If full refresh on a large table (>10M rows):
   - Implement incremental refresh
   - Read: `references/incremental-refresh.md`
3. If calculated columns are slow:
   - Move computation to Power Query / source SQL
   - Read: `../power-bi-dax-development/references/optimization-guide.md` (Calculated Column Trade-Off section)
4. Check Power Query for non-folding steps (breaks query folding)

### Scenario: Direct Lake Fallback / Slow Cold State

1. Verify whether Direct Lake model is actually using Direct Lake mode:
   - Check `DirectLakeBehavior` property and refresh history in Fabric portal
   - If SQL queries appear in DAX Studio Server Timings → fallback occurred
2. If **fallback detected** (DL on SQL):
   - Check Delta table row count vs. SKU guardrails → scale up or OPTIMIZE
   - Check if table references a SQL view → use Delta table instead
   - Check for SQL-based RLS → switch to semantic model RLS with fixed identity
   - Set `DirectLakeBehavior = DirectLakeOnly` to surface issues during dev
3. If **cold-state slow** (first query after framing):
   - Verify V-Order is enabled on Delta tables (Delta Analyzer)
   - Run `OPTIMIZE` to compact small Parquet files into larger row groups
   - Check if Overwrite mode is used for data loads (forces full reload)
   - Switch to append + delete patterns for incremental framing benefit
4. If **framing fails**:
   - Check Parquet file count vs. SKU limit (e.g., 1,000 for F2-F8)
   - Run `OPTIMIZE` to reduce file count → re-frame
5. Read: `../power-bi-semantic-model/references/directlake-guide.md`

## Anti-Pattern Quick Scan

Run this mental checklist against the model's measures before deep analysis:

```
□ Any division without DIVIDE()? → Fix immediately
□ Any calculated columns on fact tables? → Replace with measures
□ Any FILTER(FactTable, ...) in CALCULATE? → Use dimension filters
□ Any IF/SWITCH inside SUMX/iterators? → Split into CALCULATE calls
□ Any measure reference inside SUMX over fact table? → Use column refs
□ Any nested iterators on large tables? → Restructure with VAR + ADDCOLUMNS
□ Any ALLEXCEPT with cross-filtered columns? → Use ALL + VALUES
□ Any FORMAT() in measures? → Use format string property instead
□ Any DISTINCTCOUNT on high-cardinality text? → Use INT surrogate key
```

→ Full list with examples: `../power-bi-dax-development/references/anti-patterns.md`

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-dax-development` | Cross-reference | DAX optimization guide, anti-patterns, query plan analysis |
| `power-bi-semantic-model` | Cross-reference | VertiPaq optimization, storage mode decisions, Direct Lake tuning |
| `power-bi-pbip-report` | Cross-reference | Report-level optimization (visual count, slicer design) |
| `power-bi-feedback-iteration` | Upstream | Performance complaints route here from the feedback skill |
