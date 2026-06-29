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

---

## TOP N Chart Pattern

A ranked bar chart limited to the top (or bottom) N dimension members by a measure.
This is one of the most common analytical patterns — "Top 10 Products by Revenue", "Top 5 Customers by Margin".

### Component Layout

```
┌──────────────────────────────────────────────┐
│ title: "Top 10 Products by Revenue"          │
│                                               │
│  Product A  ████████████████████  $1.2M      │
│  Product B  ████████████████      $980K      │
│  Product C  ████████████          $820K      │
│  ...                                          │
│  Product J  ████                  $340K      │
└──────────────────────────────────────────────┘
```

- `visualType: "barChart"` (horizontal) — best for ranked lists with long category labels
- `visualType: "clusteredColumnChart"` (vertical) — use when N ≤ 5 and labels are short
- Sort: value descending (largest bar at top / left)
- Data labels: show on bars for direct reading (remove y-axis instead)

### Complete visual.json snippet

```json
{
  "name": "barChart-top10-products",
  "position": { "x": 260, "y": 90, "z": 5000, "height": 400, "width": 680, "tabOrder": 500 },
  "visual": {
    "visualType": "barChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimProduct" } },
                "Property": "ProductName"
              }
            },
            "queryRef": "DimProduct.ProductName"
          }]
        },
        "Y": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                "Property": "Total Revenue"
              }
            },
            "queryRef": "MeasureTable.Total Revenue"
          }]
        }
      },
      "sortDefinition": {
        "sort": [{
          "field": {
            "Measure": {
              "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
              "Property": "Total Revenue"
            }
          },
          "direction": "Descending"
        }],
        "isDefaultSort": true
      }
    },
    "objects": {
      "dataLabels": [{ "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } }],
      "categoryAxis": [{ "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } }],
      "valueAxis": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]
    },
    "drillFilterOtherVisuals": true
  },
  "filterConfig": {
    "filters": [{
      "name": "topn-filter-revenue",
      "field": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "DimProduct" } },
          "Property": "ProductName"
        }
      },
      "type": "TopN",
      "filter": {
        "Version": 2,
        "From": [
          {
            "Name": "subquery",
            "Expression": {
              "Subquery": {
                "Query": {
                  "Version": 2,
                  "From": [
                    { "Name": "d", "Entity": "DimProduct", "Type": 0 },
                    { "Name": "m", "Entity": "MeasureTable", "Type": 0 }
                  ],
                  "Select": [{
                    "Column": {
                      "Expression": { "SourceRef": { "Source": "d" } },
                      "Property": "ProductName"
                    },
                    "Name": "field"
                  }],
                  "OrderBy": [{
                    "Direction": 2,
                    "Expression": {
                      "Measure": {
                        "Expression": { "SourceRef": { "Source": "m" } },
                        "Property": "Total Revenue"
                      }
                    }
                  }],
                  "Top": 10
                }
              }
            },
            "Type": 2
          },
          { "Name": "d", "Entity": "DimProduct", "Type": 0 }
        ],
        "Where": [{
          "Condition": {
            "In": {
              "Expressions": [{
                "Column": {
                  "Expression": { "SourceRef": { "Source": "d" } },
                  "Property": "ProductName"
                }
              }],
              "Table": { "SourceRef": { "Source": "subquery" } }
            }
          }
        }]
      }
    }]
  }
}
```

### Bottom N variant

Change `Direction: 2` → `Direction: 1` (ascending) in the `OrderBy` to get **Bottom N** (lowest values). Title and filter name should reflect this: "Bottom 5 Products by Margin".

### Combining TOP N with slicer context

The TOP N filter applies **after** slicer selections — slicers filter the dataset first, then
TOP N ranks within the remaining data. This means "Top 10 by Revenue in Q1" automatically
works when a date slicer is on the page with no additional changes needed.

### Dynamic TOP N (user-controlled N value)

For an interactive N selector (user picks "Top 5", "Top 10", "Top 20"), the approach shifts
to the semantic model layer — not the report layer:
- Create a disconnected `TopN Selector` table with values like 5, 10, 20
- Add a slicer for that table
- Reference the slicer selection in a RANKX/TOPN DAX measure
- Use a visual-level filter: `type: "Advanced"` with `measure > 0` on the rank measure

The static `type: "TopN"` filterConfig approach is used when N is fixed at report design time.

### Design rules

- Use **horizontal bar chart** for N > 5 or when category labels are long (product names, store names)
- Use **vertical column chart** for N = 3–5 with short labels
- Always **sort descending** (largest first) — this is the natural reading order for rankings
- Title pattern: **"Top [N] [Dimension] by [Measure]"** — e.g., "Top 10 Customers by Gross Profit"
- Show **data labels** on bars; hide the value axis (redundant with labels)
- Optionally add a **rank label** column (DAX: `RANKX`) as a second series or tooltip for readability
- Pair with a KPI card above showing the **total** so viewers understand what percentage the top N represents

---

## Sync Slicers (reportExtensions)

Sync slicers share filter state across multiple pages. Configuration lives in
`reportExtensions.json` at the report definition root level.

### reportExtensions.json Structure

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/reportExtensions/1.0.0/schema.json",
    "extensions": [
        {
            "extension": {
                "name": "SlicerSync",
                "entities": [
                    {
                        "name": "date-range-sync",
                        "extends": {
                            "visual": {
                                "objectType": "slicer"
                            }
                        },
                        "properties": {
                            "syncGroup": "DateRangeGroup",
                            "syncedPages": [
                                "ReportSection_overview",
                                "ReportSection_detail",
                                "ReportSection_analysis"
                            ],
                            "visibleOnPages": [
                                "ReportSection_overview",
                                "ReportSection_detail"
                            ]
                        }
                    },
                    {
                        "name": "category-sync",
                        "extends": {
                            "visual": {
                                "objectType": "slicer"
                            }
                        },
                        "properties": {
                            "syncGroup": "CategoryGroup",
                            "syncedPages": [
                                "ReportSection_overview",
                                "ReportSection_detail"
                            ],
                            "visibleOnPages": [
                                "ReportSection_overview"
                            ]
                        }
                    }
                ]
            }
        }
    ]
}
```

### Sync Slicer Rules

| Property | Purpose |
|---|---|
| `syncGroup` | Group name — slicers in the same group share state |
| `syncedPages` | Pages where the filter is applied (even if slicer is hidden) |
| `visibleOnPages` | Pages where the slicer visual is shown |

**Design rules:**
- **Sync date slicers** across all pages — users expect date context to persist
- **Sync primary category slicers** (Region, Product Category) across overview + detail pages
- **Don't sync analysis-specific slicers** (e.g., "Top N" selector) — they're page-scoped
- A slicer can be synced (filter applied) but hidden on a page — useful when the slicer appears on page 1 but the filter should also affect page 2

---

## Visual Interactions

Control how visuals cross-filter each other. In PBIR format, interactions are
configured in the page.json or individual visual.json files.

### Interaction Types

| Type | Value | Behavior |
|---|---|---|
| Filter | `filter` | Source visual filters the target (removes non-matching rows) |
| Highlight | `highlight` | Source visual highlights matching data in target (dims others) |
| None | `none` | No interaction — target visual is unaffected |

### Visual Interaction JSON

```jsonc
// In visual.json — configure how this visual RECEIVES interactions
{
    "visual": {
        "visualType": "barChart",
        "interactivity": {
            "isExcludedFromInteraction": false,
            "interactions": [
                {
                    "source": "visual_slicer_region",
                    "type": "filter"
                },
                {
                    "source": "visual_pie_category",
                    "type": "highlight"
                },
                {
                    "source": "visual_card_total",
                    "type": "none"
                }
            ]
        }
    }
}
```

### Interaction Best Practices

| Guideline | Reason |
|---|---|
| Use **filter** for slicers → charts | Slicers should definitively filter data |
| Use **highlight** for chart → chart | Shows context without removing data |
| Use **none** for KPI cards as targets | KPI cards shouldn't change on click |
| Limit cross-filter chains | A→B→C→A loops cause confusion |

---

## Page-Level Filters (pageFilters)

Apply page-wide filters that affect all visuals on a page. Configured in
the page-level filter configuration:

```json
{
    "pageFilters": {
        "filters": [{
            "name": "page-filter-active-only",
            "field": {
                "Column": {
                    "Expression": { "SourceRef": { "Entity": "DimProduct" } },
                    "Property": "IsActive"
                }
            },
            "type": "Categorical",
            "filter": {
                "Version": 2,
                "From": [{ "Name": "p", "Entity": "DimProduct", "Type": 0 }],
                "Where": [{
                    "Condition": {
                        "In": {
                            "Expressions": [{
                                "Column": {
                                    "Expression": { "SourceRef": { "Source": "p" } },
                                    "Property": "IsActive"
                                }
                            }],
                            "Values": [[{ "Literal": { "Value": "true" } }]]
                        }
                    }
                }]
            }
        }]
    }
}
```
