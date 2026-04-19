# Recipe: Search-Box Lookup (Very High Cardinality)

- **id:** `search-box-high-card`
- **Family:** search
- **Control type:** slicer (dropdown, search-only) OR custom text-search visual
- **Cardinality:** very-high (> 10 000)
- **Typical footprint:** 280 × 40

---

## Composition

```
┌──────────────────────────────────────────┐
│ 🔍  Customer ID or name                  │
│     (Type ≥ 3 characters...)             │
└──────────────────────────────────────────┘

After typing "acm"
┌──────────────────────────────────────────┐
│ 🔍  acm                                  │
│  • Acme Industries (CUST-0042)           │
│  • Acme Logistics  (CUST-1188)           │
│  • ACM Services    (CUST-9023)           │
└──────────────────────────────────────────┘
```

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field | High-cardinality identifier or searchable name | `DimCustomer[CustomerName]` |
| Secondary display | Optional ID suffix for disambiguation | `DimCustomer[CustomerID]` |

---

## Property Snippet

```json
{
  "visualType": "slicer",
  "objects": {
    "data":   [{ "properties": { "mode":  { "expr": { "Literal": { "Value": "'Dropdown'" }}}}}],
    "search": [{ "properties": { "isVisible": { "expr": { "Literal": { "Value": "true" }}}}}],
    "selection":[{"properties": { "selectAllCheckboxEnabled": false, "singleSelect": true }}]
  }
}
```

For very-high cardinality (> 100 000), prefer:
- Single-select dropdown with search-only mode, OR
- A search-box custom visual that pushes down DirectQuery filter

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Select All | OFF | Meaningless with that many items |
| Single-select | ON (usually) | Lookup pattern → one result at a time |
| Default selection | None / "Pick a customer…" | Force explicit pick |
| Min chars before filter | 3 | Reduces noise in result list |

---

## Anti-patterns

❌ Unfiltered list of 50 000 SKUs — UI lags and user scrolls forever.
❌ Using this when the user doesn't know the exact value — surface a summary visual and use drillthrough instead.
❌ Pairing with Select-All — it picks the entire dataset and hammers the backend.

---

## Pairs well with

- `drillthrough-detail` layout — search opens the detail page for the picked item
- `dimension-nav-hub` layout — search sits at the top of a nav hub
- Customer / SKU / Invoice / Ticket lookup pages
