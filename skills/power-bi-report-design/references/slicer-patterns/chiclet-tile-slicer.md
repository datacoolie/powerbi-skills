# Recipe: Chiclet / Tile Slicer (Low-Cardinality Buttons)

> **Preview:** [![chiclet-tile-slicer preview](../../assets/slicer-previews/chiclet-tile-slicer.svg)](../../assets/slicer-previews/chiclet-tile-slicer.svg)

- **id:** `chiclet-tile-slicer`
- **Family:** category
- **Control type:** slicer (tile)
- **Cardinality:** low (3–7 values)
- **Typical footprint:** 1 row × 3–7 tiles, ~40–60 px tall

---

## Composition

```
┌──────────────────────────────────────────────────────┐
│  Channel                                             │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                     │
│  │ MT  │ │ GT  │ │E-com│ │ All │                     │
│  └─────┘ └─────┘ └─────┘ └─────┘                     │
└──────────────────────────────────────────────────────┘
```

Primary dimension always visible — zero clicks to see the options, one click to apply.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field | Categorical column with 2–7 distinct values | `DimChannel[ChannelName]` |
| Header | Slicer title (can hide if self-evident) | `"Channel"` |

---

## Property Snippet (Power BI `visual.json` excerpt)

```json
{
  "visualType": "slicer",
  "objects": {
    "data": [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Basic'" }}}}}],
    "general": [{ "properties": { "orientation": { "expr": { "Literal": { "Value": "1" }}}}}],
    "items":   [{ "properties": { "outlineWeight": { "expr": { "Literal": { "Value": "1" }}}}}],
    "selection":[{"properties": { "selectAllCheckboxEnabled": false, "singleSelect": false }}]
  }
}
```

(Orientation `1` = horizontal tiles; set `singleSelect` per use case.)

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Multi-select | ON (with Ctrl) | Comparison is often the point |
| Select All | ON (as a tile) | Lets user reset without re-opening the pane |
| Default selection | All | Aggregated story first |
| Orientation | Horizontal | Fits 1-row top-header bar |

---

## Anti-patterns

❌ Wrapping onto 2 rows — means cardinality is too high (switch to dropdown).
❌ Mixed label lengths ("Modern Trade" + "MT" + "E-commerce") — align labels before use.
❌ Chiclet slicer for a dimension that changes ≥ monthly (stale list; use dynamic dropdown).

---

## Pairs well with

- `sync-slicer-group` — same tile bar across Analysis pages
- `top-header-filter-bar` — as one of 2–4 bars in the header
