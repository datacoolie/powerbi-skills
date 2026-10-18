# Page Layout Templates

Starting-point templates for common page types.
Adjust dimensions and visuals to match specific requirements.

> **Canvas.** The default report canvas is **1920×1080 (FHD)**. Every sketch below is drawn on 1920×1080 with
> real coordinates: 32 px page margin, 24 px gutters, header band 72 px, all values multiples of 8. Where a row
> cannot divide evenly on the 8-px grid, the right-most visual absorbs the remainder (e.g. 448/448/448/440).
> To adapt a sketch to another canvas, or to take exact slots from a library recipe, use
> `python scripts/rescale_layout.py --layout <id> --canvas <WxH> --format md`.
> The tooltip template (320×240) is a separate small canvas.

> **Visual preview catalog:** rendered SVGs for every layout (base + annotated + dark variants) live in
> [`../assets/layout-previews/`](../assets/layout-previews/). For a one-page overview of the whole catalog see
> [`../assets/layouts-contact-sheet.svg`](../assets/layouts-contact-sheet.svg);
> for the theme × layout compatibility grid see
> [`../assets/theme-layout-matrix.svg`](../assets/theme-layout-matrix.svg).

---

## Overview Page Template

The landing page — executive summary with navigation to detail pages.

```
Layout (1920×1080):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1920×72) z:0                 │
│   textbox-title (32,12) "Report Title"              │
│   slicer-date-range (1360,12 → 528×48)              │
├─────────────────────────────────────────────────────┤
│ KPI Row (y:96, h:120)                               │
│  card-kpi-1  card-kpi-2  card-kpi-3  card-kpi-4     │
│  (x:32,w:448) (x:504) (x:976) (x:1448,w:440)        │
├─────────────────────────────────────────────────────┤
│ Primary (y:240, h:432)                              │
│  ┌───────────────────────┐ ┌──────────────────────┐ │
│  │ lineChart-trend       │ │ clusteredBar-top-n   │ │
│  │ (32,240 → 1072×432)   │ │ (1128,240 → 760×432) │ │
│  └───────────────────────┘ └──────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ Secondary (y:696, h:288)                            │
│  pivotTable-summary (32,696 → 1856×288)             │
├─────────────────────────────────────────────────────┤
│ Navigation (y:1008, h:40)                           │
│  actionButton-detail  actionButton-drillthrough     │
└─────────────────────────────────────────────────────┘
```

## Detail / Analysis Page Template

Deep-dive page with filters and detailed breakdowns.

```
Layout (1920×1080):
┌────────┬────────────────────────────────────────────┐
│ Filter │ shape-header-bg (312,0 → 1608×72)          │
│ Panel  │   textbox-title  slicer-date-range         │
│ (0,0)  ├────────────────────────────────────────────┤
│ w:288  │ KPI Row (y:96, h:104)                      │
│ h:1080 │  card-kpi-1  card-kpi-2  card-kpi-3        │
│        ├────────────────────────────────────────────┤
│ slicer │ Main Chart Area (y:224, h:384)             │
│ -cat1  │  lineClusteredColumnComboChart-main        │
│ slicer │  (312,224 → 1576×384)                      │
│ -cat2  ├────────────────────────────────────────────┤
│ slicer │ Detail Table (y:632, h:344)                │
│ -cat3  │  tableEx-detail (312,632 → 1576×344)       │
│        ├────────────────────────────────────────────┤
│ action │ Nav: actionButton-back (312,1000 → 160×40) │
│ Button │                                            │
│ -reset │                                            │
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
Layout (1920×1080):
┌─────────────────────────────────────────────────────┐
│ Header: textbox-entity-name + actionButton-back     │
│ (actionButton with "Back" navigation type)          │
├─────────────────────────────────────────────────────┤
│ Entity Summary (y:96, h:144)                        │
│  card-attr-1  card-attr-2  card-attr-3  card-attr-4 │
├─────────────────────────────────────────────────────┤
│ Trend (y:264, h:360)                                │
│  lineChart-entity-trend (32,264 → 1856×360)         │
├─────────────────────────────────────────────────────┤
│ Detail (y:648, h:392)                               │
│  tableEx-entity-transactions (32,648 → 1856×392)    │
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
Layout (1920×1080):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1920×72)                     │
│ textbox-title (32,16)       slicer-period (1568,12) │
├─────────────────────────────────────────────────────┤
│ KPI Row (y:96, h:104) — card×4 (w:448; last 440)    │
│ card-1 (32,96)  card-2 (504,96)  card-3 (976,96)    │
│ card-4 (1448,96)                                    │
├──────────────────────────┬──────────────────────────┤
│ Row 1 (y:224, h:400)     │ w:920 | 912, gap:24      │
│  chart-1                 │  chart-2                 │
│  (32,224 → 920×400)      │  (976,224 → 912×400)     │
├──────────────────────────┼──────────────────────────┤
│ Row 2 (y:648, h:400)     │                          │
│  chart-3                 │  chart-4                 │
│  (32,648 → 920×400)      │  (976,648 → 912×400)     │
└──────────────────────────┴──────────────────────────┘
```

Use background shapes behind each chart pair or per quadrant for visual
grouping. Place shapes at z:100-500, charts at z:5000+.

## Left-Sidebar Filter Layout

Dedicated filter panel on the left, main content on the right. Found in
Sales Analysis, Trade Analytics, and Financial reports.

```
Layout (1920×1080):
┌──────────┬──────────────────────────────────────────┐
│ Sidebar  │ shape-header-bg (312,0 → 1608×72)        │
│ (0,0)    │ textbox-title (336,16)                   │
│ w:288    ├──────────────────────────────────────────┤
│          │ KPI Row (y:96)                           │
│ shape-bg │  card-1 (312,96)  card-2 (712,96)        │
│ (0,0→    │  card-3 (1112,96)  card-4 (1512,96)      │
│ 288×1080)│  (w:376, h:104 each)                     │
│          ├──────────────────────────────────────────┤
│ slicer-1 │ Main Chart Area (y:224)                  │
│ (24,96   │  chart-primary (312,224 → 1576×384)      │
│  →240×80)├──────────────────────────────────────────┤
│ slicer-2 │ Detail Area (y:632)                      │
│ (24,200  │  tableEx or matrix (312,632 → 1576×408)  │
│  →240×80)│                                          │
│ slicer-3 │                                          │
│ (24,304  │                                          │
│  →240×80)│                                          │
│ slicer-4 │                                          │
│ (24,408  │                                          │
│  →240×80)│                                          │
│          │                                          │
│ btn-reset│                                          │
│ (24,1000 │                                          │
│  →240×40)│                                          │
└──────────┴──────────────────────────────────────────┘
```

Sidebar shape uses a contrasting background color (e.g., dark with white
slicer text, or light gray with dark text). Slicers use dropdown mode to
save vertical space. Include a "Reset Filters" action button at the bottom.

## KPI Scorecard Layout (Executive Summary)

Dense card grid for C-level executive pages. Prioritizes numbers over charts.
Found in Financial Dashboard, BTM Manufacturing.

```
Layout (1920×1080):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1920×72)                     │
│ image-logo (32,16 → 40×40)  textbox-title (88,16)   │
├─────────────────────────────────────────────────────┤
│ KPI Row 1 — Primary Metrics (y:96, h:136)           │
│  card×3 large (w:600/600/608, gap:24)               │
│  (32,96)  (656,96)  (1280,96)                       │
│  Each: value + label + trend sparkline indicator    │
├─────────────────────────────────────────────────────┤
│ KPI Row 2 — Secondary Metrics (y:256, h:104)        │
│  card×5 medium (w:352 each, gap:24)                 │
│  (32,256) (408,256) (784,256) (1160,256) (1536,256) │
├─────────────────────────────────────────────────────┤
│ Visual Row (y:384, h:320)                           │
│  combo-chart (32,384 → 1224×320)                    │
│  donut-chart (1280,384 → 608×320)                   │
├─────────────────────────────────────────────────────┤
│ Detail Row (y:728, h:320)                           │
│  matrix or table (32,728 → 1856×320)                │
└─────────────────────────────────────────────────────┘
```

Use background shapes behind each KPI row. Primary cards have larger fonts
(28-36pt value, 11pt label), secondary cards use 18-22pt values. Apply
conditional formatting colors (green/red) on variance KPIs.

## Tab-Navigation Layout (Multi-View Single Page)

Uses bookmark-driven tabs to show different visual groups on the same page.
Common in reports with 10+ related views. See [`navigation-patterns.md`](navigation-patterns.md)
for the bookmark navigation pattern.

```
Layout (1920×1080):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1920×72)                     │
│ textbox-title (32,16)                               │
├─────────────────────────────────────────────────────┤
│ Tab Bar (y:72, h:40)                                │
│ shape-tab-bg (0,72 → 1920×40)                       │
│ btn-tab1 (32,76) btn-tab2 (224,76) btn-tab3 (416,76)│
│ (w:176, h:32 each — active tab has accent underline)│
├─────────────────────────────────────────────────────┤
│ Filter Row (y:128, h:48)                            │
│ slicer-1 (32,128→440×48) slicer-2 (496,128→440×48)  │
│ slicer-3 (960,128→440×48)                           │
├─────────────────────────────────────────────────────┤
│ Content Area (y:200 → bottom)                       │
│ ┌─ group-tab1-visuals (shown) ──────────────────┐   │
│ │  chart-a (32,200 → 920×416)                   │   │
│ │  chart-b (976,200 → 912×416)                  │   │
│ │  table-c (32,640 → 1856×408)                  │   │
│ └───────────────────────────────────────────────┘   │
│ ┌─ group-tab2-visuals (hidden bookmark) ────────┐   │
│ │  (separate set of visuals, same positions)    │   │
│ └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

Create one bookmark per tab. Each bookmark toggles visibility of visual
groups. Tab buttons use `"type": "'Bookmark'"` action pointing to their
respective bookmark. Style active tab with accent color fill/underline.
