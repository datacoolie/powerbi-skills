# Layout: Finance P&L Waterfall

- **id:** `finance-pnl-waterfall`
- **Canvas:** 1664 × 936
- **Style personality:** Analytical (see `../executor-analytical.md`)
- **Audience:** CFO, controllers, FP&A analysts
- **Visual count:** 6 (hero waterfall + supporting)

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│  Big-Idea P&L title (24pt)                 [Period slicer]    │ 64
├────────────────────────────────────────────────────────────────┤
│  ┌──────────┐┌──────────┐┌──────────┐┌──────────┐              │
│  │ Revenue  ││  COGS    ││Gross Marg││Net Income│              │ 128
│  │ + delta  ││ + delta  ││ + delta  ││ + delta  │              │
│  └──────────┘└──────────┘└──────────┘└──────────┘              │
├────────────────────────────────────────────────────────────────┤ 208
│                                                                │
│    ██ ↑ +Rev                                                   │
│    ██                ↓ -COGS                                   │
│  ██──────────────────██ =Gross     ↓ -OpEx                     │ 440
│                         ────────────██                         │
│                                     ────────────── = Net       │
│        HERO: P&L WATERFALL (actual or vs plan)                │
├────────────────────────────────────────────────────────────────┤ 664
│  ┌─────────────────────┐  ┌─────────────────────┐             │
│  │ Cost breakdown bar  │  │ Variance matrix     │             │ 248
│  │ (top N categories)  │  │ (line × plan/act)   │             │
│  └─────────────────────┘  └─────────────────────┘             │
└────────────────────────────────────────────────────────────────┘ 936
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Page title | 32 | 16 | 1200 | 48 | textbox | Big-Idea framing |
| Period slicer | 1248 | 16 | 384 | 48 | slicer | Horizontal dropdown |
| KPI 1-4 | 32+(i×408) | 88 | 392 | 112 | card | Revenue / COGS / GM / NI + YoY% |
| Hero waterfall | 32 | 216 | 1600 | 440 | waterfallChart | `chart-templates/waterfall-bridge.md` |
| Cost breakdown | 32 | 672 | 792 | 248 | clusteredBarChart | `bar-comparison.md`, top-N opex categories |
| Variance matrix | 840 | 672 | 792 | 248 | pivotTable | `matrix-scorecard.md`, lines × plan / actual / var% |

---

## Navigation

- Drillthrough entry point: right-click a waterfall segment → "See details" page
- Period slicer cross-filters all 6 visuals (matrix + breakdown + waterfall + KPIs)

---

## Theme + iconography guidance

- **Palette:** conservative financial — blue `data0` for positive, red `bad` for negative, `neutral` gray for totals
- **Logo:** company wordmark top-left of title bar at `(32, 24)`, max height 28px. Legal entity name + reporting currency ISO-4217 code go immediately right of the logo (audit context).
- **Icons:** minimal; threshold dots on KPI deltas only
- **Fonts:** Segoe UI, 24pt titles, 14pt labels, ALL currency right-aligned with `$#,0;$(#,0)` format
- **Format strings:** use thousands/millions abbreviation for hero axis; full precision in matrix

---

## When NOT to use this layout

- ❌ Revenue-only story (use `sales-performance` layout)
- ❌ > 10 waterfall categories (split into Revenue Walk + Cost Walk pages)
- ❌ Executive who can't absorb a waterfall (swap hero for a 2-bar Plan vs Actual)

---

## Data quality gotchas

- **Sign convention:** expenses must be negative in the waterfall source (or explicitly flagged as `isSubtotal`/`isNegative`)
- **Subtotal bars:** mark Gross Margin and Net Income as subtotals in the chart data role, not as additional deltas
- **Variance denominator:** `(Actual - Plan) / ABS(Plan)` — the ABS prevents sign flips on negative plan
- **Missing categories:** if a line has no activity this period, render as $0 with `neutral` color, not omitted
