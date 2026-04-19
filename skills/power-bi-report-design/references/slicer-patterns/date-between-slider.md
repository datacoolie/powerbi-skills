# Recipe: Date Between Slider (Absolute Range)

- **id:** `date-between-slider`
- **Family:** date
- **Control type:** slicer (between)
- **Cardinality:** continuous
- **Typical footprint:** 360 × 56

---

## Composition

```
┌────────────────────────────────────────────────────────┐
│ Date range                                             │
│ 2024-01-01  ●─────────────────────●  2024-12-31        │
└────────────────────────────────────────────────────────┘
```

Two thumb drag-handles; input boxes let users type exact dates.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field | Date column, marked as date table | `DimDate[Date]` |

---

## Property Snippet

```json
{
  "visualType": "slicer",
  "objects": {
    "data": [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Between'" }}}}}],
    "date": [{ "properties": { "includeToday": { "expr": { "Literal": { "Value": "true" }}}}}]
  }
}
```

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Start date | Earliest date in data | Full range visible |
| End date | Latest / Today | Current as of today |
| Include today | ON | Matches users' mental model |

---

## Anti-patterns

❌ Using absolute-between on a regularly-reviewed report — range stays frozen; users think data is stale. Use `date-relative-rolling` instead.
❌ Date-between slicer on mobile — thumbs too small for touch. Use relative-date buttons.
❌ Pairing with a relative-date slicer on the same page — filters fight each other.

---

## Pairs well with

- `numeric-range-slicer` — same interaction model
- `left-rail-global-panel` — date range at the top of the rail
- Retrospective / investigation pages (locked period)
