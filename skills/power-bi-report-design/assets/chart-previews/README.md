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

All 21 previews are hand-authored 320×180 monochrome schematics that use
`currentColor` (with opacity variants for layering). They inherit the active
theme accent from whatever surface they're embedded on — light UI, dark UI,
Design Spec §5 rendered to PDF — without re-export. No hard-coded fills, no
gradients, no filters.

### Core 13 recipes

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

## Known gaps

None — all 21 recipes in [`chart-templates-index.json`](../../references/chart-templates/chart-templates-index.json)
have previews. Schematics are content-free and license-free to re-use anywhere
under this skill.
