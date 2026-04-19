# Recipe: Hierarchy Slicer (Expand / Collapse)

- **id:** `hierarchy-slicer`
- **Family:** category
- **Control type:** slicer (hierarchy)
- **Cardinality:** medium at each level (8–25); deep hierarchies fine
- **Typical footprint:** 240 × 320

---

## Composition

```
┌──────────────────────────────┐
│ Geography                    │
├──────────────────────────────┤
│ ▾ ☐ Americas                 │
│   ▾ ☐ United States          │
│     ☐ California             │
│     ☐ New York               │
│   ▸ ☐ Canada                 │
│ ▸ ☐ EMEA                     │
│ ▸ ☐ APAC                     │
└──────────────────────────────┘
```

One slicer replaces 3 cascading slicers. Users drill at their own pace.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field (ordered) | Hierarchy levels, top-to-bottom | `DimGeo[Region]`, `DimGeo[Country]`, `DimGeo[State]` |

Alternative hierarchies:
- Calendar: `Year` → `Quarter` → `Month`
- Product: `Category` → `Subcategory` → `SKU`
- Org: `BU` → `Department` → `Team`

---

## Property Snippet

```json
{
  "visualType": "slicer",
  "objects": {
    "data":      [{ "properties": { "mode":  { "expr": { "Literal": { "Value": "'Dropdown'" }}}}}],
    "hierarchy": [{ "properties": { "isExpanded": { "expr": { "Literal": { "Value": "false" }}}}}],
    "selection": [{ "properties": { "selectAllCheckboxEnabled": false, "singleSelect": false }}]
  }
}
```

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Expand state | Collapsed at root | Don't overwhelm; user drills when needed |
| Select All | OFF | Parent-check cascades; redundant |
| Default selection | None (= all data shown) | Cleaner than auto-selecting a single node |
| Multi-select | ON | Comparison across siblings |

---

## Anti-patterns

❌ Hierarchy with 4+ levels on mobile — rows wrap, lose the tree.
❌ Skewed hierarchies (1 Region → 50 Countries) — feels like a flat dropdown.
❌ Mixing unrelated levels (putting `Product` under `Region`) — meaningless drill.

---

## Pairs well with

- `sync-slicer-group` — hierarchy state persists across Analysis pages
- `drillthrough-detail` layout — hierarchy narrows, drillthrough zooms
