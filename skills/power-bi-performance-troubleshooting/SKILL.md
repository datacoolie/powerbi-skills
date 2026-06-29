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
| `references/fabric-capacity-monitoring.md` | Capacity-level diagnosis: CU saturation, throttling, Fabric Metrics App, Evaluation Config |

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

→ For quick symptom-to-fix mapping, see the Layer tables in Step 3 above.
→ For DAX-specific anti-patterns, see `../power-bi-dax-development/references/anti-patterns.md`.

## MCP Tools for Performance Analysis

Use these PowerBI Modeling MCP tools during diagnosis:

| Tool | Use For |
|---|---|
| `dax_query_operations` | Run test queries, measure execution time, capture traces |
| `table_operations` | Check row counts, partitions, storage mode |
| `column_operations` | Inspect data types, cardinality |
| `measure_operations` | Review expressions for anti-patterns |

## Common Scenarios — Quick Reference

| Scenario | Start With | Key Reference |
|---|---|---|
| Slow dashboard (multiple visuals) | Performance Analyzer → identify slowest visual | `references/performance-analyzer-guide.md` |
| Composite model slow queries | Check storage modes → Dual dimensions → aggregation | `references/aggregation-tables.md` |
| Model too large for Pro (>1 GB) | VertiPaq Analyzer → sort columns by size | `references/dax-studio-workflow.md` §VertiPaq |
| Refresh taking too long | Check partition strategy → incremental refresh | `references/incremental-refresh.md` |
| Direct Lake fallback / cold state | Check DirectLakeBehavior → V-Order → OPTIMIZE | `../power-bi-semantic-model/references/directlake-guide.md` |
| Capacity throttling / multi-report slow | Fabric Capacity Metrics App → CU analysis | `references/fabric-capacity-monitoring.md` |

## DAX Anti-Pattern Scan

Before deep analysis, run the anti-pattern checklist:
→ **Read `../power-bi-dax-development/references/anti-patterns.md`** — 18 patterns with fixes and benchmarks.

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-dax-development` | Cross-reference | DAX optimization guide, anti-patterns, query plan analysis |
| `power-bi-semantic-model` | Cross-reference | VertiPaq optimization, storage mode decisions, Direct Lake tuning |
| `power-bi-report-authoring` | Cross-reference | Report-level optimization (visual count, slicer design) |
| `power-bi-feedback-iteration` | Upstream | Performance complaints route here from the feedback skill |
