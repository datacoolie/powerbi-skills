# Incident Postmortem

- Canvas: `1664×936` (landscape-16x9)
- Style: `analytical` · Domain: `technology`
- Visuals: 8
- Zones: `title-bar, slicer-row, mttr-kpis, incident-timeline, rca-pareto, supporting-pair`

## Use when
Post-incident review — MTTR / MTBF trend, timeline reconstruction, root-cause pareto

## Avoid when
Without structured incident data (severity, root_cause, duration)

## Recommended themes
`tech-monitoring`, `high-contrast-dark`, `brand-ibm-carbon`

## Chart patterns
`kpi-card-with-spark`, `gantt-timeline`, `pareto`

## Data requirements
- min_rows: 20
- required_measures: `mttr`, `incident_count`
- required_dimensions: `severity`, `service`
- date_grain: `day`

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
