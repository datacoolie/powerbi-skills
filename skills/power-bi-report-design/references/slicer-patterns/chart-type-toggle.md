# Recipe: Chart-Type Toggle (Selected-Visuals Bookmark)

- **id:** `chart-type-toggle`
- **Family:** parameter
- **Control type:** bookmark buttons + stacked visuals (Selection pane)
- **Cardinality:** 2–4 chart-type variants
- **Scope:** single visual frame on a page

---

## Composition

```
┌───────────────────────────────────────────────────────────────┐
│  Revenue by Region                     [ Bar ] [ Line ] [Tbl] │
│                                        ▲ active                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                                                         │  │
│  │     ██   ██   ██                                        │  │
│  │  ██ ██   ██   ██   ██                                   │  │
│  │  ██ ██   ██   ██   ██   ██                              │  │
│  │   N    NE    E    SE    S    SW    W    NW              │  │
│  │                                                         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  (Other visuals on this page DO NOT change when you click a   │
│   toggle above — only the chart inside this frame swaps.)     │
└───────────────────────────────────────────────────────────────┘
```

Two or three visuals bound to the same data are stacked in the same frame
using the Selection pane. A small button group swaps which one is visible via
a bookmark with **Data = off** and **Display scope = Selected visuals** so
only the stacked group toggles. Slicers, other visuals, and filter state are
untouched.

---

## Slots & Bindings

| Slot | Purpose | Example |
|---|---|---|
| Visual A | Variant 1 (e.g. clustered bar) | `Revenue by Region — Bar` |
| Visual B | Variant 2 (e.g. line) | `Revenue by Region — Line` |
| Visual C | Variant 3 optional (e.g. table) | `Revenue by Region — Table` |
| Button group | 2–3 buttons, one per variant | Bar · Line · Table |
| Bookmark per button | Captures visibility of the stacked group only | `chart-bar`, `chart-line`, `chart-table` |

---

## Bookmark configuration (critical)

```yaml
bookmarks:
  - name: chart-bar
    update:
      Data: off              # do NOT capture filter / slicer state
      Display: on            # capture hide / show from Selection pane
      Current_Page: off
    scope: Selected visuals  # KEY — applies only to picked visuals
    selected_visuals:
      - Revenue-by-Region-Bar
      - Revenue-by-Region-Line
      - Revenue-by-Region-Table
      - Button-Bar
      - Button-Line
      - Button-Table
    captures:
      - Revenue-by-Region-Bar      = visible
      - Revenue-by-Region-Line     = hidden
      - Revenue-by-Region-Table    = hidden
      - Button-Bar.state           = active
      - Button-Line.state          = default
      - Button-Table.state         = default
```

Repeat for `chart-line` and `chart-table`, inverting the visibility captures.
Because **Data = off**, clicking a toggle does NOT reset slicers or cross-filters.

---

## Selection pane setup

1. Place visuals A / B / C at the same X, Y, W, H.
2. Rename them in the Selection pane to clear, stable names (the bookmark
   binds by name — renames after bookmarking break the link).
3. Group the stacked visuals + the toggle buttons into one Selection pane
   group for cleanliness.
4. For each bookmark: set visibility of only the target visual to visible,
   hide the other two, then **right-click → Update**.

---

## Usage patterns

| Pattern | Variants | When |
|---|---|---|
| Chart type swap | Bar · Line · Table | Let the reader pick the encoding that suits them |
| Detail level swap | Summary · Detail · Raw | Layered audience on one frame |
| Time-grain swap | Daily · Weekly · Monthly | Cheaper than a separate date-grain slicer |
| Before / After swap | Current view · Annotated view | Narrative storytelling |

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Default variant | Variant A (bar / summary) | Most common encoding first |
| Active button styling | Filled accent; others outline | Reader sees current state |
| Button count | 2–3 | More → use a `field-parameter-switch` instead |
| Data capture | **off** | Toggle must not reset filter state |
| Display scope | **Selected visuals** | Must not hide unrelated visuals |

---

## Anti-patterns

❌ Leaving bookmark **Data = on** — clicking a toggle resets every slicer on the page, infuriating users.
❌ Leaving bookmark scope as **All visuals** — hides unrelated visuals or reveals hidden overlays elsewhere.
❌ Using this for measure/dimension swaps (use `field-parameter-switch` — no bookmark maintenance).
❌ 4+ variants — stack of hidden visuals grows, performance drops, bookmark count doubles.
❌ Renaming a stacked visual after bookmarks exist — silently unbinds the bookmark.
❌ Using this to swap between *unrelated* visuals (different data, different grain). The reader loses orientation.

---

## Pairs well with

- `field-parameter-switch` — same frame could swap **type** via this recipe AND **measure** via a field parameter
- `role-based-bookmark` — page-scoped bookmark vs this recipe's visual-scoped bookmark
- Analytical and exploration archetypes

---

## Performance note

Stacked visuals are **all rendered** whether visible or not. Keep variants
cheap (≤ 3) and share the same query-generating fields where possible so the
model caches one result set.

---

## Mobile

Stacked visuals survive mobile layout but the button row must be placed
above, not beside, the visual — horizontal space is too tight. Cap to 2 variants on mobile.
