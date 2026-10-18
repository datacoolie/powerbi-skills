# Layout: Executive Overview (16:9)

> **Preview:** [![exec-overview-16x9 preview](../../assets/layout-previews/exec-overview-16x9.svg)](../../assets/layout-previews/exec-overview-16x9.svg) · variants: [annotated](../../assets/layout-previews/exec-overview-16x9-annotated.svg) · [dark](../../assets/layout-previews/exec-overview-16x9-dark.svg)

- **id:** `exec-overview-16x9`
- **Canvas:** 1920 × 1080
- **Style personality:** Executive (see `../executor-executive.md`)
- **Audience:** C-suite, board, monthly/quarterly business review
- **Visual count:** 4 (excluding slicers; usually zero slicers)
- **Pairs with themes:** any restrained / muted theme; neutral background preferred

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│                                                                │
│   Big-Idea page title (24pt Semibold)                         │ 64
│   Subtitle (14pt Regular, muted)                              │
├────────────────────────────────────────────────────────────────┤ 112
│                                                                │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                  │
│  │ KPI 1  │ │ KPI 2  │ │ KPI 3  │ │ KPI 4  │                  │ 128
│  └────────┘ └────────┘ └────────┘ └────────┘                  │
├────────────────────────────────────────────────────────────────┤ 264
│                                                                │
│                                                                │
│        HERO visual (trend or primary breakdown)               │
│                                                                │ 472
│        Reference line(s) / target / prior-year                │
│                                                                │
├────────────────────────────────────────────────────────────────┤ 760
│                                                                │
│  ┌─────────────────────┐  ┌─────────────────────┐            │
│  │ Supporting visual 1 │  │ Supporting visual 2 │            │ 296
│  │                     │  │                     │            │
│  └─────────────────────┘  └─────────────────────┘            │
└────────────────────────────────────────────────────────────────┘ 1080
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Page title | 32 | 24 | 1856 | 64 | textbox | Big-Idea phrasing, 24pt Semibold |
| KPI 1 | 32 | 112 | 456 | 128 | card | Apply `chart-templates/kpi-banner.md` |
| KPI 2 | 504 | 112 | 448 | 128 | card | |
| KPI 3 | 968 | 112 | 448 | 128 | card | |
| KPI 4 | 1432 | 112 | 456 | 128 | card | |
| Hero visual | 32 | 264 | 1856 | 472 | line OR bar | `chart-templates/trend-line.md` or `bar-comparison.md` |
| Supporting 1 | 32 | 760 | 920 | 296 | varies | |
| Supporting 2 | 968 | 760 | 920 | 296 | varies | |

Gutters: 16px between KPIs, 16px between supporting, 24px vertical between zones. Margins 32px (24px top and bottom). All multiples of 8.

---

## Navigation

Single-page — no navigation bar. If multi-page, add a 48h button bar at y=96 (x=32, w=1856) and push the KPI row down to y=168 (Hero then starts at y=320 with h=416).

---

## Theme + iconography guidance

- **Palette:** muted; 1-2 accents reserved for highlight on hero visual
- **Logo:** company wordmark top-left of title bar at `(32, 24)`, max height 28px; leave the page title right of it at `(80, 24)`. Leave empty if the theme enforces text-only headers.
- **Icons:** KPI-set icons (trend-up, trend-down, target-hit) on each card
- **Fonts:** Segoe UI throughout

---

## When NOT to use this layout

- ❌ Audience is analysts or ops — too sparse
- ❌ > 4 KPIs (use Analytical's KPI banner instead)
- ❌ Dense time-series exploration needed (use Analytical hero + supporting grid)
- ❌ Multiple dimensions of comparison (use supporting grid of 3, not 2)

---

## Customization allowed

- Swap KPI count 3-5 (adjust widths proportionally, keep 16px gutter)
- Replace supporting-pair with single full-width visual if hero is itself small-multiple
- Add bottom footnote row (y=1032, h=24) for methodology text — shrink Supporting 1/2 to h=248 so they end at y=1008
- **FHD headroom (optional)**: none — the base table is already at this layout's own 4-visual Executive cap (see "Customization NOT allowed").

## Customization NOT allowed

- Changing canvas size (defeats the "16:9" preset)
- Adding a third supporting row (breaks the ≤ 4 visual rule for Executive)
- Removing the KPI row (KPIs are core to the Executive pattern)
