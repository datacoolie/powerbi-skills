# Layout: Chiclet Nav Strip

- **id:** `chiclet-nav-strip`
- **Canvas:** 1664 × 936
- **Style personality:** Analytical / operational hybrid — button-driven navigation
- **Audience:** Power-user sales / commercial / trade teams, kiosks with touch-friendly filters
- **Visual count:** 10 (chiclet button slicer row + 4 KPI cards + 2 body charts + 1 footer strip) — reflow-enhanced (was 8)
- **Pairs with themes:** branded — chiclet buttons inherit the primary accent
- **Observed in:** `references-pbip/Trade Analytics Demo (V.AFC.IDP).Report/` and `FMCG_Sales Analytics Demo v.2024.01 (Eng).Report/`

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Header bar: title + logo                                      │ 62
├────────────────────────────────────────────────────────────────┤
│ [ChicletSlicer button row — category / region / channel]      │ 73
├────────────────────────────────────────────────────────────────┤
│ KPI1    KPI2    KPI3    KPI4                                  │ 114
├───────────────────────────────┬────────────────────────────────┤
│                               │                                │
│  Main chart (hero)            │  Breakdown / secondary        │ 546
│                               │                                │
├───────────────────────────────┴────────────────────────────────┤
│ Footer strip: "Data refreshed {ts} · Source · Owner"          │ 42
└────────────────────────────────────────────────────────────────┘ 936
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Header bar (shape) | 0 | 0 | 1664 | 62 | shape | Accent fill |
| Page title | 31 | 16 | 1300 | 31 | textbox | 18pt Semibold, on header |
| Chiclet slicer row | 0 | 62 | 1664 | 73 | chicletSlicer (custom visual) | Horizontal buttons, single-select |
| KPI 1–4 | 31 / 437 / 842 / 1248 | 156 | 385 | 104 | card | Left-accent colour stripe |
| Main chart | 31 | 281 | 988 | 598 | lineStackedColumnComboChart OR barChart | Hero |
| Breakdown chart | 1040 | 281 | 593 | 598 | donutChart / horizontalBar / matrix | |
| Footer strip (shape + text) | 0 | 894 | 1664 | 42 | shape + textbox | Refresh time, data source, page owner |

Gutters: 16px between KPIs, 16px between hero and breakdown. Chiclet row spans edge-to-edge on purpose — it reads as the primary filter surface.

---

## Navigation

- Chiclet row IS the single filter control. If multiple filter dimensions are needed, stack two chiclet rows (push KPI row to y=176, hero to y=272, shrink hero h to 404).
- Optional page-tab strip can replace the footer (footer becomes `actionButton` row) — but choose one or the other, never both.

---

## Theme + iconography guidance

- **Palette:** chiclet buttons use the theme's primary accent for selected state, muted neutral for unselected. KPI card left-stripe takes the same accent.
- **Logo:** right-aligned in header at `(x=1196, y=12)` max height 24px; title anchors to the left. This mirrors how many branded sales dashboards place their corporate mark away from the main reading flow.
- **Icons:** small category glyph per chiclet (same weight across all buttons). No other icons elsewhere.
- **Fonts:** chiclet label 12pt Semibold; KPI value 26pt; footer 10pt muted.

---

## When NOT to use this layout

- ❌ Filter dimension has > 6 values — chiclets overflow or shrink below tap-target size
- ❌ Filter dimension is continuous (dates, amounts) — use a range slicer, not chiclets
- ❌ Touch-unfriendly environment AND mouse users prefer dropdowns — chiclet row is overkill
- ❌ Dense analytical pages needing multiple slicers — use `left-rail-filter-analytical` instead

---

## Customization allowed

- Add a second chiclet row for a second low-cardinality dimension
- Swap the breakdown chart for a small-multiples grid (keep the same slot)
- Replace the footer with an `actionButton` page-tab row (keep h=32)

## Customization NOT allowed

- Using chiclets as the ONLY way to see filter state (always pair with visual cross-filter so the user knows what's applied)
- Placing chiclets below the KPI row (breaks the "filter-first, then read" chrome pattern)
- Exceeding 56px chiclet row height — the band stops reading as chrome and becomes content

---

## Reflow additions (v0.6)

Selected chiclet(s) answer *which filter*; a **summary commentary band** below the KPI row answers *what it means*. A **secondary chiclet row** for a 2nd low-cardinality dimension (e.g. Channel under Region) multiplies analytical depth without adding a slicer panel.

### Integration

Insert **Chiclet row 2** at `y=140, h=62` — pushes KPI row to `y=214`, Main/Breakdown charts to `y=339`, and compresses chart `h` from `598` to `555`. Summary commentary sits between KPIs and charts at `y=325, h=14`.

### New slots

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Chiclet row 2 | 0 | 140 | 1664 | 62 | chicletSlicer (custom visual) | Secondary dimension (channel / segment / team); single-select |
| Summary commentary | 31 | 325 | 1602 | 14 | textbox | 1-line interpretation of current filter + KPI state; 11pt muted |

