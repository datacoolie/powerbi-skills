# Recipe: Voronoi Share (Deneb sibling)

> **Preview:** [![voronoi-share preview](../../assets/chart-previews/voronoi-share.svg)](../../assets/chart-previews/voronoi-share.svg)

- **id:** `voronoi-share`
- **Visual type:** `Deneb6E97C82C58E5467CA7C3188B3E36ADE7` ★
- **Parent recipe:** [`deneb-custom.md`](deneb-custom.md)
- **Typical size:** 560 × 560 (square)

---

## Composition

```
┌──────────────────────┐
│   ┌──────┬───┐         │
│   │  A   │   │         │     Each cell = one category
│   │      │ B │         │     Cell area ∝ measure value
│   ├──┬───┤   │         │     Neighbors determined by seed distance
│   │C │ D ├───┤         │
│   │  │   │ E │         │
│   └──┴───┴───┘         │
└──────────────────────┘
```

Space-filling tessellation where each point owns its closest region.
Alternative to treemap for non-rectangular packing.

---

## Slots

| Role | Binding example |
|---|---|
| Seeds | Category list + 2D position (can be synthetic) | `DimProduct[ProductName]` + generated coordinates |
| Value (area) | `[Revenue]` |

---

## Vega-Lite support

Vega-Lite has limited native support; usually requires Vega (not Vega-Lite)
spec with `geoshape` mark plus Voronoi transform.

Inherits scaffold from [`deneb-custom.md`](deneb-custom.md).

## Do-NOT list

- ❌ Using when rectangular packing works (→ `treemap-hierarchy`)
- ❌ > 30 cells (labels crowd)
- ❌ Assigning random seeds (cell layout becomes meaningless)
- ❌ Encoding both cell area AND color by the same measure (redundant)
