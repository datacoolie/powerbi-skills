# HR Headcount & Attrition

> **Preview:** [![hr-headcount-attrition preview](../../assets/layout-previews/hr-headcount-attrition.svg)](../../assets/layout-previews/hr-headcount-attrition.svg) · variants: [annotated](../../assets/layout-previews/hr-headcount-attrition-annotated.svg) · [dark](../../assets/layout-previews/hr-headcount-attrition-dark.svg)

- Canvas: `1920×1080` (landscape-16x9)
- Style: `analytical` · Domain: `hr`
- Visuals: 8
- Zones: `title-bar, slicer-row, kpi-row-4, headcount-bridge, attrition-waterfall, exit-reason-bar`

## Use when
Monthly people review; headcount walk from starting to ending balance with hires/exits/transfers and attrition composition

## Avoid when
When exit-reason data is not captured or the org is < 100 employees

## Recommended themes
`hr-people-analytics`, `consulting-authority`, `microsoft-fluent`, `nord-frost`

## Chart patterns
`kpi-card-with-spark`, `waterfall`, `stacked-bar`

## Data requirements
- min_rows: 100
- required_measures: `headcount`, `hires`, `exits`
- required_dimensions: `date`, `department`
- date_grain: `month`

## Customization allowed
- **FHD headroom (optional)** — coordinates in `layouts-index.json` zone space; `exit-reason-bar` shrinks to `(16, 688, 1008, 376)` to make room (8 → 10 visuals, within the Analytical budget of 12):
  - `attrition-by-tenure-band` at `(1048, 688, 432, 376)` — at what tenure do people leave?
  - `regretted-vs-non-regretted` at `(1504, 688, 400, 376)` — how much of the attrition is regretted loss?

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
