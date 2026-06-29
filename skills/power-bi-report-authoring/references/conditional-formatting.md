# Conditional Formatting Patterns

Read this when applying data-driven visual formatting in PBIR. Conditional
formatting is supported on chart `dataPoint` properties (charts) and on table /
matrix `values` cells, but **not** on container objects like axes, legends, or
visual containers.

Related references:
- [`formatting.md`](formatting.md) — value encoding, selectors, VCOs.
- [`formatting-overview.md`](formatting-overview.md) — cascade and encoding.
- [`table.md`](table.md) — table/matrix authoring and style presets.

> Examples use illustrative `<table>.<measure>` identifiers — substitute your own.

## Contents

- [Type 1: Color Gradient (FillRule)](#type-1-color-gradient-fillrule)
- [Type 2: Rules-Based Formatting](#type-2-rules-based-formatting)
- [Type 3: Icon Sets](#type-3-icon-sets)
- [Type 4: Data Bars](#type-4-data-bars)
- [Type 5: Web URL](#type-5-web-url)
- [Type 6: Field Value](#type-6-field-value)

## Type 1: Color Gradient (FillRule)

Applies data-driven color gradients. Uses `linearGradient2` (2-stop) or `linearGradient3` (3-stop).

**Supported on** `dataPoint.fill` (or `dataPoint.fillRule`) for: barChart,
clusteredBarChart, clusteredColumnChart, columnChart, funnel,
hundredPercentStackedBarChart, hundredPercentStackedColumnChart, ribbonChart,
lineStackedColumnComboChart, lineClusteredColumnComboChart, map, filledMap,
shapeMap, treemap, scatterChart, heatMap.

**For tables/matrices**: add an entry to the `values` object array (NOT `columnFormatting`).
The entry must use:
- A `selector` with `data: [{ dataViewWildcard: { matchingOption: 1 } }]` and
  `metadata` pointing to the measure's queryRef.
- A `FillRule` with `Input` using `SelectRef` / `ExpressionName` (referencing
  the measure's queryRef) instead of a direct `Measure` / `SourceRef`.

> ⚠️ **Do NOT use `columnFormatting`** for conditional formatting on tables/matrices.
> `columnFormatting` is for static styling only (alignment, display units, etc.).
> PBI Desktop enables conditional formatting via "cell elements" which writes to
> the `values` array, not `columnFormatting`.

**Pivot table / matrix gradient example** (placed as entry in `values` array inside `objects`):

```json
{
  "properties": {
    "backColor": {
      "solid": {
        "color": {
          "expr": {
            "FillRule": {
              "Input": {
                "SelectRef": { "ExpressionName": "metrics.NetIncome" }
              },
              "FillRule": {
                "linearGradient3": {
                  "min": {
                    "color": { "Literal": { "Value": "'#FF0000'" } },
                    "value": { "Literal": { "Value": "-5000000D" } }
                  },
                  "mid": {
                    "color": { "Literal": { "Value": "'#FFFFFF'" } },
                    "value": { "Literal": { "Value": "0D" } }
                  },
                  "max": {
                    "color": { "Literal": { "Value": "'#00FF00'" } },
                    "value": { "Literal": { "Value": "5000000D" } }
                  },
                  "nullColoringStrategy": {
                    "strategy": { "Literal": { "Value": "'asZero'" } }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "selector": {
    "data": [{ "dataViewWildcard": { "matchingOption": 1 } }],
    "metadata": "metrics.NetIncome"
  }
}
```

The `metadata` and `ExpressionName` values must match the measure's `queryRef`
from the visual's `queryState`.

**Key differences from chart conditional formatting:**
| Aspect | Charts (`dataPoint`) | Pivot Tables (`values`) |
|--------|---------------------|------------------------|
| Object | `dataPoint` | `values` |
| Property | `fill` | `backColor` or `fontColor` |
| Input ref | `Measure` + `SourceRef` | `SelectRef` + `ExpressionName` |
| Selector | `metadata` only | `data: [{ dataViewWildcard }]` + `metadata` |
| `matchingOption` | `0` | `1` |

**3-color gradient** (linearGradient3):

```json
{
  "solid": {
    "color": {
      "expr": {
        "FillRule": {
          "Input": {
            "Measure": {
              "Expression": { "SourceRef": { "Entity": "metrics" } },
              "Property": "GrossMargin"
            }
          },
          "FillRule": {
            "linearGradient3": {
              "min": {
                "color": { "Literal": { "Value": "'#FF0000'" } },
                "value": { "Literal": { "Value": "-0.01D" } }
              },
              "mid": {
                "color": { "Literal": { "Value": "'#FFFF00'" } },
                "value": { "Literal": { "Value": "0D" } }
              },
              "max": {
                "color": { "Literal": { "Value": "'#00FF00'" } },
                "value": { "Literal": { "Value": "0.01D" } }
              },
              "nullColoringStrategy": {
                "strategy": { "Literal": { "Value": "'asZero'" } }
              }
            }
          }
        }
      }
    }
  }
}
```

**2-color gradient** (linearGradient2) — omit `mid`:

```json
{
  "fillRule": {
    "linearGradient2": {
      "min": { "color": { "expr": { "Literal": { "Value": "'#DEEFFF'" } } } },
      "max": { "color": { "expr": { "Literal": { "Value": "'#118DFF'" } } } },
      "nullColoringStrategy": {
        "strategy": { "expr": { "Literal": { "Value": "'noColor'" } } }
      }
    }
  }
}
```

When `value` is omitted from color stops, PBI auto-calculates from data range.

> ⚠️ **FillRule color stops must use `Literal` hex values** — `ThemeDataColor`
> silently renders black inside `linearGradient2` / `linearGradient3` color stops.
> To use theme-aware colors, read `dataColors[N]` from the theme file and compute
> a lighter tint (blend 40-60% toward `#FFFFFF`) for the min stop.

**For single-series bar/column charts** — the most common use case. Apply a
value-gradient so the highest bar is darkest and lowest is lightest:

```json
"dataPoint": [{
  "properties": {
    "fill": {
      "solid": {
        "color": {
          "expr": {
            "FillRule": {
              "Input": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "<table>" } },
                  "Property": "<measure>"
                }
              },
              "FillRule": {
                "linearGradient2": {
                  "min": { "color": { "Literal": { "Value": "'#D0E8F5'" } } },
                  "max": { "color": { "Literal": { "Value": "'#56B4E9'" } } },
                  "nullColoringStrategy": {
                    "strategy": { "Literal": { "Value": "'noColor'" } }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "selector": {
    "data": [{ "dataViewWildcard": { "matchingOption": 0 } }]
  }
}]
```

Key requirements:
- **`Input`** must reference the Y-axis measure (Measure or Aggregation field)
- **`selector`** must be `data: [{ dataViewWildcard: { matchingOption: 0 } }]` —
  without this selector, the gradient does not render
- **Min color**: light tint of the base color (blend ~50% toward white)
- **Max color**: the base color at full saturation (never darker — avoid black)
- ⚠️ **Gradient color stops use `Literal` directly** — do NOT add an `expr`
  wrapper inside the gradient `min.color` / `max.color`. Write
  `{ "Literal": { "Value": "'#hex'" } }` not
  `{ "expr": { "Literal": { "Value": "'#hex'" } } }`.
  The `expr` wrapper exists on the outer `fill.solid.color.expr.FillRule` but
  NOT inside the gradient stops. Adding `expr` inside stops causes a
  Desktop crash (`Cannot read properties of undefined (reading 'accept')`
  in `visitFillRuleStop`).

**Null coloring strategies:**

| Strategy | Behavior |
|----------|----------|
| `"asZero"` | Treat nulls as zero — apply corresponding gradient color |
| `"noColor"` | No color (transparent/default) |
| `"specificColor"` | Use the `color` property from the strategy object |

## Type 2: Rules-Based Formatting

Applies colors based on value conditions using `ComparisonKind`:

```json
{
  "properties": {
    "backColor": {
      "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } }
    },
    "backColorRule": {
      "cases": [
        {
          "condition": {
            "Compare": {
              "ComparisonKind": 2,
              "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "Sales" } }, "Property": "Amount" } },
              "Right": { "Literal": { "Value": "1000D" } }
            }
          },
          "value": { "expr": { "Literal": { "Value": "'#1AAB40'" } } }
        },
        {
          "condition": {
            "Compare": {
              "ComparisonKind": 3,
              "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "Sales" } }, "Property": "Amount" } },
              "Right": { "Literal": { "Value": "0D" } }
            }
          },
          "value": { "expr": { "Literal": { "Value": "'#D64554'" } } }
        }
      ]
    }
  }
}
```

**ComparisonKind values:**

| Value | Operator | Meaning |
|-------|----------|---------|
| 0 | `==` | Equal |
| 1 | `>` | Greater Than |
| 2 | `>=` | Greater Than or Equal |
| 3 | `<` | Less Than |
| 4 | `<=` | Less Than or Equal |

## Type 3: Icon Sets

Adds icons alongside values in tables/matrices based on thresholds.

```json
{
  "properties": {
    "iconRule": {
      "iconDefinition": {
        "mode": "IconSet",
        "layout": "Before",
        "icons": [
          { "style": "TrafficLightGreen", "percent": 67 },
          { "style": "TrafficLightYellow", "percent": 33 },
          { "style": "TrafficLightRed", "percent": 0 }
        ]
      }
    }
  }
}
```

**IconLayout values:** `"Before"` (left of value), `"After"` (right), `"IconOnly"` (no text)

**IconVerticalAlignment values:** `"Top"`, `"Middle"`, `"Bottom"`

Built-in icon categories: Directional (arrows, triangles), Shapes (traffic lights,
circles), Indicators (flags, checkmarks), Ratings (stars, bars, signal strength).

Custom icons can be defined in theme JSON (see theming.md § Custom Icons).

## Type 4: Data Bars

In-cell bar visualization for tables/matrices. Applied per-column via metadata selector.

```json
{
  "properties": {
    "dataBars": {
      "positiveColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#118DFF'" } } } } },
      "negativeColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#D64554'" } } } } },
      "axisColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#999999'" } } } } },
      "reverseDirection": { "expr": { "Literal": { "Value": "false" } } },
      "hideText": { "expr": { "Literal": { "Value": "false" } } }
    }
  },
  "selector": { "metadata": "Sales.Revenue" }
}
```

Properties: `positiveColor`, `negativeColor`, `axisColor` (fills), `reverseDirection` (bool),
`hideText` (bool), `minValue`/`maxValue` (optional numeric scale bounds).

## Type 5: Web URL

Turns text into clickable hyperlinks using a URL field:

```json
{
  "properties": {
    "webUrl": {
      "expr": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "Companies" } },
          "Property": "WebsiteUrl"
        }
      }
    }
  }
}
```

Supported in tables and matrices.

## Type 6: Field Value

Applies colors directly from a data field containing color names or hex codes:

```json
{
  "properties": {
    "backColor": {
      "expr": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "Products" } },
          "Property": "CategoryColor"
        }
      }
    }
  }
}
```

Supported color formats: CSS color names, #hex (3/6/8 digit), RGB, RGBA, HSL, HSLA.
