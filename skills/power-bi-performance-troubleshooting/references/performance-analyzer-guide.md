# Performance Analyzer Guide

How to use Performance Analyzer in Power BI Desktop to identify visual-level
performance bottlenecks. This is always the **first step** in any performance
investigation.

---

## Opening Performance Analyzer

1. In Power BI Desktop, go to **View** tab → **Performance Analyzer**
2. The Performance Analyzer pane opens on the right
3. Click **Start recording**
4. Interact with the report (navigate pages, click slicers, refresh visuals)
5. Click **Stop** when done
6. Analyze the captured events

Alternatively, click **Refresh visuals** to force all visuals on the current
page to re-query and re-render — this gives a complete page load profile.

---

## Reading the Output

Each visual is listed with its total duration and three sub-components:

| Component | What It Measures | Typical Range |
|---|---|---|
| **DAX Query** | Time for the engine to execute the visual's query | 10ms – 30,000ms |
| **Visual Display** | Time for the visual to render in the browser/canvas | 5ms – 2,000ms |
| **Other** | Time waiting for other visuals, network, or internal overhead | 0ms – 5,000ms |

### Interpreting Results

```
Performance Analyzer Results:
┌──────────────────────────────────────────────────────────┐
│ Visual Name          │ Total │ DAX Query │ Display │ Other│
├──────────────────────┼───────┼───────────┼─────────┼──────┤
│ card-total-revenue   │  120  │    85     │   30    │   5  │  ← OK
│ line-trend-monthly   │  450  │   380     │   65    │   5  │  ← OK
│ matrix-detail        │ 8200  │  7800     │  350    │  50  │  ← DAX problem
│ slicer-category      │ 3100  │  2900     │  180    │  20  │  ← DAX problem
│ scatter-customers    │ 1500  │   200     │ 1250    │  50  │  ← Render problem
└──────────────────────────────────────────────────────────┘
```

### Decision Matrix

| If... | Then... | Next Action |
|---|---|---|
| DAX Query is the largest component | Query or model problem | Copy query → DAX Studio |
| Visual Display is the largest component | Too many data points or complex render | Reduce data, simplify visual |
| Other is the largest component | Visual waiting for other queries | Check cross-filter chain |
| All visuals have similar "Other" time | Sequential query bottleneck | Reduce visual count on page |
| Total page > 10 seconds | Multiple problems likely | Fix the slowest 2-3 visuals first |

---

## Copying the DAX Query

For any visual with high DAX Query time:

1. Expand the visual entry in Performance Analyzer
2. Click **Copy query** — this copies the exact DAX that Power BI generated
3. Paste into **DAX Studio** for deeper analysis (Server Timings, query plan)

The copied query is the actual query that Power BI sends to the engine, including
all active filters from slicers, page filters, and visual-level filters.

### What the Copied Query Looks Like

```dax
// Simplified example — actual queries include full filter context
DEFINE
  VAR __DS0FilterTable =
    TREATAS({"2024"}, 'DimDate'[Year])
EVALUATE
  SUMMARIZECOLUMNS(
    'DimProduct'[Category],
    __DS0FilterTable,
    "Total_Sales", 'FactSales'[Total Sales],
    "Margin", 'FactSales'[% Margin]
  )
ORDER BY 'DimProduct'[Category]
```

---

## Common Patterns in Performance Analyzer

### Pattern 1: One Slow Visual, Others Fast

**Diagnosis:** The slow visual's measure is the bottleneck.
**Action:** Copy its DAX query → analyze in DAX Studio → optimize the measure.

### Pattern 2: All Visuals Slow, Similar Timing

**Diagnosis:** Model-level issue OR too many visuals competing for resources.
**Action:**
- Check visual count (reduce to ≤ 8)
- Check if a shared slicer is applying an expensive filter
- Check model size and storage mode

### Pattern 3: First Load Slow, Subsequent Interactions Fast

**Diagnosis:** Cold cache problem — data not yet in memory.
**Action:**
- This is normal for first load (especially DirectQuery)
- For Import models, ensure Premium/Fabric capacity keeps models pinned
- For DirectQuery, consider aggregation tables for landing page queries

### Pattern 4: Slicer Selection Causes Long Delay

**Diagnosis:** Slicer triggers re-query of all cross-filtered visuals.
**Action:**
- Enable **Apply button** on slicers (batch filter changes)
- Disable cross-filtering on visuals that don't need it
- Switch high-cardinality slicers to dropdown mode
- See `references/report-level-optimization.md`

### Pattern 5: Visual Display Time is High

**Diagnosis:** Visual rendering too many data points or using complex SVG.
**Action:**
- Reduce rows returned (add TOP N filter, aggregate further)
- For scatter charts: reduce point count or add sampling
- For maps: reduce geographic granularity
- For tables/matrices: paginate or limit visible rows
- Replace heavy custom visuals with standard visuals

---

## Benchmarking Protocol

When measuring before/after improvement:

1. **Close all other PBI Desktop files** (memory contention)
2. **Refresh the model** to ensure up-to-date data
3. Click **Start recording** in Performance Analyzer
4. Click **Refresh visuals** (not just interact — force full refresh)
5. Record the timings for each visual
6. **Repeat 3 times** — use the **median** value (not the first run)
7. Apply optimization
8. **Refresh visuals** again (3 times, median)
9. Compare before vs. after for each visual

### Reporting Template

```
Performance Improvement Report
──────────────────────────────
Visual: [visual name]
Measure: [measure name]
Change: [what was optimized]

Before: DAX Query = XXX ms | Visual Display = XXX ms | Total = XXX ms
After:  DAX Query = XXX ms | Visual Display = XXX ms | Total = XXX ms
Improvement: XX% reduction in total time

Notes: [any caveats, trade-offs]
```

---

## Quick Reference

| Task | How |
|---|---|
| Open Performance Analyzer | View tab → Performance Analyzer |
| Record all visuals | Start recording → Refresh visuals → Stop |
| Get DAX query for a visual | Expand visual → Copy query |
| Identify slowest visual | Sort by total duration (largest first) |
| Distinguish query vs render | Compare DAX Query vs Visual Display columns |
| Benchmark properly | 3 runs, median, refresh between runs |
