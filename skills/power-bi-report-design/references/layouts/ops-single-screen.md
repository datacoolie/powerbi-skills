# Layout: Operational Single-Screen Status Board

> **Preview:** [![ops-single-screen preview](../../assets/layout-previews/ops-single-screen.svg)](../../assets/layout-previews/ops-single-screen.svg) · variants: [annotated](../../assets/layout-previews/ops-single-screen-annotated.svg) · [dark](../../assets/layout-previews/ops-single-screen-dark.svg)

- **id:** `ops-single-screen`
- **Canvas:** 1920 × 1080 (wall-mount TV and desktop; for a TV, keep the grid and raise density/type size instead of changing canvas)
- **Style personality:** Operational (see `../executor-operational.md`)
- **Audience:** Line supervisors, control-room operators, NOC
- **Visual count:** 10-12 (dense, status-driven)
- **Refresh:** < 5 minutes (timestamp mandatory)

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│  TITLE (32pt)         [Last refresh: 09:14:22]  [● LIVE]      │ 72
├────────────────────────────────────────────────────────────────┤
│  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐              │
│  │ KPI1 ││ KPI2 ││ KPI3 ││ KPI4 ││ KPI5 ││ KPI6 │             │ 152
│  │ 48pt ││      ││      ││      ││      ││      │  (status   │
│  └──────┘└──────┘└──────┘└──────┘└──────┘└──────┘   strip)    │
├────────────────────────────────────────────────────────────────┤ 272
│  ┌────────────────────────────────┐ ┌─────────────────────┐    │
│  │  STATUS MATRIX (entities × KPI)│ │ EXCEPTION FEED      │   │
│  │  traffic-light cells           │ │ (scrolling list of  │   │ 488
│  │                                │ │ alerts w/ timestamp)│   │
│  └────────────────────────────────┘ └─────────────────────┘    │
├────────────────────────────────────────────────────────────────┤ 784
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │ Trend 1 │ │ Trend 2 │ │ Trend 3 │ │ Trend 4 │              │ 264
│  │ sparkln │ │ sparkln │ │ sparkln │ │ sparkln │              │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘               │
└────────────────────────────────────────────────────────────────┘ 1080
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Page title | 32 | 24 | 1344 | 48 | textbox | 32pt Semibold, site/line name |
| Refresh timestamp | 1392 | 32 | 312 | 32 | textbox | Dynamic M-driven text; update ≤ 5 min |
| Live indicator | 1720 | 32 | 168 | 32 | card | Pulsing `good` dot if fresh, `bad` if stale |
| KPI 1-6 | 32+(i×312) | 96 | 296 | 152 | card | 48pt value, threshold-colored |
| Status matrix | 32 | 272 | 1152 | 488 | pivotTable | `chart-templates/matrix-scorecard.md` |
| Exception feed | 1200 | 272 | 688 | 488 | tableEx | Sort DESC by timestamp |
| Trend 1-4 | 32+(i×472) | 784 | 448 | 264 | lineChart | Sparkline-style; shared Y axis |

Margins: 32px left/right/bottom. Gaps: 16px within a group (KPI cards, matrix↔feed), 24px between the four trend tiles and between bands. All slots multiples of 8.

---

## Navigation

None — operational boards are standalone. If drill is needed, use double-click behaviors, not buttons. No cross-filter (operators read, don't query).

---

## Theme + iconography guidance

- **Palette:** dark background (background2 dark) + high-contrast `good` / `bad` / `neutral` tokens
- **Logo:** site / plant logo top-left at `(32, 24)`, 32–40px tall — readable from 3m. Pair with plant/shift label right of it. Skip secondary corporate mark — the wall board context is local.
- **Icons:** mandatory status icons on every KPI (●, ▲, ▼)
- **Fonts:** Segoe UI, **48pt** KPI values, **16pt** table cells, no text below 14pt

---

## When NOT to use this layout

- ❌ Executive summary (too dense, too technical)
- ❌ Interactive analytical exploration (users can't drill a wall board)
- ❌ Single-KPI focus (use a card-only kiosk layout)
- ❌ Audience views on phone (operational boards are fixed-display)

---

## Customization allowed

- **FHD headroom (optional)**: one extra slot, answering "how old is the open backlog?" — shrink **Exception feed** to `x=1200, y=272, w=688, h=312`, then add **Open exceptions by age** (bar chart, age buckets) at `x=1200, y=600, w=688, h=160`. Ends at y=760 like the matrix; no overlap. Total stays within the Operational ≤ 14 budget (13).

---

## Data quality gotchas

- **Staleness:** if refresh > 5 min, flip live indicator to `bad` — operators must see data is old
- **Blank cells** in status matrix must render as `neutral`, not `good` (never signal OK when unknown)
- **Exception feed:** cap at last 50 events; older events belong in a history page
