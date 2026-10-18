# Layout: Manufacturing Line Status (OEE)

> **Preview:** [![mfg-line-status preview](../../assets/layout-previews/mfg-line-status.svg)](../../assets/layout-previews/mfg-line-status.svg) · variants: [annotated](../../assets/layout-previews/mfg-line-status-annotated.svg) · [dark](../../assets/layout-previews/mfg-line-status-dark.svg)

- **id:** `mfg-line-status`
- **Canvas:** 1920 × 1080 (shop-floor display and desktop — one canvas; the display differs only by density: larger fonts, no slicer)
- **Style personality:** Operational (see `../executor-operational.md`)
- **Audience:** Production supervisors, line operators, plant manager
- **Visual count:** 10 (line-level OEE detail)

---

## Zone map (1920 × 1080)

Numbers inside a band are its height; numbers on a divider are the y where the next band starts.

```
┌────────────────────────────────────────────────────────────────┐ 0
│  LINE A-3 — Shift 2         [Last refresh: 14:22]  [● RUNNING]│ 48
├────────────────────────────────────────────────────────────────┤ 88
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │   OEE    │ │Availability│ │Performance│ │ Quality  │         │ 144
│  │  82.3%   │ │  94.1%   │ │  91.2%   │ │  96.0%   │           │
│  │  (48pt)  │ │          │ │          │ │          │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
├────────────────────────────────────────────────────────────────┤ 256
│  ┌──────────────────────────────┐ ┌──────────────────────────┐ │
│  │  Hourly output (bars)        │ │ Downtime Pareto (bars)   │ │ 288
│  │  + target line               │ │ top-N reason codes       │ │
│  └──────────────────────────────┘ └──────────────────────────┘ │
├────────────────────────────────────────────────────────────────┤ 568
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  │
│  │ Scrap % trend   │ │ Speed trend     │ │ First-pass yield│  │ 208
│  │ (spark)         │ │ (spark)         │ │ (spark)         │  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘  │
├────────────────────────────────────────────────────────────────┤ 800
│  Current Work Orders table (WO# / product / target / actual / status)│ 248
└────────────────────────────────────────────────────────────────┘ 1080
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Page title | 32 | 24 | 1376 | 48 | textbox | Line + shift (dynamic from slicer or URL param) |
| Refresh + status | 1424 | 32 | 464 | 40 | card group | Live indicator mandatory |
| OEE card | 32 | 88 | 440 | 144 | card | 48pt, threshold-colored (`bad` < 65, `neutral` 65-80, `good` > 80) |
| Availability card | 504 | 88 | 440 | 144 | card | Same threshold logic |
| Performance card | 976 | 88 | 440 | 144 | card | Same threshold logic |
| Quality card | 1448 | 88 | 440 | 144 | card | Same threshold logic |
| Hourly output | 32 | 256 | 920 | 288 | clusteredColumnChart | Reference line = target throughput |
| Downtime Pareto | 968 | 256 | 920 | 288 | clusteredBarChart | Sorted DESC, top-N reason codes |
| Trend 1 (scrap %) | 32 | 568 | 608 | 208 | lineChart | Sparkline-style, shared axis |
| Trend 2 (speed) | 656 | 568 | 608 | 208 | lineChart | Sparkline-style, shared axis |
| Trend 3 (first-pass yield) | 1280 | 568 | 608 | 208 | lineChart | Sparkline-style, shared axis |
| Work orders table | 32 | 800 | 1856 | 248 | tableEx | Conditional format `status` column |

Margins 32px. Gutters: 32px between the four KPI cards (4 × 440 + 3 × 32 = 1856), 16px between paired charts and between the three trends, 24px between rows.

---

## Navigation

- NOT interactive — shop-floor display is read-only
- If accessed from a plant overview, drillthrough field = Line ID
- No slicers except an optional Shift picker (top-right) on desktop variant

---

## Theme + iconography guidance

- **Palette:** dark industrial — dark background2, high-contrast `good` (green) / `bad` (red) / `neutral` (amber) tokens
- **Logo:** plant + line badge top-left at `(32, 24)`, 40px tall — must be readable from ≥ 5m. Corporate logo optional, top-right small. Include line-ID chip next to the logo so operators instantly recognize the board.
- **Icons:** status icons on every KPI and on work-order rows
- **Fonts:** 48pt OEE value, 32pt other KPI values, 14pt minimum everywhere else
- **Reference lines:** target throughput on hourly chart in `neutral` dashed line

---

## When NOT to use this layout

- ❌ Plant or corporate overview (use `ops-single-screen` with multi-line summary)
- ❌ Historical OEE analysis (use `sales-performance`-style analytical page with time slicer)
- ❌ Non-discrete manufacturing (process plants need flow rates, not unit counts)

---

## Data quality gotchas

- **OEE formula:** Availability × Performance × Quality — all three inputs must be on the same time window
- **Target line** on hourly output is shift-dependent; ensure the target changes when shift changes
- **Downtime code completeness:** operators sometimes leave downtime uncoded — render uncoded as `neutral` and separate from real reasons
- **Work-order status:** use an enum `Running / Setup / Down / Complete`, not free text
