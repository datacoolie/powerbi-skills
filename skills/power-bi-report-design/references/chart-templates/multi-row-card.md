# Recipe: Multi-Row Card

> **Preview:** [![multi-row-card preview](../../assets/chart-previews/multi-row-card.svg)](../../assets/chart-previews/multi-row-card.svg)

- **id:** `multi-row-card`
- **Visual type:** `multiRowCard`
- **Typical size:** 536 × 200 (4–8 metrics stacked)

---

## Composition

```
┌──────────────────────────────────┐
│ Revenue              $4.2M       │
│ ───────────────────────────────  │
│ Gross Margin         38.4%       │
│ ───────────────────────────────  │
│ Customers            12,840      │
│ ───────────────────────────────  │
│ AOV                  $327        │
└──────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Fields | 4–8 measures at equal weight | `[Revenue]`, `[Gross Margin %]`, `[Customers]`, `[AOV]` |
| Category (optional) | Row-per-category grouping | `DimRegion[RegionName]` |

---

## Formatting (theme-aware)

- **Card fill:** `background` with subtle border (`secondary` 1px)
- **Label:** `foreground` muted 60% opacity, 10pt Regular
- **Value:** `foreground`, 18pt Semibold
- **Bar separator:** `secondary` 0.5px between rows
- **Accent bar:** optional 3px left border in `data0` for visual grouping

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | 4 metrics max, large value (22pt), no accent bar |
| Analytical | 6–8 metrics, 16pt, accent bar to group domains |
| Operational | Category-grouped rows with status color per row |

---

## Do-NOT list

- ❌ > 8 metrics (audience cannot prioritize — split into two cards or use `sparkline-table`)
- ❌ Mixing different units without visible unit labels ($, %, ct)
- ❌ Using for a single metric (→ `kpi-banner`)
- ❌ Using when trend-per-row matters (→ `sparkline-table`)
- ❌ Row heights uneven

---

## Data quality gotchas

- `BLANK()` measures render as empty rows — confirm desired behavior
- Percent measures must be formatted as percent, not decimal strings
- Categorical row grouping multiplies height — cap category count at 5

---

## Checklist

- [ ] 4–8 metrics
- [ ] Each metric has a business-friendly label
- [ ] Unit visible (currency symbol, % sign, count suffix)
- [ ] Row height consistent
- [ ] Recipe choice documented vs alternatives (see `kpi-banner.md` decision matrix)
