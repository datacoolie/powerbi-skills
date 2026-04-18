# FinOps Cloud Cost Governance

- Canvas: `1664×936` (landscape-16x9)
- Style: `analytical` · Domain: `technology`
- Visuals: 9
- Zones: `title-bar, slicer-row, kpi-row-4, cloud-spend-stack, anomaly-flags, budget-burn-gauge`

## Use when
Monthly cloud spend review — spend by service/team, anomaly detection, budget burn-down

## Avoid when
Without tagged cost data or a per-team budget allocation

## Recommended themes
`corporate-financial`, `tech-monitoring`, `brand-stripe`, `consulting-authority`

## Chart patterns
`stacked-area`, `anomaly-trend`, `gauge`

## Data requirements
- min_rows: 500
- required_measures: `cost`, `budget`
- required_dimensions: `service`, `team`
- date_grain: `day`

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
