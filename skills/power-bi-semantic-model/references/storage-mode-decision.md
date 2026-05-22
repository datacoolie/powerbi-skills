# Storage Mode Decision Matrix

Use this decision tree to choose the correct storage mode for each table in a Power BI model.

## Decision Flow

```
START: What kind of table is this?
│
├─► Dimension Table (small, descriptive)
│   └─► Is model Composite (mixed storage)?
│       ├─► Yes → Dual mode (works with both Import and DQ sides)
│       └─► No  → Same as fact table mode
│
├─► Fact Table (large, transactional)
│   └─► WHERE is the data?
│       │
│       ├─► Fabric Lakehouse (Delta format)
│       │   └─► Data size?
│       │       ├─► Any size → DirectLake (RECOMMENDED — best of both worlds)
│       │       └─► Cannot use DirectLake? → Import with incremental refresh
│       │
│       ├─► SQL Database / Data Warehouse
│       │   └─► Need real-time data?
│       │       ├─► Yes → DirectQuery
│       │       │   └─► Can live with 15-min delay? → Consider scheduled Import
│       │       └─► No  → Import
│       │           └─► Data > 1GB? → Import with incremental refresh
│       │
│       ├─► Analysis Services (existing model)
│       │   └─► Live connection or extend?
│       │       ├─► Just connect → Live Connection (no local model)
│       │       └─► Need to add tables → Composite (DQ to existing + Import for new)
│       │
│       └─► Other sources (APIs, files, cloud services)
│           └─► Import (only option for most non-SQL sources)
│
└─► Aggregation Table (pre-computed summary)
    └─► Import mode always (small, fast lookups)
```

## Mode Comparison

| Feature | Import | DirectQuery | DirectLake | Composite |
|---|---|---|---|---|
| **Data freshness** | Schedule refresh | Real-time | Near real-time | Mixed |
| **Query speed** | Fastest | Depends on source | Fast (cached) | Mixed |
| **Model size limit** | ~1GB (shared) / 10GB+ (Premium) | No limit | No limit | Mixed |
| **Data source** | Any | SQL, AS, some cloud | Fabric Lakehouse only | Any combination |
| **DAX support** | Full | Full (slower iterator) | Full | Full |
| **Works offline** | Yes | No | No | Partially |
| **Incremental refresh** | Yes | N/A | Automatic | Yes (Import parts) |

## Direct Lake Mode (Fabric)

Direct Lake reads Delta Parquet files directly from OneLake into VertiPaq —
combining Import-level speed with near-real-time freshness. Two variants:

| Variant | Fallback | Composite Support |
|---|---|---|
| Direct Lake on OneLake | No fallback (errors on guardrail breach) | Yes (DL + Import, DL + DQ) |
| Direct Lake on SQL | Falls back to DirectQuery | No (use chained composite) |

Can now be created from Power BI Desktop (GA 2025) from any OneLake source.
DL + Import tables in same model supported (DL on OneLake only).

**Full guide** — requirements, guardrails, framing, fallback, V-Order, composite patterns →
`directlake-guide.md`

## Composite Model Patterns

| Pattern | Summary |
|---|---|
| **Hot & Cold** | Recent data DQ (real-time) + historical Import + Dual dims |
| **Extend Existing** | Published model via DQ chain + local Import tables + Dual bridges |
| **Aggregation + Detail** | Import summary + DQ detail + Dual dims (auto-selects agg at matching grain) |
| **Direct Lake + Import** | DL facts + Import reference/calculated tables + Dual dims |
| **Chained Composite** | Published DL model ← DQ chain ← local Import tables |

**Full pattern details with code examples** → `directlake-guide.md` §Composite Patterns

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| DirectQuery for small tables | Unnecessary source queries | Switch to Import |
| Import for 10GB+ on shared capacity | Exceeds capacity limits | Use Direct Lake or DQ |
| Bi-directional across DQ + Import | Performance killer | Use single-direction + DAX |
| No aggregation for >100M row DQ | Slow queries | Add Import aggregation layer |
| Mixed storage without Dual dimensions | Filter propagation breaks | Set dimensions to Dual |
| Direct Lake without running OPTIMIZE | Too many small Parquet files → guardrail breach | Schedule regular OPTIMIZE on Delta tables |
| Overwrite mode on DL Delta tables | Destroys Delta log → forces cold reload | Use append + delete patterns for incremental framing |
| Direct Lake without V-Order | Slow transcoding, poor compression | Ensure V-Order enabled in Lakehouse |
| Direct Lake on SQL with SQL-based RLS | Silent fallback to DirectQuery | Use semantic model RLS with fixed identity instead |
