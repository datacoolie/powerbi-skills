# Patient Flow

- Canvas: `1664×936` (landscape-16x9)
- Style: `operational` · Domain: `healthcare`
- Visuals: 7
- Zones: `title-bar, slicer-row, patient-flow-sankey, wait-time-distribution, census-heatmap`

## Use when
Live / daily patient flow review — ED to admit to discharge Sankey with wait times and census

## Avoid when
Outpatient-only settings where flow is linear

## Recommended themes
`healthcare-pharma`, `high-contrast-dark`, `accessible-okabe-ito`

## Chart patterns
`sankey`, `histogram`, `matrix-heat`

## Data requirements
- min_rows: 200
- required_measures: `patient_count`, `wait_time`
- required_dimensions: `unit`, `stage`
- date_grain: `day`

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
