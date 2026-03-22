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
without affecting other visuals on the page:
```json
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
```
`isInvertedSelectionMode: true` means "exclude these values" (NOT IN logic).

## Sort Definition

Control visual sort order — apply to any chart with `queryState`:
```json
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
```
**Default rule**: Always sort bar/column charts by value descending unless the category
has a natural order (time, sequential stages).
