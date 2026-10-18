# Narrative Story Page

> **Preview:** [![narrative-story-page preview](../../assets/layout-previews/narrative-story-page.svg)](../../assets/layout-previews/narrative-story-page.svg) · variants: [annotated](../../assets/layout-previews/narrative-story-page-annotated.svg) · [dark](../../assets/layout-previews/narrative-story-page-dark.svg)

- Canvas: `1920×1080` (landscape-16x9)
- Style: `executive` · Domain: `cross-domain`
- Visuals: 5
- Zones: `title-bar, narrative-text-panel, annotated-chart-large, insight-callouts, footer`

## Use when
Text-heavy insight narrative — scrollytelling style with annotated chart and pull-quotes

## Avoid when
Operational audiences expecting dense KPI grids

## Customization allowed
- **FHD headroom (optional)**: one extra slot, answering "which segment drives the change?" — shrink `insight-callouts` to `x=1120, y=432, w=784, h=360`, then add **Driver breakdown** (small bar chart) at `x=1120, y=808, w=784, h=200`. Ends at y=1008 like the annotated chart; no overlap. Stays within the Executive ≤ 6 visuals budget.

## Recommended themes
`consulting-authority`, `brand-stripe`, `media-entertainment`, `sustainability-esg`

## Chart patterns
`annotated-chart`, `callout-text`, `pull-quote`

## Data requirements
- min_rows: 12
- required_measures: `primary_metric`
- required_dimensions: `date`
- date_grain: `month`

See `layouts-index.json` for full machine-readable entry including `zones_detail[]`.
