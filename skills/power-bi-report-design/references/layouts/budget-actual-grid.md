# Layout: Budget vs Actual Grid

- **id:** `budget-actual-grid`
- **Canvas:** 1664 × 936
- **Style personality:** Analytical — budget workbench
- **Audience:** FP&A analysts, budget owners, line managers during re-forecast
- **Visual count:** 10 (4 actual / estimate card pairs + 1 pivot matrix + 1 trend + 1 slicer + 1 title) — reflow-enhanced (was 8)
- **Pairs with themes:** neutral; 1 accent for "estimate" vs solid base for "actual"
- **Observed in:** `references-pbip/AEON_BGT_Data Analysis_Demo.Report/` — "Overview"

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Title + slicer: Period                                        │ 73
├─────────────────────────────────────┬──────────────────────────┤
│                                     │                          │
│ Actual / estimate card pairs        │                          │
│ ┌──────────┐ ┌──────────┐           │                          │
│ │ Act1     │ │ Est1     │           │                          │
│ └──────────┘ └──────────┘           │                          │
│ ┌──────────┐ ┌──────────┐           │  Pivot matrix            │ 530
│ │ Act2     │ │ Est2     │           │  (Product × Period)     │
│ └──────────┘ └──────────┘           │                          │
│ ┌──────────┐ ┌──────────┐           │                          │
│ │ Act3     │ │ Est3     │           │                          │
│ └──────────┘ └──────────┘           │                          │
│ ┌──────────┐ ┌──────────┐           │                          │
│ │ Act4     │ │ Est4     │           │                          │
│ └──────────┘ └──────────┘           │                          │
├─────────────────────────────────────┤                          │
│  Trend chart (actual vs estimate)   │                          │ 312
└─────────────────────────────────────┴──────────────────────────┘ 936
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Title | 31 | 21 | 910 | 42 | textbox | "Budget vs Actual — {Period}" |
| Slicer: Period | 1222 | 21 | 411 | 42 | slicer (buttons) | MTD / QTD / YTD |
| Actual card 1–4 | 31 | 94 / 208 / 322 / 437 | 286 | 104 | card | Left column, solid accent left-border |
| Estimate card 1–4 | 333 | 94 / 208 / 322 / 437 | 286 | 104 | card | Right column, muted / hatched left-border |
| Trend chart | 31 | 572 | 588 | 333 | lineChart | Actual line solid, estimate line dashed |
| Pivot matrix | 645 | 94 | 988 | 811 | pivotTable | Rows=product / BU, cols=period, values=actual + estimate |

Pair spacing: 12px between Actual/Estimate card in each row, 8px vertical between rows. The pair alignment is itself the read signal — left-column is always actual, right-column always estimate.

---

## Navigation

Single-page workbench. Optional "Scenario" bookmarks row above title bar (push title to y=56, slicer to y=56).

---

## Theme + iconography guidance

- **Palette:** one solid accent for "Actual", the same accent at 40% opacity / hatched for "Estimate". NO other hues.
- **Logo:** omit on this workbench page — the audience is internal analysts. If branding is mandated, put it in the title bar at `(24, 16)` max height 24px and shift title to x=76.
- **Icons:** none in cards. Small legend chip near trend chart: ■ Actual · ▨ Estimate.
- **Fonts:** card value 24pt Semibold, label 11pt muted. Matrix headers 11pt bold, cells 11pt.

---

## When NOT to use this layout

- ❌ No estimate / forecast data available — collapses to a single-column actuals page (use `exec-overview-16x9` instead)
- ❌ > 6 metrics needing pairs — grid over-runs the vertical space
- ❌ Mobile / tooltip — matrix is unreadable at small canvases

---

## Customization allowed

- Add a third column "Variance %" card between Actual and Estimate (widths: 180 / 180 / 180 with 8px gutter)
- Collapse trend chart if screen real estate is limited (extend matrix down into the bottom band)
- Swap matrix for a ranked-bar (top contributors to variance)

## Customization NOT allowed

- Reversing column order (estimate-left / actual-right — breaks the "what is" before "what was planned" reading)
- Using different accents for each pair (the eye needs a single actual-vs-estimate colour pattern)

---

## Reflow additions (v0.6)

The matrix dominates the right half but offers no interpretive layer. Reclaim a **52h commentary strip** above it for narrative callouts, and a **right-edge %-attainment heatmap column** that converts the matrix's raw numbers into a scan-friendly traffic-light encoding per row.

### Integration

Shrink **Pivot matrix** `h` from `811` to `759` (matrix starts at `y=146` instead of `y=94`; 52h commentary slot goes above). Narrow matrix `w` from `988` to `820` to create a 156w heatmap column at `x=1477`.

### New slots

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Budget commentary strip | 645 | 94 | 988 | 52 | textbox + shape | Key driver commentary; refreshes monthly; 12pt |
| %-attainment heatmap | 1477 | 146 | 156 | 759 | matrix (% formatting) | Rows mirror pivot; single-column heat: red<90, amber 90–100, green>100 |

