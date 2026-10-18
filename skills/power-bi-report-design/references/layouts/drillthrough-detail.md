# Layout: Drillthrough Detail

> **Preview:** [![drillthrough-detail preview](../../assets/layout-previews/drillthrough-detail.svg)](../../assets/layout-previews/drillthrough-detail.svg) · variants: [annotated](../../assets/layout-previews/drillthrough-detail-annotated.svg) · [dark](../../assets/layout-previews/drillthrough-detail-dark.svg)

- **id:** `drillthrough-detail`
- **Canvas:** 1920 × 1080
- **Style personality:** Analytical
- **Audience:** Analyst investigating a specific entity (product, customer, region, store)
- **Visual count:** 6 (excluding back button)
- **Entry:** right-click drillthrough from any hub page

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ [Back]   Entity: {selected name}                               │ 64
├────────────────────────────────────────────────────────────────┤
│   Entity header: key attributes (textbox / card grid)          │ 168
├────────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐                                │
│  │ Metric 1   │  │ Metric 2   │                                │ 448
│  │ trend      │  │ breakdown  │                                │
│  └────────────┘  └────────────┘                                │
├────────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐                                │
│  │ Metric 3   │  │ Metric 4   │                                │ 720
│  │ comparison │  │ composition│                                │
│  └────────────┘  └────────────┘                                │
├────────────────────────────────────────────────────────────────┤
│   Transactions table (top 20, sortable)                        │ 1080
└────────────────────────────────────────────────────────────────┘
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Back button | 32 | 24 | 112 | 40 | button | **REQUIRED** — wired to source page or prev. Icon: chevron-left |
| Entity title | 160 | 24 | 1728 | 40 | textbox | Binds to the drillthrough field |
| Entity header | 32 | 88 | 1856 | 80 | multi-row card OR textbox grid | 3-5 attributes: ID, owner, start-date, etc. |
| Metric 1: trend | 32 | 192 | 920 | 256 | line | |
| Metric 2: breakdown | 968 | 192 | 920 | 256 | bar | |
| Metric 3: comparison | 32 | 464 | 920 | 256 | column / bar | YoY, vs peers, vs plan |
| Metric 4: composition | 968 | 464 | 920 | 256 | stacked bar / donut | |
| Transactions table | 32 | 744 | 1856 | 312 | tableEx | Top 20 rows, sorted by date desc |

Gutters: 16px inside a group (back button ↔ title, metric grid), 24px between groups (title row ↔ header ↔ metric grid ↔ table). Page margins 32px (24px top and bottom).

---

## Required elements (design rule)

- **Back button** — non-negotiable. Drillthrough pages without one **fail linter** (error in `design_quality_check.py`).
- **Entity title bound to the drillthrough field** — so the page shows which entity is being viewed
- **Drillthrough filter panel** — hidden (set `drillthroughFilters.hidden: true` for clean display)
- **Page visibility** — set page `hidden: true` so it doesn't appear in page tabs

---

## Theme + iconography guidance

- Same theme as the rest of the report (drillthrough is not a mode change)
- **Logo:** omit on drillthrough (this is a detail page reached from a parent; showing the logo again wastes space). If a brand mark is required by style guide, place it top-right at ≤ 16px.
- Back button icon: chevron-left or arrow-left
- No KPI-set icons on metric visuals (detail view, not status view)

---

## When NOT to use this layout

- ❌ As a primary page (it's always an entry via drillthrough)
- ❌ Executive reports (drillthrough is an analytical interaction)
- ❌ When drillthrough target has < 3 metrics to show (use tooltip page instead)

---

## Customization allowed

- Swap the 2×2 metric grid to 3×1 or 1×3 when one metric dominates
- Replace transactions table with matrix if hierarchical
- Add a second row of metrics (4→6) by compressing header
- **FHD headroom (optional)** — at most two extra slots, each carved from a donor slot (donor shrinks as stated; visual count 6 → 8, within the Analytical ≤ 12 budget):
  - *Entity status vs plan* — card at (1408, 88, 480, 80); shrink Entity header to w=1360. Answers "is this entity on track against plan?" (% to plan + traffic-light), not another absolute total.
  - *Transaction mix* — bar at (1408, 744, 480, 312); shrink Transactions table to w=1360. Answers "which transaction types drive this entity's volume?"

## Customization NOT allowed

- Removing the back button
- Making the page visible in tabs (defeats drillthrough UX)
- Hiding the entity title (user loses context)
