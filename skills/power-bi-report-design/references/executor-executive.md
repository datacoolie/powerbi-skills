# Role: Executor — Executive Style Personality

> **Inherits from `executor-base.md`.** Read that first; this file overrides density and narrative voice only.

---

## When this personality applies

- **Audience:** C-suite, board, monthly/quarterly business review attendees
- **Reading context:** 2-3 minutes to grasp, often projected on a screen, often printed
- **Goal:** Clear decision support, not data exploration
- **STYLE brief answer:** "boardroom", "executive review", "monthly exec deck"

---

## Density

| Element | Executive rule |
|---|---|
| Visuals per page (excl. slicers) | **≤ 4** |
| Slicers per page | **≤ 3** (often zero — pre-filtered views) |
| KPI cards | 3-5 max, always one row |
| Pages per report | **3-6** total |
| Text density | High — narrative annotations dominate |

---

## Narrative voice (Big-Idea titles)

Page titles and visual titles **state the insight, not the subject**.

| ❌ Bland | ✅ Big-Idea |
|---|---|
| "Sales by Region" | "North region missed plan by 12%" |
| "Revenue Trend" | "Revenue momentum steady through Q3" |
| "Top Products" | "Three SKUs drive 60% of margin" |
| "Cost Analysis" | "Freight cost inflation offsetting price gains" |

Rules:
- Titles are **full sentences** when the insight is definitive
- **Quantify** when possible ("12%", "three SKUs", "$4.2M gap")
- Avoid hedging words ("possibly", "seems to") — exec audiences want conclusions

---

## Page structure (typical)

```
┌──────────────────────────────────────────────────┐
│ Big-Idea page title (24pt, 56 h)                │
├──────────────────────────────────────────────────┤
│ [KPI 1] [KPI 2] [KPI 3] [KPI 4]    (120 h)     │
├──────────────────────────────────────────────────┤
│                                                  │
│  Hero visual — usually trend or                 │
│  single definitive chart (400 h)                │
│                                                  │
├──────────────────────────────────────────────────┤
│ [Supporting visual 1] [Supporting visual 2]     │
│                                    (280 h)      │
└──────────────────────────────────────────────────┘
```

4 visuals = KPI row (4 cards = 1 visual compositionally) + hero + two supporting. That's the ceiling.

---

## Annotation heaviness

Executive pages are **annotation-heavy**:
- Reference lines on trend charts (plan, prior year, target)
- Callout textboxes over chart areas pointing to key inflection points
- Direct data labels on bar charts (no separate axis reading required)
- Footnotes explaining methodology where material

Use `textbox` visuals layered over charts for callouts. Keep them terse (≤ 15 words).

---

## Color discipline

- **Muted / restrained** palette
- 1-2 accent colors max for highlights
- Heavy use of neutral grays for non-focal data
- Reserve the accent color for the **one thing the reader should notice**

Example — in a bar chart showing regional revenue, ALL bars are neutral gray EXCEPT the region that missed plan, which is the accent red.

---

## Whitespace

Executive style is **generous with whitespace**:
- Gutter between visuals: 24-32px (vs 8-16px elsewhere)
- Left / right safe zone: 32px (vs 16px)
- Top padding above hero visual: 16-24px

Visuals should feel "framed", not crammed.

---

## Titles & subtitles

Every visual has:
- **Title** (14pt, Semibold) — Big-Idea phrasing
- **Subtitle** (11pt, Regular, muted color) — measure context or time frame
  - Example title: "North region missed plan by 12%"
  - Example subtitle: "FY2025 YTD revenue vs. plan, by region"

---

## What NOT to do in Executive style

- ❌ Tables or matrices (too detail-heavy for exec audiences)
- ❌ More than 1 slicer (audience isn't filtering live)
- ❌ Dense grids of small-multiple visuals
- ❌ Drillthrough / bookmark navigation (too interactive)
- ❌ Tooltips with heavy data (executives don't hover)
- ❌ Color gradients / heatmaps (prefer categorical accent)

---

## When to escalate to Analytical

If the user's WHAT answer (decision this enables) requires **comparison across 5+ dimensions** or **data exploration**, the audience is not truly executive — route to Analytical personality.

---

## Checklist before Polisher

- [ ] Every page has ≤ 4 visuals (excl. slicers)
- [ ] Every visual title is Big-Idea phrasing
- [ ] Hero visual dominates (~40% of page height)
- [ ] At least one annotation / reference line on the hero visual
- [ ] Palette uses ≤ 2 accent colors
- [ ] Gutter ≥ 24px between visuals
