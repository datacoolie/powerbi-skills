# Layout: Cohort / Retention Grid

> **Preview:** [![cohort-retention-grid preview](../../assets/layout-previews/cohort-retention-grid.svg)](../../assets/layout-previews/cohort-retention-grid.svg) · variants: [annotated](../../assets/layout-previews/cohort-retention-grid-annotated.svg) · [dark](../../assets/layout-previews/cohort-retention-grid-dark.svg)

- **id:** `cohort-retention-grid`
- **Canvas:** 1920 × 1080
- **Style personality:** Analytical — Period-indexed cohort matrix (cohort vs. age-in-months) + supporting ranking / trend
- **Audience:** Customer analytics leads, growth / retention analysts
- **Visual count:** 9 — reflow-enhanced (was 7)
- **Pairs with themes:** neutral body with one accent — pattern designed to read on any corporate palette.
- **Observed in:** `references-pbip/Retail Sales Analysis Demo.Report/` — 'Cohort Analysis' (13 visuals)

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Header: title · cohort-month slicer · metric toggle            │ 88
├────────────────┬───────────────────────────────────────────────┤
│                │                                               │
│ Slicer rail    │   COHORT MATRIX (rows = cohort, cols = M+n)   │ 640
│  · Cohort      │                                               │
│  · Segment     │                                               │
│  · Metric      │                                               │
│                │                                               │
├────────────────┼───────────────────────┬───────────────────────┤
│                │  Retention curve      │  Cohort size bars     │ 296
│                │  (line, indexed)      │  (by cohort month)    │
│                │                       │                       │
└────────────────┴───────────────────────┴───────────────────────┘ 1080
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Header | 0 | 0 | 1920 | 88 | shape + textbox + slicer | Title + cohort-month + metric toggle |
| Slicer rail | 24 | 104 | 336 | 480 | slicer × 3 | Cohort / Segment / Metric; the rail column below it (y=600..1056) is free for the optional FHD headroom slots |
| Cohort matrix | 384 | 104 | 1512 | 640 | pivotTable (with conditional formatting gradient) | Rows = cohort month, columns = age bucket (M+0..M+11) |
| Retention curve | 384 | 760 | 736 | 296 | lineChart | Indexed retention% by age bucket, series = segment |
| Cohort size bars | 1136 | 760 | 760 | 296 | clusteredColumnChart | # customers per cohort month |

Gutters: 24px edge margin; 16px between zones; 8px inside KPI card rows.

---

## Navigation

- Reachable from the report's top-nav chiclet strip or landing page. Include a small 'Home' actionButton in the header when not the landing page.
- Cross-links out to related drillthrough / detail pages should be surfaced via card-level actions, not a separate nav rail.

---

## Theme + iconography guidance

- **Palette:** Sequential single-hue for cohort matrix (data-ink); neutral rest. Retention curve uses one accent.
- **Logo:** Header top-left at (24, 32) max height 24px.
- **Icons:** Optional clock / funnel glyph next to 'Cohort'.
- **Fonts:** Header 16pt, matrix cells 10pt, axis 9pt.

---

## When NOT to use this layout

- ❌ Data does not have a clear acquisition event / cohort key — the matrix collapses
- ❌ Audience is executive (too granular) — summarize with `scorecard-kpi-grid` + a single retention KPI instead
- ❌ Fewer than 6 cohort periods — a bar chart is enough

---

## Customization allowed

- Change matrix conditional formatting from absolute counts to row-% (index)
- Replace cohort-size bars with a lifetime-value line chart
- FHD headroom (optional): up to two extra slots in the free rail column below the slicers (no overlap with existing slots; Analytical budget of 12 stays respected) — **Retention by segment** at `x=24, y=600, w=336, h=224` (clusteredBarChart, M+3 retention % per segment: which segment keeps customers best?) and **Early-life retention trend** at `x=24, y=840, w=336, h=216` (lineChart, M+1 retention % by cohort month: are newer cohorts retaining better than older ones?)

## Customization NOT allowed

- Removing the matrix — defeats the pattern
- Exceeding 18 cohort columns (matrix becomes illegible)

---

## Reflow additions (v0.6)

Cohort matrix is the star but without a **benchmark line** on the retention curve you can't tell whether retention is 'good'. A **cohort-quality KPI** in the header (Avg M+3 retention, trend arrow) anchors the page's headline number.

### Integration

Retention curve shrinks from `w=736` to `w=576`; benchmark callout panel occupies `x=976, y=760, w=144, h=296`. Cohort-quality KPI fits in the header right side at `x=1488, y=16, w=408, h=56`.

### New slots

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Cohort-quality KPI | 1488 | 16 | 408 | 56 | card | Avg M+3 retention % + trend arrow (vs prior cohort); 18pt value; overlay on the Header band |
| Benchmark callout | 976 | 760 | 144 | 296 | card + shape | Industry benchmark band shown as horizontal reference line on curve, with value card; overlay on the strip freed when Retention curve shrinks to w=576 |

