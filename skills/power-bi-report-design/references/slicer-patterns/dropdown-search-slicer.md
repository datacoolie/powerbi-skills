# Recipe: Dropdown Slicer with Search

- **id:** `dropdown-search-slicer`
- **Family:** category
- **Control type:** slicer (dropdown)
- **Cardinality:** medium (8–25 values)
- **Typical footprint:** 220 × 32 collapsed; 220 × 240 when opened

---

## Composition

```
Collapsed                         Opened
┌──────────────────┐              ┌──────────────────┐
│ Brand ▾          │              │ 🔍 search...     │
└──────────────────┘              │ ☑ All            │
                                  │ ☐ Aqua           │
                                  │ ☐ Brixton        │
                                  │ ☐ Crest          │
                                  │ ...              │
                                  └──────────────────┘
```

Keyboard-searchable; compact when idle, expanding only on click.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field | Categorical column, 8–25 distinct values | `DimProduct[BrandName]` |
| Header | Short label | `"Brand"` |

---

## Property Snippet

```json
{
  "visualType": "slicer",
  "objects": {
    "data":     [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Dropdown'" }}}}}],
    "search":   [{ "properties": { "isVisible": { "expr": { "Literal": { "Value": "true" }}}}}],
    "selection":[{ "properties": { "selectAllCheckboxEnabled": true, "singleSelect": false }}]
  }
}
```

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Search box | ON | Medium cardinality needs typeahead |
| Select All | ON | Reset path |
| Default selection | All | Aggregated story first |
| Multi-select | ON (with Ctrl) | Users compare N items |

---

## Anti-patterns

❌ Using dropdown for ≤ 7 values (user can't see options without clicking — use chiclet).
❌ Dropdown for > 10 000 rows (virtualization suffers; use `search-box-high-card` or drillthrough).
❌ Three cascading dropdowns — consolidate with `hierarchy-slicer`.

---

## Pairs well with

- `left-rail-global-panel` — 3–5 dropdowns stacked
- `hierarchy-slicer` — when cascading becomes natural
