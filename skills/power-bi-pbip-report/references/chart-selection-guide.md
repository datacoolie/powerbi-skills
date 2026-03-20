# Chart Selection Guide

Reference for selecting the right Power BI visual type based on the data relationship,
audience, and editorial intent. Derived from *Storytelling with Data* (Knaflic, 2015),
*Storytelling with Data: Let's Practice!* (Knaflic, 2020), and *Data Visualization:
A Handbook for Data Driven Design* (Kirk, 2nd ed., 2019).

---

## Decision Framework

**Start with the editorial angle, not the chart type.** Ask:
1. What type of comparison or relationship is being shown?
2. What is the single most important insight this visual must convey?
3. What action should the viewer take after seeing it?

Then select the chart that makes that answer most obvious for the target audience.

---

## Chart Selection by Data Relationship

| Data Relationship | Recommended Chart | Power BI `visualType` | Notes |
|---|---|---|---|
| **Change over time — single series** | Line chart | `lineChart` | Most readable for trends; use consistent time intervals |
| **Change over time — few series** | Multi-series line chart | `lineChart` | Max 4-5 series; beyond that → small multiples |
| **Comparing categories — few items** | Horizontal bar chart | `clusteredBarChart` | Category labels read naturally left-to-right |
| **Comparing categories — vertical** | Vertical column chart | `clusteredColumnChart` | Use only when column count is small (≤8) |
| **Ranking — emphasis on order** | Sorted horizontal bar chart | `clusteredBarChart` | Sort descending (largest at top) |
| **Part-to-whole — few parts** | Stacked bar chart | `barChart` / `columnChart` | Max 4-5 segments; label base segment |
| **Part-to-whole — many parts (50+)** | Treemap | `treemap` | Size = area, not height; largest top-left |
| **Discrete progress toward target** | Bullet chart | *(custom visual)* | Preferred over gauge for density |
| **Time intervals — start/end/delta** | Waterfall chart | `waterfallChart` | Shows increases, decreases, and net result |
| **Distribution of values** | Histogram / box plot | *(requires custom visual)* | Bin size matters in histogram |
| **Correlation between two metrics** | Scatter plot | `scatterChart` | Squared aspect ratio preferred; add trend line |
| **Correlation + magnitude** | Bubble chart | `scatterChart` (with `Size` role) | Use area (not diameter) to encode size |
| **Flows between categories** | Waterfall / Sankey | `waterfallChart` / *(custom)* | Sankey needs interactivity for complex flows |
| **Geographic patterns** | Filled map | `map` | Use equal-area projections for thematic data |
| **Single large number** | Card visual | `card` | "One or two numbers — just show the number" |
| **Multiple KPIs** | Multi-row card | `multiRowCard` | Keep to ≤6 metrics for readability |
| **Status vs. target** | KPI visual | `kpi` | Shows indicator + trend axis + goal |
| **Before-after comparison** | Slopegraph | *(line with 2 time points)* | Very clean for exactly 2 periods |

---

## Hard Rules — Non-Negotiable

### NEVER use these:

**❌ 3D Charts (any type)**
> "Never use 3D. The only exception is if you are actually plotting a third dimension of data.
> 3D skews our numbers, making them difficult or impossible to interpret or compare."
> — *Storytelling with Data*

- 3D bars tilt the visual plane; bar heights are read against an invisible tangent plane
- 3D pies magnify front slices, shrink back slices — the pie no longer represents the data
- Power BI offers 3D variants of some visuals — always choose the flat version

**❌ Pie Charts (almost always)**
> "The human eye isn't good at ascribing quantitative value to two-dimensional space.
> Pie charts are hard for people to read."
> — *Storytelling with Data*

- When slices are close in size: impossible to tell which is bigger
- When slices differ significantly: can only say "bigger" or "smaller" — not by how much
- Alternatives that are always clearer: sorted horizontal bar chart, 100% stacked bar
- **Only acceptable exception**: Part-of-whole communication where the total equals 100%
  AND there are ≤3 clearly distinct segments (e.g., 75% vs. 25%)

**❌ Donut Charts**
> "With a donut chart, we ask the audience to compare arc lengths.
> Don't use donut charts."
> — *Storytelling with Data*

- Even harder than pie (arc length is less intuitive than area)
- The empty center wastes space and provides no information

**❌ Secondary Y-Axis**
> "It takes time and reading to understand which data reads against which axis.
> Generally not a good idea."
> — *Storytelling with Data*

- Implies a relationship between the two series that may not exist
- Alternatives: pull graphs apart vertically with a shared x-axis, or label data points directly

**❌ Donut + Pie + 3D in Power BI**
Power BI `visualType` values to avoid (prefer alternatives):

| Avoid | Use Instead |
|---|---|
| `pieChart` | `clusteredBarChart` (sorted) or `barChart` (100% stacked) |
| `donutChart` | `clusteredBarChart` (sorted) or `barChart` (100% stacked) |
| Any 3D variant | Flat equivalent |

---

## Common Mistakes by Chart Type

### Bar / Column Charts
- ❌ **Truncated y-axis** — must start at zero; a bar at 95 vs. 100 looks equal but shouldn't
- ❌ **Bar width narrower than gaps** — looks like a stem plot; bars should be wider than the
  white space between them
- ❌ **Too many categories (20+) in a column chart** — labels overlap; switch to horizontal bar
- ❌ **No ordering** — bars presented alphabetically hide the story; sort by value unless a
  natural order exists
- ✅ Direct-label bars instead of y-axis when there are few categories

### Line Charts
- ❌ **Inconsistent time intervals** — e.g., plotting Jan, Feb, Apr (missing March) without
  a gap creates a false visual impression of continuity
- ❌ **Too many lines (>5)** — becomes spaghetti chart; split into small multiples
- ❌ **Aspect ratio too tall or too wide** — perceived trend steepness is a function of aspect
  ratio; adjust until the most meaningful trends appear at roughly 45°
- ✅ Zero baseline is optional for line charts (unlike bar charts) — position, not length,
  encodes the value
- ✅ Use a dotted or dashed line to distinguish forecast from actuals

### Stacked Bar / Area Charts
- ❌ **More than 4-5 segments** — non-baseline segments have no common reference point;
  comparisons become impossible
- ❌ **Stacked area charts** — accumulation + no baseline makes middle/top series unreadable;
  use small multiples instead
- ✅ 100% stacked bar works well for Likert-scale survey data (diverging from center)
- ✅ Only the bottom/left segment (which has a consistent baseline) is easily readable

### Scatter / Bubble Charts
- ❌ **Non-square aspect ratio** — distorts correlation perception; aim for approximately
  equal height and width
- ❌ **Bubble size encoding using diameter** — area = π × r²; halving diameter quarters the
  area; always encode with area
- ❌ **Overplotting without transparency** — dense clusters appear as solid blobs; use
  transparency in the data color settings
- ✅ Add a trend line to make the direction of correlation explicit

### Maps
- ❌ **Choropleth with raw counts** — large regions appear important only because of land area;
  always normalize to rate/percentage/per-capita for choropleth
- ❌ **Too many geographic markers** — clutters the map; use filtering or clustering
- ✅ For city-level data, proportional symbol maps (bubbles at lat/lon) are more honest
  than choropleths

### Tables / Matrices
- ❌ **Heavy grid lines** — use subtle separators or white space only
- ❌ **More than 8-10 columns** — becomes a spreadsheet, not a report visual
- ✅ Use conditional formatting (background color or data bars) to turn the numbers into
  a heatmap-style scannable view
- ✅ Freeze the first column when many rows; add totals row

### Cards / KPIs
- ❌ **Too many KPI cards in a row (>6)** — audience can't prioritize; group by importance
- ❌ **No context** — a number alone is meaningless; always pair with trend, target, or
  comparison (vs. prior period, vs. budget)
- ✅ Cards with sparklines or trend arrows convey more in the same space as a plain card
- ✅ Lead with the most important metric (leftmost card = first attention)

---

## Choosing Between Similar Chart Types

### Trends over time: Line vs. Bar vs. Area

| Use | When |
|---|---|
| **Line chart** | Continuous time series; emphasizing trend direction |
| **Column chart** | Discrete time periods where individual values matter as much as trend |
| **Area chart** | Single series where the magnitude (volume) below the line is meaningful |
| **Stacked area** | Avoid — use small multiples instead |

### Comparisons: Horizontal Bar vs. Column

| Use | When |
|---|---|
| **Horizontal bar** (`clusteredBarChart`) | Long category names; many categories (>8); ranking by value |
| **Vertical column** (`clusteredColumnChart`) | Chronological order (time on x-axis); few categories (≤8) |

### Part-to-whole: Stacked Bar vs. Treemap vs. Pie

| Use | When |
|---|---|
| **100% stacked bar** | Comparing composition across multiple groups simultaneously |
| **Treemap** | Single group with many components (>10); hierarchy exists |
| **Pie** | Only if ≤3 distinct segments, total = 100%, and you have no better option |

### Multiple KPIs: Card vs. Table vs. Multi-row Card

| Use | When |
|---|---|
| **Card** (`card`) | Single hero metric with maximum visual weight |
| **Multi-row card** (`multiRowCard`) | 4-8 related metrics at equal visual weight |
| **Table** (`tableEx`) | Many metrics with row-level detail needed |

---

## Audience and Purpose Modifiers

Adjust chart complexity for the consumption context:

| Setting | Duration | Complexity Tolerance | Design Strategy |
|---|---|---|---|
| **Executive (boardroom)** | 5-30 sec | Low | Simple chart + statement title + 1 accent color |
| **Analytical (analyst)** | 5-15 min | High | Scatter, small multiples, data table; let them explore |
| **Operational (dashboard)** | Repeated glances | Medium | KPI cards at top + trend line + threshold indicator |
| **Presentation prop** | 30-60 sec per slide | Low | Minimal — speaker provides context; visual accents only |

**Key rule**: The right chart is *"whatever will be easiest for your audience to read."*
Never choose a chart to impress — choose it to communicate.

---

## Power BI Visual Type Quick Reference

### Prefer These Built-in Visuals

| Purpose | `visualType` | Notes |
|---|---|---|
| Trend over time | `lineChart` | Default for time series |
| Category comparison | `clusteredBarChart` | Horizontal; best for categories |
| Column comparison | `clusteredColumnChart` | Vertical; use for time on x-axis |
| Stacked bar | `barChart` | Horizontal stacked; use for compositions |
| Stacked column | `columnChart` | Vertical stacked |
| Part-to-whole | `treemap` | For many segments; avoid pie |
| Waterfall | `waterfallChart` | Cumulative changes |
| Scatter / Bubble | `scatterChart` | Correlation; add size role for bubble |
| KPI card | `card` | Single hero metric |
| Multi KPI | `multiRowCard` | Multiple metrics at equal weight |
| Status vs. target | `kpi` | Indicator + trend + goal |
| Filter | `slicer` | Date, category, or hierarchy filter |
| Detail grid | `pivotTable` | Matrix with row/column groupings |
| Flat table | `tableEx` | Row-level or summary table |
| Geographic | `map` | Filled/bubble map |
| Custom tooltip | *(card + chart)* | On tooltip page (320×240) |

### Avoid or Use With Caution

| `visualType` | Reason | Alternative |
|---|---|---|
| `pieChart` | Arc/area hard to compare | `clusteredBarChart` (sorted) |
| `donutChart` | Arc length unreadable | `clusteredBarChart` (sorted) |
| `gauge` | Only shows one value; wastes space | `kpi` or `card` with target |
| `funnel` | Misleading unless stages are actually sequential | `clusteredBarChart` |
| `areaChart` | Stacked version unreadable; single area often better as line | `lineChart` |
