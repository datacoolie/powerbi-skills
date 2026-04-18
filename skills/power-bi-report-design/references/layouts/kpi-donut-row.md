# Layout: KPI Donut Row

- **id:** `kpi-donut-row`
- **Canvas:** 1664 × 936
- **Style personality:** Executive — financial "at-a-glance"
- **Audience:** CFO, FP&A leads, monthly financial review
- **Visual count:** 12 (4 donut KPIs + 4 variance cards + 2 trend charts) — reflow-enhanced (was 10)
- **Pairs with themes:** muted neutral with 1 accent + 1 secondary semantic
- **Observed in:** `references-pbip/Financial Dashboard Demo (FMCG) (Eng ver).Report/` — "Financial Overview"

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Header bar: logo + page title + period selector (right)       │ 83
├────────────────────────────────────────────────────────────────┤
│ ⬤ Donut1  ⬤ Donut2  ⬤ Donut3  ⬤ Donut4    (progress-to-target)│ 198
├────────────────────────────────────────────────────────────────┤
│ Var 1   │ Var 2   │ Var 3   │ Var 4      (vs-plan cards)      │ 114
├────────────────────────────────────────────────────────────────┤
│                                │                                │
│  Trend chart — Revenue path    │  Trend chart — Margin path    │ 364
│                                │                                │
└────────────────────────────────────────────────────────────────┘ 936
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Header bar (shape) | 0 | 0 | 1664 | 83 | shape | Accent fill; page chrome |
| Page title | 31 | 21 | 832 | 42 | textbox | 22pt Semibold, on header |
| Period selector | 1144 | 21 | 489 | 42 | slicer (buttons) | MTD · QTD · YTD |
| Donut KPI 1–4 | 31 / 437 / 842 / 1248 | 104 | 385 | 208 | donutChart (as KPI) | Progress vs target, big centre figure |
| Variance card 1–4 | 31 / 437 / 842 / 1248 | 328 | 385 | 104 | card | Δ vs plan + sparkline row |
| Revenue trend | 31 | 452 | 801 | 458 | lineChart | Actual vs target overlay |
| Margin trend | 863 | 452 | 770 | 458 | lineChart | Actual vs prior-year overlay |

Gutters: 16px between donut columns, 8px between donut and its variance card (visual coupling), 24px between card-row and trend-row.

---

## Navigation

Header-bar period selector is the ONLY page filter. If the report has an exec-overview upstream, include a small "← Overview" button at `(24, 16)` inside the header and shift the title 48px right.

---

## Theme + iconography guidance

- **Palette:** accent for the donut "achieved" arc; muted fill for "remaining". Semantic green/red reserved for variance-card delta glyphs only.
- **Logo:** company wordmark on the left of the header bar at `(24, 20)`, max height 24px. Period selector anchors to header right — the two should not overlap at any canvas width ≥ 1200.
- **Icons:** one sector icon inside each donut centre (revenue, cost, margin, cash); same weight/stroke.
- **Fonts:** donut centre value 28pt Semibold; variance-card delta 14pt with colored arrow glyph.

---

## When NOT to use this layout

- ❌ KPIs without a target — donuts lose meaning (use `scorecard-kpi-grid` instead)
- ❌ More than 5 KPIs — the row breaks onto two lines and cards decouple
- ❌ Audience wants raw numbers only — the donut's progress framing is editorial

---

## Customization allowed

- Reduce to 3 donuts + 3 cards (widen each column proportionally)
- Replace one trend with a horizontal bar of "top 5 lines of business"
- Collapse variance cards if space is tight (donut centre can carry both value and Δ)

## Customization NOT allowed

- Swapping donuts for gauges (different visual semantics; use a different layout)
- Removing the header bar (breaks the branded-exec look)
- Stacking trends vertically in the remaining 352h (charts become flat ribbons)

---

## Reflow additions (v0.6)

The baseline layout fills the canvas with donuts + variance cards + 2 trend charts, but the right edge of the margin trend is visually light. Reclaim a 290w right rail to surface **top-5 contributors** and a **driver sparkline stack** — answering the natural follow-up question 'what drove the delta?' in the same glance.

### Integration

Shrink **Margin trend** from `w=770` to `w=510` (keeps legibility; drops one month of x-axis tick labels). Keep `Revenue trend` unchanged.

### New slots

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Top-5 contributors | 1383 | 452 | 250 | 220 | tableEx (compact) | Rank list: measure + ΔvPlan sparkline per row |
| Driver sparkline stack | 1383 | 680 | 250 | 230 | lineChart × 4 (small-multiple) | Per-KPI mini-trend, labels right-aligned |

