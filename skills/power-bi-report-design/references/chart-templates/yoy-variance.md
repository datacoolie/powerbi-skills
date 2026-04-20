# Recipe: Year-over-Year Variance

> **Preview:** [![yoy-variance preview](../../assets/chart-previews/yoy-variance.svg)](../../assets/chart-previews/yoy-variance.svg)

- **id:** `yoy-variance`
- **Visual type:** `clusteredColumn` (default) OR `lineClusteredColumnCombo` (when variance is a % line overlaid)
- **Typical size:** 816 × 384 (supporting slot)

---

## Composition

### Variant A — Clustered column (two periods, side-by-side)

```
┌────────────────────────────────────────────┐
│  $5M                                      │
│                                            │
│   ██ ██                                    │  ← current year (data0)
│   ██ ██  ██ ██                             │  ← prior year (data1, muted)
│   ██ ██  ██ ██  ██ ██  ██ ██               │
│   ██ ██  ██ ██  ██ ██  ██ ██  ██ ██        │
│                                            │
│   Q1     Q2     Q3     Q4     YTD          │
└────────────────────────────────────────────┘
```

### Variant B — Combo (bars = current, line = YoY%)

```
┌────────────────────────────────────────────┐
│  $5M                              +20%    │  ← variance line, secondary axis
│  $4M   ═══════●                           │
│         ●═══════════●                     │  ← YoY % line
│  $3M   ██       ██                        │
│  $2M   ██   ██  ██   ██                   │  ← current revenue bars
│        ██   ██  ██   ██   ██              │
│        Q1   Q2  Q3   Q4  YTD              │
└────────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category axis | Period grain (Month, Quarter, etc.) | `DimDate[Month Name]` or `DimDate[Quarter]` |
| Current series | Current-year measure | `[Total Revenue]` |
| Prior series | Prior-year measure | `[Prior Year Revenue]` |
| Variance (Combo) | YoY % | `[YoY Revenue %]` |

---

## Formatting (theme-aware)

### Variant A
- Current series: `data0` saturated
- Prior series: `data0` muted (30-40% opacity) OR `neutral`
- Data labels: ON, only on current series
- Tooltip must include variance % (even though not visualized)

### Variant B
- Bars: `data0`
- Line: `data1` OR accent color
- Secondary axis for line: 0 to max(variance %) × 1.2
- Line markers ON; data labels on line ON (format as `+12%` / `-5%`)
- Conditional color on line: `good` if positive, `bad` if negative

---

## Narrative frame by style

| Style | Preferred variant | Rationale |
|---|---|---|
| Executive | Variant B (combo) with bold variance callouts | Executives want the "so what" — variance line tells it |
| Analytical | Variant A (clustered) for side-by-side reading | Analysts compare actuals directly |
| Operational | Rarely used — YoY is not an ops status metric |

---

## Labeling conventions

- **Title:** include the comparison explicitly — "Revenue by quarter: FY2025 vs FY2024"
- **Legend:** "Current year" / "Prior year" (not "Sum of Revenue" / "Sum of Prior Year Revenue")
- **Variance labels:** prefix with + / − ; use parentheses for negatives in finance contexts

---

## Do-NOT list

- ❌ Stacked (current + prior stacked on top) — kills comparison
- ❌ Area chart for YoY comparison — overlaps obscure data
- ❌ Show variance as a separate axis without explicit axis title / unit
- ❌ Use cumulative YTD on monthly grain without saying so (reader confusion)

---

## Data quality gotchas

- **Prior-year measure** — must use time-intelligence (SAMEPERIODLASTYEAR or CALCULATE with DATEADD) not a hard-coded filter
- **Incomplete prior year** — if comparing MTD to prior-year-MTD, explicitly measure this (`[PY Revenue MTD]`, not `[Prior Year Revenue]` filtered at report level)
- **Fiscal vs calendar year** — confirm which the prior-year measure uses
- **Variance when prior = 0** — handle divide-by-zero (return BLANK or large sentinel)

---

## Checklist

- [ ] Variant selected (A or B) and matches style personality
- [ ] Current series uses full-saturation color; prior series muted
- [ ] Variance sign handled (+/-)
- [ ] Title names both periods
- [ ] Prior-year measure uses time-intelligence (Phase 3)
- [ ] Variance measure handles divide-by-zero
