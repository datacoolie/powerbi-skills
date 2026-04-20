# Recipe: Area Chart (Single Series)

> **Preview:** [![area-chart preview](../../assets/chart-previews/area-chart.svg)](../../assets/chart-previews/area-chart.svg)

- **id:** `area-chart`
- **Visual type:** `areaChart`
- **Typical size:** 536 × 320

> **Single-series only.** Stacked area is banned by `shared-standards.md` —
> see the do-NOT list below.

---

## Composition

```
┌────────────────────────────────────────┐
│                             ▁▃▅▇▇▆▆    │
│                     ▁▃▅▇██████████     │
│             ▁▃▅▇██████████████████     │
│     ▁▃▅▇██████████████████████████     │
│ Jan  Feb  Mar  Apr  May  Jun  Jul      │
└────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Axis | Continuous time | `DimDate[Date]` |
| Values | Single additive measure | `[Active Users]` |
| Tooltip | Secondary context | `[DAU]`, `[Retention %]` |

---

## Formatting (theme-aware)

- **Fill:** `data0` at 40% opacity
- **Line stroke:** `data0` at 100%, 2px
- **Axis:** zero baseline required (magnitude beneath the line is part of the story)
- **Data labels:** OFF (would overflow the filled region)
- **Gridlines:** horizontal only, muted

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Reserved — usually a `trend-line` is cleaner. Use area only when volume under the line is the point (e.g., cumulative users) |
| Analytical | Single-series with reference line overlay |
| Operational | Not recommended — `trend-line` with threshold is more scannable |

---

## Do-NOT list

- ❌ **Stacked area chart** — middle/top series have no baseline; switch to
  `small-multiples-trend` or clustered column
- ❌ Multi-series overlapping area (series occlude each other)
- ❌ Truncated y-axis — area depth is the message, zero baseline required
- ❌ Missing date intervals shown as continuous (creates false trend)
- ❌ Rainbow fill (single accent color only)

---

## When to use vs `trend-line`

| Use | When |
|---|---|
| **Area chart** | Magnitude / volume under the curve is part of the story (cumulative totals, active counts) |
| **Trend line** | Change / slope is the story — no need for volume emphasis |

---

## Data quality gotchas

- Missing dates in the fact table cause visual gaps — bridge with a Date table
- Negative values below zero hide the fill (below baseline) — switch to
  `surplus-deficit-area` or a column chart
- Cumulative measures must reset correctly on year / quarter boundaries

---

## Checklist

- [ ] Single series only
- [ ] Zero baseline enforced
- [ ] Time axis is continuous (Date table spans full range)
- [ ] Fill opacity ≤ 40% so line remains readable
- [ ] Volume under curve is genuinely meaningful (else use `trend-line`)
