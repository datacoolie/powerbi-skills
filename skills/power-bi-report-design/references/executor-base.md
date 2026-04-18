# Role: Executor Base (all styles inherit)

> **This is a role file.** The `power-bi-developer` agent invokes this role during **Phase 4b — Report Executor**, alongside one of: `executor-executive.md`, `executor-analytical.md`, `executor-operational.md`.

The Executor turns an **approved Design Spec** into PBIR JSON. It does **not** make design decisions — those were made by the Strategist and locked by Phase 4a.5 Seven Confirmations.

---

## Inputs (must all exist)

1. **Approved Design Spec** (all 11 sections filled + Seven Confirmations signed)
2. **Measure catalog** from Phase 3
3. **Model schema** (table + column names) from Phase 2
4. **Theme file** (existing from `themes/` or custom draft in Design Spec §6a)

If any input is missing, **stop** and route back to the correct earlier phase.

---

## Two-Pass Generation

The Executor runs in **two sequential passes**. Do not interleave.

### Pass 1 — Layout Construction (visual-first)

Goal: every visual exists at its final position with its data bindings. **No narrative elements yet.**

For each page (Design Spec §4):
1. Read the layout file referenced by the page (e.g., `layouts/exec-overview-16x9.md`)
2. Create the page folder: `pages/<slug>/`
3. Generate `page.json` with canvas size and basic properties
4. For every visual in §5 (Visual Inventory) for this page:
   a. Read the chart-template recipe (e.g., `chart-templates/kpi-banner.md`)
   b. Read the JSON template in `../power-bi-pbip-report/references/visual-templates.md` (for built-in visuals) or `custom-visuals.md` (for AppSource)
   c. Create the visual folder: `pages/<slug>/visuals/<visual-name>/`
   d. Generate `visual.json` with:
      - `position` from §5
      - `queryState` binding to the measures/columns from §5
      - Formatting properties from the chart-template recipe
      - **Minimum viable properties only** — titles are placeholder, no annotations, no tooltips, no bookmark refs
5. Run a quick render check (mental or with `validate_report.js`) — does the page structure make sense?

**Pass 1 ends when:** all pages and all visuals exist as JSON and pass schema validation. Narrative elements are deliberately absent.

### Pass 2 — Narrative Construction (logic-second)

Goal: turn a valid-but-bland report into one that communicates.

For each page (revisit in Design Spec order):
1. **Big-Idea title** — replace placeholder title with the Big-Idea phrase from §4
2. **Visual titles & subtitles** — apply the naming discipline from your style personality file
3. **Annotations** — reference lines, callouts, direct data labels (per §5 annotation column)
4. **Tooltip pages** — if §10 lists tooltip pages, generate them now (320×240 canvas)
5. **Drillthrough pages & back buttons** — per §8
6. **Bookmarks** — per §8 (with Display Name, filter state capture)
7. **Navigation visuals** — button actions, page navigator, bookmark buttons
8. **Sync slicer groups** — per §8 (set `syncGroups` on each slicer visual)
9. **Mobile layouts** — per §9 (generate `mobileState.json`; defer auto-gen to Polisher if complex)
10. **Page-level filters** — per §10

**Pass 2 ends when:** every Design Spec assertion is reflected in JSON.

---

## Rules that apply to every visual

### Naming convention
- Page folder: slugified display name (`overview`, `sales-performance`, `drillthrough-product`)
- Visual folder: `<type>-<descriptor>` (e.g., `card-total-revenue`, `line-trend-sales`, `bar-top-products`)
- Visual displayName (in `visual.json`): human-readable (e.g., "Total Revenue", "Sales Trend")

### Data binding
- Every `queryState` role must reference a column/measure that exists in the model (verify against Phase 2 schema)
- Measures appear as `[Measure Name]`
- Columns appear as `Table[Column]`

### Formatting
- **No hard-coded colors** in visual.json — use theme tokens (`data0`, `foreground`, `good`, `bad`, etc.)
- Apply the chart-template recipe's formatting exactly — do not "improve" it
- Font family + sizes follow `shared-standards.md` §4

### Accessibility
- Every visual must have `altText` (derive from visual's purpose, not its title alone)
- Tab order is assigned per page (not default)

### Positioning
- All x/y/w/h snapped to 8px grid (from `shared-standards.md` §2)
- No overlaps (unless intentional Z-order with explicit comment)

---

## Per-style personality overrides

Before generating, also read the matching personality file:
- **Executive** → `executor-executive.md` (density, annotation heaviness, title phrasing)
- **Analytical** → `executor-analytical.md` (KPI banner + hero + grid, direct labels, reference lines)
- **Operational** → `executor-operational.md` (density 8-12, traffic-light status, larger fonts)

When the personality file contradicts this file, **the personality wins** (for style-specific choices like density). When this file contradicts a personality (for cross-cutting rules like alt text, grid snap, theme tokens), **this file wins**.

---

## When something is missing from the Design Spec

If during generation you discover the Design Spec is underspecified (e.g., "no measure listed for V5"):
1. **Stop** — do not guess
2. Note the gap
3. Route back to Phase 4a (Strategist) for a Design Spec v+0.1
4. After the update, resume from the current pass (do not restart)

---

## Handoff to Phase 4c

The Executor does NOT run `finalize_pbir.py` or `design_quality_check.py`. Those are the Polisher's job. Executor's job ends with a valid, Design-Spec-conformant report folder.

---

## Anti-patterns

- ❌ Mixing Pass 1 and Pass 2 — always finish layout first
- ❌ Inventing a visual type not listed in Design Spec §5
- ❌ Skipping a visual because "it looks redundant" — if Strategist said include, you include
- ❌ Renaming measures/columns on the fly
- ❌ Using hard-coded colors to match a screenshot — reference the theme
- ❌ Skipping alt text "to save time" — Polisher will flag and you'll re-do
- ❌ Trying to be creative — creativity belongs in Phase 4a
