# Recipe: Lollipop Chart

> **Preview:** [![lollipop preview](../../assets/chart-previews/lollipop.svg)](../../assets/chart-previews/lollipop.svg)

- **id:** `lollipop`
- **Visual type:** `clusteredBarChart` with narrow bars + markers OR custom Deneb lollipop
- **Typical size:** 536 × 384

---

## Composition

```
┌────────────────────────────────────────┐
│ Region A    ─────●  $4.2M               │
│ Region B    ───●    $2.8M               │
│ Region C    ──●     $2.1M               │
│ Region D    ─●      $1.3M               │
│ Region E    ●       $0.8M               │
└────────────────────────────────────────┘
```

A thin bar with an emphasized endpoint marker. Draws attention to the tip
value while implying the connection to zero.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category axis | Categorical dimension | `DimRegion[RegionName]` |
| Value axis | Primary measure (endpoint) | `[Revenue]` |
| Marker size | Optional secondary measure | `[Growth %]` |

---

## Formatting (theme-aware)

- **Bar:** `foreground` muted 30%, 2px stroke
- **Marker:** `data0` filled circle, 8–12px radius
- **Data label:** at marker end, `foreground`
- **Gridlines:** OFF

Built-in implementation: set `clusteredBarChart` bar width to ~20% and
overlay a scatter chart or use data-label "icon" trick. Cleaner: Deneb sibling.

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Single highlighted marker (accent), others neutral |
| Analytical | Dual encoding — bar length + marker size for secondary measure |
| Operational | Marker color by status (good/warn/bad) |

---

## Do-NOT list

- ❌ Bar wider than marker (defeats the purpose — use `bar-comparison`)
- ❌ > 15 categories (cluttered)
- ❌ Marker sizes varying by diameter instead of area (double-encoding error)
- ❌ Using for time-series (use `trend-line` with markers)

---

## When to use vs `bar-comparison`

| Use | When |
|---|---|
| **Lollipop** | Endpoint emphasis; dual encoding needed; categorical value is a single point |
| **Bar comparison** | Magnitude itself is the story; dense comparison across many categories |

---

## Data quality gotchas

- Markers at zero disappear visually — add a tiny offset or filter zero values
- When implemented as overlaid scatter + bar, the two visuals can desync on filter interactions — link via common measure
- Negative values: marker placement below zero requires explicit axis config

---

## Checklist

- [ ] ≤ 15 categories
- [ ] Bar stroke narrower than marker
- [ ] Marker uses area encoding (not diameter) if sized by measure
- [ ] Sort order explicit (desc by value)
- [ ] Single accent color unless secondary encoding documented
