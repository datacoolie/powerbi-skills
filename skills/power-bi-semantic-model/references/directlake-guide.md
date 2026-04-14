# Direct Lake Mode — Comprehensive Guide

Direct Lake is a Power BI semantic model table storage mode available in
Microsoft Fabric. It reads Delta Parquet files directly from OneLake into
VertiPaq memory — combining Import-level query speed with DirectQuery-level
data freshness, without copying data.

---

## How Direct Lake Works

```
Traditional Import:       Source DB → ETL → Copy into VertiPaq → Query
Traditional DirectQuery:  Source DB ← SQL query ← DAX engine ← Report
Direct Lake:              Delta Parquet in OneLake → Read into VertiPaq → Query
                          (no copy, no SQL translation)
```

### Key Concepts

1. **Delta tables in OneLake** — Data must be stored as Delta format in a
   Fabric Lakehouse or Warehouse
2. **VertiPaq engine** — Same engine as Import mode; DAX queries processed
   identically once data is in memory
3. **Framing** — A lightweight metadata refresh (~seconds) that points the
   semantic model to the latest Delta table version
4. **Transcoding** — On-demand loading of column data from Parquet into
   VertiPaq memory segments (happens per-column, per-query)
5. **No SQL translation** — Unlike DirectQuery, Direct Lake reads columnar
   Parquet natively without generating SQL queries

### Two Variants

| Variant | Source | Fallback | Composite Support |
|---|---|---|---|
| **Direct Lake on OneLake** | Any Fabric Delta table source (Lakehouse, Warehouse, shortcuts) | No fallback — fails if guardrails exceeded | Yes (DL + Import, DL + DQ via XMLA tools) |
| **Direct Lake on SQL** | Single Lakehouse/Warehouse via SQL analytics endpoint | Falls back to DirectQuery | No (DL tables only; extend via composite model chaining) |

---

## Framing Lifecycle

Framing is the "refresh" operation for Direct Lake — but it only updates
metadata references, not data.

### How Framing Works

```
1. Semantic model analyzes Delta log of each table
2. Identifies which Parquet files are current (latest commit version)
3. Updates internal pointers to reference those files
4. Evicts only column segments whose underlying data changed (incremental framing)
5. Retains dictionaries when possible (no full re-encode)
6. Takes seconds, not minutes/hours like Import refresh
```

### Framing Triggers

| Trigger | Behavior |
|---|---|
| **Automatic updates** (default ON) | Model reframes automatically when data changes are detected in OneLake |
| **Manual refresh** (Power BI service) | User triggers refresh from workspace |
| **Programmatic refresh** (REST API) | `POST /datasets/{id}/refreshes` — useful for CI/CD pipelines |
| **Scheduled refresh** | Standard Power BI schedule configuration |
| **Automatic page refresh** | Report-level setting for near-real-time dashboards |

### Data Freshness SLA

- **Automatic updates enabled:** Data visible after a short detection interval
  (typically within minutes after Delta table write completes)
- **Automatic updates disabled:** Data visible only after manual/scheduled framing
- **Data is NOT real-time** — there is always a gap between Delta write and
  framing completion. Set stakeholder expectations accordingly

### Incremental Framing Optimization

Direct Lake uses incremental framing to minimize cold-state impact:
- Analyzes Delta log → drops only segments from changed row groups
- Retains existing dictionaries → adds new values without full rebuild
- If underlying data used **non-destructive patterns** (append-only, partitioned
  deletes), most segments survive framing → fast warm-up

**Anti-pattern:** Using **Overwrite** mode when loading data erases the Delta
log, forcing Direct Lake to do a full cold reload of all columns.

---

## Memory States

| State | Description | Performance |
|---|---|---|
| **Cold** | No data in memory; all columns must be transcoded from Parquet | Slowest (first query after framing/eviction) |
| **Semiwarm** | Some segments retained; only changed data must reload | Moderate (incremental framing benefit) |
| **Warm** | All queried columns loaded in VertiPaq | Fast (comparable to Import) |
| **Hot** | Warm + VertiScan caches populated | Fastest (cache hits) |

**Goal:** Minimize time in Cold state. Use incremental framing + V-Order
to accelerate cold → warm transition.

---

## Capacity Guardrails per SKU

When guardrails are exceeded:
- **Direct Lake on OneLake** → Refresh fails; model cannot be queried
- **Direct Lake on SQL** → Falls back to DirectQuery (if fallback enabled)

| Fabric SKU | Parquet Files/Table | Row Groups/Table | Rows/Table (millions) | Max Model Size on Disk (GB) | Max Memory (GB) |
|---|---|---|---|---|---|
| F2 | 1,000 | 1,000 | 300 | 10 | 3 |
| F4 | 1,000 | 1,000 | 300 | 10 | 3 |
| F8 | 1,000 | 1,000 | 300 | 10 | 3 |
| F16 | 1,000 | 1,000 | 300 | 20 | 5 |
| F32 | 1,000 | 1,000 | 300 | 40 | 10 |
| F64 / P1 | 5,000 | 5,000 | 1,500 | Unlimited | 25 |
| F128 / P2 | 5,000 | 5,000 | 3,000 | Unlimited | 50 |
| F256 / P3 | 5,000 | 5,000 | 6,000 | Unlimited | 100 |
| F512 / P4 | 10,000 | 10,000 | 12,000 | Unlimited | 200 |
| F1024 / P5 | 10,000 | 10,000 | 24,000 | Unlimited | 400 |
| F2048 | 10,000 | 10,000 | 24,000 | Unlimited | 400 |

**Notes:**
- Max Memory is not a hard guardrail but exceeding it causes excessive
  paging in/out — major performance degradation
- Parquet files, row groups, and rows per table are **per-query** guardrails
  (except Max Model Size which is model-level)
- **Always run `OPTIMIZE`** on Delta tables to keep file/row-group counts
  within limits — this is the #1 cause of unexpected fallback

---

## DirectQuery Fallback

### When Fallback Occurs (Direct Lake on SQL Only)

| Trigger | Description |
|---|---|
| Guardrail exceeded | Table rows, files, or row groups exceed SKU limits |
| SQL view as source | Semantic model table references a SQL analytics endpoint view (not a Delta table) |
| SQL-based RLS | SQL analytics endpoint enforces row-level security |
| SQL-based CLS | Column-level security enforced on SQL endpoint |
| Unprocessed tables | Tables created via XMLA without sending refresh command |

**Direct Lake on OneLake does NOT support fallback** — queries fail with
an error instead of silently degrading.

### Controlling Fallback Behavior

The `DirectLakeBehavior` property on the semantic model controls fallback:

| Value | Behavior |
|---|---|
| `Automatic` (default) | Falls back to DirectQuery silently |
| `DirectLakeOnly` | Fails with error instead of falling back |
| `DirectQueryOnly` | Always uses DirectQuery (disables Direct Lake) |

**Recommendation:** Set to `DirectLakeOnly` in development/testing to surface
fallback issues early. Use `Automatic` in production only if you accept the
performance trade-off.

### Detecting Fallback

1. **Fabric Capacity Metrics App** — Monitor "DirectQuery fallback" metric
2. **DAX Studio** — If Server Timings shows SQL queries being generated on
   a Direct Lake model, fallback has occurred
3. **DMV queries:**
   ```sql
   SELECT [TableName], [Description]
   FROM $SYSTEM.TMSCHEMA_TABLES
   WHERE [StorageMode] = 4  -- Direct Lake tables
   ```
4. **Refresh history** — Fabric portal → Direct Lake tab shows framing
   failures and fallback warnings

---

## Direct Lake Performance Tuning

### V-Order Optimization

V-Order is a write-time optimization that reorders and compresses Parquet
data for optimal VertiScan performance:

- **Enabled by default** in Fabric Lakehouse
- Dramatically reduces transcoding time (cold → warm)
- Enables VertiScan to compute on compressed data (skips decompression)
- External tools (Spark jobs outside Fabric) may not apply V-Order

**Verify V-Order is enabled:**
```python
import sempy_labs as labs
results = labs.delta_analyzer("your_table_name")
# Check 'VOrder enabled' in Summary output
```

### Delta Table Optimization

| Task | Command | When to Run |
|---|---|---|
| **OPTIMIZE** | `spark.sql("OPTIMIZE tableName")` | After bulk loads; weekly for append-heavy tables |
| **VACUUM** | `spark.sql("VACUUM tableName RETAIN 168 HOURS")` | Daily/weekly to purge stale file versions |
| **OPTIMIZE + ZORDER** | `spark.sql("OPTIMIZE tableName ZORDER BY (DateKey)")` | When queries frequently filter by specific columns |

**Critical:** VACUUM retention must be longer than the interval between
framings — otherwise Direct Lake references deleted Parquet files → query errors.

### Row Group Size Guidelines

| Row Group Size | Assessment | Action |
|---|---|---|
| 1M – 16M rows | Optimal | Default Fabric behavior — no action needed |
| > 16M rows | Acceptable | Fabric may use larger for compressible data |
| < 1M rows | Problematic | Too many small segments — run OPTIMIZE |
| < 10K rows | Critical | Streaming ingestion artifact — OPTIMIZE immediately |

### Partition Strategy for Delta Tables

Use low-cardinality columns for Delta table partitioning:

```
Good:  PARTITIONED BY (year_month)          →  ~60 partitions for 5 years
Good:  PARTITIONED BY (region)              →  ~10 partitions
Bad:   PARTITIONED BY (customer_id)         →  100,000+ partitions → too many files
Bad:   PARTITIONED BY (date)                →  1,825 partitions for 5 years → borderline
```

**Benefits:**
- Constrains OPTIMIZE/VACUUM to changed partitions only
- Enables incremental framing to preserve most segments
- Reduces file counts per partition (stays within guardrails)

**Rule:** Partition column should have < 100-200 distinct values.

---

## Composite Model Patterns with Direct Lake

### Pattern 1: Direct Lake + Import (Most Common)

```
Direct Lake tables:  Fact tables from Lakehouse (large, auto-refreshed)
Import tables:       Small reference tables, calculated tables, Power Query transforms
Dimensions:          Dual mode (bridges both sides)
```

**When to use:**
- Fact data in Lakehouse + reference data from external sources
- Need calculated columns (not supported on Direct Lake tables)
- Self-service analyst needs to add local data to IT-managed lakehouse

**Requirements:**
- Only supported for **Direct Lake on OneLake**
- Can add Import tables via Power BI web modeling or Desktop live edit
- DirectQuery tables can be added via XMLA tools

### Pattern 2: Chained Composite Model (Extend Existing Direct Lake)

```
Published Direct Lake semantic model  ← DirectQuery chained connection
Local Import/DQ tables               ← Additional data sources
```

**When to use:**
- IT publishes a Direct Lake model; analyst extends with local data
- Need to combine Direct Lake model with other data sources
- Works for both DL on OneLake and DL on SQL endpoints

### Unsupported Combinations

| Scenario | Supported? |
|---|---|
| DL on OneLake + Import tables | ✅ Yes |
| DL on OneLake + DQ tables (via XMLA) | ✅ Yes |
| DL on SQL + Import tables in same model | ❌ No — use chained composite instead |
| DL on SQL + DQ tables in same model | ❌ No |
| Calculated columns referencing DL columns | ❌ No — compute upstream in Lakehouse |
| User-defined aggregation tables on DL | ❌ No — aggregate at Delta table level |

---

## Direct Lake Limitations

Key limitations to validate before choosing Direct Lake:

| Limitation | Impact | Workaround |
|---|---|---|
| No calculated columns on DL tables | Cannot add computed columns in model | Pre-compute in Lakehouse ETL |
| No hybrid tables | Cannot mix Import + DQ partitions | Use full Direct Lake or full Import |
| No user-defined aggregation tables | Cannot create Import agg on DL tables | Pre-aggregate in Lakehouse |
| No model-level table partitions | Cannot use incremental refresh partitions | Partition at Delta table level |
| Requires Fabric capacity (F/P SKU) | Not available on Pro license | Use Import for Pro workspaces |
| Cannot develop fully offline | Need Fabric workspace connection | Import for offline development |
| No personal workspaces (My Workspace) | Must use standard workspace | Create a dev workspace |
| Cross-region not supported | Model and source must be same region | Use shortcuts to bring data to same region |
| Bidirectional relationships | May not work with OneLake security RLS | Use single-direction + DAX |
| String column max 32,764 chars | Long text columns may truncate | Trim in Lakehouse ETL |

---

## Direct Lake vs Import — Decision Guide

| Factor | Choose Direct Lake | Choose Import |
|---|---|---|
| Data volume | > 1 GB or fast-growing | < 1 GB and stable |
| Data freshness | Need < 1 hour latency | Daily/weekly refresh acceptable |
| Infrastructure | Fabric capacity available | Pro/PPU license only |
| Development workflow | Team can publish to Fabric workspace | Need offline/Desktop-only development |
| Calculated columns needed | Can pre-compute in Lakehouse | Must compute in model |
| Data preparation | Done upstream (Spark, Dataflows, T-SQL) | Done in Power Query (model author) |
| Self-service augmentation | Use composite model (DL + Import) | Native Import model |

### Migration Path: Import → Direct Lake

```
1. Move data into Fabric Lakehouse (Delta format)
2. Apply V-Order: ensure OPTIMIZE runs with V-Order enabled
3. Verify guardrails: check table row counts vs. SKU limits
4. Create new Direct Lake semantic model pointing to Lakehouse
5. Recreate measures (DAX transfers directly)
6. Move calculated columns to Lakehouse ETL (Spark/SQL)
7. Test with DirectLakeBehavior = DirectLakeOnly to catch fallback
8. Validate report performance: cold and warm state benchmarks
9. Switch production reports to new model
```

---

## Monitoring Direct Lake

### Fabric Capacity Metrics App

Monitor these Direct Lake-specific metrics:
- Direct Lake framing operations count and duration
- DirectQuery fallback frequency
- Memory consumption vs. SKU limits
- Capacity unit consumption per model

### DMV Queries (via DAX Studio or XMLA)

```sql
-- Check table storage modes
SELECT [Name], [StorageMode], [RefreshTime]
FROM $SYSTEM.TMSCHEMA_TABLES

-- Check column segment residency (warm/cold analysis)
SELECT *
FROM $SYSTEM.DISCOVER_STORAGE_TABLE_COLUMN_SEGMENTS
WHERE [TABLE_ID] = 'YourTableName'

-- Check row counts per table
SELECT [TableName], [RowsCount]
FROM $SYSTEM.DISCOVER_STORAGE_TABLES
WHERE [RowsCount] > 0
```

### Delta Analyzer (Notebook)

```python
import sempy_labs as labs

# Analyze Delta table health
results = labs.delta_analyzer("your_table_name")

# Key outputs:
# - Summary: row count, row groups, files, V-Order status, total size
# - Row group size distribution
# - Parquet file details
```

---

## Quick Reference

| Topic | Key Point |
|---|---|
| Engine | VertiPaq (same as Import) — DAX performance comparable to Import |
| Refresh | Framing (seconds) — metadata only, no data copy |
| Data source | Delta tables in OneLake (Lakehouse or Warehouse) |
| Licensing | Fabric capacity (F SKU) or Premium (P SKU) required |
| Guardrails | Per-SKU limits on rows, files, row groups — exceed → fail or fallback |
| Fallback | DL on OneLake: no fallback (errors). DL on SQL: DirectQuery fallback |
| V-Order | Must be enabled — dramatically improves transcoding speed |
| OPTIMIZE | Run regularly to compact small files → stay within guardrails |
| VACUUM | Run regularly but retain versions longer than framing interval |
| Composite | DL on OneLake + Import supported. DL on SQL: use model chaining |
| Calculated columns | Not supported on DL tables — pre-compute in Lakehouse |
| Development | Requires Fabric workspace; cannot work fully offline |
| Monitoring | Capacity Metrics App + DMVs + Delta Analyzer |
