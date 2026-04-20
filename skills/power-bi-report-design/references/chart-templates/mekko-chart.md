# Recipe: Mekko / Marimekko Chart

> **Preview:** [![mekko-chart preview](../../assets/chart-previews/mekko-chart.svg)](../../assets/chart-previews/mekko-chart.svg)

- **id:** `mekko-chart`
- **Visual type:** `MekkoChart1513095496262` ★ (custom visual)
- **Typical size:** 824 × 480

---

## Composition

```
┌───────────────────────────────────────────────┐
│ Region A ████▓▓▒▒  │ B ██▓▓▒  │ C ██▓▒  │ D ██ │
│ ← wider = more volume                          │
│ ↑ taller stack = product mix within region     │
│                                                  │
│ █ Product 1  ▓ Product 2  ▒ Product 3           │
└───────────────────────────────────────────────┘
```

Stacked column chart where column **width** encodes a second measure (e.g.,
market size) and column **height** encodes share (always 100%). Reveals
volume × mix simultaneously.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category axis | Primary dimension (width) | `DimRegion[RegionName]` |
| Series | Stack dimension (height segments) | `DimProduct[Category]` |
| Values | Measure (product revenue) | `[Revenue]` |
| Width | Second measure (market size) | `[Market Size]` OR column total of Values |

---

## Formatting (theme-aware)

- **Segment colors:** `data0…data4` in stack order
- **Column border:** 1px `background`
- **Labels:** % share on largest segment only (to avoid clutter)
- **Width scale:** linear to the width measure (not log)

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | ≤ 4 columns, ≤ 3 stack segments, one highlighted bar |
| Analytical | Full decomposition, tooltip shows both width and height measures |
| Operational | Not recommended — complexity doesn't suit glance reading |

---

## Do-NOT list

- ❌ > 6 columns (widths become unreadable)
- ❌ > 5 stack segments (segments < 5% disappear)
- ❌ Binding width to a non-additive measure (distorts meaning)
- ❌ Sorting columns alphabetically (sort by width desc)
- ❌ Using two Mekkos side-by-side (too dense)

---

## Data quality gotchas

- Width measure must be the sum of stack values OR a genuinely related
  second measure — unrelated pairings mislead
- Column labels rotate when narrow — keep names short or use TopN
- Segment minimums < 3% lose visibility — roll into "Other"

---

## Checklist

- [ ] ≤ 6 columns, ≤ 5 stack segments
- [ ] Width measure semantically tied to the height encoding
- [ ] Columns sorted by width desc
- [ ] Segments < 3% consolidated into "Other"
- [ ] Custom visual registered in `report.json`
- [ ] Tooltip exposes both width and height measures
