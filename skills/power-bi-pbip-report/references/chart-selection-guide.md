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
| **Part-to-whole — percentage** | Waffle chart | `WaffleChart1453776852267` ★ | Discrete squares; intuitive for ratios |
| **Hierarchical part-of-whole** | Sunburst | `Sunburst1445472000808` ★ | Multi-level ring chart; 3+ nested levels |
| **Discrete progress toward target** | Bullet chart | `BulletChart1443347686880` ★ | Preferred over gauge for density |
| **Gauge with target needle** | Tachometer | `Tachometer1474636471549` ★ | Semicircular gauge with color ranges |
| **Time intervals — start/end/delta** | Waterfall chart | `waterfallChart` | Shows increases, decreases, and net result |
| **Distribution of values** | Histogram | `histogramXY6E3D5691159E41859A007A262D4B0E9E` ★ | Bin size matters |
| **Distribution — median/quartiles** | Box & Whisker | `BoxWhiskerChart1455240051538` ★ | Shows outliers, median, IQR |
| **Distribution — density shape** | Violin Plot | `ViolinPlot1445472000811` ★ | Richer than box plot for shape |
| **Correlation between two metrics** | Scatter plot | `scatterChart` | Squared aspect ratio preferred; add trend line |
| **Correlation + magnitude** | Bubble chart | `scatterChart` (with `Size` role) | Use area (not diameter) to encode size |
| **Flows between categories** | Sankey diagram | `SankeyDiagram1458048422238` ★ | Interactive flow paths between nodes |
| **Circular relationships** | Chord chart | `ChordChart1443052498688` ★ | Inter-entity transfers, bidirectional flows |
| **Diverging comparison (A vs B)** | Tornado chart | `TornadoChart1452517688218` ★ | Side-by-side diverging bars |
| **Multi-dimensional scoring** | Radar chart | `RadarChart1423470498847` ★ | Spider/web chart; 5-10 attributes |
| **Market share × segment size** | Mekko chart | `MekkoChart1513095496262` ★ | Variable-width stacked bar |
| **Daily activity heatmap** | Calendar heatmap | `bciCalendarCC0FA2BFE4B54EE1ACCFE383B9B1DE61` ★ | Colored calendar grid by value |
| **Geographic patterns** | Filled map | `map` | Use equal-area projections for thematic data |
| **Single large number** | Card visual | `card` | "One or two numbers — just show the number" |
| **Multiple KPIs** | Multi-row card | `multiRowCard` | Keep to ≤6 metrics for readability |
| **Rich KPI with formatting** | Advance Card | `advanceCardE03760C5AB684758B56AA29F9E6C257B` ★ | Conditional colors, icons, multiple rows |
| **Status vs. target** | KPI visual | `kpi` | Shows indicator + trend axis + goal |
| **Before-after comparison** | Slopegraph | *(line with 2 time points)* | Very clean for exactly 2 periods |
| **Image-based filter** | Chiclet Slicer | `ChicletSlicer1448559807354` ★ | Tile/button slicer with images |
| **Interactive date range** | Timeline Slicer | `Timeline1447991079100` ★ | Drag-to-select date range slider |
| **Project timeline** | Gantt Chart | `Gantt1467746032498` ★ | Task bars, milestones, dependencies |
| **Word/text frequency** | Word Cloud | `WordCloud1447959067750` ★ | Word size proportional to measure |
| **Fully custom chart** | Deneb | `Deneb6E97C82C58E5467CA7C3188B3E36ADE7` ★ | Vega/Vega-Lite declarative grammar |
| **Animated time playback** | Play Axis | `playAxis23F08FF12F11460BB525B1A3ADED385C` ★ | Auto-play through time periods |
| **Financial variance (IBCS)** | Zebra BI Cards | `zebraBiCards2C860CFAA9944091B75F0DBD117F20FA` ★ | IBCS-compliant AC/PY/FC cards |
| **Grouped + stacked bars** | Clustered Stacked | `clusteredstackedchartB0483D9875581356AF8B510BAAC9CFE4` ★ | Combine clustering with stacking |
| **Enhanced drill funnel** | Drill Down Funnel | `funnelDrilldownD423170ED341443BBDECDD3BA5FB49D2` ★ | Funnel with stage drill-down |

★ = Custom visual — requires `publicCustomVisuals` registration in `report.json`.
See `custom-visuals.md` for full identifiers, templates, and query roles.

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

### Custom Visuals — Use for Visual Diversity

| Purpose | Custom Visual | `visualType` |
|---|---|---|
| Rich KPI card | Advance Card | `advanceCardE03760C5AB684758B56AA29F9E6C257B` |
| Image/tile slicer | Chiclet Slicer | `ChicletSlicer1448559807354` |
| Date range slider | Timeline Slicer | `Timeline1447991079100` |
| Gauge with target | Tachometer | `Tachometer1474636471549` |
| Actual vs. target | Bullet Chart | `BulletChart1443347686880` |
| Diverging comparison | Tornado Chart | `TornadoChart1452517688218` |
| Distribution box plot | Box & Whisker | `BoxWhiskerChart1455240051538` |
| Value distribution | Histogram | `histogramXY6E3D5691159E41859A007A262D4B0E9E` |
| Hierarchical rings | Sunburst | `Sunburst1445472000808` |
| Percentage blocks | Waffle Chart | `WaffleChart1453776852267` |
| Flow between nodes | Sankey Diagram | `SankeyDiagram1458048422238` |
| Circular relationships | Chord Chart | `ChordChart1443052498688` |
| Multi-axis scoring | Radar Chart | `RadarChart1423470498847` |
| Variable-width bars | Mekko Chart | `MekkoChart1513095496262` |
| Calendar heatmap | BCI Calendar | `bciCalendarCC0FA2BFE4B54EE1ACCFE383B9B1DE61` |
| Color-intensity grid | Table Heatmap | `TableHeatmap1445497103790` |
| Any custom chart | Deneb (Vega/Vega-Lite) | `Deneb6E97C82C58E5467CA7C3188B3E36ADE7` |
| Word frequency | Word Cloud | `WordCloud1447959067750` |
| Project scheduling | Gantt Chart | `Gantt1467746032498` |
| Animated playback | Play Axis | `playAxis23F08FF12F11460BB525B1A3ADED385C` |
| Financial IBCS cards | Zebra BI Cards | `zebraBiCards2C860CFAA9944091B75F0DBD117F20FA` |
| Grouped + stacked | Clustered Stacked Chart | `clusteredstackedchartB0483D9875581356AF8B510BAAC9CFE4` |
| Part vs total overlay | Nested Total Bar | `nestedTotalBarChartC2D32E67DFF64FDD9564CF2CFCD20141` |
| Variance analysis | Variance Chart | `variance8E4BB1B41A8942A7B897C7014A6E1F56` |
| Drill funnel | Drill Down Funnel | `funnelDrilldownD423170ED341443BBDECDD3BA5FB49D2` |

All custom visuals require registration in `report.json` → `publicCustomVisuals`.
See `custom-visuals.md` for complete JSON templates and query role mappings.
