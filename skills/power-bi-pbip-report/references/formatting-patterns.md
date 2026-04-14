# Advanced Formatting Patterns

Detailed JSON formatting patterns derived from real-world reference reports.
Use these to produce polished, professional-looking visuals.

For basic formatting (visual container objects, color expressions, literal values),
see the main SKILL.md.

---

## Rounded Corners (Border Radius)

Apply rounded corners to shapes, visual containers, and cards for a modern aesthetic:
```json
"border": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
    "radius": { "expr": { "Literal": { "Value": "8D" } } },
    "width": { "expr": { "Literal": { "Value": "1D" } } }
  }
}]
```
Common values: `8D` (subtle), `15D` (medium), `30D` (pill-shaped for shapes/tiles).

## Drop Shadow

Add depth with shadows on key visuals — especially KPI cards and primary charts:
```json
"visualContainerObjects": {
  "dropShadow": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#000000'" } } } } },
      "position": { "expr": { "Literal": { "Value": "'Outer'" } } },
      "preset": { "expr": { "Literal": { "Value": "'BottomRight'" } } }
    }
  }]
}
```

## Conditional Data Point Colors via Selectors

Color specific data points based on category values. Uses `scopeId.Comparison` in the
`selector.data` array to target individual bars/slices:
```json
"dataPoint": [
  { "properties": { "fill": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 6, "Percent": 0 } } } } } } },
  {
    "properties": {
      "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#DE6203'" } } } } }
    },
    "selector": {
      "data": [{
        "scopeId": {
          "Comparison": {
            "ComparisonKind": 0,
            "Left": { "Column": { "Expression": { "SourceRef": { "Entity": "TableName" } }, "Property": "ColumnName" } },
            "Right": { "Literal": { "Value": "'TargetValue'" } }
          }
        }
      }]
    }
  }
]
```
`ComparisonKind`: `0` = Equals. First entry (no selector) sets the default color; subsequent
entries with selectors override specific data points.

## Series-Specific Colors via Metadata Selector

Color individual measures in multi-measure charts (e.g., combo charts with 2 Y-axis measures):
```json
"dataPoint": [
  {
    "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } } } } },
    "selector": { "metadata": "MeasureTable.Measure1" }
  },
  {
    "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FF6B35'" } } } } } },
    "selector": { "metadata": "MeasureTable.Measure2" }
  }
]
```

## Data Label Backgrounds

Add semi-transparent backgrounds behind data labels for contrast against chart elements:
```json
"labels": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "enableBackground": { "expr": { "Literal": { "Value": "true" } } },
    "backgroundColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } },
    "backgroundTransparency": { "expr": { "Literal": { "Value": "30L" } } },
    "labelDisplayUnits": { "expr": { "Literal": { "Value": "1000D" } } },
    "labelPrecision": { "expr": { "Literal": { "Value": "1L" } } }
  }
}]
```
`labelDisplayUnits`: `1D` = none, `1000D` = thousands, `1000000D` = millions, `1000000000D` = billions.

## Axis Formatting (Clean, Minimal)

Remove axis clutter following Storytelling with Data principles:
```json
"categoryAxis": [{
  "properties": {
    "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } },
    "fontSize": { "expr": { "Literal": { "Value": "9D" } } },
    "labelColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0 } } } } },
    "concatenateLabels": { "expr": { "Literal": { "Value": "true" } } },
    "preferredCategoryWidth": { "expr": { "Literal": { "Value": "50D" } } }
  }
}],
"valueAxis": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "false" } } },
    "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } },
    "gridlineStyle": { "expr": { "Literal": { "Value": "'dotted'" } } }
  }
}]
```
**Default rule**: Hide value axis and show data labels directly on bars instead. This
follows the clutter reduction principle — let data speak without gridlines.

## Legend Formatting (Compact)

```json
"legend": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "showTitle": { "expr": { "Literal": { "Value": "false" } } },
    "position": { "expr": { "Literal": { "Value": "'Top'" } } },
    "fontSize": { "expr": { "Literal": { "Value": "8D" } } },
    "labelColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0 } } } } }
  }
}]
```
Prefer hiding legend entirely and using direct labels when feasible.

## Visual Header (Hide for Cleaner Look)

Remove the hover "..." menu header on visuals that are primarily decorative or static:
```json
"visualContainerObjects": {
  "visualHeader": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "false" } } }
    }
  }]
}
```

## Padding (Custom Spacing Inside Visuals)

```json
"visualContainerObjects": {
  "padding": [{
    "properties": {
      "top": { "expr": { "Literal": { "Value": "6D" } } },
      "left": { "expr": { "Literal": { "Value": "8D" } } },
      "right": { "expr": { "Literal": { "Value": "8D" } } },
      "bottom": { "expr": { "Literal": { "Value": "6D" } } }
    }
  }]
}
```

## Visual-Level Filters (filterConfig)

Apply filters directly on a visual to exclude nulls, specific values, or set ranges
without affecting other visuals on the page.

`filterConfig` is a **top-level property** of `visual.json` — it is a sibling of `visual`,
`position`, and `name`. It is **not** nested inside `visual`:

```json
{
  "$schema": "...",
  "name": "...",
  "position": { ... },
  "visual": { ... },
  "filterConfig": {
  "filters": [{
    "name": "filter-exclude-nulls",
    "field": { "Column": { "Expression": { "SourceRef": { "Entity": "TableName" } }, "Property": "ColumnName" } },
    "type": "Categorical",
    "filter": {
      "Version": 2,
      "From": [{ "Name": "t", "Entity": "TableName", "Type": 0 }],
      "Where": [{
        "Condition": {
          "Not": {
            "Expression": {
              "In": {
                "Expressions": [{ "Column": { "Expression": { "SourceRef": { "Source": "t" } }, "Property": "ColumnName" } }],
                "Values": [[{ "Literal": { "Value": "null" } }]]
              }
            }
          }
        }
      }]
    },
    "objects": {
      "general": [{ "properties": { "isInvertedSelectionMode": { "expr": { "Literal": { "Value": "true" } } } } }]
    }
  }]
  }
}
```
`isInvertedSelectionMode: true` means "exclude these values" (NOT IN logic).

> ❌ **Common errors**: `visual.filterConfig` (wrong — must be top-level); `visual.query.filters` (invalid — `filters` lives in `filterConfig.filters`, not in the query).

## Sort Definition

Control visual sort order. Place `sortDefinition` inside `visual.query` — **not** directly inside `visual`:

```json
"visual": {
  "visualType": "barChart",
  "query": {
    "queryState": { ... },
    "sortDefinition": {
      "sort": [{
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
            "Property": "MeasureName"
          }
        },
        "direction": "Descending"
      }],
      "isDefaultSort": true
    }
  }
}
```

> ❌ **Common errors**: `visual.sortDefinition` (wrong level — must be `visual.query.sortDefinition`);  
> `sort[0].queryRef` (invalid — use `sort[0].field`); `rowLimit` (not a valid property — do not generate it).

**Default rule**: Always sort bar/column charts by value descending unless the category
has a natural order (time, sequential stages).

## TOP N Filter (filterConfig)

Limit a visual to the Top N (or Bottom N) items by a measure or aggregated column.
This uses `type: "TopN"` in `filterConfig` — a subquery selects the ranked dimension
members, and the outer filter keeps only rows whose field value is in that subquery result.

### Variant A — Top N by a Measure

Use when the ranking column is an explicit DAX measure (e.g., `[Total Sales]`, `[Revenue]`):

```json
"filterConfig": {
  "filters": [
    {
      "name": "topn-filter-by-measure",
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
                  "Select": [
                    {
                      "Column": {
                        "Expression": { "SourceRef": { "Source": "d" } },
                        "Property": "ProductName"
                      },
                      "Name": "field"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": { "SourceRef": { "Source": "m" } },
                          "Property": "Total Sales"
                        }
                      }
                    }
                  ],
                  "Top": 10
                }
              }
            },
            "Type": 2
          },
          { "Name": "d", "Entity": "DimProduct", "Type": 0 }
        ],
        "Where": [
          {
            "Condition": {
              "In": {
                "Expressions": [
                  {
                    "Column": {
                      "Expression": { "SourceRef": { "Source": "d" } },
                      "Property": "ProductName"
                    }
                  }
                ],
                "Table": { "SourceRef": { "Source": "subquery" } }
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Key properties:**
- `Direction: 2` = Descending → **Top N** (highest values). Use `Direction: 1` for **Bottom N** (lowest values).
- `Top: 10` = the N count — change to any integer.
- The `From` array in the subquery must include `MeasureTable` when ranking by a DAX measure.
- `"Name": "field"` in `Select` is a required alias — keep it exactly as `"field"`.

### Variant B — Top N by Aggregated Column

Use when ranking by an aggregation of a raw column (no explicit measure).
Replace the `Measure` expression with an `Aggregation`:

```json
"OrderBy": [
  {
    "Direction": 2,
    "Expression": {
      "Aggregation": {
        "Expression": {
          "Column": {
            "Expression": { "SourceRef": { "Source": "d" } },
            "Property": "SalesAmount"
          }
        },
        "Function": 0
      }
    }
  }
]
```

`Aggregation.Function` values: `0` = Sum, `1` = Count, `2` = Min, `3` = Max, `4` = Average, `5` = DistinctCount.
Note: When using Aggregation (Variant B), `MeasureTable` is **not** needed in the `From` array — only the dimension table.

### Always pair with Sort Definition

A TOP N filter limits the chart to N items but does not sort them. Always add `sortDefinition`
inside `visual.query` so bars render largest-first:

```json
"visual": {
  "visualType": "barChart",
  "query": {
    "queryState": { ... },
    "sortDefinition": {
      "sort": [{
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
            "Property": "Total Sales"
          }
        },
        "direction": "Descending"
      }],
      "isDefaultSort": true
    }
  }
}
```

---

## Drillthrough Page Configuration

A drillthrough page accepts filter context from other pages. Configure via
the page.json `type` property and visual-level filter config.

### Page-Level Setup (page.json)

Set the page `type` to `2` (drillthrough) in the page definition:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
  "name": "ReportSection_drillthrough_product",
  "displayName": "Product Detail",
  "displayOption": "FitToPage",
  "type": 2,
  "height": 720,
  "width": 1280
}
```

Page type values: `0` = Normal, `1` = Tooltip, `2` = Drillthrough.

### Drillthrough Filter Field

The drillthrough target field is configured as a `filterConfig` on a hidden
visual or directly in the page's filter configuration. The filter captures
the selected dimension value from the source page:

```json
"filterConfig": {
  "filters": [{
    "name": "drillthrough-product-filter",
    "field": {
      "Column": {
        "Expression": { "SourceRef": { "Entity": "DimProduct" } },
        "Property": "ProductName"
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
                "Property": "ProductName"
              }
            }],
            "Values": []
          }
        }
      }]
    },
    "howCreated": "Drillthrough"
  }]
}
```

### Back Button (Required)

Every drillthrough page must include a back button. Use an actionButton with
`type: 'Back'`:

```json
{
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "icon": [{ "properties": {
        "shapeType": { "expr": { "Literal": { "Value": "'LeftArrow'" } } }
      }}],
      "action": [{ "properties": {
        "type": { "expr": { "Literal": { "Value": "'Back'" } } }
      }}],
      "outline": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "false" } } }
      }}]
    }
  },
  "position": { "x": 16, "y": 8, "z": 20000, "width": 48, "height": 48 }
}
```

---

## Conditional Formatting Rules

### Color Scale (Gradient Fill)

Apply a continuous color gradient based on a measure value. This uses
`fillRule` with `linearGradient2` (two-stop) or `linearGradient3` (three-stop).

**Two-stop gradient (min → max):**

```json
"values": [{
  "properties": {
    "backColor": {
      "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } }
    }
  }
},
{
  "properties": {
    "backColor": {
      "fillRule": {
        "linearGradient2": {
          "min": {
            "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
          },
          "max": {
            "color": { "expr": { "Literal": { "Value": "'#118DFF'" } } }
          },
          "nullColoringStrategy": { "strategy": { "expr": { "Literal": { "Value": "'asZero'" } } } }
        },
        "inputProperty": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
            "Property": "MeasureName"
          }
        }
      }
    }
  },
  "selector": { "metadata": "MeasureTable.MeasureName" }
}]
```

**Three-stop gradient (min → mid → max):**

```json
"backColor": {
  "fillRule": {
    "linearGradient3": {
      "min": {
        "color": { "expr": { "Literal": { "Value": "'#FF0000'" } } },
        "value": { "expr": { "Literal": { "Value": "0D" } } }
      },
      "mid": {
        "color": { "expr": { "Literal": { "Value": "'#FFFF00'" } } },
        "value": { "expr": { "Literal": { "Value": "50D" } } }
      },
      "max": {
        "color": { "expr": { "Literal": { "Value": "'#00B050'" } } },
        "value": { "expr": { "Literal": { "Value": "100D" } } }
      },
      "nullColoringStrategy": { "strategy": { "expr": { "Literal": { "Value": "'asZero'" } } } }
    },
    "inputProperty": {
      "Measure": {
        "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
        "Property": "Achievement %"
      }
    }
  }
}
```

### Rules-Based Conditional Formatting

Apply discrete colors based on value ranges. Use the `conditionalFormatting`
approach with rules in the visual objects:

```json
"values": [{
  "properties": {
    "fontColor": {
      "solid": { "color": { "expr": { "Literal": { "Value": "'#333333'" } } } }
    }
  }
},
{
  "properties": {
    "fontColor": {
      "fillRule": {
        "linearGradient2": {
          "min": {
            "color": { "expr": { "Literal": { "Value": "'#FF0000'" } } },
            "value": { "expr": { "Literal": { "Value": "0D" } } }
          },
          "max": {
            "color": { "expr": { "Literal": { "Value": "'#00B050'" } } },
            "value": { "expr": { "Literal": { "Value": "1D" } } }
          }
        },
        "inputProperty": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Sales" } },
            "Property": "Growth %"
          }
        }
      }
    }
  },
  "selector": { "metadata": "Sales.Growth %" }
}]
```

### Icon Sets via DAX Measures

Power BI doesn't natively support icon sets in PBIR JSON. Use a DAX
measure with Unicode characters or emoji as a workaround:

```dax
Status Icon =
VAR _achievement = [Achievement %]
RETURN
    SWITCH(
        TRUE(),
        _achievement >= 1.0, "🟢",     // ● Green circle
        _achievement >= 0.8, "🟡",     // ● Yellow circle
        "🔴"                            // ● Red circle
    )
```

### Data Bars via DAX

Similarly, approximate data bars with a repeat-character measure:

```dax
Data Bar =
VAR _pct = DIVIDE([Revenue], [Max Revenue])
VAR _bars = REPT("█", ROUND(_pct * 20, 0))
RETURN _bars
```

---

## Quick Reference — Formatting Patterns

| Pattern | Section | Key Property |
|---|---|---|
| Rounded corners | Border Radius | `border.radius` |
| Drop shadow | Drop Shadow | `dropShadow.preset` |
| Conditional data point color | Data Point Colors | `selector.data.scopeId` |
| Series color | Series Colors | `selector.metadata` |
| Data label background | Data Labels | `enableBackground` |
| Hide value axis | Axis Formatting | `show: false` on valueAxis |
| Visual-level filter | filterConfig | `filterConfig.filters[]` |
| Sort order | Sort Definition | `visual.query.sortDefinition` |
| Top N filter | TOP N Filter | `filterConfig` type `"TopN"` |
| Drillthrough page | Drillthrough | `page.json` type `2` |
| Color scale gradient | Conditional Formatting | `fillRule.linearGradient2/3` |
| Rules-based color | Conditional Formatting | `fillRule` with value stops |
| Icon sets | DAX workaround | Unicode/emoji in measure |
