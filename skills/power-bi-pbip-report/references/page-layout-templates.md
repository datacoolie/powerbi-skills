# Page Layout Templates

Starting-point templates for common page types. Canvas size: 1664×936.
Adjust dimensions and visuals to match specific requirements.

---

## Overview Page Template

The landing page — executive summary with navigation to detail pages.

```
Layout (1664×936):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1664×78) z:0                │
│   textbox-title (13,13) "Report Title"              │
│   slicer-date-range (1170,13 → 481×52)             │
├─────────────────────────────────────────────────────┤
│ KPI Row (y:91, h:104)                               │
│  card-kpi-1  card-kpi-2  card-kpi-3  card-kpi-4    │
│  (x:13,w:397) (x:423,w:397) (x:832,w:397) (x:1242)│
├─────────────────────────────────────────────────────┤
│ Primary (y:208, h:390)                              │
│  ┌─────────────────────┐ ┌──────────────────────┐ │
│  │ lineChart-trend     │ │ clusteredBarChart-top-n │ │
│  │ (13,208 → 975×390)  │ │ (1001,208 → 650×390)   │ │
│  └─────────────────────┘ └──────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ Secondary (y:611, h:260)                            │
│  pivotTable-summary (13,611 → 1638×260)             │
├─────────────────────────────────────────────────────┤
│ Navigation (y:884, h:39)                            │
│  actionButton-detail  actionButton-drillthrough     │
└─────────────────────────────────────────────────────┘
```

## Detail / Analysis Page Template

Deep-dive page with filters and detailed breakdowns.

```
Layout (1664×936):
┌────────┬────────────────────────────────────────────┐
│ Filter │ shape-header-bg (260,0 → 1404×65)          │
│ Panel  │   textbox-title  slicer-date-range          │
│ (0,0)  ├────────────────────────────────────────────┤
│ w:247  │ KPI Row (y:72, h:85)                       │
│ h:936  │  card-kpi-1  card-kpi-2  card-kpi-3        │
│        ├────────────────────────────────────────────┤
│ slicer │ Main Chart Area (y:169, h:364)             │
│ -cat1  │  lineClusteredColumnComboChart-main         │
│ slicer │  (273,169 → 1378×364)                      │
│ -cat2  ├────────────────────────────────────────────┤
│ slicer │ Detail Table (y:546, h:338)                │
│ -cat3  │  tableEx-detail (273,546 → 1378×338)       │
│        ├────────────────────────────────────────────┤
│ action │ Nav: actionButton-back (273,897 → 130×33)  │
│ Button │                                             │
│ -reset │                                             │
└────────┴────────────────────────────────────────────┘
```

## Drillthrough Page Template

Target page for right-click drillthrough — shows entity-level detail.

```json
// page.json additions:
{
  "type": "Drillthrough",
  "visibility": "HiddenInViewMode"
}
```

```
Layout (1664×936):
┌─────────────────────────────────────────────────────┐
│ Header: textbox-entity-name + actionButton-back     │
│ (actionButton with "Back" navigation type)          │
├─────────────────────────────────────────────────────┤
│ Entity Summary (y:78, h:130)                        │
│  card-attr-1  card-attr-2  card-attr-3  card-attr-4 │
├─────────────────────────────────────────────────────┤
│ Trend (y:221, h:325)                                │
│  lineChart-entity-trend (13,221 → 1638×325)         │
├─────────────────────────────────────────────────────┤
│ Detail (y:559, h:364)                               │
│  tableEx-entity-transactions (13,559 → 1638×364)    │
└─────────────────────────────────────────────────────┘
```

The drillthrough parameter filter is automatically applied by Power BI
when the user right-clicks a record and selects "Drillthrough."

## Tooltip Page Template

Custom tooltip — small canvas shown on hover.

```json
// page.json:
{
  "type": "Tooltip",
  "visibility": "HiddenInViewMode",
  "width": 320,
  "height": 240
}
```

```
Layout (320×240):
┌───────────────────────────┐
│ textbox-title (5,5)       │
├───────────────────────────┤
│ card-primary (5,30 → 150) │
│ card-secondary (165,30)   │
├───────────────────────────┤
│ clusteredBarChart-detail  │
│ (5,100 → 310×130)        │
└───────────────────────────┘
```

Keep tooltip pages minimal — max 3-4 visuals. Load time is critical since
tooltips appear on hover.

## Dashboard Grid Layout (Comparison / Multi-KPI)

Equal-sized chart grid for side-by-side comparison. Used in Manufacturing,
Supply Chain, and multi-metric analysis pages.

```
Layout (1664×936):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1664×56)                    │
│ textbox-title (13,8)        slicer-period (1200,10) │
├─────────────────┬───────────────────────────────────┤
│ KPI Row (y:64)  │ card×4 evenly spaced (w:390 each)│
│ card-1 (13,64)  card-2 (421,64) ...  card-4 (1261,64)│
│ (h:90 each)                                         │
├────────────────────┬────────────────────────────────┤
│ Chart Row 1 (y:170)                                 │
│  chart-1           │  chart-2                       │
│  (13,170→808×350)  │  (843,170→808×350)             │
├────────────────────┼────────────────────────────────┤
│ Chart Row 2 (y:536)                                 │
│  chart-3           │  chart-4                       │
│  (13,536→808×350)  │  (843,536→808×350)             │
└────────────────────┴────────────────────────────────┘
```

Use background shapes behind each chart pair or per quadrant for visual
grouping. Place shapes at z:100-500, charts at z:5000+.

## Left-Sidebar Filter Layout

Dedicated filter panel on the left, main content on the right. Found in
Sales Analysis, Trade Analytics, and Financial reports.

```
Layout (1664×936):
┌──────────┬──────────────────────────────────────────┐
│ Sidebar  │ shape-header-bg (280,0 → 1384×56)       │
│ (0,0)    │ textbox-title (293,8)                    │
│ w:268    ├──────────────────────────────────────────┤
│          │ KPI Row (y:64)                           │
│ shape-bg │  card-1 (293,64)  card-2 (623,64)       │
│ (0,0→    │  card-3 (953,64)  card-4 (1283,64)      │
│  268×936)│  (w:318, h:90 each)                     │
│          ├──────────────────────────────────────────┤
│ slicer-1 │ Main Chart Area (y:168)                  │
│ (13,80   │  chart-primary (293,168 → 1358×400)     │
│  →242×70)├──────────────────────────────────────────┤
│ slicer-2 │ Detail Area (y:582)                      │
│ (13,160  │  tableEx or matrix (293,582 → 1358×340) │
│  →242×70)│                                          │
│ slicer-3 │                                          │
│ (13,240  │                                          │
│  →242×70)│                                          │
│ slicer-4 │                                          │
│ (13,320  │                                          │
│  →242×70)│                                          │
│          │                                          │
│ btn-reset│                                          │
│ (13,860  │                                          │
│  →242×40)│                                          │
└──────────┴──────────────────────────────────────────┘
```

Sidebar shape uses a contrasting background color (e.g., dark with white
slicer text, or light gray with dark text). Slicers use dropdown mode to
save vertical space. Include a "Reset Filters" action button at the bottom.

## KPI Scorecard Layout (Executive Summary)

Dense card grid for C-level executive pages. Prioritizes numbers over charts.
Found in Financial Dashboard, BTM Manufacturing.

```
Layout (1664×936):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1664×56)                    │
│ image-logo (13,8 → 40×40)  textbox-title (60,8)    │
├─────────────────────────────────────────────────────┤
│ KPI Row 1 — Primary Metrics (y:70, h:120)           │
│  card×3 large (w:530 each, gap:22)                  │
│  (13,70)  (557,70)  (1101,70)                       │
│  Each: value + label + trend sparkline indicator     │
├─────────────────────────────────────────────────────┤
│ KPI Row 2 — Secondary Metrics (y:206, h:90)         │
│  card×5 medium (w:318 each, gap:12)                 │
│  (13,206) (343,206) (673,206) (1003,206) (1333,206) │
├─────────────────────────────────────────────────────┤
│ Visual Row (y:312, h:300)                           │
│  combo-chart (13,312 → 1084×300)                    │
│  donut-chart (1113,312 → 538×300)                   │
├─────────────────────────────────────────────────────┤
│ Detail Row (y:628, h:294)                           │
│  matrix or table (13,628 → 1638×294)                │
└─────────────────────────────────────────────────────┘
```

Use background shapes behind each KPI row. Primary cards have larger fonts
(28-36pt value, 11pt label), secondary cards use 18-22pt values. Apply
conditional formatting colors (green/red) on variance KPIs.

## Tab-Navigation Layout (Multi-View Single Page)

Uses bookmark-driven tabs to show different visual groups on the same page.
Common in reports with 10+ related views. See `navigation-patterns.md`
for the bookmark navigation pattern.

```
Layout (1664×936):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1664×56)                    │
│ textbox-title (13,8)                                │
├─────────────────────────────────────────────────────┤
│ Tab Bar (y:56, h:36)                                │
│ shape-tab-bg (0,56 → 1664×36)                      │
│  btn-tab1 (13,58) btn-tab2 (173,58) btn-tab3 (333,58)│
│  (w:148, h:32 each — active tab has accent underline)│
├─────────────────────────────────────────────────────┤
│ Filter Row (y:96, h:50)                             │
│  slicer-1 (13,96→380×44) slicer-2 (410,96→380×44)  │
│  slicer-3 (807,96→380×44)                           │
├─────────────────────────────────────────────────────┤
│ Content Area (y:158 → bottom)                       │
│ ┌─ group-tab1-visuals (shown) ──────────────────┐ │
│ │  chart-a (13,158 → 808×370)                     │ │
│ │  chart-b (843,158 → 808×370)                    │ │
│ │  table-c (13,544 → 1638×378)                    │ │
│ └─────────────────────────────────────────────────┘ │
│ ┌─ group-tab2-visuals (hidden bookmark) ──────────┐ │
│ │  (separate set of visuals, same positions)       │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

Create one bookmark per tab. Each bookmark toggles visibility of visual
groups. Tab buttons use `"type": "'Bookmark'"` action pointing to their
respective bookmark. Style active tab with accent color fill/underline.
