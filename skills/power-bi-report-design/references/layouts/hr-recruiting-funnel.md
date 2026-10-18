# Recruiting Funnel

> **Preview:** [![hr-recruiting-funnel preview](../../assets/layout-previews/hr-recruiting-funnel.svg)](../../assets/layout-previews/hr-recruiting-funnel.svg) · variants: [annotated](../../assets/layout-previews/hr-recruiting-funnel-annotated.svg) · [dark](../../assets/layout-previews/hr-recruiting-funnel-dark.svg)

- Canvas: `1920×1080` (landscape-16x9)
- Style: `analytical` · Domain: `hr`
- Visuals: 7
- Zones: `title-bar, slicer-row, time-to-fill-kpi, candidate-funnel, offer-accept-rates, supporting-pair`

## Use when
Talent acquisition review — candidate pipeline, stage conversion, offer acceptance, time-to-fill

## Avoid when
When ATS data exports < 4 pipeline stages

## Recommended themes
`hr-people-analytics`, `brand-salesforce`, `marketing-digital`

## Chart patterns
`funnel`, `conversion-bar`, `kpi-card-with-spark`

## Data requirements
- min_rows: 200
- required_measures: `candidate_count`, `offer_accept_rate`
- required_dimensions: `stage`, `requisition`
- date_grain: `month`

## Customization allowed
- **FHD headroom (optional)** — coordinates in `layouts-index.json` zone space; `supporting-pair` shrinks to `(16, 808, 1008, 256)` to make room (7 → 9 visuals, within the Analytical budget of 12):
  - `source-of-hire-effectiveness` at `(1048, 808, 432, 256)` — which sourcing channels deliver hires at the lowest cost?
  - `open-req-aging` at `(1504, 808, 400, 256)` — which open requisitions are aging beyond the time-to-fill target?

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
