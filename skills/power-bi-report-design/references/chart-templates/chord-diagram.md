# Recipe: Chord Diagram

> **Preview:** [![chord-diagram preview](../../assets/chart-previews/chord-diagram.svg)](../../assets/chart-previews/chord-diagram.svg)

- **id:** `chord-diagram`
- **Visual type:** `ChordChart1443052498688` ★ (custom visual)
- **Typical size:** 560 × 560 (square)

---

## Composition

```
         ┌── A ──┐
        /   │╲   \
       /    │ ╲   \      Arcs = nodes (sized by total flow)
      F     │  ╲   B     Ribbons = bidirectional flows between pairs
       \    │  ╱  /      Ribbon thickness = flow volume
        \   │ ╱  /
         └── C ──┘
```

Circular layout with node arcs around the perimeter and curved ribbons
connecting pairs. Shows bidirectional transfers.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| From | Source node | `FactTransfer[SourceRegion]` |
| To | Target node | `FactTransfer[TargetRegion]` |
| Values | Flow magnitude | `[Transfer Amount]` |

---

## Formatting (theme-aware)

- **Node arcs:** `data0…dataN` per node
- **Ribbons:** source-color tint at 50% opacity
- **Labels:** tangent to arc, 10pt
- **Gap between arcs:** 3° (prevents visual merging)

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Rarely — consider a directional bar chart instead |
| Analytical | 5–10 nodes, interactive highlight on hover |
| Operational | Not recommended |

---

## Do-NOT list

- ❌ > 15 nodes (ribbons crisscross unreadably)
- ❌ Unidirectional flows (→ `sankey-flow` instead)
- ❌ Self-loops (node-to-self) — exclude or document
- ❌ Rainbow per-ribbon colors (use node colors)
- ❌ Missing labels (arcs become anonymous)

---

## When to use vs `sankey-flow`

| Use | When |
|---|---|
| **Chord** | Bidirectional flows; both senders and receivers are the same set |
| **Sankey** | Unidirectional left-to-right flow through stages; distinct source/target sets |

---

## Data quality gotchas

- Flows are often asymmetric (A→B ≠ B→A) — verify the visual sums both directions correctly
- Missing pairs render as no ribbon (not zero) — confirm desired behavior
- Large nodes visually dominate and hide small-volume relationships — filter or TopN

---

## Checklist

- [ ] ≤ 15 nodes
- [ ] Flows are bidirectional (source + target from same set)
- [ ] Self-loops excluded or documented
- [ ] Labels visible on all arcs
- [ ] Custom visual registered in `report.json`
- [ ] Tooltip shows A→B and B→A amounts separately
