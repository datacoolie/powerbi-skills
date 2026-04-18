# Recipe: Histogram (Distribution Shape)

- **id:** `histogram-distribution`
- **Visual type:** `columnChart` with pre-bucketed bins OR native `histogram`
  custom visual
- **Typical size:** 536 × 336

---

## Composition

```
               ▇▇
            ▇▇ ▇▇ ▇▇
         ▇▇ ▇▇ ▇▇ ▇▇ ▇▇
      ▇▇ ▇▇ ▇▇ ▇▇ ▇▇ ▇▇ ▇▇
   ▇▇ ▇▇ ▇▇ ▇▇ ▇▇ ▇▇ ▇▇ ▇▇ ▇▇
   └──────── bins ──────────┘
                │
              mean
```

Vertical bars per bin. Answers **"what's the shape?"** — is the metric
bimodal, skewed, has a long tail. Target audience: analysts and ops managers.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Axis | Bin label (pre-computed) | `[Bin]` |
| Values | Count of observations | `COUNTROWS(FactOrder)` |
| Reference | Mean / Median vertical line | `[Mean]`, `[Median]` |

---

## DAX bin pattern

```dax
Bin =
SWITCH(TRUE(),
    [OrderValue] < 100,           "< 100",
    [OrderValue] < 500,           "100-499",
    [OrderValue] < 1000,          "500-999",
    [OrderValue] < 5000,          "1k-5k",
    ">= 5k"
)
```

---

## Formatting (theme-aware)

- **Bars:** `data0`, no gap (or very small gap) so bars read as continuous bins
- **Axis labels:** bin lower-bound ("100", "500", …) — compact
- **Mean line:** `accent` vertical dashed, labelled
- **Median line:** second `accent2` vertical, optional

---

## Do-NOT list

- ❌ Use too few bins (5) — shape information is lost
- ❌ Use unequal-width bins without labelling the intervals
- ❌ Render as line chart (connecting bin tops implies continuity of entities
  that isn't real)
- ❌ Compare 2+ histograms by overlaying — use small multiples

---

## Checklist

- [ ] 8-20 bins
- [ ] Bin intervals equal width (or clearly labelled when not)
- [ ] Mean OR median reference line present
- [ ] Bar gap minimal (< 5%) so distribution shape reads
