# Recipe: Hidden & Applied Filter (Governance)

- **id:** `hidden-applied-filter`
- **Family:** governance
- **Control type:** filter pane (hidden + locked)
- **Cardinality:** n/a
- **Scope:** report / page (most commonly page)

---

## Composition

```
Filters pane (Designer view)              Viewer canvas
┌─────────────────────────┐               ┌──────────────────────────┐
│ Page filters            │               │                          │
│ ─────────────────────── │               │  PAGE CONTENT            │
│ [IsActive] = TRUE   🔒👁 │  (hidden in   │   (no slicer shown —     │
│ [Period]    = Q1-24 🔒👁 │   viewer)     │    filter invisibly      │
│                         │               │    applied)              │
└─────────────────────────┘               └──────────────────────────┘

Icons: 🔒 locked (user can't change), 👁 hidden (not shown to viewer)
```

Filter is **applied** (data reflects it) but **invisible and uneditable** to the viewer.

---

## When to use

| Scenario | Filter | Hidden? | Locked? |
|---|---|---|---|
| Data-quality hygiene | `[IsTestRecord] = FALSE` | ✅ | ✅ |
| Active-records only | `[IsActive] = TRUE` | ✅ | ✅ |
| Retrospective page pinned to a period | `[FiscalQuarter] = 'Q1-2024'` | ❌ visible | ✅ locked |
| Environment partition | `[Tenant] = 'Production'` | ✅ | ✅ |
| Exclude a known-bad region in audit period | `[Region] <> 'Region-X'` | ❌ | ✅ (visible so users know) |

---

## Slots & Bindings

| Slot | Purpose |
|---|---|
| Filter field | Any column |
| Operator | `=`, `<>`, `IN`, `TopN`, etc. |
| Value | Literal, parameter, or measure-driven |
| Visibility | `hidden` / `visible` |
| Edit lock | `locked` / `unlocked` |

---

## Property Snippet

```json
{
  "filters": [
    {
      "name": "IsActive",
      "field": { "Column": { "Expression": "DimProduct", "Property": "IsActive" } },
      "filter": { "Values": [ true ] },
      "ordinal": 0,
      "howCreated": "User",
      "isHiddenInViewMode": true,
      "isLockedInViewMode": true
    }
  ]
}
```

---

## Governance guardrails

- **Always document** every hidden filter in the Design Spec (§10.2 "Hidden filters").
- **Never** use a hidden filter to disguise incomplete or biased data — surfaces in audit and erodes trust.
- **Prefer RLS** over hidden filters for per-user scoping; hidden filters apply identically to everyone.

---

## Defaults

| Setting | Default |
|---|---|
| Locked | ON when hidden |
| Hidden | ON for hygiene filters; OFF for context-defining filters (Q1 page) |
| Audit annotation | Add `description` field listing business rationale |

---

## Anti-patterns

❌ Using hidden filters instead of RLS ("hide the Region slicer from user X") — not a security boundary; easily bypassed by download / export.
❌ Hidden filter that changes meaning over time without a review cadence (stale exclusions).
❌ Hiding a filter that materially alters the numbers without surfacing it in a tooltip or footnote.

---

## Pairs well with

- `role-based-bookmark` — bookmark toggles hidden filters as a view switcher
- Paginated / `paginated-export-a4` layouts (locked period)
- All layouts that depict a fixed retrospective period
