# VertiPaq Optimization Guide

How to design a Power BI semantic model so VertiPaq compresses it
efficiently and queries run fast. Based on "Optimizing DAX" (Ferrari &
Russo, 2nd Ed, 2024).

---

## How VertiPaq Works

VertiPaq is the in-memory columnar store that powers Import and DirectLake
models. Each column is compressed and stored independently.

**Compression pipeline per column:**
1. Build a dictionary of distinct values (hash encoding for strings)
2. Encode each row as a dictionary index
3. Apply RLE (Run-Length Encoding) on the sorted index list

**Query pipeline:**
- Storage Engine (SE) scans columns in parallel (multi-threaded)
- Formula Engine (FE) orchestrates and finalizes results (single-threaded)
- Goal: maximize work done by SE, minimize FE work

---

## The #1 Factor: Column Cardinality

**Cardinality** = number of distinct values in a column.

Lower cardinality → smaller dictionary → better RLE → smaller model → faster queries.

| Cardinality | Effect |
|---|---|
| 1 (constant) | Single dictionary entry, maximum RLE — essentially free |
| < 100 | Excellent compression, fast scans |
| < 10,000 | Good for dimension columns |
| 100,000+ | Poor compression, slow scans — review if column is needed |
| Millions | Hash encoding required, often as large as the source data |

---

## Encoding Types

### Value Encoding (best)
Applied to **integers** with a reasonably small range.
The values themselves become the dictionary — no extra overhead.

```
DateKey INT (20200101 to 20241231) → ~1825 distinct values → value encoding
CustomerKey INT (1 to 1,000,000) → may fall back to hash at high cardinality
```

### Hash Encoding (common)
Applied to **strings** and high-cardinality numbers. A dictionary maps each
distinct value to a compact integer index. Higher cardinality = larger
dictionary.

```
CustomerName TEXT (1M distinct names) → dictionary of 1M entries
ProductCode TEXT ("PRD-00001" to "PRD-10000") → 10K dictionary entries
```

### RLE (Run-Length Encoding)
Applied **on top of** value or hash encoding, after segments are sorted.
If adjacent rows have the same encoded value, they are stored as a single
(value, count) pair.

```
Before RLE: [1, 1, 1, 1, 1, 2, 2, 3, 3, 3, ...]
After RLE:  [(1,5), (2,2), (3,3), ...]   ← much smaller
```

RLE benefits most from:
- Low cardinality columns
- Columns that sort well (grouped values, not random)
- Dimension columns (Region, Category, Year) in fact tables

---

## Column Design Rules

### Rule 1: Remove Unused Columns

Hidden columns still consume memory and are still compressed. **Remove** any
column not used in relationships, measures, visuals, or filters.

```
-- In Power Query, remove at source before load:
= Table.RemoveColumns(Source, {"DebugField", "InternalCode", "LegacyID"})
```

Check with VertiPaq Analyzer: columns sorted by "Size" column show the
biggest wins.

### Rule 2: Never Use DateTime as a Relationship Key

A DateTime column (date + time component) has cardinality equal to the
number of unique timestamps — potentially millions.

```
Bad:  FactSales[OrderDateTime] DATETIME (1M distinct timestamps) → huge dictionary
Good: FactSales[OrderDateKey] INT (YYYYMMDD, e.g. 20241231) → ~1825 distinct values
```

Always separate date and time:
- `OrderDateKey` INT (YYYYMMDD) — for relationships
- `OrderTimeKey` INT (HHMM or HHMMSS) if time detail is needed
- Or strip time in Power Query: `Date.From([OrderDateTime])`

### Rule 3: Use INT Keys, Not TEXT Keys

Integer keys use value encoding. Text keys use hash encoding with a string
dictionary — larger and slower.

```
Bad:  FactSales[ProductCode] TEXT "PRD-00001"  → hash encoding
Good: FactSales[ProductKey] INT 1 to 10000     → value encoding
```

If you must use text codes, add a surrogate INT key in the dimension and
use that for the relationship.

### Rule 4: Never Put Calculated Columns on Fact Tables

Calculated columns on fact tables:
- Are computed after data loads, from scratch on each refresh
- Prevent VertiPaq from applying its optimal sort order
- Block RLE compression on adjacent columns
- Inflate model size significantly for large tables

```
-- BAD: Calculated column on FactSales (10M rows)
Profit = FactSales[Revenue] - FactSales[Cost]

-- GOOD: DAX measure (no storage, computed on demand)
[Profit] = SUM(FactSales[Revenue]) - SUM(FactSales[Cost])

-- ALSO GOOD: Pre-compute in Power Query (before load = no compression penalty)
= Table.AddColumn(Source, "Profit", each [Revenue] - [Cost], type number)
```

### Rule 5: Reduce String Column Cardinality

High-cardinality text columns are the most common cause of oversized models.

| Strategy | Example |
|---|---|
| Move to dimension | Don't store CustomerName in FactSales — join to DimCustomer |
| Categorize | Map 10K product codes → 50 product categories |
| Truncate | Store ZIP5 "12345" not ZIP9 "12345-6789" |
| Remove precision | Round "1.23456789" to "1.23" |
| Strip constants | Remove common prefix "PROD-" from every row |

### Rule 6: Bin Continuous Numeric Values

If a numeric column is used for grouping (not aggregation), bin it to
reduce cardinality:

```m
-- In Power Query: create a Price Tier column from Price
PriceTier = if [Price] < 10 then "Low"
            else if [Price] < 50 then "Medium"
            else "High"
```

Store the original Price in the fact table for SUM/AVG but use the binned
tier column for slicing/grouping in visuals.

---

## Relationship Key Design

Relationships join tables on key columns. The key column design affects
both model size and query speed.

| Key Type | Encoding | Join Speed | Recommendation |
|---|---|---|---|
| INT surrogate (1, 2, 3...) | Value | Fastest | Best practice |
| INT YYYYMMDD date key | Value | Fast | Use for date dimensions |
| BIGINT natural key | Value/Hash | Medium | Acceptable |
| TEXT natural key | Hash | Slowest | Avoid if possible |
| GUID text | Hash | Very slow | Always replace with INT |

### Referential Integrity

Enable referential integrity on Import mode relationships. This signals to
VertiPaq that there are no orphaned rows, allowing it to skip null checks
during scans — measurable speed improvement on large fact tables.

```
In powerbi-modeling-mcp/relationship_operations:
"assumeReferentialIntegrity": true
```

---

## Dimension vs. Fact Table Rules

| Rule | Dimension Tables | Fact Tables |
|---|---|---|
| Calculated columns | Acceptable (small tables) | **Avoid** |
| Text columns | Fine (filtering/grouping) | Only if necessary |
| DateTime columns | Use Date + separate Time | Use INT DateKey |
| Cardinality target | Any (small row count) | Minimize per column |
| Unused columns | Remove | **Must remove** |

---

## Model Size Targets

| Capacity | Import Limit | Practical Target |
|---|---|---|
| Shared (free/Pro) | ~1 GB | < 250 MB |
| Premium Per User | 100 GB | < 10 GB |
| Premium / Fabric | 400 GB | Size appropriate |

Use **VertiPaq Analyzer** (free in DAX Studio) to measure:
- Total model size
- Top columns by size
- Cardinality per column
- RLE ratio per column

---

## Quick Checklist

```
□ No DateTime relationship keys (split to Date + Time)
□ INT surrogate keys on all relationships
□ All unused columns removed (not just hidden)
□ No calculated columns on fact tables with > 1M rows
□ High-cardinality text columns moved to dimensions or removed
□ Referential integrity enabled for Import mode relationships
□ VertiPaq Analyzer shows RLE ratio > 3x on common columns
□ Model size under capacity target
```
