# DAX Studio Workflow for Performance Analysis

DAX Studio is the essential external tool for deep-dive performance diagnosis.
Use it after Performance Analyzer identifies a slow DAX query.

---

## Setup and Connection

### Opening DAX Studio

1. In Power BI Desktop with the report open:
   **External Tools** tab → **DAX Studio**
2. DAX Studio connects automatically to the local Analysis Services instance
3. Verify connection: bottom status bar shows the dataset name

### Key Tabs to Enable

Before running queries, enable these features:

- **Server Timings** — Toolbar → Server Timings button (⏱ icon) → ON
- **Query Plan** — Toolbar → Query Plan button → ON (optional, for advanced diagnosis)

---

## Server Timings Analysis

Server Timings is the most important diagnostic feature. It breaks query
execution into two engines:

### Formula Engine (FE) vs Storage Engine (SE)

| Engine | Role | Characteristics |
|---|---|---|
| **Formula Engine (FE)** | Processes DAX logic, iterates, evaluates expressions | Single-threaded, in-memory |
| **Storage Engine (SE)** | Scans data from the model (VertiPaq or DirectQuery) | Multi-threaded, disk/memory I/O |

### Reading Server Timings Output

After running a query with Server Timings enabled:

```
Total:          4,200 ms
  FE:           1,800 ms (43%)
  SE:           2,400 ms (57%)
  SE Queries:        12
  SE Cache:           3
```

| Metric | Meaning |
|---|---|
| Total | End-to-end query execution time |
| FE (Formula Engine) | Time spent in DAX evaluation |
| SE (Storage Engine) | Time spent scanning/reading data |
| SE Queries | Number of storage engine requests |
| SE Cache | SE requests served from cache (not re-scanned) |

### Diagnosis by FE/SE Ratio

| Pattern | Bottleneck | Common Cause | Fix |
|---|---|---|---|
| FE > 80% | Formula Engine | Row-by-row iteration, complex CALCULATE | Rewrite DAX to avoid SUMX/FILTER on large tables |
| SE > 80% | Storage Engine | Large table scans, missing aggregations | Add aggregation tables, reduce model size, optimize relationships |
| FE ≈ SE | Both | Complex query on large data | Address both: simplify DAX AND reduce data scanned |
| SE Queries > 20 | Too many scans | Measure with many sub-queries | Simplify measure, cache intermediate results with variables |

---

## Copying and Running DAX Queries

### From Performance Analyzer

1. In Performance Analyzer, expand a slow visual
2. Click **Copy query** — this copies the exact DAX query Power BI generated
3. Paste into DAX Studio query window

### Query Structure

Performance Analyzer queries look like:

```dax
// DAX Query
DEFINE
    VAR __DS0FilterTable =
        TREATAS({"2024"}, 'Date'[Year])

EVALUATE
    SUMMARIZECOLUMNS(
        'Product'[Category],
        __DS0FilterTable,
        "Revenue", [Total Revenue],
        "Quantity", [Total Quantity]
    )
```

**Do NOT modify the query structure** when benchmarking. Run it as-is to
reproduce the exact performance characteristics.

### Benchmarking Protocol

1. **Clear cache first:** In DAX Studio → Run button dropdown → **Clear Cache then Run**
2. **Run 3 times** with cache clearing between runs
3. **Record median** of the 3 runs (cold cache = worst case)
4. **Run once WITHOUT clear cache** to see warm-cache performance

```
Cold cache runs:   3200ms, 3100ms, 3400ms → Median: 3200ms
Warm cache run:    450ms
```

---

## CallbackDataID Analysis

In the Server Timings detail, each SE query shows a **CallbackDataID**:

- **Same CallbackDataID** across multiple SE queries = same logical scan
  (the engine split it for parallelism) — Normal behavior
- **Different CallbackDataIDs** = different logical requests — Each represents
  a separate data scan (look for redundant scans)

### What to Look For

| Pattern | Meaning | Action |
|---|---|---|
| 1-3 unique CallbackDataIDs | Efficient query | Normal — no action needed |
| 5-10 unique CallbackDataIDs | Moderately complex | Review if all scans are necessary |
| 10+ unique CallbackDataIDs | Over-complex query | Measure likely has nested iterations — simplify |
| Large datacache sizes (> 1M rows) | SE returning too much data | Add filters, reduce granularity |

---

## Datacache Sizes

Each SE query returns a **datacache** — a temporary result set passed to FE.

### Reading Datacache Output

In Server Timings, the SE queries show rows returned:

```
SE Query 1: 150 rows      ← Small, efficient
SE Query 2: 50,000 rows   ← Moderate
SE Query 3: 2,500,000 rows ← PROBLEM — FE must iterate over 2.5M rows
```

### Datacache Size Guidelines

| Rows Returned | Assessment | Action |
|---|---|---|
| < 1,000 | Excellent | No optimization needed |
| 1,000 - 100,000 | Acceptable | Monitor but likely OK |
| 100,000 - 1,000,000 | Warning | Can FE handle this? Check FE time |
| > 1,000,000 | Critical | Rewrite DAX to push aggregation into SE |

**Goal:** Push as much computation as possible into the Storage Engine
(multi-threaded) so the Formula Engine (single-threaded) receives small
datacaches.

---

## VertiPaq Analyzer

VertiPaq Analyzer shows the physical storage structure of your model:

### Running VertiPaq Analyzer

In DAX Studio → **Advanced** tab → **View Metrics** (or Ctrl+Alt+M)

### Key Metrics

| Metric | What It Shows | Target |
|---|---|---|
| Table Size | Total memory consumption per table | Identify largest tables |
| Column Cardinality | Unique values per column | High cardinality = large dictionaries |
| Column Size | Memory used by column data + dictionary | Target for optimization |
| Encoding | Hash vs. Value encoding | Value encoding is more efficient |
| Rows | Row count per table/partition | Verify expected counts |
| Relationship Size | Memory used by relationship indexes | Large = many-to-many or high cardinality |

### Optimization Actions by Finding

| Finding | Optimization |
|---|---|
| Column with high cardinality + large size | Remove if unused; reduce precision (round numbers) |
| Large text columns | Move to a separate dimension table |
| Unused columns consuming memory | Remove from model |
| Table with unnecessary detail rows | Aggregate to higher granularity |
| Large relationship sizes | Review cardinality; consider bridge tables |

### Model Size Budget

| Model Size | Assessment |
|---|---|
| < 100 MB | Small — no concerns |
| 100-500 MB | Medium — optimize largest columns |
| 500 MB - 1 GB | Large — aggressive optimization needed |
| > 1 GB | Very large — consider aggregation tables or DirectQuery |

---

## End-to-End DAX Studio Workflow

### For a Slow Visual

```
1. Performance Analyzer → Identify slow visual → Copy DAX query
2. DAX Studio → Paste query
3. Enable Server Timings → Clear Cache then Run
4. Check FE vs SE split:
   - FE heavy → DAX complexity problem → Rewrite measure
   - SE heavy → Data volume problem → Add aggregations / reduce model
5. Check SE queries:
   - Too many CallbackDataIDs → Simplify measure
   - Large datacaches → Push aggregation into SE
6. Run 3× for benchmarking → Record cold-cache median
7. Apply fix → Re-benchmark → Compare
```

### For Model Size Review

```
1. DAX Studio → View Metrics (VertiPaq Analyzer)
2. Sort tables by size → Identify top 3 largest
3. For each large table:
   a. Sort columns by size → Identify top consumers
   b. Check cardinality → High cardinality columns using most memory
   c. Check if column is used in any report visuals
   d. Remove unused columns or reduce cardinality
4. Re-run View Metrics → Compare total model size
```

---

## Quick Reference

| Task | DAX Studio Feature |
|---|---|
| Measure execution time | Server Timings |
| FE vs SE split | Server Timings → Total/FE/SE |
| Number of data scans | Server Timings → SE Queries |
| Rows returned per scan | Server Timings → Datacache sizes |
| Logical query plan | Query Plan tab |
| Model memory breakdown | View Metrics (VertiPaq Analyzer) |
| Column cardinality | View Metrics → Column details |
| Clear cache + run | Run dropdown → Clear Cache then Run |
| Cold-cache benchmark | Clear Cache then Run × 3 → Median |
