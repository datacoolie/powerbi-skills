# Recipe: Time-Series Trend (Line)

- **id:** `trend-line`
- **Visual type:** `lineChart` (occasionally `lineClusteredColumnCombo` for combo with bars)
- **Typical size:** 1632 × 320 (hero) OR 792 × 280 (supporting)

---

## Composition

```
┌────────────────────────────────────────────────────────────┐
│ $5M ─────────────────────────────────  $4.8M              │ ← reference line (plan)
│                                                            │
│       ●────●                           ●                  │ ← series 1 (actuals)
│   ●──╱      ╲──────●────●                ╲──●             │
│                                                            │
│ ┄┄┄┄─┄┄┄┄─┄┄┄┄─┄┄┄┄─┄┄┄┄─┄┄┄┄─┄┄┄┄        prior year      │ ← series 2 (dashed)
│                                                            │
│ Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov Dec │
└────────────────────────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Time axis (X) | Continuous date | `DimDate[Date]` (at Month grain) |
| Value axis (Y) | Primary measure | `[Total Revenue]` |
| Secondary series | (optional) comparison | `[Prior Year Revenue]` |
| Reference line | Target / plan | Static value OR `[Plan Revenue]` |

---

## Formatting (theme-aware)

- **Series 1 color:** `data0`, line weight 3px, markers ON (circle, 6px)
- **Series 2 color:** `neutral` (gray), line weight 2px, dashed, markers OFF
- **Reference line:** `maximum` or muted accent, dashed 2px, label ON ("Plan: $4.8M")
- **Value axis:** visible when no data labels; hidden when showing start + end labels only
- **Time axis:** visible, 10pt, gridlines OFF

---

## Endpoint labeling (Analytical + Executive default)

Turn on data labels for:
- **First data point** (start value as baseline)
- **Last data point** (current value)
- **Inflection points** (max, min) if meaningful

Suppress all other labels — they create noise.

---

## Narrative frame by style

| Style | Default recipe |
|---|---|
| Executive | Single series, heavy annotation, reference line labeled, callout textbox over key inflection. |
| Analytical | 2 series (current vs prior), reference line, endpoint labels only, markers on current series. |
| Operational | Rarely used (ops prefers card / gauge). If used: last-7-days rolling, threshold band shaded. |

---

## Time-axis grain rules

| Range covered | Grain |
|---|---|
| ≤ 31 days | Day |
| 32 days - 12 months | Month |
| 13-36 months | Month OR Quarter |
| 37+ months | Quarter OR Year |

Never mix grains in one series. Use "Continuous" axis type unless data has gaps (then "Categorical").

---

## Series count cap

- 1 series: ideal
- 2-3 series: OK, distinct colors
- 4 series: last resort — differentiate by color + marker shape
- 5+ series: **switch to small-multiples** (`small-multiples-trend` recipe — see gaps)

---

## Do-NOT list

- ❌ Secondary Y-axis unless the same unit and justified
- ❌ Filled-area line chart by default (obscures comparison) — only when single series + emphasizing magnitude
- ❌ Line chart with < 3 data points (use card)
- ❌ Color-only series differentiation (add markers)
- ❌ Smoothed (curved) lines — implies data between points that doesn't exist

---

## Data quality gotchas

- **Date table** — visual must bind to the Date column of a marked-as-date table
- **Gaps in data** — decide: hide (gap), zero (drop to axis), or interpolate (connect). Default: hide.
- **Incomplete current period** — last data point may include partial data; consider shading or suppressing it

---

## Checklist

- [ ] Binds to date table's Date column (not a text month name)
- [ ] Endpoint labels on (start + end values)
- [ ] Reference line added with label if Design Spec §5 specifies comparison
- [ ] Secondary series in gray / dashed if present
- [ ] Markers ON for primary series
- [ ] Number of series ≤ 4 (else use small multiples)
