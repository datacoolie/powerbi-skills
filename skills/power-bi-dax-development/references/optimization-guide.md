# DAX Optimization Guide

Performance optimization strategies based on "Optimizing DAX"
(Ferrari & Russo, 2nd Ed, 2024) and VertiPaq engine internals.

---

## Engine Architecture

The DAX query engine has two components:

| Component | Role | Threading |
|-----------|------|-----------|
| **Formula Engine (FE)** | Parses DAX, builds query plan, orchestrates execution | Single-threaded |
| **Storage Engine (SE)** | Scans VertiPaq/DirectQuery, returns data caches | Multi-threaded |

**Goal**: Push as much work as possible to the SE (multi-threaded) and
minimize FE processing (single-threaded bottleneck).

### Key Implications

- **Iterators** that cannot be pushed to SE run row-by-row in FE → slow
- **Context transitions** inside iterators create one SE query per row
- **CallbackDataID** in a query plan = FE is handling logic that SE cannot → performance risk
- **Complex IF/SWITCH** inside SUMX forces callback → move conditions to CALCULATE

---

## VertiPaq Encoding & Cardinality

VertiPaq stores each column using one of three encodings:

| Encoding | When Used | Size |
|----------|-----------|------|
| **Value encoding** | Low cardinality integers | Smallest (in-memory math) |
| **Hash encoding** | Strings, high-cardinality numbers | Larger (dictionary + index) |
| **RLE (Run-Length)** | Post-sort compression on columns | Depends on sort order |

### Cardinality Is the #1 Factor

Column cardinality (number of distinct values) is the single biggest driver
of model size and query speed:

1. **Remove unused columns** — they still consume memory
2. **Reduce cardinality** — round decimals, bin dates to month, group rare categories
3. **Split high-cardinality columns** — e.g., datetime → date + time
4. **Avoid calculated columns** on fact tables — they prevent compression optimization
5. **Prefer INT over STRING** for keys — value encoding is faster than hash encoding

### Sort Order Matters

VertiPaq sorts each table by the column with lowest entropy first.
Best practices:
- **Star schema** helps: dimension keys have good compression
- Avoid sorting fact tables by high-cardinality columns
- Use `ORDER BY` in partition expressions when possible

---

## CALCULATE Optimization

### Rule 1: Use Separate Arguments (Not AND/OR)

Each CALCULATE filter argument is evaluated independently and merged.
Combining filters in a single FILTER is slower because it becomes a single
table scan.

```dax
-- BAD: Single FILTER with AND (scans full table in FE)
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(DimProduct),
        DimProduct[Color] = "Red" && DimProduct[Brand] = "Contoso"
    )
)

-- GOOD: Separate arguments (each pushed to SE independently)
CALCULATE(
    [Total Sales],
    DimProduct[Color] = "Red",
    DimProduct[Brand] = "Contoso"
)
-- Benchmark: Up to 12x faster on large models
```

### Rule 2: Filter Dimension Tables, Not Fact Tables

```dax
-- BAD: Filters fact table (huge table scan)
CALCULATE(
    [Total Sales],
    FILTER(FactSales, FactSales[Quantity] > 10)
)

-- GOOD: If possible, move filter to dimension or use column filter
CALCULATE(
    [Total Sales],
    FactSales[Quantity] > 10  -- Simple column predicate, SE-friendly
)
```

### Rule 3: Prefer Column Filters Over Table Filters

Simple column predicates like `Table[Column] = Value` are optimized by the
engine into direct SE filters. FILTER() over a full table forces FE scan.

```dax
-- SE-optimized (column predicate)
CALCULATE([Total Sales], DimProduct[Color] = "Red")

-- FE scan (table filter)
CALCULATE([Total Sales], FILTER(ALL(DimProduct), DimProduct[Color] = "Red"))
```

Use FILTER() only when you need:
- Multi-column conditions on the same row
- Complex expressions that reference measures

---

## Iterator Optimization

Iterators (SUMX, AVERAGEX, MAXX, MINX, COUNTX, FILTER) evaluate an
expression row by row. They perform well when the expression can be pushed
to SE.

### Avoid IF/SWITCH Inside Iterators

```dax
-- BAD: IF forces callback to FE for each row
SUMX(
    FactSales,
    IF(FactSales[Type] = "Online", FactSales[Amount] * 1.1, FactSales[Amount])
)

-- GOOD: Split into two CALCULATE calls (each fully SE)
VAR _onlineSales =
    CALCULATE(SUMX(FactSales, FactSales[Amount] * 1.1), FactSales[Type] = "Online")
VAR _otherSales =
    CALCULATE(SUM(FactSales[Amount]), FactSales[Type] <> "Online")
RETURN
    _onlineSales + _otherSales
-- Benchmark: 5-7.5x faster
```

### FILTER Over Fact Tables — Use Column Subset

When you must filter a fact table, limit columns to reduce datacache size:

```dax
-- BAD: Iterates full fact table schema
FILTER(FactSales, FactSales[Amount] > 100)

-- BETTER: Use ADDCOLUMNS on a key column to limit materialisation
FILTER(
    SELECTCOLUMNS(FactSales, "Key", FactSales[SalesKey], "Amt", FactSales[Amount]),
    [Amt] > 100
)
```

---

## Context Transition Cost

Every context transition inside an iterator generates a separate SE query.

| Scenario | Cost |
|----------|------|
| Measure in SUMX over **dimension table** (few rows) | Acceptable |
| Measure in SUMX over **fact table** (millions of rows) | Very expensive |
| Nested context transitions (measure calling measure in iterator) | Compounding cost |

### Safe Pattern

```dax
-- OK: Iterating over a small dimension table
SUMX(
    VALUES(DimProduct[ProductKey]),  -- Typically < 10K rows
    [Profit Margin]                  -- Context transition per product
)

-- DANGEROUS: Iterating over fact table with measure reference
SUMX(
    FactSales,                       -- Millions of rows
    [Calculated Metric]              -- Context transition per row = millions of SE queries
)
```

---

## Materialization

**Materialization** = the SE creating a temporary in-memory table (datacache)
to hold intermediate results.

### Early vs. Late Materialization

| Type | Description | Impact |
|------|-------------|--------|
| **Early** | Large datacache created before FE processes | Large memory, slow |
| **Late** | Small datacaches, combined by FE | Less memory, usually faster |

### Signs of Bad Materialization

- **Large datacache** (millions of rows in Server Timings)
- **1 SE query** returning everything rather than many small ones
- **High FE time** relative to SE time

### How to Fix

1. Use SUMMARIZE instead of ADDCOLUMNS when grouping (avoids early materialization)
2. Remove unnecessary columns from iterator expressions
3. Break complex expressions into simpler CALCULATE calls
4. Use TREATAS instead of FILTER for virtual relationships

```dax
-- BAD: Early materialization — ADDCOLUMNS creates huge datacache
SUMX(
    ADDCOLUMNS(FactSales, "Margin", FactSales[Amount] - FactSales[Cost]),
    [Margin]
)

-- GOOD: Direct expression, no intermediate table
SUMX(FactSales, FactSales[Amount] - FactSales[Cost])
```

---

## DirectQuery Optimization

When tables use DirectQuery mode:

1. **Create proper indexes** on filtered/joined columns in the source database
2. **Minimize the number of columns** in visuals — each column = new SQL query
3. **Avoid complex DAX** — FE cannot push complex expressions to SQL
4. **Use aggregation tables** — pre-aggregated import-mode tables for common queries
5. **Limit cross-source joins** — joining DirectQuery to VertiPaq forces FE processing
6. **Set query reduction options** — apply filters on button click, reduce auto-refresh

### Aggregation Tables

```
User query → Engine checks agg table first
  → If agg table covers the query → Use fast Import mode
  → If not → Fall through to DirectQuery
```

Design aggregation tables with:
- GROUP BY on common dimension keys
- SUM/COUNT/MIN/MAX of fact measures
- Only the grain levels used in 80%+ of queries

---

## Composite Model Optimization

Models mixing Import and DirectQuery require special attention because queries
cross engine boundaries. Based on "Optimizing DAX" Ch. 20-22 (Ferrari & Russo).

### How Cross-Engine Queries Work

When a DAX query spans Import (local VertiPaq) and DirectQuery (remote) tables:

1. The local FE orchestrates the query
2. FE sends **DAX queries** (not xmSQL) to the remote engine
3. Remote engine returns datacaches to the local FE
4. Local FE combines results from both engines

**The critical bottleneck:** Data transferred between engines. Every column and
row in the datacache costs network time and local memory.

### The Table Filter Trap

Using FILTER on a full remote table forces the entire table to be serialized,
sent to the local engine, then sent back as a filter parameter — catastrophic:

```dax
-- CATASTROPHIC in composite models:
Customer in Segment =
SUMX(
    Segments,
    COUNTROWS(
        FILTER(
            Customer,                        -- Remote table
            [Sales Amount] > Segments[Min]   -- Context transition per segment row
            && [Sales Amount] <= Segments[Max]
        )
    )
)
-- Engine behavior:
-- 1. Downloads ALL columns of Customer table to local engine
-- 2. For each Segment row, sends Customer table BACK to remote as filter
-- 3. Remote evaluates [Sales Amount] per customer
-- 4. Entire Customer table returned again as a datacache
-- Result: Multiple round-trips with full table → query takes 30+ seconds

-- FIX: Use column references instead of table references
Customer in Segment =
SUMX(
    Segments,
    VAR _min = Segments[Min]
    VAR _max = Segments[Max]
    RETURN COUNTROWS(
        FILTER(
            VALUES(Customer[CustomerKey]),   -- Single column, not full table!
            VAR _custSales = [Sales Amount]
            RETURN _custSales > _min && _custSales <= _max
        )
    )
)
-- Only CustomerKey is transferred, not all Customer columns → 10-50x faster
```

**Golden rule for composite models:** Never use a full table reference when a
single column reference suffices. The engine sends ALL columns of any table
referenced in FILTER, even if only one column is needed.

### Cross-Engine Join Patterns

| Pattern | Performance | Notes |
|---------|-------------|-------|
| Import fact → Import dimension | Best | Standard VertiPaq join |
| DQ fact → DQ dimension (same source) | Good | Remote SQL join |
| DQ fact → Import dimension | Moderate | Dimension sent to remote as filter |
| Import fact → DQ dimension | Poor | Requires local materialization |
| DQ source A → DQ source B | Very poor | No direct join; FE handles both |

### DISTINCTCOUNT in DirectQuery

DISTINCTCOUNT forces the remote engine to scan the full column without
pre-aggregation optimizations. For large tables this is very slow:

```dax
-- Slow on DirectQuery:
# Unique Customers = DISTINCTCOUNT(Sales[CustomerKey])

-- Workaround: create an Import aggregation table with pre-computed distinct counts
-- Then use agg table for common queries; DirectQuery only as fallback
```

### Composite Model Optimization Checklist

```
□ All dimension tables are in Import or Dual mode (fastest filtering)
□ Dual mode dimensions eliminate cross-engine joins for mixed-mode queries
□ FILTER() never references a full remote table — use VALUES(Table[Column]) instead
□ Measures avoid context transition on remote fact tables
□ Aggregation tables cover 80%+ of common query patterns
□ TREATAS is used instead of FILTER for virtual relationships across engine boundaries
□ DISTINCTCOUNT on DQ tables is minimized or pre-aggregated
□ Server Timings checked for large datacaches (indicator of excessive materialization)
□ Number of DAX queries to remote server is monitored (each one = round-trip latency)
```

---

## Calculated Column vs. Runtime Trade-Off

Based on "Optimizing DAX" Ch. 2 (Ferrari & Russo). Deciding whether to
pre-compute a value in a calculated column or compute it at query time
in an iterator.

### Trade-Off Matrix

| Factor | Calculated Column | Runtime Iterator |
|--------|-------------------|-----------------|
| **Query speed** | Faster (pre-computed) | Slower (computed per query) |
| **Memory (RAM)** | Larger model (column stored in VertiPaq) | Smaller model |
| **Refresh time** | Longer (sequential, single-threaded) | No impact on refresh |
| **Compression** | Depends on cardinality of result | Not stored |
| **Flexibility** | Fixed at refresh time; no filter context | Context-aware |

### Decision Framework

Use a **calculated column** when:
- The expression involves **multiple columns** in a complex formula
  and the measure is used heavily across many visuals
- The formula is compute-intensive and the result has **low cardinality**
  (good compression, small RAM cost)
- You need to create a **relationship key** or **sort-by column**
- The value is needed for **VertiPaq indexing** (e.g., boolean flag column for
  fast filtering: `IsHighValue = Sales[Amount] >= 200`)

Use a **runtime expression** (measure/iterator) when:
- RAM is constrained and the column would have **high cardinality**
- The expression is simple (e.g., `Qty * Price`) — the iterator overhead is tiny
- The value must be **context-aware** (respond to filters)
- The calculation is used in **few visuals** (pre-computing for all rows is wasteful)

### How to Measure the Trade-Off

```
1. Create the calculated column; disable its AvailableInMDX property
2. Process the model; note refresh time increase
3. Check VertiPaq Analyzer: note RAM increase for the new column
4. Run a benchmark query with the calculated column (SUM of it)
5. Run the same benchmark with the iterator (SUMX with expression)
6. Compare:
   - If query speed improvement > 2x AND RAM increase < 10% → keep the column
   - If RAM increase > 15% with marginal speed improvement → remove the column
   - If the column is needed by only 1-2 reports → keep the iterator
```

### Alternative: Compute in Data Source

If a calculated column is beneficial but its RAM cost is too high, compute
it in the Power Query / SQL source instead:

```
-- In Power Query: add column at source (computed during ETL, not DAX)
= Table.AddColumn(Source, "LineAmount", each [Quantity] * [NetPrice], Decimal.Type)

-- Benefits:
-- Processed during parallel ETL (not sequential DAX calculated column)
-- Can be optimized by SQL Server column store indexes
-- Same RAM cost as calculated column, but faster refresh
```

---

## Performance Debugging Workflow

### Tools

| Tool | What It Shows |
|------|---------------|
| **DAX Studio → Server Timings** | FE time, SE time, SE query count, datacache sizes |
| **DAX Studio → Query Plan** | Logical/physical plan, materialization points |
| **Performance Analyzer** (Power BI Desktop) | Visual-level timing, DAX query generated |
| **VertiPaq Analyzer** | Model size, column cardinality, encoding, relationships |

### Step-by-Step

1. **Identify slow visual** → Performance Analyzer → copy DAX query
2. **Open DAX Studio** → paste query → enable Server Timings
3. **Run query** → check:
   - SE/FE ratio (SE should dominate; high FE = problem)
   - Number of SE queries (too many = context transition problem)
   - CallbackDataID presence (= FE handling what SE should)
   - Datacache row counts (large = materialization problem)
4. **Read query plan** → look for:
   - Early materialization → restructure to late materialization
   - Unnecessary columns → REMOVECOLUMNS or simplify
   - Missing SE pushdown → simplify expression for SE compatibility
5. **Optimize** → apply rules above → re-measure → compare

### Benchmarking Rules

- Always **clear cache** before benchmarking (`CTRL+F5` in DAX Studio)
- Run query **3+ times** and take the median
- Compare SE time separately from FE time
- Watch for **cold vs. warm** cache differences
- Document before/after with Server Timings screenshots

---

## Quick Reference: Optimization Checklist

| # | Check | Impact |
|---|-------|--------|
| 1 | Separate CALCULATE filter arguments | Up to 12x |
| 2 | Avoid IF/SWITCH inside iterators | 5-7.5x |
| 3 | Filter dimensions, not fact tables | 3-10x |
| 4 | No context transition on fact tables | 10-100x |
| 5 | Remove unused columns from model | Model size |
| 6 | Reduce column cardinality | Model size + speed |
| 7 | Use INT keys over STRING keys | Encoding + joins |
| 8 | Check for CallbackDataID in plans | FE bottleneck |
| 9 | Minimize cross-source joins | Composite models |
| 10 | Use aggregation tables for DirectQuery | Query speed |

---

## Direct Lake DAX Considerations

Direct Lake uses the same VertiPaq engine as Import, so most DAX patterns
work identically. However, some behaviors differ due to the on-demand
transcoding model and the potential for DirectQuery fallback.

### DAX Patterns That Work the Same

All standard DAX measures, CALCULATE, iterators, time intelligence patterns,
and SUMMARIZECOLUMNS work natively on Direct Lake tables. No DAX rewriting
is needed when migrating measures from Import to Direct Lake.

### Unsupported on Direct Lake Tables

| Feature | Impact | Workaround |
|---|---|---|
| Calculated columns | Cannot add to DL tables | Pre-compute in Lakehouse ETL (Spark/SQL) |
| Calculated tables referencing DL columns | Cannot reference DL column data | Use Import tables or compute upstream |
| Hybrid tables (mixed Import + DQ partitions) | Not supported | Use pure Direct Lake for the table |

### Fallback-Triggering Scenarios (DL on SQL Only)

These do NOT change DAX syntax but cause the engine to silently switch
to DirectQuery mode, degrading performance:

| Scenario | Why It Triggers Fallback |
|---|---|
| SQL analytics endpoint enforces RLS | DL can't read Parquet directly when SQL RLS applies |
| Source is a SQL view (not Delta table) | No Parquet files to read — must query SQL endpoint |
| Table exceeds capacity guardrails | Too many rows/files/row groups for the SKU |
| SQL-based column-level security | Security check requires SQL endpoint query |

**Tip:** Set `DirectLakeBehavior = DirectLakeOnly` during development to
surface these issues as errors instead of silent degradation.

### Performance Differences vs Import

| Aspect | Import | Direct Lake |
|---|---|---|
| First query (cold) | Fast (data already in memory) | Slower (must transcode from Parquet) |
| Subsequent queries (warm) | Fast | Equally fast (same VertiPaq engine) |
| After framing (refresh) | Full reload | Incremental — only changed segments evicted |
| Memory pressure | Evicted data requires full refresh | Evicted data re-transcodes on next query |

### Best Practices for Direct Lake DAX

1. **Use variables** — Reduce repeated SE scans; even more important in Direct
   Lake where cold-state SE scans involve Parquet reads
2. **Avoid excessive SUMMARIZECOLUMNS nesting** — Each visual generates
   SUMMARIZECOLUMNS; deeply nested measures can create many SE requests
3. **Filter dimensions, not facts** — Same as Import, but the penalty for
   scanning large Direct Lake fact columns is amplified in cold state
4. **Test in cold state** — Clear cache (`processClear` + `processFull` via
   XMLA) to simulate real-world first-query experience
