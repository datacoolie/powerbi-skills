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

Models mixing Import and DirectQuery:

1. **Keep dimensions in Import mode** — faster filtering and relationships
2. **Use DISTINCTCOUNT carefully** — forces full scan in DirectQuery
3. **Minimize cross-engine queries** — VertiPaq-to-DirectQuery joins are expensive
4. **TREATAS is better than FILTER** for cross-source virtual relationships

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
