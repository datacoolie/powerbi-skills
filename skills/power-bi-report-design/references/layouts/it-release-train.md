# Release Train (DORA)

- Canvas: `1664×936` (landscape-16x9)
- Style: `analytical` · Domain: `technology`
- Visuals: 8
- Zones: `title-bar, slicer-row, dora-kpi-strip, release-swimlane, deployment-frequency-trend, supporting-pair`

## Use when
Engineering effectiveness review — deployment frequency, lead time, change-failure rate, MTTR (DORA)

## Avoid when
Without CI/CD telemetry feeding a consolidated pipeline table

## Recommended themes
`tech-monitoring`, `brand-atlassian`, `brand-google-material`

## Chart patterns
`swimlane`, `kpi-card-with-spark`, `line-yoy`

## Data requirements
- min_rows: 100
- required_measures: `deploy_count`, `lead_time`, `cfr`
- required_dimensions: `service`, `team`
- date_grain: `week`

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
