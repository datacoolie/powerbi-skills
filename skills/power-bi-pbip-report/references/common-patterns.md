# Common Report Patterns

Reusable layout and component patterns found across real-world Power BI reports.
Canvas size: 1664×936 (standard).

---

## KPI Header Row

A row of 3-5 card visuals across the top of a page. Cards are typically
80-160px wide and 50-70px tall, with themed backgrounds and rounded corners.

```
┌─────────────────────────────────────────────────────────┐
│ card-kpi-1     card-kpi-2     card-kpi-3     card-kpi-4 │
│ (13,10 w:390)  (416,10 w:390) (819,10 w:390) (1222,10) │
│ h:65           h:65           h:65           h:65 w:429 │
└─────────────────────────────────────────────────────────┘
```

Each card: `visualType: "card"`, single measure in `Values`, with:
- `z: 8000` (above background shapes)
- `visualContainerObjects.background.color` matching theme accent or white
- `visualContainerObjects.border.radius: 8D` for rounded corners
- `visualContainerObjects.dropShadow.show: true` for depth
- `objects.labels.fontSize: 16D`, bold
- `objects.categoryLabels.fontSize: 8D` for the sub-label

## Slicer Panel

**Top row slicers** (compact dropdown, fits 2-3 across header):
```
slicer-date-range (1100,13 w:551 h:52) — dropdown mode
slicer-category  (830,13 w:257 h:52) — dropdown mode
```

**Left panel slicers** (vertical stack, used in Detail/Analysis layouts):
```
shape-bg-filter-panel (0,0 w:247 h:936 z:0) — background shape
slicer-cat1 (13,91 w:221 h:65) — dropdown
slicer-cat2 (13,169 w:221 h:65) — dropdown
slicer-cat3 (13,247 w:221 h:65) — dropdown
slicer-cat4 (13,325 w:221 h:65) — dropdown
actionButton-reset (13,832 w:221 h:39) — reset filters bookmark
```

All slicers default to:
- `objects.data.mode: "'Dropdown'"` (compact, saves space)
- `objects.header.background` in theme accent color with white text
- `objects.selection.selectAllCheckboxEnabled: true`
- `visualContainerObjects.visualHeader.show: false` (hide "..." menu)
- `visualContainerObjects.border.show: false`

## Slicer Sync Groups

When a slicer should apply across multiple pages, add `syncGroup` to the visual:
```json
"syncGroup": {
  "groupName": "Date Range",
  "fieldChanges": true,
  "filterChanges": true
}
```
Place identical slicers (same field, same syncGroup name) on each page. Power BI
synchronizes their selection state automatically.

## Sync Slicers Across Pages

When slicers should apply consistently across multiple pages (e.g., a global date range
or department filter), use **sync slicers** via `reportExtensions.json`. This is the
**default recommendation** for multi-page reports — it prevents users from having to
re-select filters on each page.

Sync slicers are configured in `reportExtensions.json` at the report level. The file
defines which slicer visual syncs across which pages:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/reportExtension/1.0.0/schema.json",
  "entities": []
}
```

In practice, sync slicers work by placing identical slicer visuals on each page (same field,
same configuration) and Power BI synchronizes their selection state. To set this up in PBIR:
1. Add the same slicer visual (same field and configuration) to each page that needs it
2. Use consistent naming: e.g., `slicer-date-range` on every page
3. The sync behavior is managed by Power BI Desktop when the report is opened

**Default rule:** For any multi-page report, always include sync slicers for date range
and primary category filters unless the user explicitly requests independent page filtering.

## Background Shape

A colored rectangle behind a group of visuals for visual grouping:
- Use `visualType: "shape"` with no query
- Set low z-order (e.g., 0) so it appears behind data visuals
- Configure with `objects.shape.tileShape: "'rectangleRounded'"` for rounded rectangle
- Set `visualContainerObjects.background.color` and `transparency`
- Common transparency values: `20D`-`40D` for subtle section backgrounds

## Visual Grouping with Background Regions

Use overlapping background shapes to create distinct visual regions on a page.
This applies the Gestalt **enclosure** principle:

```
Header region:   shape-header-bg (0,0 → 1664×78 z:0) — dark accent color, 0% transparency
KPI region:      shape-kpi-bg    (0,78 → 1664×130 z:0) — light grey, 20% transparency
Filter region:   shape-filter-bg (0,0 → 247×936 z:0) — medium grey, 36% transparency
Content region:  shape-content-bg (260,78 → 1404×858 z:0) — white or transparent
```
Always set `z: 0` on backgrounds so data visuals render on top.

## Page Navigator (Built-in)

For multi-page reports, use the `pageNavigator` visual instead of manual action buttons.
It automatically generates clickable tiles for all visible report pages:

```json
{
  "name": "pageNavigator-main",
  "position": { "x": 650, "y": 0, "z": 5000, "height": 57, "width": 654, "tabOrder": 0 },
  "visual": {
    "visualType": "pageNavigator",
    "objects": {
      "layout": [{
        "properties": {
          "rowCount": { "expr": { "Literal": { "Value": "2L" } } },
          "orientation": { "expr": { "Literal": { "Value": "0D" } } },
          "cellPadding": { "expr": { "Literal": { "Value": "2L" } } }
        }
      }],
      "pageTabs": [{
        "properties": {
          "fontColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0 } } } } },
          "fontSize": { "expr": { "Literal": { "Value": "9D" } } },
          "bold": { "expr": { "Literal": { "Value": "true" } } }
        }
      }]
    },
    "drillFilterOtherVisuals": true
  }
}
```
`orientation`: `0D` = Horizontal, `1D` = Vertical.
Use `rowCount` to control how many rows of tabs appear.

## Image Navigation Menu (Icon-Based)

For branded navigation, use `image` visuals with page navigation links. Each image
acts as a clickable icon that navigates to a specific page:

```json
{
  "name": "image-nav-procurement",
  "position": { "x": 1200, "y": 2, "z": 27000, "height": 46, "width": 50, "tabOrder": 24000 },
  "visual": {
    "visualType": "image",
    "objects": {
      "general": [{
        "properties": {
          "imageUrl": {
            "expr": {
              "ResourcePackageItem": {
                "PackageName": "RegisteredResources",
                "PackageType": 1,
                "ItemName": "icon-procurement.png"
              }
            }
          }
        }
      }]
    },
    "visualContainerObjects": {
      "visualLink": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
          "navigationSection": { "expr": { "Literal": { "Value": "'target-page-name'" } } }
        }
      }]
    }
  }
}
```
Place icon images in `StaticResources/RegisteredResources/`. Typical size: 40-50px square.

## Visual Interactions (Page-Level)

Configure cross-filtering behavior between visuals in `page.json`. By default, all
visuals cross-filter each other. Customize with:

```json
"visualInteractions": [
  {
    "source": "slicer-date-range",
    "target": "lineChart-trend",
    "type": "DataFilter"
  },
  {
    "source": "clusteredBarChart-categories",
    "target": "pivotTable-detail",
    "type": "HighlightFilter"
  },
  {
    "source": "card-kpi-total",
    "target": "lineChart-trend",
    "type": "NoFilter"
  }
]
```

Interaction types:
- `DataFilter` — clicking source filters target (most common; slicers always use this)
- `HighlightFilter` — clicking source highlights matching data in target (preserves context)
- `NoFilter` — source does not affect target at all

**Default rule**: Let slicers DataFilter everything. Set chart-to-chart interactions to
HighlightFilter (so clicking a bar highlights across all visuals but doesn't remove data).
Use NoFilter on KPI cards so they always show the page total regardless of chart clicks.
