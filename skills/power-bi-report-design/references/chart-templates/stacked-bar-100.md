# Recipe: 100% Stacked Bar (Share / Mix)

> **Preview:** [![stacked-bar-100 preview](../../assets/chart-previews/stacked-bar-100.svg)](../../assets/chart-previews/stacked-bar-100.svg)

- **id:** `stacked-bar-100`
- **Visual type:** `hundredPercentStackedBar` OR `hundredPercentStackedColumn`
- **Typical size:** 536 × 384

---

## Composition

```
Category A  ████████  ██████ ████████  ████   ██
Category B  █████     ████████  ██████ ██████ █████
Category C  ███████████ ████  █████    ███    ██
            0%          50%                 100%
```

Each row sums to 100%. Use to compare **composition** (mix, share-of-total)
across entities, not absolute magnitude.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Axis | Entity / period | `DimRegion[Region]` |
| Legend | Part dimension (≤ 5 parts) | `DimChannel[Channel]` |
| Values | Single additive measure | `[Revenue]` |

---

## Formatting (theme-aware)

- **Series colors:** `data0..data4` in a *semantically meaningful* order
  (e.g. Core → Growth → Other), not alphabetical
- **Labels:** percentage, hide values < 5% (noise)
- **Category axis:** sort categories DESC by primary segment (e.g. Core share)
  so the reader's eye follows the story
- **Gridlines:** OFF

---

## Do-NOT list

- ❌ > 5 stack segments (use a small-multiples trend or matrix instead)
- ❌ Compare absolute totals with this visual (use a clustered bar + size
  visual title: "mix shown — scale masked")
- ❌ Non-additive measures (ratios, distinct counts)
- ❌ Default rainbow palette — one accent for the part-of-interest,
  neutrals for the rest

---

## Narrative frame by style

| Style | Treatment |
|---|---|
| Executive | 3-4 segments max; one segment accent-colored as the Big-Idea (e.g. "% from new products"). Row labels bold. |
| Analytical | Up to 5 segments; show labels on all segments ≥ 5%; sort by primary segment DESC. |
| Operational | Status colors per segment (green/amber/red by tier); last-updated stamp in subtitle. |

---

## Checklist

- [ ] ≤ 5 segments
- [ ] Legend sort is semantic (Core → Growth → Other), not alphabetical
- [ ] Sort axis by primary segment DESC
- [ ] Hide data labels < 5%
- [ ] One accent color if there's a single part-of-interest
