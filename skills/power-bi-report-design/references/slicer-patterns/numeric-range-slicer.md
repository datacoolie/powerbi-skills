# Recipe: Numeric Range Slider

- **id:** `numeric-range-slicer`
- **Family:** numeric
- **Control type:** slicer (between)
- **Cardinality:** continuous
- **Typical footprint:** 320 × 56

---

## Composition

```
┌────────────────────────────────────────────────────────┐
│ Order value ($)                                        │
│   $0     ●────────────────●          $50 000           │
│          2 500             25 000                       │
└────────────────────────────────────────────────────────┘
```

Two thumbs; optional numeric input boxes for exact bounds.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field | Numeric column (measure-like dimension) | `FactSales[OrderValue]` |

---

## Property Snippet

```json
{
  "visualType": "slicer",
  "objects": {
    "data":       [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Between'" }}}}}],
    "numericInputStyle": [{ "properties": { "show": { "expr": { "Literal": { "Value": "true" }}}}}]
  }
}
```

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Min | Dataset minimum | Full range visible |
| Max | Dataset maximum | Full range visible |
| Step | Natural unit (integer / $100) | Avoid floating-point thumb jitter |
| Formatting | Matches column format ($, #, %) | Consistent with visuals |

---

## Anti-patterns

❌ Range slider for discrete codes that are numeric (Store ID, PO number) — they're categorical; use dropdown.
❌ Range slider for outlier-heavy columns without a pre-aggregation — users stuck dragging across noise.
❌ Multiple overlapping numeric ranges on the same page without clear labels.

---

## Pairs well with

- `histogram-distribution` chart (in `chart-templates/`) — range narrows the histogram
- Customer / Order / Ticket deep-dive analytical pages
- Cohort analysis pages (e.g. Tenure bucket)
