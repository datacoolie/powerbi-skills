# Recipe: Violin Plot

> **Preview:** [![violin-plot preview](../../assets/chart-previews/violin-plot.svg)](../../assets/chart-previews/violin-plot.svg)

- **id:** `violin-plot`
- **Visual type:** `ViolinPlot1445472000811` ★ (custom visual)
- **Typical size:** 536 × 384

---

## Composition

```
┌────────────────────────────────────────┐
│ A   ╱─╲                                  │
│    │ ● │  ←── kernel density + median     │
│     ╲─╱                                  │
│ B   ╱──╲                                 │
│    │ ● ─│                                │
│     ╲──╱                                 │
│ C     ╱╲                                 │
│      │●│                                 │
│       ╲╱                                 │
└────────────────────────────────────────┘
```

Box-plot hybrid where the box is replaced by a kernel-density curve mirrored
around the median line. Reveals multi-modal distributions that boxes hide.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category | Group dimension | `DimProduct[Category]` |
| Values | Observation measure | `FactSales[OrderValue]` |

---

## Formatting (theme-aware)

- **Violin fill:** `data0` at 40% opacity
- **Violin stroke:** `data0` at 100%
- **Median line:** `foreground` 1.5px
- **Outlier dots:** `bad` 4px circles (if enabled)

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Rarely — density plots need explaining |
| Analytical | Default — annotate bimodality / skew |
| Operational | Not recommended |

---

## Do-NOT list

- ❌ Using with < 30 observations per category (density estimate unreliable)
- ❌ > 8 categories side-by-side (too much cognitive load)
- ❌ Preferring violin when `box-plot-distribution` suffices
- ❌ Different bandwidths per category (auto-bandwidth distorts comparison)

---

## When to use vs `box-plot-distribution`

| Use | When |
|---|---|
| **Violin** | Distribution shape / multi-modality is the point |
| **Box plot** | Quartiles + outliers suffice |

---

## Data quality gotchas

- Bandwidth parameter affects curve smoothness — lock it or auto-range risks
  visual discrepancy across refreshes
- Measure values must be numeric (not pre-binned categories)
- Outlier definition (1.5×IQR or custom) documented

---

## Checklist

- [ ] ≥ 30 observations per category
- [ ] ≤ 8 categories
- [ ] Median line visible
- [ ] Bandwidth setting documented
- [ ] Custom visual registered in `report.json`
- [ ] Recipe choice justified vs `box-plot-distribution`
