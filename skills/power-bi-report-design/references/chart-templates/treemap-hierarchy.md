# Recipe: Treemap (Hierarchical Share)

- **id:** `treemap-hierarchy`
- **Visual type:** `treemap` (core visual)
- **Typical size:** 560 × 360 (near-square reads best)

---

## Composition

```
┌──────────────────────┬──────────┬─────┐
│                      │          │     │
│     Beverages        │  Snacks  │Dairy│
│       42%            │    24%   │ 12% │
│                      │          ├─────┤
│                      │          │Bakry│
├──────────┬───────────┼──────────┤  8% │
│ Frozen   │  Produce  │  Meat    ├─────┤
│   7%     │    4%     │   2%     │ Oth │
└──────────┴───────────┴──────────┴─────┘
```

Area = share. A single square glance answers "which category dominates,
which are the long-tail". Optional 2-level nesting (category → subcategory)
with a child-rectangle border trick.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Group | Parent category | `DimProduct[Category]` |
| Details | Child (optional) | `DimProduct[Subcategory]` |
| Values | Area measure | `[Sales Amount]` |
| Colour saturation | Secondary measure | `[Margin %]` |

---

## Formatting (theme-aware)

- Fill: `accent` at 20-90% opacity mapped to the secondary measure
- Border: `background` 2 px between tiles so boundaries breathe
- Labels: show category name + value; hide on tiles < 3% of total
- Sort: largest tile top-left (squarified algorithm default)
- Tooltip: parent name + value + % of total + % of parent (if nested)

---

## Do-NOT list

- ❌ Use for > 2 hierarchy levels (use a decomposition tree)
- ❌ Use when no tile exceeds ~8% (bar chart reads better for flat share)
- ❌ Colour by category (kills the "magnitude" encoding) — bind colour to
  the secondary measure only
- ❌ Animate resizing — ruins comparability

---

## Checklist

- [ ] Top tile ≥ 3× the median tile (otherwise bar chart)
- [ ] Small tiles (< 3%) have no labels
- [ ] Colour encodes a separate measure from area, not category
- [ ] Tooltip discloses % of total
