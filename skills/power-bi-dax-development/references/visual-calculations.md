# Visual Calculations Reference

Visual calculations are DAX expressions defined and executed directly on a visual,
operating on aggregated data rather than model detail rows. Available since
January 2024 (Power BI Desktop).

---

## Overview

| Aspect | Model Measure | Visual Calculation |
|---|---|---|
| Stored in | Semantic model | Visual definition |
| Context | Filter context (complex) | Visual rows/columns (simple) |
| Computed at | Detail level, then aggregated | Post-aggregation |
| Reusable | Across all visuals | Only on the defining visual |
| Performance | Depends on complexity | Often faster (fewer rows) |
| Created via MCP | Yes (`measure_operations`) | No — report UI only |

**Key advantage:** Visual calculations remove the complexity of filter context.
They work on "what you see" in the visual matrix.

---

## When to Use Visual Calculations vs Model Measures

**Use visual calculations when:**
- Running sum, moving average, or cumulative total
- Comparing to previous/next row (vs-previous, vs-first, vs-last)
- Percent of parent or grand total within the visual
- The calculation is needed on one visual only
- You want simpler DAX without understanding filter context

**Use model measures when:**
- The metric must be shared across multiple visuals
- You need precise filter context control (CALCULATE, ALL, etc.)
- The calculation must appear in slicers or page-level filters
- You need to reference the measure in other DAX expressions
- The model is consumed by Excel PivotTables or third-party tools

---

## Available Functions

### Visual-Only Functions (cannot use in model measures)

| Function | Description | Shortcut To |
|---|---|---|
| `RUNNINGSUM(column)` | Running sum along axis | WINDOW |
| `MOVINGAVERAGE(column, windowSize)` | Moving average over N rows | WINDOW |
| `PREVIOUS(column)` | Value from previous row | OFFSET(-1) |
| `NEXT(column)` | Value from next row | OFFSET(1) |
| `FIRST(column)` | Value from first row of axis | INDEX(1) |
| `LAST(column)` | Value from last row of axis | INDEX(-1) |
| `RANGE(size)` | Slice of rows on axis | WINDOW |
| `COLLAPSE(expr, axis)` | Aggregate to parent level | — |
| `COLLAPSEALL(expr, axis)` | Aggregate to grand total | — |
| `EXPAND(expr, axis)` | Average of children | — |
| `ISATLEVEL(column)` | Is column present at current hierarchy level | — |
| `LOOKUP(expr, col, val)` | Look up value with context | — |
| `LOOKUPWITHTOTALS(expr, col, val)` | Look up value with totals | — |

### Model Functions Also Usable in Visual Calculations

OFFSET, INDEX, WINDOW, RANK, ROWNUMBER — these work in both contexts.

---

## Common Patterns

### Running Sum

```dax
Running Total = RUNNINGSUM([Sales Amount])
```

### Moving Average

```dax
-- 3-period moving average (including current)
Avg3M = MOVINGAVERAGE([Sales Amount], 3)

-- 12-period moving average (excluding current)
Avg12M_Prev = MOVINGAVERAGE([Sales Amount], 12, FALSE)
```

### Versus Previous

```dax
Sales vs Previous = [Sales Amount] - PREVIOUS([Sales Amount])

Sales vs Previous % = DIVIDE(
    [Sales Amount] - PREVIOUS([Sales Amount]),
    PREVIOUS([Sales Amount])
)
```

### Versus First / Last

```dax
Growth vs First = [Sales Amount] - FIRST([Sales Amount])
Diff vs Last = [Sales Amount] - LAST([Sales Amount])
```

### Percent of Parent

```dax
% of Parent = DIVIDE([Sales Amount], COLLAPSE([Sales Amount], ROWS))
```

### Percent of Grand Total

```dax
% of Total = DIVIDE([Sales Amount], COLLAPSEALL([Sales Amount], ROWS))
```

### Average of Children

```dax
Avg Children = EXPAND([Sales Amount], ROWS)
```

---

## Parameters

### Axis

Specifies direction of calculation: `ROWS` or `COLUMNS`.
If omitted, defaults to the first axis of the visual.

### Reset

Controls when the calculation restarts within a hierarchy:

| Value | Behavior |
|---|---|
| `NONE` (default) | No reset — continuous across all rows |
| `LOWESTPARENT` | Reset at the immediate parent level |
| `HIGHESTPARENT` | Reset at the top-level parent |
| Integer (positive) | Reset at Nth level from top (1 = highest) |
| Integer (negative) | Reset at Nth level from current (-1 = immediate parent) |
| Field reference | Reset when the specified field changes |

### Examples with Reset

```dax
-- Running sum that restarts each year
YTD Sales = RUNNINGSUM([Sales Amount], ROWS, , , HIGHESTPARENT)

-- Moving average that restarts per category
Cat Avg = MOVINGAVERAGE([Sales Amount], 3, TRUE, ROWS, , , [Category])
```

---

## Limitations

| Limitation | Workaround |
|---|---|
| Cannot reference model items not on the visual | Add the field to the visual first |
| Cannot be used in slicers or filters | Use model measures for filtering |
| Cannot be referenced by other visuals | Create a model measure if sharing needed |
| Cannot be created via MCP/XMLA tools | Report-level UI or PBIR JSON only |
| Not supported in live connections | Works in Import, DirectQuery, Direct Lake |
| Format must be set via visual properties | Use Data Format options in Format pane |
| Cannot reference other visual calculations in model | Self-contained within the visual |

---

## Decision Matrix

| Scenario | Best Option |
|---|---|
| Running total shown on one chart | Visual calculation |
| Running total used in 5+ visuals | Model measure (WINDOW pattern) |
| Moving average for trend line | Visual calculation |
| YoY comparison across all pages | Model measure or calculation group |
| % of parent in a matrix | Visual calculation (COLLAPSE) |
| % of total used in conditional formatting | Model measure (ALLSELECTED) |
| Quick comparison vs previous period | Visual calculation (PREVIOUS) |
| Complex multi-step metric | Model measure (more control) |

---

## Sources

- https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-overview
- https://learn.microsoft.com/dax/runningsum-function-dax
- https://learn.microsoft.com/dax/movingaverage-function-dax
