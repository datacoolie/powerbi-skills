# Layout: Wide Flat Tooltip

- **id:** `wide-flat-tooltip`
- **Canvas:** 1200 × 320
- **Style personality:** Analytical — Panoramic tooltip (~1200×320) showing 1–3 side-by-side sparklines / trend bars
- **Audience:** Hover consumers — enrichment when the default 320×240 tooltip is insufficient
- **Visual count:** 3
- **Pairs with themes:** neutral body with one accent — pattern designed to read on any corporate palette.
- **Observed in:** `references-pbip/Sales Analysis Demo (V.GF).Report/` — 'Tooltip trendline' (900×300); `SALES ANALYTICS DEMO (v.AFC).Report/` — 'TOOLTIPS DAILY SALES' (1200×320)

---

## Zone map

```
┌──────────────────────────────────────────────────────────────────┐ 0
│ Tooltip header: entity name · period · primary value             │ 40
├────────────────────┬──────────────────────┬──────────────────────┤
│                    │                      │                      │
│ ~ Spark 1 (QTY)    │  ~ Spark 2 (VALUE)   │   ~ Spark 3 (MIX%)   │ 240
│                    │                      │                      │
├────────────────────┴──────────────────────┴──────────────────────┤
│ Tooltip footer: 3 delta labels · scale                           │ 40
└──────────────────────────────────────────────────────────────────┘
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Tooltip header | 0 | 0 | 1200 | 40 | textbox + card | Entity label + primary value |
| Spark panel 1 | 8 | 48 | 388 | 240 | lineChart or sparkline | Metric A over time |
| Spark panel 2 | 404 | 48 | 388 | 240 | lineChart or sparkline | Metric B over time |
| Spark panel 3 | 800 | 48 | 392 | 240 | lineChart or sparkline | Metric C over time or mix breakdown |

Gutters: 16px between primary zones; 8px inside KPI card rows.

---

## Navigation

- Reachable from the report's top-nav chiclet strip or landing page. Include a small 'Home' actionButton in the header when not the landing page.
- Cross-links out to related drillthrough / detail pages should be surfaced via card-level actions, not a separate nav rail.

---

## Theme + iconography guidance

- **Palette:** Neutral; accent only the current-period marker. No axis labels except min/max.
- **Logo:** NOT allowed (tooltip should be ultra-light).
- **Icons:** Optional one 10px glyph per panel title.
- **Fonts:** Header 12pt Semibold, panel titles 9pt, value callouts 11pt bold.

---

## When NOT to use this layout

- ❌ The hover source fits `tooltip-page` (320×240) — always prefer the small tooltip for point-hovers
- ❌ The hover reveals a table — tables don't compress into a wide tooltip; show a drillthrough page instead
- ❌ Use-case is mobile — tooltips don't render on touch

---

## Customization allowed

- Collapse to 2 panels (610w each) for two-metric hovers
- Change canvas to 900×300 for narrower tooltip sources
- Add a 'trend 6M / 12M' toggle via bookmark (one only)

## Customization NOT allowed

- Putting full chart legends — tooltips must stay quick-read
- Page navigation buttons — tooltips cannot be navigated
- Exceeding 4 visuals (performance; page can flash on hover)
