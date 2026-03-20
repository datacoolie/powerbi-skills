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

## DirectLake Mode (Fabric)

DirectLake is the recommended mode for Fabric environments:

```
Requirements:
- Data must be in Delta format in a Fabric Lakehouse or Warehouse
- Semantic model must be in a Fabric workspace
- Tables are read directly from Delta Parquet files (no import/copy)
- Falls back to DirectQuery if data exceeds memory limits

Benefits:
✅ Fast query performance (reads columnar Parquet directly)
✅ No scheduled refresh needed (auto-detects Delta changes)
✅ No data duplication (single copy in lakehouse)
✅ Supports large datasets without Import size limits
```

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

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| DirectQuery for small tables | Unnecessary source queries | Switch to Import |
| Import for 10GB+ on shared capacity | Exceeds capacity limits | Use DirectLake or DQ |
| Bi-directional across DQ + Import | Performance killer | Use single-direction + DAX |
| No aggregation for >100M row DQ | Slow queries | Add Import aggregation layer |
| Mixed storage without Dual dimensions | Filter propagation breaks | Set dimensions to Dual |
