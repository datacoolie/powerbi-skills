# Layout: Geographic / Territory Map

> **Preview:** [![geo-territory-map preview](../../assets/layout-previews/geo-territory-map.svg)](../../assets/layout-previews/geo-territory-map.svg) · variants: [annotated](../../assets/layout-previews/geo-territory-map-annotated.svg) · [dark](../../assets/layout-previews/geo-territory-map-dark.svg)

- **id:** `geo-territory-map`
- **Canvas:** 1920 × 1080
- **Style personality:** Analytical
- **Audience:** Regional managers, sales ops, logistics planners
- **Visual count:** 6
- **Pairs with themes:** any; map fill uses sequential single-hue scale

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Title bar: "Territory performance — {Region}"                 │ 64
├────────────────────────────────────────────────────────────────┤
│ Region slicer row (Region · Sub-region · Period · Metric)     │ 56
├────────────────────────────────────────────────────────────────┤
│                                      │                         │
│        MAP HERO                      │   KPI stack (3)         │ 320
│   (filled map + bubble overlay       │   • Revenue             │
│    sized by volume)                  │   • Growth YoY          │
│                                      │   • # territories hit   │
│                                      ├─────────────────────────┤
│                                      │   Ranked bar (top 10    │ 280
│                                      │   regions, sorted)      │
├────────────────────────────────────────────────────────────────┤
│ Territory table: region × rep × revenue × plan% × status      │ 224
└────────────────────────────────────────────────────────────────┘ 1080
```

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Title bar | 32 | 24 | 1856 | 64 | textbox | |
| Region slicer | 32 | 112 | 1856 | 56 | slicer × 4 | |
| Map hero | 32 | 192 | 1200 | 616 | azureMap | Bubble size = volume; fill = metric |
| KPI: Revenue | 1248 | 192 | 640 | 96 | card | |
| KPI: Growth YoY | 1248 | 304 | 640 | 96 | card | |
| KPI: Coverage | 1248 | 416 | 640 | 96 | card | |
| Ranked bar | 1248 | 528 | 640 | 280 | bar (descending) | Top 10 regions |
| Territory table | 32 | 832 | 1856 | 224 | pivotTable | Status column with traffic-light icons |

Gutters: 16px inside a group (map ↔ right column, KPI stack ↔ ranked bar), 24px between rows. Margins 32px (24px top and bottom).

## Navigation

Cross-filter from map → ranked bar → table is automatic. For drill into a single rep, enable **Drillthrough** to `drillthrough-detail` page keyed on `TerritoryId`.

## Theme + iconography guidance

- **Map**: filled map first choice (no API key); Azure Map only if plot density demands it
- **Logo:** company wordmark top-left of title bar at `(32, 24)`, max height 28px. Region / country flag icons, if used, live on table rows — never on the logo slot.
- **Icons**: map-pin, compass, flag on KPIs
- **Avoid** rainbow scales — use sequential single-hue for revenue fill

## When NOT to use this layout

- ❌ No geographic grain in data
- ❌ Single territory drill (use `drillthrough-detail`)
- ❌ Logistics route detail (use dedicated route-optimization tool, not PBI)

## Customization allowed

- **FHD headroom (optional)** — one extra slot carved from the table row (visual count 6 → 7, within the Analytical ≤ 12 budget): *Revenue trend* line at (1248, 832, 640, 224); shrink Territory table to w=1200. Answers "is revenue in the selected territory rising or flat over time?" — the map and table only show a snapshot.
