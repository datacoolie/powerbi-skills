# Visual JSON Templates

Complete `visual.json` templates for common Power BI visual types in PBIR format.
Each template includes the required structure with `$schema`, `name`, `position`, and
the `visual` object containing `visualType`, `query`, and common formatting `objects`.

Replace placeholder values:
- `VISUAL_NAME` → type-prefixed slug (e.g., `card-total-revenue`)
- `TableName` / `ColumnName` / `MeasureName` → actual semantic model references
- Position values → actual layout coordinates

All templates use schema version `visualContainer/2.7.0`.

## Table of Contents

**Structure & Patterns:**
- [visual.json Top-Level Structure](#visual.json-top-level-structure-schema-validated)
- [Field Expression Patterns](#field-expression-patterns)
- [Accessibility Properties](#accessibility-properties)

**Data Visuals:**
- [Card](#card) · [Card (New Visual)](#card-new-visual) · [Multi Row Card](#multi-row-card) · [KPI Visual](#kpi-visual)
- [Clustered Bar Chart](#clustered-bar-chart-horizontal) · [Clustered Column Chart](#clustered-column-chart-vertical) · [Stacked Column Chart](#stacked-column-chart) · [Stacked Bar Chart](#stacked-bar-chart-horizontal)
- [Line Chart](#line-chart) · [Area Chart](#area-chart) · [Stacked Area Chart](#stacked-area-chart)
- [Line & Clustered Column Combo](#line--clustered-column-combo-chart) · [Line & Stacked Column Combo](#line--stacked-column-combo-chart)
- [Donut Chart](#donut-chart) · [Pie Chart](#pie-chart) · [Treemap](#treemap) · [Funnel Chart](#funnel-chart)
- [Waterfall Chart](#waterfall-chart) · [Ribbon Chart](#ribbon-chart) · [Scatter Chart](#scatter-chart) · [Gauge](#gauge)
- [Table (tableEx)](#table-tableex) · [Matrix (pivotTable)](#matrix-pivottable)
- [Slicer](#slicer) · [Map (Bubble)](#map-bubble-map) · [Filled Map (Choropleth)](#filled-map-choropleth)

**AI Visuals:**
- [Decomposition Tree](#decomposition-tree) · [Key Influencers](#key-influencers)

**Layout & Decorative:**
- [Shape](#shape-decorative) · [Basic Shape](#basic-shape) · [Textbox](#textbox) · [Image](#image)
- [Action Button](#action-button) · [Page Navigator](#page-navigator)

---

## visual.json Top-Level Structure (Schema-Validated)

```
visual.json
├── $schema          ← required
├── name             ← required
├── position         ← required (x, y, z, height, width, tabOrder)
├── visual/          ← required
│   ├── visualType
│   ├── query/
│   │   ├── queryState/   ← data bindings (Category, Y, Values, etc.)
│   │   └── sortDefinition/  ← ✅ CORRECT location for sort
│   ├── objects/          ← visual formatting
│   ├── visualContainerObjects/  ← container formatting (border, shadow, etc.)
│   └── drillFilterOtherVisuals
├── filterConfig/    ← ✅ CORRECT location (top-level, NOT inside visual)
│   └── filters[]
├── isHidden
└── annotations[]
```

**Critical placement rules:**

| Property | Correct path | ❌ WRONG — do not put here |
|---|---|---|
| `sortDefinition` | `visual.query.sortDefinition` | `visual.sortDefinition` |
| `filterConfig` | top-level (sibling of `visual`) | `visual.filterConfig` |
| `filters` | `filterConfig.filters` | `visual.query.filters` |
| `queryRef` | `query.queryState.<role>.projections[].queryRef` | `sortDefinition.sort[].queryRef` |

`rowLimit` is **not a valid property** anywhere in `visual.json` — do not generate it.

---

## Field Expression Patterns

Every data-bound visual needs field references in its `query.queryState`. Three patterns cover all cases:

**Column reference** (dimension field):
```json
{
  "field": {
    "Column": {
      "Expression": { "SourceRef": { "Entity": "TableName" } },
      "Property": "ColumnName"
    }
  },
  "queryRef": "TableName.ColumnName",
  "nativeQueryRef": "ColumnName"
}
```

**Measure reference** (calculated measure):
```json
{
  "field": {
    "Measure": {
      "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
      "Property": "MeasureName"
    }
  },
  "queryRef": "MeasureTable.MeasureName",
  "nativeQueryRef": "MeasureName"
}
```

**Aggregation reference** (inline aggregation of a column):
```json
{
  "field": {
    "Aggregation": {
      "Expression": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "TableName" } },
          "Property": "ColumnName"
        }
      },
      "Function": 0
    }
  },
  "queryRef": "Sum(TableName.ColumnName)",
  "nativeQueryRef": "Total ColumnName",
  "displayName": "Total ColumnName"
}
```

Aggregation `Function` values: `0` = Sum, `1` = Avg, `2` = Count, `3` = Min, `4` = Max, `5` = CountNonNull, `6` = Median, `7` = StdDev, `8` = Var.

---

## Accessibility Properties

Every non-decorative visual should include `altText` for screen readers and
a meaningful `tabOrder` for keyboard navigation. These are top-level
properties in `visual.json` (siblings of `visual`, `position`, `name`).

### Alt Text

```json
{
  "$schema": "...",
  "name": "bar-revenue-by-region",
  "position": { "..." : "..." },
  "visual": { "..." : "..." },
  "altText": "Bar chart showing revenue by region. North leads with $2.4M, followed by South at $1.8M."
}
```

**Alt text rules:**
- Describe the **visual type** and **what it shows** (chart type + key insight)
- Include the **most important data point** when possible
- For KPI cards: `"Total Revenue: $4.2M, up 12% from prior year"`
- For decorative shapes/backgrounds: use `""` (empty string) to mark as decorative
- Keep under 250 characters — screen readers truncate long descriptions
- For dynamic data, consider using a DAX measure as alt text source

### Tab Order

```json
"position": {
    "x": 10,
    "y": 100,
    "z": 8000,
    "height": 300,
    "width": 500,
    "tabOrder": 1000
}
```

**Tab order rules:**
- Assign `tabOrder` in reading order: top-left → right → down (Z-pattern)
- Use increments of 1000 (e.g., 1000, 2000, 3000) to allow insertions
- KPI cards first (1000–4000), then main chart (5000), then supporting (6000+)
- Navigation buttons: highest tab order (9000+)
- Decorative shapes: `tabOrder: -1` (skip in tab navigation)
- `tabOrder: 0` means "auto" — avoid for important visuals; assign explicit values

---

## Card

Single KPI value display. Query role: `Values`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "card-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 8000,
    "height": 96,
    "width": 140,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "card",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "labels": [
        {
          "properties": {
            "fontSize": { "expr": { "Literal": { "Value": "22D" } } },
            "bold": { "expr": { "Literal": { "Value": "true" } } },
            "color": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#333333'" } } }
              }
            },
            "labelDisplayUnits": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "categoryLabels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
            "color": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#666666'" } } }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "title": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
            "radius": { "expr": { "Literal": { "Value": "8D" } } }
          }
        }
      ],
      "dropShadow": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#000000'" } } } } },
            "position": { "expr": { "Literal": { "Value": "'Outer'" } } },
            "preset": { "expr": { "Literal": { "Value": "'BottomRight'" } } },
            "transparency": { "expr": { "Literal": { "Value": "85D" } } }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "padding": [
        {
          "properties": {
            "left": { "expr": { "Literal": { "Value": "10D" } } },
            "right": { "expr": { "Literal": { "Value": "10D" } } },
            "top": { "expr": { "Literal": { "Value": "8D" } } },
            "bottom": { "expr": { "Literal": { "Value": "8D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

For KPI cards, use `categoryLabels.show = true` to display the measure name
below the value. Pair with background shapes at lower z-order for grouped
visual sections. Use `labelDisplayUnits: 0D` for auto-formatting, or
`1000000D` for millions, `1000000000D` for billions.

---

## Multi Row Card

Multiple KPI values in a grid. Query role: `Values`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "multiRowCard-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 8000,
    "height": 150,
    "width": 400,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "multiRowCard",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Measure1"
                }
              },
              "queryRef": "MeasureTable.Measure1",
              "nativeQueryRef": "Measure1"
            },
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Measure2"
                }
              },
              "queryRef": "MeasureTable.Measure2",
              "nativeQueryRef": "Measure2"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Clustered Bar Chart (Horizontal)

Horizontal bars comparing categories. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "clusteredBarChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 450,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "clusteredBarChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ColumnName"
                }
              },
              "queryRef": "TableName.ColumnName",
              "nativeQueryRef": "ColumnName",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "valueAxis": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } },
            "gridlineShow": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "labels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "title": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "text": { "expr": { "Literal": { "Value": "'Chart Title'" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Clustered Column Chart (Vertical)

Vertical bars. Same structure as clustered bar but vertical. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "clusteredColumnChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 450,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "clusteredColumnChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ColumnName"
                }
              },
              "queryRef": "TableName.ColumnName",
              "nativeQueryRef": "ColumnName",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "valueAxis": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } },
            "gridlineShow": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "labels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "9D" } } },
            "enableBackground": { "expr": { "Literal": { "Value": "true" } } },
            "backgroundTransparency": { "expr": { "Literal": { "Value": "40D" } } }
          }
        }
      ],
      "legend": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "title": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "text": { "expr": { "Literal": { "Value": "'Chart Title'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "11D" } } },
            "fontFamily": { "expr": { "Literal": { "Value": "'Segoe UI Semibold'" } } },
            "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#333333'" } } } } }
          }
        }
      ],
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
            "radius": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ],
      "dropShadow": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#000000'" } } } } },
            "position": { "expr": { "Literal": { "Value": "'Outer'" } } },
            "preset": { "expr": { "Literal": { "Value": "'BottomRight'" } } },
            "transparency": { "expr": { "Literal": { "Value": "85D" } } }
          }
        }
      ],
      "padding": [
        {
          "properties": {
            "left": { "expr": { "Literal": { "Value": "5D" } } },
            "right": { "expr": { "Literal": { "Value": "5D" } } },
            "top": { "expr": { "Literal": { "Value": "5D" } } },
            "bottom": { "expr": { "Literal": { "Value": "5D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Stacked Column Chart

Stacked vertical bars. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "columnChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 450,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "columnChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ColumnName"
                }
              },
              "queryRef": "TableName.ColumnName",
              "nativeQueryRef": "ColumnName",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Line Chart

Trend line over time. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "lineChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 280,
    "width": 500,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "lineChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DateTable" } },
                  "Property": "Date"
                }
              },
              "queryRef": "DateTable.Date",
              "nativeQueryRef": "Date",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "lineStyles": [
        {
          "properties": {
            "strokeWidth": { "expr": { "Literal": { "Value": "2D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Area Chart

Filled area trend. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "areaChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 280,
    "width": 500,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "areaChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DateTable" } },
                  "Property": "Date"
                }
              },
              "queryRef": "DateTable.Date",
              "nativeQueryRef": "Date",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Line & Clustered Column Combo Chart

Combo chart with columns and lines. Query roles: `Category`, `Y` (columns), `Y2` (lines).
Most commonly used chart type for trend + comparison (e.g., revenue bars + growth rate line).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "lineClusteredColumnComboChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 550,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "lineClusteredColumnComboChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DateTable" } },
                  "Property": "Month"
                }
              },
              "queryRef": "DateTable.Month",
              "nativeQueryRef": "Month",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Revenue"
                }
              },
              "queryRef": "MeasureTable.Revenue",
              "nativeQueryRef": "Revenue"
            }
          ]
        },
        "Y2": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "GrowthRate"
                }
              },
              "queryRef": "MeasureTable.GrowthRate",
              "nativeQueryRef": "GrowthRate"
            }
          ]
        }
      }
    },
    "objects": {
      "valueAxis": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "gridlineShow": { "expr": { "Literal": { "Value": "true" } } },
            "gridlineStyle": { "expr": { "Literal": { "Value": "'dotted'" } } },
            "gridlineColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E8E8E8'" } } } } }
          }
        }
      ],
      "lineStyles": [
        {
          "properties": {
            "strokeWidth": { "expr": { "Literal": { "Value": "3D" } } },
            "lineStyle": { "expr": { "Literal": { "Value": "'solid'" } } },
            "showMarker": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "labels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "9D" } } },
            "enableBackground": { "expr": { "Literal": { "Value": "true" } } },
            "backgroundTransparency": { "expr": { "Literal": { "Value": "40D" } } }
          }
        }
      ],
      "legend": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "position": { "expr": { "Literal": { "Value": "'Top'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "9D" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
            "radius": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ],
      "dropShadow": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#000000'" } } } } },
            "position": { "expr": { "Literal": { "Value": "'Outer'" } } },
            "preset": { "expr": { "Literal": { "Value": "'BottomRight'" } } },
            "transparency": { "expr": { "Literal": { "Value": "85D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Donut Chart

Ring chart showing part-to-whole. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "donutChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 250,
    "width": 250,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "donutChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "CategoryColumn"
                }
              },
              "queryRef": "TableName.CategoryColumn",
              "nativeQueryRef": "CategoryColumn",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "legend": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "position": { "expr": { "Literal": { "Value": "'Bottom'" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Pie Chart

Same structure as donut. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "pieChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 250,
    "width": 250,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "pieChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "CategoryColumn"
                }
              },
              "queryRef": "TableName.CategoryColumn",
              "nativeQueryRef": "CategoryColumn",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Slicer

Filter control. Query role: `Values`. Uses `slicer` within `objects` for configuration.
Default mode is Dropdown — this saves space and works best for most scenarios.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "slicer-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 9000,
    "height": 50,
    "width": 200,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ColumnName"
                }
              },
              "queryRef": "TableName.ColumnName",
              "nativeQueryRef": "ColumnName"
            }
          ]
        }
      }
    },
    "objects": {
      "data": [
        {
          "properties": {
            "mode": { "expr": { "Literal": { "Value": "'Dropdown'" } } }
          }
        }
      ],
      "header": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#333333'" } } }
              }
            },
            "textSize": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ],
      "items": [
        {
          "properties": {
            "fontColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#333333'" } } }
              }
            },
            "textSize": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "visualHeader": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ]
    },
    "syncGroup": {
      "groupName": "sync-ColumnName",
      "fieldChanges": true,
      "filterChanges": true
    },
    "drillFilterOtherVisuals": true
  }
}
```

**syncGroup**: Include `syncGroup` to sync slicer selections across pages.
Slicers with the same `groupName` stay in sync. Set to the same value on
all pages. Omit `syncGroup` if the slicer is page-specific only.

### Slicer Modes

Change the `data.mode` property:
- `"'Basic'"` → Dropdown list (default)
- `"'Dropdown'"` → Dropdown
- `"'Between'"` → Range slider (for dates/numbers)
- `"'Before'"` → Before date
- `"'After'"` → After date
- `"'List'"` → List with checkboxes

### Date Range Slicer

For date slicers, use `Between` mode and reference a date column:

```json
"objects": {
  "data": [
    {
      "properties": {
        "mode": { "expr": { "Literal": { "Value": "'Between'" } } }
      }
    }
  ],
  "general": [
    {
      "properties": {
        "orientation": { "expr": { "Literal": { "Value": "0D" } } }
      }
    }
  ]
}
```

---

## Table (tableEx)

Flat table with columns. Query role: `Values` (each column is a projection).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "tableEx-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 4000,
    "height": 250,
    "width": 600,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "tableEx",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "Column1"
                }
              },
              "queryRef": "TableName.Column1",
              "nativeQueryRef": "Column1"
            },
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "Column2"
                }
              },
              "queryRef": "TableName.Column2",
              "nativeQueryRef": "Column2"
            },
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "total": [
        {
          "properties": {
            "totals": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Matrix (pivotTable)

Cross-tab / pivot table. Query roles: `Rows`, `Columns`, `Values`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "pivotTable-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 4000,
    "height": 300,
    "width": 650,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "pivotTable",
    "query": {
      "queryState": {
        "Rows": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "RowCategory"
                }
              },
              "queryRef": "TableName.RowCategory",
              "nativeQueryRef": "RowCategory",
              "active": true
            }
          ]
        },
        "Columns": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ColumnCategory"
                }
              },
              "queryRef": "TableName.ColumnCategory",
              "nativeQueryRef": "ColumnCategory",
              "active": true
            }
          ]
        },
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "objects": {
      "total": [
        {
          "properties": {
            "totals": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "subTotals": [
        {
          "properties": {
            "rowSubtotals": { "expr": { "Literal": { "Value": "true" } } },
            "columnSubtotals": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Treemap

Hierarchical area chart. Query roles: `Group`, `Values`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "treemap-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 280,
    "width": 350,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "treemap",
    "query": {
      "queryState": {
        "Group": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "CategoryColumn"
                }
              },
              "queryRef": "TableName.CategoryColumn",
              "nativeQueryRef": "CategoryColumn",
              "active": true
            }
          ]
        },
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Waterfall Chart

Shows incremental positive/negative contributions. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "waterfallChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 280,
    "width": 500,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "waterfallChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "StepName"
                }
              },
              "queryRef": "TableName.StepName",
              "nativeQueryRef": "StepName",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Funnel Chart

Narrowing stages. Query roles: `Category`, `Y`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "funnel-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 280,
    "width": 300,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "funnel",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "StageName"
                }
              },
              "queryRef": "TableName.StageName",
              "nativeQueryRef": "StageName",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "MeasureName"
                }
              },
              "queryRef": "MeasureTable.MeasureName",
              "nativeQueryRef": "MeasureName"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Gauge

Dial showing progress toward a target. Query roles: `Y`, `TargetValue`, `MinValue`, `MaxValue`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "gauge-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 200,
    "width": 200,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "gauge",
    "query": {
      "queryState": {
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "ActualValue"
                }
              },
              "queryRef": "MeasureTable.ActualValue",
              "nativeQueryRef": "ActualValue"
            }
          ]
        },
        "TargetValue": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "TargetValue"
                }
              },
              "queryRef": "MeasureTable.TargetValue",
              "nativeQueryRef": "TargetValue"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Shape (Decorative)

Background rectangle, line, or decorative element. No query — purely visual.
Use shapes for visual grouping, header backgrounds, and section dividers.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "shape-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 0,
    "height": 936,
    "width": 1664,
    "tabOrder": -1
  },
  "visual": {
    "visualType": "shape",
    "objects": {
      "line": [
        {
          "properties": {
            "lineColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } }
              }
            },
            "show": { "expr": { "Literal": { "Value": "false" } } },
            "roundEdge": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ],
      "fill": [
        {
          "properties": {
            "fillColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#F2F2F2'" } } }
              }
            },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "dropShadow": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#000000'" } } } } },
            "position": { "expr": { "Literal": { "Value": "'Outer'" } } },
            "preset": { "expr": { "Literal": { "Value": "'BottomRight'" } } },
            "transparency": { "expr": { "Literal": { "Value": "85D" } } }
          }
        }
      ]
    }
  }
}
```

For **rounded rectangle** backgrounds: set `line.roundEdge` to `10D`-`20D`.
For **section grouping**: place multiple overlapping shapes at z:100-500 with
different fill colors to create visual zones behind content visuals.

---

## Textbox

Static rich text content. No query.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "textbox-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 9000,
    "height": 40,
    "width": 300,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "textbox",
    "objects": {
      "general": [
        {
          "properties": {
            "paragraphs": [
              {
                "textRuns": [
                  {
                    "value": "Your text here",
                    "textStyle": {
                      "fontFamily": "'Segoe UI'",
                      "fontSize": "'14pt'",
                      "fontWeight": "'bold'",
                      "fontColor": "'#333333'"
                    }
                  }
                ]
              }
            ]
          }
        }
      ]
    }
  }
}
```

---

## Image

Static image visual. References an image from RegisteredResources.
Can also be used as a navigation icon with `visualLink` for page navigation.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "image-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 9000,
    "height": 60,
    "width": 60,
    "tabOrder": -1
  },
  "visual": {
    "visualType": "image",
    "objects": {
      "general": [
        {
          "properties": {
            "imageUrl": {
              "expr": {
                "ResourcePackageItem": {
                  "PackageName": "RegisteredResources",
                  "PackageType": "RegisteredResources",
                  "ItemName": "image-filename.png"
                }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    }
  }
}
```

### Image with Page Navigation

Use `visualLink` in `visualContainerObjects` to make an image act as a
clickable navigation icon to another page:

```json
{
  "name": "image-nav-icon",
  "position": { "x": 10, "y": 200, "z": 12000, "height": 40, "width": 40, "tabOrder": 0 },
  "visual": {
    "visualType": "image",
    "objects": {
      "general": [
        {
          "properties": {
            "imageUrl": {
              "expr": {
                "ResourcePackageItem": {
                  "PackageName": "RegisteredResources",
                  "PackageType": "RegisteredResources",
                  "ItemName": "nav-icon.png"
                }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "visualLink": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
            "navigationSection": { "expr": { "Literal": { "Value": "'target-page-name'" } } }
          }
        }
      ],
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    }
  }
}
```

---

## Action Button

Navigation or bookmark button. No data query. Supports page navigation,
bookmark activation, back navigation, and web URL actions.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "actionButton-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 10000,
    "height": 40,
    "width": 120,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "text": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "text": { "expr": { "Literal": { "Value": "'Button Label'" } } },
            "fontFamily": { "expr": { "Literal": { "Value": "'Segoe UI'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
            "fontColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
              }
            }
          }
        }
      ],
      "fill": [
        {
          "properties": {
            "fillColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } }
              }
            }
          }
        }
      ],
      "outline": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "action": [
        {
          "properties": {
            "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
            "destination": { "expr": { "Literal": { "Value": "'target-page-name'" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    }
  }
}
```

### Action Types

Change the `action.type` and related properties:

- **Page Navigation**: `"type": "'PageNavigation'"`, `"destination": "'page-name'"`
- **Bookmark**: `"type": "'Bookmark'"`, `"bookmark": "'bookmark-name'"`
- **Back**: `"type": "'Back'"` (for drillthrough return)
- **Web URL**: `"type": "'WebUrl'"`, `"url": "'https://...'"` (only for external links)

### Tab-Style Button (Flat)

For tab-bar navigation, use flat styling with no fill and an accent underline:

```json
{
  "name": "actionButton-tab-sales",
  "position": { "x": 13, "y": 58, "z": 10000, "height": 32, "width": 148, "tabOrder": 0 },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "text": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "text": { "expr": { "Literal": { "Value": "'Sales'" } } },
            "fontFamily": { "expr": { "Literal": { "Value": "'Segoe UI'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
            "fontBold": { "expr": { "Literal": { "Value": "true" } } },
            "fontColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } }
              }
            }
          }
        }
      ],
      "fill": [
        {
          "properties": {
            "fillColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
              }
            },
            "transparency": { "expr": { "Literal": { "Value": "100D" } } }
          }
        }
      ],
      "outline": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ],
      "action": [
        {
          "properties": {
            "type": { "expr": { "Literal": { "Value": "'Bookmark'" } } },
            "bookmark": { "expr": { "Literal": { "Value": "'tab-sales'" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    }
  }
}
```

---

## Scatter Chart

XY plot with optional size bubble. Query roles: `Category`, `X`, `Y`, `Size`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "scatterChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 400,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "scatterChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ItemName"
                }
              },
              "queryRef": "TableName.ItemName",
              "nativeQueryRef": "ItemName",
              "active": true
            }
          ]
        },
        "X": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "XMeasure"
                }
              },
              "queryRef": "MeasureTable.XMeasure",
              "nativeQueryRef": "XMeasure"
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "YMeasure"
                }
              },
              "queryRef": "MeasureTable.YMeasure",
              "nativeQueryRef": "YMeasure"
            }
          ]
        },
        "Size": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "SizeMeasure"
                }
              },
              "queryRef": "MeasureTable.SizeMeasure",
              "nativeQueryRef": "SizeMeasure"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Line & Stacked Column Combo Chart

Columns are stacked (part-to-whole) with a line overlay. Query roles: `Category`, `Y` (stacked columns), `Y2` (lines), `Series` (stack breakdown).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "lineStackedColumnComboChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 550,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "lineStackedColumnComboChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DateTable" } },
                  "Property": "Month"
                }
              },
              "queryRef": "DateTable.Month",
              "nativeQueryRef": "Month",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Revenue"
                }
              },
              "queryRef": "MeasureTable.Revenue",
              "nativeQueryRef": "Revenue"
            }
          ]
        },
        "Y2": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "GrowthRate"
                }
              },
              "queryRef": "MeasureTable.GrowthRate",
              "nativeQueryRef": "GrowthRate"
            }
          ]
        },
        "Series": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "CategoryColumn"
                }
              },
              "queryRef": "TableName.CategoryColumn",
              "nativeQueryRef": "CategoryColumn",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "lineStyles": [
        {
          "properties": {
            "strokeWidth": { "expr": { "Literal": { "Value": "3D" } } },
            "lineStyle": { "expr": { "Literal": { "Value": "'solid'" } } }
          }
        }
      ],
      "labels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
            "radius": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ],
      "dropShadow": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#000000'" } } } } },
            "position": { "expr": { "Literal": { "Value": "'Outer'" } } },
            "preset": { "expr": { "Literal": { "Value": "'BottomRight'" } } },
            "transparency": { "expr": { "Literal": { "Value": "85D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Ribbon Chart

Ranking chart showing how categories change rank over time. Query roles: `Category`, `Y`, `Series`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "ribbonChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 350,
    "width": 550,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "ribbonChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DateTable" } },
                  "Property": "Month"
                }
              },
              "queryRef": "DateTable.Month",
              "nativeQueryRef": "Month",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Revenue"
                }
              },
              "queryRef": "MeasureTable.Revenue",
              "nativeQueryRef": "Revenue"
            }
          ]
        },
        "Series": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "ProductCategory"
                }
              },
              "queryRef": "TableName.ProductCategory",
              "nativeQueryRef": "ProductCategory",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "labels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "9D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Stacked Area Chart

Area chart showing part-to-whole composition over time. Query roles: `Category`, `Y`, `Series`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "stackedAreaChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 500,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "stackedAreaChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DateTable" } },
                  "Property": "Month"
                }
              },
              "queryRef": "DateTable.Month",
              "nativeQueryRef": "Month",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Amount"
                }
              },
              "queryRef": "MeasureTable.Amount",
              "nativeQueryRef": "Amount"
            }
          ]
        },
        "Series": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "Region"
                }
              },
              "queryRef": "TableName.Region",
              "nativeQueryRef": "Region",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "lineStyles": [
        {
          "properties": {
            "strokeWidth": { "expr": { "Literal": { "Value": "2D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Stacked Bar Chart (Horizontal)

Horizontal stacked bars for part-to-whole by category. Query roles: `Category`, `Y`, `Series`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "barChart-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 300,
    "width": 500,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "barChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "Department"
                }
              },
              "queryRef": "TableName.Department",
              "nativeQueryRef": "Department",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Amount"
                }
              },
              "queryRef": "MeasureTable.Amount",
              "nativeQueryRef": "Amount"
            }
          ]
        },
        "Series": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "Subcategory"
                }
              },
              "queryRef": "TableName.Subcategory",
              "nativeQueryRef": "Subcategory",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "legend": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "position": { "expr": { "Literal": { "Value": "'Bottom'" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Page Navigator

Built-in visual that renders page tabs for navigation between report pages.
No query — automatically shows all visible pages.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "pageNavigator-nav",
  "position": {
    "x": 0,
    "y": 900,
    "z": 15000,
    "height": 36,
    "width": 1664,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "pageNavigator",
    "objects": {
      "navigation": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "pageTabs": [
        {
          "properties": {
            "fontFamily": { "expr": { "Literal": { "Value": "'Segoe UI'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
            "fontColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#605E5C'" } } }
              }
            },
            "fontBold": { "expr": { "Literal": { "Value": "false" } } },
            "tabFill": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
              }
            },
            "selectedTabFill": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } }
              }
            },
            "selectedFontColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
              }
            },
            "selectedFontBold": { "expr": { "Literal": { "Value": "true" } } },
            "hoverFill": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#E8E8E8'" } } }
              }
            },
            "tabAlignment": { "expr": { "Literal": { "Value": "'Left'" } } },
            "verticalAlignment": { "expr": { "Literal": { "Value": "'Middle'" } } },
            "tabPaddingLeft": { "expr": { "Literal": { "Value": "12D" } } },
            "tabPaddingRight": { "expr": { "Literal": { "Value": "12D" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "false" } } }
          }
        }
      ]
    }
  }
}
```

---

## Map (Bubble Map)

Geographic bubble map. Query roles: `Category` (location), `Size` (bubble size), `Color` (optional gradient).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "map-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 400,
    "width": 600,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "map",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "City"
                }
              },
              "queryRef": "TableName.City",
              "nativeQueryRef": "City",
              "active": true
            }
          ]
        },
        "Size": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Revenue"
                }
              },
              "queryRef": "MeasureTable.Revenue",
              "nativeQueryRef": "Revenue"
            }
          ]
        }
      }
    },
    "objects": {
      "categoryLabels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "9D" } } }
          }
        }
      ],
      "bubbles": [
        {
          "properties": {
            "bubbleSize": { "expr": { "Literal": { "Value": "50D" } } }
          }
        }
      ],
      "mapControls": [
        {
          "properties": {
            "autoZoom": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "mapStyles": [
        {
          "properties": {
            "theme": { "expr": { "Literal": { "Value": "'grayscale'" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Filled Map (Choropleth)

Geographic choropleth showing color-shaded regions. Query roles: `Category` (location), `Y` (saturation value).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "filledMap-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 5000,
    "height": 400,
    "width": 600,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "filledMap",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "TableName" } },
                  "Property": "Country"
                }
              },
              "queryRef": "TableName.Country",
              "nativeQueryRef": "Country",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "Revenue"
                }
              },
              "queryRef": "MeasureTable.Revenue",
              "nativeQueryRef": "Revenue"
            }
          ]
        }
      }
    },
    "objects": {
      "legend": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "position": { "expr": { "Literal": { "Value": "'BottomCenter'" } } }
          }
        }
      ],
      "mapControls": [
        {
          "properties": {
            "autoZoom": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "mapStyles": [
        {
          "properties": {
            "theme": { "expr": { "Literal": { "Value": "'grayscale'" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Card (New Visual)

The new card visual (`cardVisual`) — supports multiple values and enhanced formatting.
Query roles: `Data`, `Detail`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "cardVisual-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 8000,
    "height": 96,
    "width": 200,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "cardVisual",
    "query": {
      "queryState": {
        "Data": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
                  "Property": "TotalRevenue"
                }
              },
              "queryRef": "MeasureTable.TotalRevenue",
              "nativeQueryRef": "TotalRevenue"
            }
          ]
        }
      }
    },
    "objects": {
      "cards": [
        {
          "properties": {
            "fontSize": { "expr": { "Literal": { "Value": "28D" } } },
            "bold": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "categoryLabels": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
            "radius": { "expr": { "Literal": { "Value": "8D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## Basic Shape

Geometric shape element (circle, triangle, arrow, etc.). No query — decorative only.
Use `shapeType` to select shape: `"'rectangle'"`, `"'oval'"`, `"'triangle'"`, `"'arrow'"`, `"'pentagon'"`, `"'hexagon'"`, `"'star'"`, etc.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "basicShape-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 500,
    "height": 80,
    "width": 80,
    "tabOrder": -1
  },
  "visual": {
    "visualType": "basicShape",
    "objects": {
      "line": [
        {
          "properties": {
            "lineColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } }
              }
            },
            "weight": { "expr": { "Literal": { "Value": "2D" } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } },
            "roundEdge": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ],
      "fill": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fillColor": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } }
              }
            },
            "transparency": { "expr": { "Literal": { "Value": "20D" } } }
          }
        }
      ],
      "rotation": [
        {
          "properties": {
            "angle": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ]
    }
  }
}
```

---

## KPI Visual

`visualType: "kpi"`

Single-metric KPI with trend indicator and target comparison.
Best on executive dashboards where a number + directional trend is needed.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "VISUAL_NAME",
  "position": {
    "x": 0, "y": 0, "z": 0,
    "height": 180, "width": 300,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "kpi",
    "query": {
      "queryState": {
        "Indicator": {
          "projections": [
            {
              "field": {
                "Measure": { "Expression": { "SourceRef": { "Entity": "TableName" } }, "Property": "ActualMeasure" }
              },
              "queryRef": "TableName.ActualMeasure",
              "active": true
            }
          ]
        },
        "TrendLine": {
          "projections": [
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Date" } }, "Property": "Date" }
              },
              "queryRef": "Date.Date",
              "active": true
            }
          ]
        },
        "Goal": {
          "projections": [
            {
              "field": {
                "Measure": { "Expression": { "SourceRef": { "Entity": "TableName" } }, "Property": "TargetMeasure" }
              },
              "queryRef": "TableName.TargetMeasure",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "indicator": [
        {
          "properties": {
            "indicatorDisplayUnits": { "expr": { "Literal": { "Value": "0D" } } },
            "fontSize": { "expr": { "Literal": { "Value": "27D" } } }
          }
        }
      ],
      "trendline": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "goal": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "fontSize": { "expr": { "Literal": { "Value": "12D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

**Query roles:** `Indicator` (main measure), `TrendLine` (date axis for sparkline), `Goal` (target measure).

---

## Decomposition Tree

`visualType: "decompositionTreeVisual"`

AI-powered visual that breaks down a measure across multiple dimensions.
Users expand branches interactively. Provide 3-6 ExplainBy dimensions.
Size large (min 500×800) due to branching layout.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "VISUAL_NAME",
  "position": {
    "x": 0, "y": 0, "z": 0,
    "height": 500, "width": 800,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "decompositionTreeVisual",
    "query": {
      "queryState": {
        "Analyze": {
          "projections": [
            {
              "field": {
                "Measure": { "Expression": { "SourceRef": { "Entity": "TableName" } }, "Property": "MeasureName" }
              },
              "queryRef": "TableName.MeasureName",
              "active": true
            }
          ]
        },
        "ExplainBy": {
          "projections": [
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Product" } }, "Property": "Category" }
              },
              "queryRef": "Product.Category",
              "active": true
            },
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Geography" } }, "Property": "Region" }
              },
              "queryRef": "Geography.Region",
              "active": true
            },
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Date" } }, "Property": "Year" }
              },
              "queryRef": "Date.Year",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "tree": [
        {
          "properties": {
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } }
          }
        }
      ],
      "dataBar": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } }
              }
            }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

**Query roles:** `Analyze` (measure to decompose), `ExplainBy` (dimensions to expand into — order = priority).

---

## Key Influencers

`visualType: "keyInfluencersVisual"`

AI visual analyzing which factors most influence a metric. Has two tabs:
Key Influencers and Top Segments. Provide 4-8 ExplainBy fields.
Size large (min 500×800).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "VISUAL_NAME",
  "position": {
    "x": 0, "y": 0, "z": 0,
    "height": 500, "width": 800,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "keyInfluencersVisual",
    "query": {
      "queryState": {
        "Analyze": {
          "projections": [
            {
              "field": {
                "Measure": { "Expression": { "SourceRef": { "Entity": "TableName" } }, "Property": "MetricToAnalyze" }
              },
              "queryRef": "TableName.MetricToAnalyze",
              "active": true
            }
          ]
        },
        "ExplainBy": {
          "projections": [
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Customer" } }, "Property": "Segment" }
              },
              "queryRef": "Customer.Segment",
              "active": true
            },
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Product" } }, "Property": "Category" }
              },
              "queryRef": "Product.Category",
              "active": true
            },
            {
              "field": {
                "Column": { "Expression": { "SourceRef": { "Entity": "Geography" } }, "Property": "Region" }
              },
              "queryRef": "Geography.Region",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {
      "influencers": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

**Query roles:** `Analyze` (metric/column to explain), `ExplainBy` (candidate influencer columns).
