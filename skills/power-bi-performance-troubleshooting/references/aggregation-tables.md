# Aggregation Tables

Pre-computed summary tables that Power BI queries instead of scanning the full
detail table. The single most impactful optimization for large datasets.

---

## When to Use Aggregation Tables

| Scenario | Detail Rows | Benefit |
|---|---|---|
| Fact table > 10M rows with summary-level reports | 10M–1B+ | 10-100x faster |
| Dashboard page loads > 5s due to large table scans | Any large | Dramatic reduction |
| DirectQuery with slow source but common aggregated queries | Any | Reduces source load |
| Composite model mixing Import + DQ | Any | DQ fallback to Import agg |

### When NOT to Use

- Detail tables < 1M rows (Import mode is already fast enough)
- Reports primarily show row-level detail (aggregation doesn't help)
- Highly dynamic filters that rarely match aggregation granularity

---

## Aggregation Design Pattern

### Step 1: Identify Aggregation Granularity

Analyze which dimensions your report visuals group by:

```
If dashboard shows:
  Revenue by Year, Region, Product Category
Then aggregate at:
  [Year] × [Region] × [ProductCategory] → SUM(Revenue), SUM(Quantity), COUNT(Orders)
```

**Rule:** Aggregate at the LOWEST granularity your summary visuals need.
If some visuals need Month and others need Year, aggregate at Month
(Year can be derived from Month).

### Step 2: Create the Aggregation Table

```dax
-- In Power Query (M), group the detail table:
= Table.Group(
    Sales,
    {"Year", "Month", "RegionKey", "ProductCategoryKey"},
    {
        {"Revenue_Sum", each List.Sum([Revenue]), type number},
        {"Quantity_Sum", each List.Sum([Quantity]), type number},
        {"OrderCount", each Table.RowCount(_), Int64.Type}
    }
)
```

**Naming convention:** `Agg_Sales_Monthly` — prefix with `Agg_`, include
the source table name and the granularity.

### Step 3: Configure Aggregations in Power BI

1. Select the aggregation table in Model view
2. Right-click → **Manage aggregations**
3. Map each column:

| Aggregation Column | Summarization | Detail Table | Detail Column |
|---|---|---|---|
| Revenue_Sum | Sum | Sales | Revenue |
| Quantity_Sum | Sum | Sales | Quantity |
| OrderCount | Count | Sales | OrderID |
| Year | GroupBy | Date | Year |
| Month | GroupBy | Date | Month |
| RegionKey | GroupBy | Region | RegionKey |
| ProductCategoryKey | GroupBy | Product | CategoryKey |

4. **Hide the aggregation table** from Report view — users should never see
   or reference it directly. Power BI routes queries automatically.

---

## Composite Model Configuration

In a Composite model, aggregation tables work as an Import-mode cache for
DirectQuery detail tables:

```
┌──────────────────────┐     ┌─────────────────────┐
│  Agg_Sales_Monthly   │     │       Sales          │
│  (Import mode)       │────▶│  (DirectQuery)       │
│  100K rows           │     │  500M rows           │
│  Refreshes hourly    │     │  Live from source     │
└──────────────────────┘     └─────────────────────┘

Query: SUM(Revenue) by Month, Region
  → Hits Agg_Sales_Monthly (Import) ✅ Fast

Query: SUM(Revenue) by Date, Customer, Product
  → Falls through to Sales (DirectQuery) ⚠️ Slower
```

### Storage Mode Settings

| Table | Storage Mode | Purpose |
|---|---|---|
| Agg_Sales_Monthly | Import | Fast aggregation cache |
| Sales (detail) | DirectQuery | Live detail-level queries |
| Date dimension | Dual | Bridges Import and DQ tables |
| Region dimension | Dual | Bridges Import and DQ tables |

**Important:** Dimension tables shared between Import and DQ tables MUST be
set to **Dual** storage mode. Otherwise, the engine cannot bridge the
relationship and aggregation hits will fail.

---

## Supported Aggregation Functions

| Summarization | Detail Column Type | Notes |
|---|---|---|
| Sum | Numeric | Most common |
| Min | Numeric, Date | |
| Max | Numeric, Date | |
| Count | Any | Counts non-blank values |
| CountRows (table) | N/A | Maps to COUNTROWS |
| GroupBy | Any | Dimension key mapping |

**Not supported natively:**
- Average → Use Sum + Count, compute average in DAX
- Distinct Count → Requires special handling (pre-computed in agg table)
- Median, Percentile → Cannot be aggregated; always falls through to detail

---

## Monitoring Aggregation Hits

### In DAX Studio (Server Timings)

After running a query with Server Timings enabled:

- **AggregationHit = true** → Query used the aggregation table ✅
- **AggregationHit = false** → Query fell through to detail table ⚠️

### Common Reasons for Aggregation Miss

| Reason | Fix |
|---|---|
| Query groups by a column not in the aggregation | Add column to agg table, or accept fallthrough |
| Query uses an unsupported aggregation (e.g., DISTINCTCOUNT) | Pre-compute in agg table |
| Filter context includes a column not in the agg table | Add the filter column to agg or remove filter |
| Dimension table not set to Dual mode | Change storage mode to Dual |
| Aggregation mappings misconfigured | Review Manage Aggregations dialog |
| Measure uses CALCULATE with complex filters | Simplify or accept fallthrough |

### Aggregation Hit Rate Target

| Hit Rate | Assessment | Action |
|---|---|---|
| > 90% | Excellent | Maintain current design |
| 70-90% | Good | Review missed queries; add columns if feasible |
| 50-70% | Moderate | Redesign aggregation granularity |
| < 50% | Poor | Aggregation is not helping; reconsider approach |

---

## Multi-Level Aggregation

For very large datasets, create multiple aggregation levels:

```
Level 1: Agg_Sales_Daily     (Date × Region × Product)     →  5M rows
Level 2: Agg_Sales_Monthly   (Month × Region × Category)   → 50K rows
Level 3: Agg_Sales_Yearly    (Year × Region)                →  500 rows

Query at Year+Region level → hits Level 3 (fastest)
Query at Month+Category   → hits Level 2
Query at Date+Product     → hits Level 1
Query at Date+Customer    → falls through to detail (100M rows)
```

**Cost:** More aggregation tables = more storage + more refresh time.
Only add levels that serve frequent query patterns.

---

## Quick Reference

| Design Decision | Recommendation |
|---|---|
| Minimum detail table size for aggregation | > 10M rows |
| Aggregation granularity | Lowest level your dashboards use |
| Naming convention | `Agg_[SourceTable]_[Granularity]` |
| Visibility | Always hidden from Report view |
| Dimension storage mode | Dual (when bridging Import ↔ DQ) |
| Target hit rate | > 80% of dashboard queries |
| Monitoring tool | DAX Studio → Server Timings |
| Refresh cadence | Match or exceed dashboard SLA |
