# Chart previews

One SVG or PNG thumbnail per chart recipe in
[`../../references/chart-templates/*.md`](../../references/chart-templates/).
Referenced from Design Spec §5 (Visual Inventory) so reviewers can recognise
each recipe at a glance.

## File naming

Filename matches the recipe's `id` in
[`chart-templates-index.json`](../../references/chart-templates/chart-templates-index.json)
with `.svg` (preferred) or `.png` extension.

Example:

| Recipe id | File |
|---|---|
| `bar-comparison` | `bar-comparison.svg` |
| `trend-line` | `trend-line.svg` |
| `waterfall-bridge` | `waterfall-bridge.svg` |

## Rules

1. Size: **320 × 180 px** viewBox for SVG, same ratio for PNG.
2. Monochrome preferred — use `currentColor` so previews inherit UI theme.
3. No real data. Pure schematic so the shape of the chart reads at a glance.
4. Every recipe in `chart-templates-index.json` must have a preview, OR live in
   the `gaps[]` array.

## Provenance

All 62 previews are hand-authored 320×180 monochrome schematics that use
`currentColor` (with opacity variants for layering). They inherit the active
theme accent from whatever surface they're embedded on — light UI, dark UI,
Design Spec §5 rendered to PDF — without re-export. No hard-coded fills, no
gradients, no filters. Every preview also carries an embedded
`<style id="preview-theme">` block with `@media (prefers-color-scheme: dark)`
so editors / viewers in dark mode render legibly.

### Core 13 recipes (v0.1)

| Recipe | Silhouette |
|---|---|
| `kpi-banner` | 4 tiles (title · value · delta · sparkline) |
| `bar-comparison` | 8 sorted-desc columns with top-rank emphasis |
| `trend-line` | Line + dot markers + dashed reference |
| `yoy-variance` | Clustered CY/PY bars + variance trace + legend |
| `waterfall-bridge` | Start → ±increments → end with connectors |
| `funnel-conversion` | 5 trapezoids + conversion % labels |
| `matrix-scorecard` | Row/col grid + status dot + row sparkline |
| `small-multiples-trend` | 2 × 3 mini-line grid, shared scale |
| `map-geo` | Region outline + proportional bubbles + pin |
| `decomposition-tree` | Root → branch → splits (3 levels, 5 leaves) |
| `scatter-quadrant` | Median cross-hairs + 4-corner labels |
| `gauge-target` | Arc + needle + target tick |
| `tornado-chart` | Diverging bars, sorted by absolute magnitude |

### Community additions (v0.2)

Inspired by widely-referenced data-viz practice (IBCS, SQLBI, Cole Nussbaumer,
Chandoo, Data Revelations, OKVIZ/xViz custom visuals). No copyrighted assets —
all silhouettes are original schematic geometry.

| Recipe | Silhouette | Story |
|---|---|---|
| `stacked-bar-100` | 5 horizontal rows, segment opacity gradient, % axis | Share / mix |
| `ribbon-chart` | 4 curving ribbons that swap rank across 5 periods | Rank-over-time |
| `bullet-chart` | 5 IBCS bullets — range band + actual bar + target tick | Actual vs target |
| `heatmap-calendar` | 7×16 day-of-week tile grid + opacity legend | Daily pattern |
| `pareto-80-20` | Sorted-desc bars + cumulative % line + 80% reference | Vital-few / ABC |
| `dumbbell-change` | Before/after dot-pairs with connectors, 6 categories | Before → after |
| `histogram-distribution` | 11-bin distribution with normal overlay + mean line | Distribution shape |
| `slope-chart` | Two vertical ticks, 8 slope lines, one accent line | Two-point change |

### Analytical additions (v0.3)

Six recipes covering tabular detail, statistical distribution, flow,
hierarchical share, dual-axis storytelling, and process control — drawn from
IBCS, SPC (Shewhart / Western Electric), and everyday finance/ops dashboards.

| Recipe | Silhouette | Story |
|---|---|---|
| `sparkline-table` | 4-row table + per-row line sparkline + end-of-line dot | Scorecard with shape |
| `box-plot-distribution` | 5 whisker/IQR boxes with median lines + outlier dots | Spread & outliers |
| `sankey-flow` | 4→3→3 columns of nodes with thickness-weighted ribbons | Stage attribution |
| `treemap-hierarchy` | 9 nested rectangles, area = share, opacity = saturation | Hierarchical share |
| `combo-dual-axis` | 8 columns on left axis + line + markers on right axis | Volume + rate |
| `control-chart-spc` | Line with UCL/Mean/LCL dashed refs + circled breach | Process control |

### Expanded catalog (v0.4)

Additional 35 recipes covering native Power BI visuals (`advance-card`,
`multi-row-card`, `kpi-indicator`, `table-detail`, `key-influencers`,
`smart-narrative`, `qna-visual`, `deneb-custom`) plus editorial chart types
drawn from the Financial Times Visual Vocabulary (adapted to Power BI).

| Family | Recipes |
|---|---|
| Native PBI | `advance-card`, `multi-row-card`, `kpi-indicator`, `table-detail`, `key-influencers`, `smart-narrative`, `qna-visual`, `deneb-custom` |
| Change / trend | `area-chart`, `connected-scatter`, `bump-chart`, `streamgraph`, `fan-chart-projection` |
| Magnitude / ranking | `lollipop`, `dot-plot`, `dot-strip-plot`, `barcode-plot`, `stacked-bar-absolute`, `zebra-bi-variance` |
| Distribution | `violin-plot`, `population-pyramid` |
| Correlation | `xy-heatmap`, `parallel-coordinates`, `network-graph` |
| Part-to-whole | `sunburst`, `waffle-chart`, `mekko-chart`, `voronoi-share` |
| Deviation / variance | `diverging-likert`, `surplus-deficit-area` |
| Spatial / scheduling | `gantt-timeline` |
| Specialist | `radar-chart`, `chord-diagram`, `candlestick-ohlc`, `word-cloud` |

## Known gaps

Ten recipes are still uncharted and tracked in
[`chart-templates-index.json`](../../references/chart-templates/chart-templates-index.json)
under `gaps[]`: `cartogram-equalised`, `cartogram-scaled`, `azure-map-flow`,
`azure-map-dot-density`, `azure-map-heatmap`, `arc-diagram`,
`isotype-pictogram`, `venn-diagram`, `slopegraph-multi`,
`clustered-stacked-combo`. Schematics are content-free and license-free to
re-use anywhere under this skill.
