# Recipe: Top-Header Compact Filter Bar

> **Preview:** [![top-header-filter-bar preview](../../assets/slicer-previews/top-header-filter-bar.svg)](../../assets/slicer-previews/top-header-filter-bar.svg)

- **id:** `top-header-filter-bar`
- **Family:** architecture
- **Control type:** slicer group (horizontal)
- **Cardinality:** n/a (wraps 2–4 slicer recipes)
- **Typical footprint:** 1280 × 64 (full-width header strip)

---

## Composition

```
┌────────────────────────────────────────────────────────────────────────────┐
│ TITLE                              Date: Last 12M ▾  Region ▾  Channel ▾   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│                          PAGE CONTENT                                      │
```

Slim horizontal strip above the page content. 2–4 primary filters, right-aligned next to a report / page title.

---

## Slots & Bindings

| Slot | Recipe | Position |
|---|---|---|
| Slot 1 | `date-relative-rolling` (narrow) | Rightmost-but-one |
| Slot 2 | `chiclet-tile-slicer` (2–4 tiles) OR `dropdown-search-slicer` | Middle |
| Slot 3 | `dropdown-search-slicer` | Left of slots 1–2 |
| Slot 4 (optional) | Secondary slicer | Leftmost of slicer group |
| Title / breadcrumb | Text | Far left |

---

## Structural Properties

- **Height:** 48–72 px
- **Background:** `background` (same as canvas) OR `background2` for subtle strip
- **Separator:** 1 px bottom border only
- **Slicer width:** 160–220 px each; fixed
- **Label alignment:** slicer header inline-left of the control (`"Region: [▾ All]"`)

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Filter count | ≤ 4 | More than 4 → use `left-rail-global-panel` |
| Sync group | `analysis` | Persist across page navigation |
| Orientation | Horizontal (header) | Saves vertical canvas space |

---

## Anti-patterns

❌ Stacking 6+ slicers across the top — becomes a wall of controls; switch to `left-rail-global-panel`.
❌ Long category labels wrapping a chiclet slicer in the header — truncates awkwardly. Shorten labels or move to rail.
❌ Filter bar without a Reset path when ≥ 3 slicers present — users get stuck.

---

## Pairs well with

- `chiclet-tile-slicer` (primary dimension chips)
- `date-relative-rolling` (right-anchored)
- `exec-overview-16x9` and `ops-single-screen` layouts
- TV wallboards (filter bar set once, rarely touched)

---

## Mobile adaptation

- Stack slicers vertically in a collapsible "Filters" card at the top of the mobile layout.
- Keep date + 1 primary filter always visible; collapse the rest.
