# Layout: Full-Page Map

- **id:** `full-page-map`
- **Canvas:** 1664 × 936
- **Style personality:** Analytical — One dominant ArcGIS / Esri map occupying ~80% of the canvas + thin slicer strip
- **Audience:** Field sales / territory managers — geography is the primary analysis axis
- **Visual count:** 4
- **Pairs with themes:** neutral body with one accent — pattern designed to read on any corporate palette.
- **Observed in:** `references-pbip/Sales Analysis (CP Demo).Report/` — 'Map' (ArcGIS visual at x≈252, y≈120, w≈1018, h≈590)

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Thin header: title + period + region slicer                   │ 78
├────────────────────────┬───────────────────────────────────────┤
│                        │                                       │
│  Compact slicer rail    │                                      │
│   · Region              │                                      │
│   · Channel             │       FULL-CANVAS MAP                │ 780
│   · Metric              │                                      │
│                        │                                       │
│                        │                                       │
├────────────────────────┴───────────────────────────────────────┤
│ Footer: legend · scale · data-last-refresh                     │ 78
└────────────────────────────────────────────────────────────────┘
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Header | 0 | 0 | 1664 | 78 | shape + textbox + slicer(Period) | Title left, period right |
| Slicer rail | 0 | 78 | 312 | 780 | slicer(Region) + slicer(Channel) + slicer(Metric) | Narrow left column |
| Map | 312 | 78 | 1352 | 780 | arcGIS / azureMap / shapeMap | Dominant visual |
| Footer / legend | 0 | 858 | 1664 | 78 | textbox + shape | Metric legend + scale + refresh stamp |

Gutters: 16px between primary zones; 8px inside KPI card rows.

---

## Navigation

- Reachable from the report's top-nav chiclet strip or landing page. Include a small 'Home' actionButton in the header when not the landing page.
- Cross-links out to related drillthrough / detail pages should be surfaced via card-level actions, not a separate nav rail.

---

## Theme + iconography guidance

- **Palette:** Map base neutral; data symbology = sequential (magnitude) or diverging (variance). Avoid decorative colours — let symbology carry meaning.
- **Logo:** Header top-left at (16, 16) max height 28px.
- **Icons:** Small marker glyph in the slicer rail next to 'Metric'.
- **Fonts:** Header 16pt, slicer labels 10pt, legend 9pt.

---

## When NOT to use this layout

- ❌ Territory count < 20 — a column chart by region communicates better
- ❌ Data is global but audience cares about 3 countries only — use `scorecard-kpi-grid` with region cards
- ❌ Tenant blocks ArcGIS Plus / Esri — fall back to `geo-territory-map`

---

## Customization allowed

- Add ONE small overlay card (value of selected region) pinned top-right of the map
- Replace the slicer rail with a collapsible outspace pane → map expands to full width

## Customization NOT allowed

- Adding other charts beside the map (shrinks map below 60% — defeats the pattern; use `sales-performance` instead)
- Embedding multiple maps — pick ONE geography visual per page
