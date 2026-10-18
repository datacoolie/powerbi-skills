# Pipeline Forecast

> **Preview:** [![sales-pipeline-forecast preview](../../assets/layout-previews/sales-pipeline-forecast.svg)](../../assets/layout-previews/sales-pipeline-forecast.svg) · variants: [annotated](../../assets/layout-previews/sales-pipeline-forecast-annotated.svg) · [dark](../../assets/layout-previews/sales-pipeline-forecast-dark.svg)

- Canvas: `1920×1080` (landscape-16x9)
- Style: `analytical` · Domain: `sales`
- Visuals: 8
- Zones: `title-bar, slicer-row, velocity-kpis, pipeline-stage-bar, forecast-vs-quota-line, supporting-pair`

## Use when
Weekly pipeline forecast — weighted stage-value, velocity, forecast vs quota

## Avoid when
Transactional / e-commerce models without multi-stage pipelines

## Recommended themes
`sales-growth`, `brand-salesforce`, `corporate-financial`

## Chart patterns
`stacked-bar`, `line-yoy`, `kpi-card-with-spark`

## Data requirements
- min_rows: 200
- required_measures: `weighted_value`, `quota`
- required_dimensions: `stage`, `rep`
- date_grain: `week`

## Customization allowed
- **FHD headroom (optional):** re-tile `supporting-pair` (y=808, h=248) from two tiles to three equal tiles of w=608 at x=24 / 656 / 1288, and add one slot at `x=1288, y=808, w=608, h=248` — *Deal slippage by stage* (open pipeline past its expected close date, bar by stage). It answers a distinct question: which weighted value is stale and unlikely to land in the forecast week. Brings the page to 9 visuals (analytical budget ≤ 12).

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
