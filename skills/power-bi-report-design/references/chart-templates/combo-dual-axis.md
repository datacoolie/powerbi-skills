# Recipe: Combo Chart (Bar + Line, Dual Axis)

- **id:** `combo-dual-axis`
- **Visual type:** `lineStackedColumnComboChart` or
  `lineClusteredColumnComboChart` (core visual)
- **Typical size:** 640 × 360

---

## Composition

```
 $M                                               %
 60├─                         ●───●               ─┤40
 50├─            ●───●───●                         ─┤30
 40├─    ●───●                       ●───●          ─┤20
 30├─                                               ─┤10
 20├─  ██    ██    ██    ██    ██    ██    ██      ─┤ 0
    └───────────────────────────────────────────────
       Jan  Feb  Mar  Apr  May  Jun  Jul  Aug
       ██ Revenue ($M, left)     ● Margin % (right)
```

Bars on the primary axis carry the **volume** story; the line on the
secondary axis carries the **ratio / rate** story. Classic finance/ops combo
— do not collapse into one axis with mismatched scales.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| X axis | Shared dimension | `DimDate[Month]` |
| Column series | Volume measure | `[Revenue]` |
| Line series | Rate / ratio measure | `[Margin %]` |
| Secondary Y | Line's own scale | axis setting |

---

## Formatting (theme-aware)

- Columns: `neutral` 70% opacity, rounded top corners, 40-60% axis width
- Line: `accent`, 2 px, markers only on first/last/extremes
- Two Y axes — left with currency formatting, right with percent + "%" suffix
- Gridlines on left axis only; right axis has ticks but no gridlines
- Legend inline with axis titles ("Revenue ($M, left) · Margin % (right)")

---

## Do-NOT list

- ❌ Dual-axis two volume measures with a shared scale — use stacked column
- ❌ More than one line on the right axis (viewer loses the scale mapping)
- ❌ Match both axes to zero origin artificially — lets one series fake alignment
- ❌ Omit the "(left)" / "(right)" legend annotation — readers get lost

---

## Checklist

- [ ] Left axis = volume, right axis = rate/ratio
- [ ] Only ONE series on each axis
- [ ] Legend explicitly names which axis each series uses
- [ ] Gridlines on primary axis only
