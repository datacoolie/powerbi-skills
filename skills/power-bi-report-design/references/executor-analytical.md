# Role: Executor — Analytical Style Personality

> **Inherits from `executor-base.md`.** Read that first; this file overrides density and narrative voice only.

---

## When this personality applies

- **Audience:** BI analysts, business managers, power users
- **Reading context:** 5-15 minutes, self-service exploration, interactive use
- **Goal:** Understand the drivers behind a metric; slice and dice
- **STYLE brief answer:** "analyst deep-dive", "self-service", "data exploration"

This is the **default personality** for most business reports.

---

## Density

| Element | Analytical rule |
|---|---|
| Visuals per page (excl. slicers) | **5-8** |
| Slicers per page | **3-6** |
| KPI cards | 4-6, one row |
| Pages per report | **4-8** |
| Text density | Moderate — data speaks; titles frame |

---

## Narrative voice (titles)

Titles describe **what the visual shows**, with a slight lean toward insight. Less assertive than Executive.

| ❌ Too bland | ✅ Analytical | ❌ Too exec |
|---|---|---|
| "Sum of Revenue" | "Revenue trend — FY2025 YTD" | "Revenue momentum steady" |
| "Bar Chart" | "Revenue by region with YoY change" | "North region lags by 12%" |
| "Table" | "Top 20 products by margin" | "Three SKUs drive 60% of margin" |

Rules:
- Titles name **the subject + the frame** (time, comparison, rank)
- Sub-titles clarify measure + filter state
- Let the data tell the story; audience will form their own conclusion

---

## Page structure (typical)

```
┌─────────────────────────────────────────────────────────┐
│ Page title + subtitle                        (56 h)    │
├─────────────────────────────────────────────────────────┤
│ [Slicer 1] [Slicer 2] [Slicer 3] [Slicer 4]  (48 h)    │
├─────────────────────────────────────────────────────────┤
│ [KPI 1][KPI 2][KPI 3][KPI 4][KPI 5]          (120 h)   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  HERO visual — trend or primary breakdown   (320 h)    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [Supporting 1]  [Supporting 2]  [Supporting 3]         │
│                                              (280 h)   │
└─────────────────────────────────────────────────────────┘
```

**Pattern:** Slicer bar → KPI banner → hero → 3-column supporting grid.

---

## Essential elements

### KPI banner (always)
- 4-6 cards
- Each shows: current value + delta vs comparison + trend spark
- Apply `chart-templates/kpi-banner.md` recipe

### Hero visual (always)
- Centered or full-width below KPI banner
- Typically: line chart (trend), bar chart (comparison), or map (geo)
- Has reference line(s) — target, plan, prior year

### Supporting grid (typical)
- 2-3 visuals, same height, aligned
- Different dimensions / breakdowns of the same metric as the hero
- Examples: revenue by region, revenue by product, revenue by channel

### Slicers
- Top row or left rail
- Sync across pages (Design Spec §8 syncGroups)
- Include Clear-All button

---

## Color discipline

- **Monochromatic depth** — one brand hue in 3-5 shades
- Categorical accents (data1, data2, data3) for true categorical breakdowns
- Don't over-color trend lines — if 3+ series, consider small-multiples instead

---

## Direct labels & reference lines

Analytical style uses data labels and reference lines liberally:
- **Bar / column:** show values as labels (no need to read axis)
- **Line:** show start value + end value as labels; add markers on inflection points
- **Reference lines:** plan, target, prior-period — always labeled

---

## Interaction richness

Analytical reports are **interactive**:
- Cross-filter between all visuals (default)
- Drillthrough to product / customer / region detail pages
- Tooltip pages with secondary breakdowns on hover
- Edit Interactions: keep slicers filtering, but KPI cards should stay un-cross-filtered by clicks on bars (to preserve the top-level summary)

---

## Whitespace

- Gutter 8-16px (denser than Executive)
- Safe zone 16px
- Visual heights aligned within rows

---

## Titles & subtitles

- **Title:** 14pt Semibold, descriptive
  - "Revenue trend — FY2025 YTD"
  - "Top 10 products by margin"
  - "Regional revenue with YoY change"
- **Subtitle:** 11pt Regular, muted
  - "Actual vs. plan" / "Current period" / "Excludes internal transfers"

---

## What NOT to do in Analytical style

- ❌ Single-visual pages (this isn't Executive)
- ❌ More than 8 visuals per page (cross into Operational territory)
- ❌ Big-Idea titles that pre-conclude the analysis ("North is failing") — let analysts conclude
- ❌ Suppressing drillthrough / tooltip pages (under-exploiting interactivity)
- ❌ Heavy annotations / callouts (belongs to Executive; clutters analyst views)

---

## Checklist before Polisher

- [ ] KPI banner with 4-6 cards on page 1
- [ ] Hero visual present on every main page
- [ ] Each page has 5-8 visuals (excl. slicers)
- [ ] At least one drillthrough or tooltip page exists
- [ ] Cross-filter behavior explicitly set (not default)
- [ ] Slicers sync across pages where appropriate
