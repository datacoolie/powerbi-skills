# Recipe: Relative-Date Rolling (Last N / Current)

- **id:** `date-relative-rolling`
- **Family:** date
- **Control type:** slicer (relative)
- **Cardinality:** continuous
- **Typical footprint:** 280 × 56

---

## Composition

```
┌──────────────────────────────────────────┐
│ Period: [Last ▾] [12] [Months ▾]          │
│                                          │
│  ○ Last   ● Next   ○ This                │
└──────────────────────────────────────────┘
```

Three knobs: **direction** (Last / Next / This), **count** (integer), **unit** (day / week / month / quarter / year). Auto-advances as clock ticks.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field | Date column from marked date table | `DimDate[Date]` |

---

## Property Snippet

```json
{
  "visualType": "slicer",
  "objects": {
    "data":      [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Relative'" }}}}}],
    "date":      [{ "properties": { "includeToday": { "expr": { "Literal": { "Value": "true" }}}}}],
    "items":     [{ "properties": { "outlineWeight": { "expr": { "Literal": { "Value": "0" }}}}}]
  }
}
```

Relative-date knob (example filter state):
```json
{
  "filter": {
    "type": "RelativeDate",
    "direction": "Last",
    "count": 12,
    "unit": "Months",
    "includeCurrentPeriod": true
  }
}
```

---

## Defaults by cadence

| Review cadence | Default | Unit |
|---|---|---|
| Daily ops dashboard | Last 7 | Days |
| Weekly ops | Last 6 | Weeks |
| Monthly executive review | Last 12 | Months |
| Quarterly board | Last 4 | Quarters |
| Annual planning | This 1 | Year |

---

## Anti-patterns

❌ Relative-date on a retrospective page ("Q1 2024 Review") — period must be locked; use `hidden-applied-filter`.
❌ Combining relative + absolute date on the same page — last wins; user can't tell which.
❌ `Last 0` / `Next 0` — confusing UX; use "This" direction.

---

## Pairs well with

- `top-header-filter-bar` — date + channel + brand in one row
- `sync-slicer-group` — same rolling window across Analysis pages
- TV-wallboard pages — date advances on screen without a touchpoint
