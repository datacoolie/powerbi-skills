# Recipe: Sunburst (Hierarchical Rings)

> **Preview:** [![sunburst preview](../../assets/chart-previews/sunburst.svg)](../../assets/chart-previews/sunburst.svg)

- **id:** `sunburst`
- **Visual type:** `Sunburst1445472000808` ★ (custom visual)
- **Typical size:** 480 × 480 (square)

---

## Composition

```
       ┌──────────────┐
       │  ╱╱─────╲╲    │
       │ ╱╱  ◯◯◯   ╲╲   │      Inner ring: Level 1 (Region)
       │ │ ◯◯◯◯◯◯  │   │      Middle ring: Level 2 (Country)
       │ │ ◯◯◯◯◯◯  │   │      Outer ring: Level 3 (City)
       │ ╲╲  ◯◯◯   ╱╱   │
       │  ╲╲─────╱╱    │
       └──────────────┘
```

Concentric rings where each ring is a hierarchy level. Outer arc length is
proportional to the measure.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Group | Hierarchy levels (ordered root → leaf) | `[Region]`, `[Country]`, `[City]` |
| Values | Primary measure | `[Revenue]` |
| Details (optional) | Tooltip dimension | — |

---

## Formatting (theme-aware)

- **Segment fill:** `data0…dataN` by root parent; children inherit with tint
- **Stroke:** 1px `background` between segments
- **Labels:** centered radially, ≥ 10pt, hidden if arc < 20°
- **Center text:** total measure or selected path

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Rarely — readers find it novel but hard to read. Prefer `treemap-hierarchy` |
| Analytical | 3–4 levels, interactive drill-down |
| Operational | Not recommended |

---

## Do-NOT list

- ❌ > 4 hierarchy levels (outer rings become unreadable threads)
- ❌ > 8 root-level categories (color palette exhausts, arcs shrink)
- ❌ Using when flat share is the story (→ `stacked-bar-100`)
- ❌ Rainbow palette across siblings (use tints of one hue per root parent)
- ❌ Labels written tangent to a narrow arc (illegible)

---

## When to use vs `treemap-hierarchy`

| Use | When |
|---|---|
| **Sunburst** | 3+ hierarchy levels AND the radial metaphor helps readers (part-of-whole at each level) |
| **Treemap** | 1–2 hierarchy levels AND rectangular packing fits the slot better |
| **Decomposition tree** | User-driven drill-down (interactive) |

---

## Data quality gotchas

- Child measure values must sum to the parent's (additive metric only)
- Missing grandchildren create gaps — fill with "Other" or exclude intentionally
- Large roots crowd out small roots' children — use TopN + Other

---

## Checklist

- [ ] ≤ 4 hierarchy levels
- [ ] ≤ 8 root-level categories (or Top-N + Other)
- [ ] Additive measure only
- [ ] Square aspect ratio
- [ ] Palette = tints of one hue per root parent
- [ ] Custom visual registered in `report.json`
