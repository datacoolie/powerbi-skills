# Inventory ABC Analysis

> **Preview:** [![supply-inventory-abc preview](../../assets/layout-previews/supply-inventory-abc.svg)](../../assets/layout-previews/supply-inventory-abc.svg) · variants: [annotated](../../assets/layout-previews/supply-inventory-abc-annotated.svg) · [dark](../../assets/layout-previews/supply-inventory-abc-dark.svg)

- Canvas: `1920×1080` (landscape-16x9)
- Style: `analytical` · Domain: `supply-chain`
- Visuals: 8
- Zones: `title-bar, slicer-row, turns-ratio-kpis, abc-matrix, stockout-risk-heatmap, supporting-pair`

## Use when
Inventory classification + turns + stockout risk for SKU portfolio

## Avoid when
Make-to-order businesses where stock levels aren't held centrally

## Recommended themes
`supply-chain-logistics`, `manufacturing-ops`, `consulting-authority`

## Chart patterns
`matrix-heat`, `kpi-card-with-spark`, `ranking-bar`

## Data requirements
- min_rows: 500
- required_measures: `turns`, `stockout_pct`
- required_dimensions: `sku`, `warehouse`
- date_grain: `week`

## Customization allowed
- **FHD headroom (optional):** re-tile `supporting-pair` (y=808, h=248) from two tiles to three equal tiles of w=608 at x=24 / 656 / 1288, and add one slot at `x=1288, y=808, w=608, h=248` — *Days of supply vs target by ABC class* (clustered bar with target marker). It answers a distinct question: is stock cover appropriate for each class, rather than how fast it turns. Brings the page to 9 visuals (analytical budget ≤ 12).

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
