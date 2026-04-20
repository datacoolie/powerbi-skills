# Recipe: Surplus / Deficit Area

> **Preview:** [![surplus-deficit-area preview](../../assets/chart-previews/surplus-deficit-area.svg)](../../assets/chart-previews/surplus-deficit-area.svg)

- **id:** `surplus-deficit-area`
- **Visual type:** `areaChart` with positive/negative conditional fill OR `lineChart` + overlay
- **Typical size:** 536 × 320

---

## Composition

```
┌────────────────────────────────────────┐
│   ▅▇██             (surplus, good)     │
│ ▃▅█████▇▅                               │
│ ═══════════════════════════  0 line     │
│        ▃▅▇█▆▃                           │
│           ▇██       (deficit, bad)     │
│ Jan Feb Mar Apr May Jun Jul Aug         │
└────────────────────────────────────────┘
```

Baseline at zero; positive shaded `good`, negative shaded `bad`. Highlights
deviation from a reference rather than absolute magnitude.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Axis | Time | `DimDate[Date]` |
| Values | Signed measure (variance, net) | `[Budget Variance]` |
| Reference | Zero line (implicit) | — |

---

## Formatting (theme-aware)

- **Positive fill:** `good` at 40% opacity
- **Negative fill:** `bad` at 40% opacity
- **Line:** `foreground` 1.5px
- **Zero line:** `foreground` 1px solid
- **Axis:** symmetric around zero (min/max balanced)

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Single metric, annotated peak / trough |
| Analytical | Multiple metrics as small multiples of this recipe |
| Operational | Threshold bands (±5%, ±10%) as reference lines |

---

## Do-NOT list

- ❌ Using for unsigned measures (area chart is the right pick)
- ❌ Asymmetric y-axis (hides the magnitude of either direction)
- ❌ Rainbow or brand colors instead of semantic good/bad
- ❌ Missing zero line (baseline disappears)
- ❌ Stacking multiple series (use small multiples)

---

## Data quality gotchas

- Variance measures must return negative for below-target; verify DAX direction
- Sparse data creates jagged transitions across zero — smooth with interpolation only if statistically honest
- Axis auto-range may favor one direction; lock min/max manually

---

## Checklist

- [ ] Measure is genuinely signed (negative is meaningful)
- [ ] Zero line visible
- [ ] Y-axis symmetric around zero
- [ ] Fills use `good` / `bad` semantic tokens
- [ ] Legend / title conveys direction ("positive = surplus")
