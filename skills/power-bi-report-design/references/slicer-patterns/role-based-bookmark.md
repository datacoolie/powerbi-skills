# Recipe: Role-Based Bookmark Filter Toggle

- **id:** `role-based-bookmark`
- **Family:** governance
- **Control type:** bookmark group + buttons
- **Cardinality:** n/a (2–4 view variants)
- **Scope:** page

---

## Composition

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  View as:  [ My Region ]  [ All Regions ]   ← buttons          │
│            (bookmark A)   (bookmark B)                         │
│                                                                │
│                                                                │
│                   PAGE CONTENT                                 │
│          (re-scopes per active bookmark)                       │
└────────────────────────────────────────────────────────────────┘
```

Small button group toggles between 2–4 predefined filter states. Each button triggers a bookmark.

---

## Slots & Bindings

| Slot | Purpose |
|---|---|
| Button 1 | Apply bookmark `view-scoped` (e.g. "My Region", inherits RLS) |
| Button 2 | Apply bookmark `view-all` (clears scope; only accessible to all-access roles) |
| Optional button 3 | Apply bookmark `view-peer-group` |
| Bookmark | Captures `filters + selected slicer values + visibility of buttons` |

---

## Bookmark configuration (conceptual)

```yaml
bookmarks:
  - name: view-scoped
    captures:
      - slicer "Region" = <user's region>
      - visual "AllRegions-only-table" = hidden
  - name: view-all
    captures:
      - slicer "Region" = All
      - visual "AllRegions-only-table" = visible
    access: controllers-only        # via role-based visibility rule
```

---

## Usage patterns

| Pattern | Button labels | Typical audience |
|---|---|---|
| Scope toggle | `My Region` / `All Regions` | Finance controllers, directors |
| Perspective toggle | `Actuals` / `Budget` / `Forecast` | Executive review |
| Granularity toggle | `Daily` / `Weekly` / `Monthly` | Ops leadership |
| Before / After | `Pre-launch` / `Post-launch` | Product analytics |

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Default bookmark | Scoped / RLS-respecting | Principle of least privilege |
| Active-state styling | Filled; others outline-only | Clear current view |
| Button count | 2–4 | More → switch to a slicer or `field-parameter-switch` |

---

## Anti-patterns

❌ 5+ bookmarks as a navigation mechanism — bookmark maintenance becomes brittle. Use a slicer or field parameter instead.
❌ Bookmark that duplicates RLS (clears Region filter for all users) — security bypass risk.
❌ Bookmark that changes page content silently (no visible button / indicator).
❌ Bookmarks with overlapping captures that fight each other on click.

---

## Pairs well with

- `hidden-applied-filter` — bookmark flips the hidden filter's value
- `sync-slicer-group` — bookmark can redirect the sync group default
- Executive / controller pages

---

## Security note

Bookmarks are **not** a security boundary. Any user who can open the report can in principle see every bookmark's captured state. Always enforce real scoping with RLS; use bookmarks as **convenience** for users who already have access to both views.
