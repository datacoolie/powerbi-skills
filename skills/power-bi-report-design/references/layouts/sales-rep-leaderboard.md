# Rep Leaderboard

> **Preview:** [![sales-rep-leaderboard preview](../../assets/layout-previews/sales-rep-leaderboard.svg)](../../assets/layout-previews/sales-rep-leaderboard.svg) · variants: [annotated](../../assets/layout-previews/sales-rep-leaderboard-annotated.svg) · [dark](../../assets/layout-previews/sales-rep-leaderboard-dark.svg)

- Canvas: `1920×1080` (landscape-16x9)
- Style: `analytical` · Domain: `sales`
- Visuals: 6
- Zones: `title-bar, slicer-row, rep-leaderboard, attainment-gauge, win-rate-spark`

## Use when
Monthly rep ranking with attainment, win-rate sparkline, goal tracking

## Avoid when
Team-selling models where revenue attribution is shared

## Recommended themes
`sales-growth`, `brand-salesforce`, `marketing-digital`

## Chart patterns
`ranking-bar`, `gauge`, `sparkline`

## Data requirements
- min_rows: 50
- required_measures: `revenue`, `quota`, `win_rate`
- required_dimensions: `rep`
- date_grain: `month`

## Customization allowed
- **FHD headroom (optional):** narrow the `win-rate-spark` container to `x=24, y=752, w=1240, h=304` and add one slot at `x=1288, y=752, w=608, h=304` — *Pipeline coverage by rep* (open pipeline ÷ remaining quota, ranked bar). It answers a distinct question: which reps can still reach quota, as opposed to who is ahead now. Brings the page to 7 visuals (analytical budget ≤ 12).

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
