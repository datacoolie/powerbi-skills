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

Direct Lake is the recommended mode for Fabric environments. It reads Delta
Parquet files directly from OneLake into the VertiPaq engine — combining
Import-level query speed with near-real-time data freshness.

```
Requirements:
- Data must be in Delta format in a Fabric Lakehouse or Warehouse
- Semantic model must be in a Fabric workspace (not My Workspace)
- Requires Fabric capacity (F SKU) or Premium (P SKU)
- Tables are read directly from Delta Parquet files (no import/copy)
- V-Order optimization recommended for best transcoding performance

Two variants:
- Direct Lake on OneLake: no fallback (errors on guardrail breach)
- Direct Lake on SQL: falls back to DirectQuery when needed

Key limitations (pre-compute these in Lakehouse ETL):
✗ No calculated columns on Direct Lake tables
✗ No user-defined aggregation tables
✗ No hybrid tables or model-level partitions

Benefits:
✅ VertiPaq engine (same as Import) — comparable query speed
✅ Framing refresh in seconds (metadata only, no data copy)
✅ Automatic updates detect Delta changes (near-real-time)
✅ No data duplication (single copy in OneLake)
✅ Supports very large datasets via per-query column loading
```

**For comprehensive Direct Lake guidance** — framing lifecycle, SKU guardrails,
fallback behavior, composite patterns, V-Order tuning, monitoring —
read `directlake-guide.md`.

## Composite Model Patterns

### Pattern 1: Hot & Cold Data
```
Hot data (recent 3 months): DirectQuery → real-time
Cold data (historical): Import → fast historical queries
Dimensions: Dual mode → works with both
```

### Pattern 2: Extend Existing Model
```
Published semantic model: DirectQuery (live connection)
New local tables: Import (additional data sources)
Bridge tables: Dual mode
```

### Pattern 3: Aggregation + Detail
```
Aggregation tables: Import (summary level)
Detail tables: DirectQuery (drill-down only)
Dimensions: Dual mode
Power BI auto-selects aggregation when query matches grain
```

### Pattern 4: Direct Lake + Import (Fabric)
```
Fact tables: Direct Lake on OneLake (large, auto-refreshed from Lakehouse)
Small reference tables: Import (external sources, Power Query transforms)
Calculated tables: Import (DL tables don't support calculated columns)
Dimensions shared by both: Dual mode
```

### Pattern 5: Chained Composite on Direct Lake
```
Published Direct Lake model: DirectQuery (chained live connection)
Analyst's local tables: Import (additional data sources)
Bridge tables: Dual mode
Use when IT publishes DL model and analysts need to extend it
```

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
