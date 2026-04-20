# Recipe: Matrix Scorecard

> **Preview:** [![matrix-scorecard preview](../../assets/chart-previews/matrix-scorecard.svg)](../../assets/chart-previews/matrix-scorecard.svg)

- **id:** `matrix-scorecard`
- **Visual type:** `pivotTable`
- **Typical size:** 960 × 420 (full-width) or 640 × 360 (half-width)

---

## Composition

```
              │ Actual │ Plan   │ Var %  │ Status │ Trend  │
──────────────┼────────┼────────┼────────┼────────┼────────┤
Region A      │ 4.2M   │ 4.0M   │ +5.0%  │  ●     │  ▲▲▲   │
Region B      │ 2.8M   │ 3.2M   │ -12.5% │  ●     │  ▼▼▼   │
Region C      │ 1.9M   │ 1.8M   │ +5.6%  │  ●     │  ▲▼▲   │
Region D      │ 0.9M   │ 1.1M   │ -18.2% │  ●     │  ▼▼▲   │
──────────────┼────────┼────────┼────────┼────────┼────────┤
Total         │ 9.8M   │ 10.1M  │ -3.0%  │  ●     │  ▼▲▼   │
```

A scorecard is a matrix where **each row is an entity** (region / product / team / KPI)
and **each column is a comparison or status lens** (actual / plan / var / status / trend).
The row grand total is meaningful and must be visible.

---

## Slots

| Slot | Content | Binding example |
|---|---|---|
| Rows | Entity dimension | `Region.RegionName` (sorted by `[Actual]` desc) |
| Columns | *(no column dim — use explicit values)* | — |
| Values | Measures as columns | `[Actual]`, `[Plan]`, `[Variance %]`, `[Status]`, *(sparkline)* |
| Row totals | On | Grand total row visible |
| Column totals | Off | Usually not meaningful across different measures |

---

## Formatting (theme-aware)

- **Header row:** bold, `foreground` on `background2`
- **Row stripes:** alternate `background` / `background2` (enables quick row scan)
- **Variance column:** conditional format background color using `good` / `neutral` / `bad` tokens
  - `> +2%` → `good` tint
  - `-2% to +2%` → `neutral` (no fill)
  - `< -2%` → `bad` tint
- **Status column:** icon set (circle) bound to threshold measure
- **Trend column:** sparkline (line or column) — **max 5 per visual**, max 52 points each
- **Number alignment:** right-aligned for all numeric columns
- **Row sort:** by primary metric descending by default (largest on top)

---

## Narrative frame

- **Executive:** include only 3-4 columns (Actual / Var % / Status / Trend). Total at bottom.
- **Analytical:** can expand to 6-8 columns with multiple time horizons (MTD / QTD / YTD)
- **Operational:** larger fonts (16pt cells), traffic-light status dots mandatory, highlight
  rows below threshold with `bad`-tint background

---

## Do NOT

- Exceed **8 columns** — switch to sparklines or split into two matrices
- Use column totals that sum across different measures (e.g., summing Status + Actual)
- Embed rainbow color scales in the value column — stick to `good`/`bad` semantic colors
- Hide row totals on a scorecard — the grand total is the point
- Apply cross-filtering FROM a matrix scorecard (users read it, they don't click it) — set
  `visualInteractions` for this visual to not filter peers

---

## Data quality gotchas

- **Variance denominator:** `(Actual - Plan) / Plan` — guard against Plan = 0 with `DIVIDE`
- **Status threshold:** put the +/- 2% threshold in a model parameter (not hardcoded)
- **Sparkline granularity:** 12 months is typical; daily data will hit the 52-point cap quickly
- **Missing entities:** use `ISBLANK` fallback so rows with no Plan still appear with "N/A"

---

## Checklist

- [ ] Rows sorted by primary metric desc (not alphabetical)
- [ ] Variance column uses `good`/`bad` tokens, not raw hex
- [ ] Status column uses icon set bound to threshold measure
- [ ] Sparkline count ≤ 5, points ≤ 52
- [ ] Grand total row visible; column total row hidden
- [ ] No cross-filter out (`visualInteractions` configured)
- [ ] Alt text: "Scorecard matrix of <N> <entities> across <metrics>, total <value>"
