# Visual Vocabulary — Intent-first chart selection

Pick the **data relationship** first, then the chart. This reference adapts the
Financial Times *Visual Vocabulary* (via Gramener's Vega edition) to Power BI, so
the Strategist can bind each chart slot in Design Spec §5 to a named, defensible
data relationship rather than a chart type.

> **Attribution** — Taxonomy, category descriptions, and chart catalog are adapted
> from:
> - Financial Times — [Visual Vocabulary](https://ft.com/vocabulary) (Alan Smith,
>   Chris Campbell, et al.)
> - Andy Kriebel — [Tableau edition](http://www.vizwiz.com/2018/07/visual-vocabulary.html)
> - Gramener — [Visual Vocabulary, Vega edition](https://github.com/gramener/visual-vocabulary-vega)
>   by Pratap Vardhan (the CSV-driven catalog this file mirrors)
>
> All categories and descriptive sentences are quoted from the original catalog.
> Power BI mappings, custom-visual notes, and banned-chart substitutes are ours.

---

## How to use this file

1. **Strategist, Phase 4a — Step 5 (visual slot binding).** For each slot on the
   layout, pick exactly one row from §[Category reference](#category-reference).
2. Write the binding as `category → chart → visualType` in Design Spec §5.
   Example: `Ranking → Ordered bar → clusteredBarChart`.
3. If the chart is in our [`chart-templates/`](chart-templates/) catalog, link the
   recipe. If it is not, add it to the [backlog](#backlog--not-yet-cataloged)
   below so the catalog grows deliberately.
4. **Polisher, Phase 4c.** `design_quality_check.py` rule W8 (rainbow palette) and
   W1 (visual-count cap) enforce the density/categorical limits this taxonomy
   implies. Do not override without documenting why in §11 of the Design Spec.

---

## The 9 categories at a glance

| Category | When to use it (verbatim from FT) |
|---|---|
| **Deviation** | Emphasise variations (+/-) from a fixed reference point (zero, target, long-term average). Also sentiment (positive/neutral/negative). |
| **Correlation** | Show the relationship between two or more variables. *Readers assume relationships are causal unless you tell them otherwise.* |
| **Ranking** | Use when an item's position in an ordered list matters more than its absolute value. |
| **Distribution** | Show values in a dataset and how often they occur. The shape (skew) can highlight inequality. |
| **Change over time** | Emphasise changing trends. Picking the correct time window is part of the story. |
| **Magnitude** | Size comparisons — relative ("larger/smaller") or absolute ("fine differences"). Usually counted values, not rates. |
| **Part-to-whole** | How one entity breaks into components. If only the *size* of components matters, prefer Magnitude. |
| **Spatial** | Only when precise location or geographical pattern is the point. |
| **Flow** | Volume or intensity of movement between states — logical sequences or geographies. |

---

## Category reference

### 1. Deviation

> Emphasise variations (+/-) from a fixed reference point.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Diverging bar | `clusteredBarChart` with conditional formatting | One series split by sign, or two series anchored at zero | [`tornado-chart.md`](chart-templates/tornado-chart.md) |
| Diverging stacked bar | `barChart` (100% stacked) | Ideal for Likert / survey sentiment | — |
| Spine | `clusteredBarChart` (single row) | Splits one value into two contrasting components (Male/Female) | — |
| Surplus / deficit filled area | `areaChart` with positive/negative rules | Baseline at zero; shade above/below | — |
| Surplus / deficit filled line | `lineChart` + `areaChart` overlay | Same as above when series are richer | [`yoy-variance.md`](chart-templates/yoy-variance.md) |

---

### 2. Correlation

> Show the relationship between two or more variables. Readers assume causality.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Scatterplot | `scatterChart` | Square aspect ratio preferred; add trend line | [`scatter-quadrant.md`](chart-templates/scatter-quadrant.md) |
| Column + line timeline | `lineClusteredColumnComboChart` | Amount (columns) vs. rate (line) — avoid secondary axis unless both scales are labelled | — |
| Connected scatterplot | `scatterChart` with `Play Axis` | Shows how the X/Y relationship evolves over time | — |
| Bubble | `scatterChart` with `Size` role | Encode area (not diameter); cap at ~30 bubbles | — |
| XY heatmap | `matrix` with data bars / conditional color | Good for pattern density, poor for precise deltas | — |

---

### 3. Ranking

> Position matters more than absolute value. Don't be afraid to highlight points of interest.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Ordered bar | `clusteredBarChart` (sorted desc) | Default choice when category names are long | [`bar-comparison.md`](chart-templates/bar-comparison.md) |
| Ordered column | `clusteredColumnChart` (sorted desc) | Use when ≤ 8 categories and labels are short | [`bar-comparison.md`](chart-templates/bar-comparison.md) |
| Ordered proportional symbol | Deneb / PowerBIVisuals circle chart ★ | Big variance between values; precise delta not important | — |
| Dot strip plot | Deneb ★ | Space-efficient ranks across many categories | — |
| Slope | Deneb ★ or `lineChart` with 2 periods | Rank change between two dates | [`yoy-variance.md`](chart-templates/yoy-variance.md) |
| Lollipop | `clusteredBarChart` with narrow bars + markers | Draws attention to the endpoint | — |
| Bump | Deneb ★ | Rank changes across many dates — group lines by color to reduce clutter | — |

---

### 4. Distribution

> Show values and how often they occur. Shape/skew highlights inequality.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Histogram | `histogramXY6E3D5691159E41859A007A262D4B0E9E` ★ | Keep column gaps minimal so shape reads | — |
| Dot plot | Deneb ★ | Min/max across categories | — |
| Dot strip plot | Deneb ★ | Individual values; problematic with collision | — |
| Barcode plot | Deneb ★ | All-data display; best for highlighting single values | — |
| Boxplot | `BoxWhiskerChart1455240051538` ★ | Median + IQR + outliers | — |
| Violin plot | `ViolinPlot1445472000811` ★ | Preferred over boxplot for complex / multimodal data | — |
| Population pyramid | `clusteredBarChart` split by sign (back-to-back) | Age × sex breakdowns | [`tornado-chart.md`](chart-templates/tornado-chart.md) |
| Cumulative curve | `lineChart` on running-total measure | Y is always cumulative, X is the measure | — |
| Frequency polygons | `lineChart` with 3-4 series max | Multi-distribution comparisons | — |

---

### 5. Change over Time

> Emphasise changing trends. Time window choice is part of the story.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Line | `lineChart` | Default for continuous time series | [`trend-line.md`](chart-templates/trend-line.md) |
| Column | `clusteredColumnChart` | Best with a single series | — |
| Column + line timeline | `lineClusteredColumnComboChart` | Amount × rate over time | — |
| Slope | `lineChart` (2 anchor dates only) | Crisp when story collapses to 2 periods | [`yoy-variance.md`](chart-templates/yoy-variance.md) |
| Area chart | `areaChart` — use sparingly | Total reads well, component changes do not | — |
| Candlestick | Deneb ★ | OHLC per period, usually financial | — |
| Fan chart (projections) | Deneb ★ | Growing uncertainty cone around a central line | — |
| Connected scatterplot | `scatterChart` with `Play Axis` | Two variables evolving together | — |
| Calendar heatmap | `bciCalendarCC0FA2BFE4B54EE1ACCFE383B9B1DE61` ★ | Daily/weekly/monthly patterns; sacrifices precision | — |
| Priestley timeline | Gantt ★ (`Gantt1467746032498`) | Events with duration | — |
| Circle timeline | Deneb ★ | Discrete events of varying size on a time axis | — |
| Vertical timeline | Custom layout / Deneb ★ | Great on mobile scroll | — |
| Seismogram | Deneb ★ | Alt. to circle timeline for extreme variance | — |
| Streamgraph | Deneb ★ | Proportional change over time; not individual values | — |

---

### 6. Magnitude

> Size comparisons — relative or absolute. Usually counted values, not rates.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Column | `clusteredColumnChart` | Must start at zero | [`bar-comparison.md`](chart-templates/bar-comparison.md) |
| Bar | `clusteredBarChart` | Good when labels are long or non-temporal | [`bar-comparison.md`](chart-templates/bar-comparison.md) |
| Paired column | `clusteredColumnChart` (2 series) | Difficult beyond 2 series — switch to small multiples | — |
| Paired bar | `clusteredBarChart` (2 series) | Same caution | — |
| Marimekko | `MekkoChart1513095496262` ★ | Size × proportion together — keep data simple | — |
| Proportional symbol | Deneb ★ | Big variance; precise delta not important | — |
| Isotype (pictogram) | Deneb ★ | Whole numbers only (never slice off an arm) | — |
| Lollipop | Narrow bar + marker | Draws focus to the value | — |
| Radar | `RadarChart1423470498847` ★ | Organise axes to tell a consistent story | — |
| Parallel coordinates | `PBI_CV_9D24DAC5_8DAD_4E53_971F_5112EB5A3C35` ★ or Deneb | Axis order is critical | — |
| Bullet | `BulletChart1443347686880` ★ | Measurement vs. target + range | [`gauge-target.md`](chart-templates/gauge-target.md) |
| Grouped symbol | Deneb ★ | Alt. to bar when highlighting individuals matters | — |

---

### 7. Part-to-whole

> Breakdown into components. If only component size matters, prefer Magnitude.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Stacked column | `clusteredColumnChart` (stacked) | ≤ 5 segments; label base segment | — |
| Marimekko | `MekkoChart1513095496262` ★ | Size × proportion | — |
| Pie | **Avoid** — replace with sorted `clusteredBarChart` or 100% stacked bar | Only exception: ≤ 3 distinct segments totalling 100 % | — |
| Donut | **Avoid** — replace same as pie | Even harder than pie | — |
| Treemap | `treemap` | Large hierarchies; struggles with many small segments | — |
| Voronoi | Deneb ★ | Points → areas; each area closest to its seed | — |
| Arc | Deneb ★ | Hemicycle; political-result style | — |
| Gridplot (waffle) | `WaffleChart1453776852267` ★ | Whole numbers; works well in small multiples | — |
| Venn | Static image / Deneb ★ | Schematic only; not quantitative | — |
| Waterfall | `waterfallChart` | Part-to-whole with signed components | [`waterfall-bridge.md`](chart-templates/waterfall-bridge.md) |
| Sunburst | `Sunburst1445472000808` ★ | 3+ nested hierarchy levels | — |

---

### 8. Spatial

> Only when location / geographical pattern is the point.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Basic choropleth (rate) | `filledMap` | Use rates, not totals; pick a sensible base geography | [`map-geo.md`](chart-templates/map-geo.md) |
| Proportional symbol map | `map` (bubble) | Totals/magnitude; small variations are hard to see | [`map-geo.md`](chart-templates/map-geo.md) |
| Flow map | `shapeMap` + Deneb ★ overlay | Unambiguous movement across a map | — |
| Contour map | Deneb ★ / Azure Maps ★ | Equal-value areas; diverging palette for +/- | — |
| Equalised cartogram | Shape Map with custom TopoJSON | Regular shapes for voting regions | — |
| Scaled cartogram | Shape Map with custom TopoJSON | Stretch/shrink by value | — |
| Dot density | Azure Maps ★ | Individual events; annotate patterns | — |
| Heat map (geographic) | Azure Maps ★ heat layer | Intensity colour, not admin-unit bound | — |

---

### 9. Flow

> Volume/intensity of movement between states.

| Chart | Power BI implementation | Notes | Template |
|---|---|---|---|
| Sankey | `SankeyDiagram1458048422238` ★ | Flow paths between nodes | [`funnel-conversion.md`](chart-templates/funnel-conversion.md) |
| Waterfall | `waterfallChart` | Sequencing of signed components | [`waterfall-bridge.md`](chart-templates/waterfall-bridge.md) |
| Chord | `ChordChart1443052498688` ★ | 2-way flows in a matrix; can show net winner | — |
| Network | `ForceGraph1438016029256` ★ or Deneb | Complex, interconnected relationships | — |

---

## Backlog — not yet cataloged

Charts from the FT/Gramener catalog that do **not** yet have a Power BI recipe
under [`chart-templates/`](chart-templates/). Each line is a candidate follow-up
item — copy into Design Spec §11 if a report needs one.

- `dot-plot`, `dot-strip-plot`, `barcode-plot` — best done in Deneb; no shared
  recipe yet.
- `bump`, `slope`, `cumulative-curve` — useful for executive ranking/deviation
  stories but no reusable template yet.
- `calendar-heatmap` — custom visual wired, but no layout-grade recipe.
- `isotype`, `gridplot`, `arc` — part-to-whole alternatives needing Deneb
  specs + icon/tile assets.
- `sankey`, `chord`, `network` — recipes only for the simple funnel case; full
  network/chord recipes missing.
- Cartograms (`equalised-cartogram`, `scaled-cartogram`) — require shared
  TopoJSON library.

---

## Cross-reference

- Chart mechanics, hard rules (never-3D, no pie, no secondary axis):
  [`chart-selection-guide.md`](chart-selection-guide.md)
- Recipe files (composition, field bindings, format-pane keys):
  [`chart-templates/`](chart-templates/) and the machine-validated
  [`chart-templates-index.json`](chart-templates/chart-templates-index.json)
- Density caps and canvas budgets per style personality:
  [`shared-standards.md`](shared-standards.md)
- Lint enforcement of these rules: `design_quality_check.py` (W1 visual count,
  W7 3-D, W8 rainbow, W9 report budget).
