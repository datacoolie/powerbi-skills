# Layout: Balanced Scorecard / KPI Grid

- **id:** `scorecard-kpi-grid`
- **Canvas:** 1664 × 936
- **Style personality:** Executive — signal-dense, low-noise
- **Audience:** Executives, strategy office, OKR owners
- **Visual count:** 12 KPI tiles (+ title, period toggle, legend)
- **Pairs with themes:** muted neutral; semantic green/amber/red only

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Title bar: "Enterprise Scorecard — {Period}"                  │ 56
├────────────────────────────────────────────────────────────────┤
│ Period toggle (MTD / QTD / YTD) on the right                  │ 40
├────────────────────────────────────────────────────────────────┤
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐                                       │
│ │K1 │ │K2 │ │K3 │ │K4 │   Perspective 1: Financial           │ 220
│ └───┘ └───┘ └───┘ └───┘                                       │
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐                                       │
│ │K5 │ │K6 │ │K7 │ │K8 │   Perspective 2: Customer            │ 220
│ └───┘ └───┘ └───┘ └───┘                                       │
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐                                       │
│ │K9 │ │K10│ │K11│ │K12│   Perspective 3: Process / Growth    │ 220
│ └───┘ └───┘ └───┘ └───┘                                       │
├────────────────────────────────────────────────────────────────┤
│ Legend strip: ● On track · ● At risk · ● Off track            │ 40
└────────────────────────────────────────────────────────────────┘ 936
```

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Title bar | 32 | 16 | 1200 | 56 | textbox | |
| Period toggle | 1240 | 24 | 392 | 40 | slicer (tile) | MTD/QTD/YTD buttons |
| KPI tile 1–4 | 32/436/840/1244 | 80 | 388 | 220 | card | Row 1 — financial perspective |
| KPI tile 5–8 | 32/436/840/1244 | 312 | 388 | 220 | card | Row 2 — customer perspective |
| KPI tile 9–12 | 32/436/840/1244 | 544 | 388 | 220 | card | Row 3 — process / growth |
| Legend strip | 32 | 780 | 1600 | 40 | textbox + shape | Traffic-light legend |

Each KPI tile contains: metric name (11pt), big value (36pt Semibold), delta vs target (12pt muted), status dot (left-edge 6px strip colored per status), mini sparkline (bottom 30% of tile).

## Theme + iconography guidance

- **Palette:** neutrals + green/amber/red traffic-light triad only — no other accents
- **Logo:** company wordmark top-left of title bar at `(32, 24)`, max height 28px — scorecards are formal exec docs, logo is expected. Period toggle pins to top-right of same bar; do not compete with logo.
- **Icons:** one per perspective (dollar, users, gear); place top-right of each tile
- **Status strip**: 6px left-edge colored bar is the primary signal, not the text

## When NOT to use this layout

- ❌ Need to explain movements — no room for narrative; pair with exec-overview
- ❌ KPIs require different time-grain per tile (scorecard assumes shared period toggle)
- ❌ Fewer than ~8 KPIs — the grid looks sparse; use `exec-overview-16x9` instead
