# Recipe: Radar / Spider Chart

> **Preview:** [![radar-chart preview](../../assets/chart-previews/radar-chart.svg)](../../assets/chart-previews/radar-chart.svg)

- **id:** `radar-chart`
- **Visual type:** `RadarChart1423470498847` ★ (custom visual)
- **Typical size:** 480 × 480 (square)

---

## Composition

```
            Quality
              │
              ●
             /|\
    Price  ●─┼─● Speed
           / | \
          ●  │  ●
      Support │ Support
            Value
```

Radial axes (5–10 attributes) with a polygon connecting one entity's scores.
Multiple entities overlay for comparison.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category | Attribute dimension (axes) | `DimAttribute[AttributeName]` |
| Legend | Entity being scored | `DimProduct[ProductName]` |
| Values | Score measure (normalized 0–100) | `[Score]` |

---

## Formatting (theme-aware)

- **Polygon stroke:** `data0…dataN` per entity, 2px
- **Polygon fill:** same color at 20% opacity
- **Axes:** `foreground` 20% opacity
- **Axis labels:** `foreground` 10pt
- **Scale rings:** 3–4 concentric gridlines, muted

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | 1 entity + 1 benchmark, fill prominent |
| Analytical | 2–3 entities overlaid, fills at 20%, legend on |
| Operational | Not recommended — radar is comparative, not operational |

---

## Do-NOT list

- ❌ > 3 entities overlaid (polygons occlude)
- ❌ > 10 axes (labels overlap, polygon becomes a circle)
- ❌ < 5 axes (bar chart is clearer)
- ❌ Mixed scales per axis (score must be normalized)
- ❌ Irregular axis ordering (arbitrary ordering changes polygon shape)

---

## Data quality gotchas

- Score measure must be normalized (0–100 or 0–1) across all axes — raw
  values with different scales distort the polygon
- Axis ordering is not neutral — place related attributes adjacent to tell
  a coherent shape story
- Missing score for any axis breaks the polygon (goes to zero)

---

## Checklist

- [ ] 5–10 axes
- [ ] ≤ 3 entities overlaid
- [ ] All scores normalized to the same scale
- [ ] Axis ordering deliberate (related attributes adjacent)
- [ ] Fill opacity ≤ 20%
- [ ] Custom visual registered in `report.json`
