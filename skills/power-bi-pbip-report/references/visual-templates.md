# Visual JSON Templates

Complete `visual.json` templates for common Power BI visual types in PBIR format.
Each template includes the required structure with `$schema`, `name`, `position`, and
the `visual` object containing `visualType`, `query`, and common formatting `objects`.

Replace placeholder values:
- `VISUAL_NAME` → type-prefixed slug (e.g., `card-total-revenue`)
- `TableName` / `ColumnName` / `MeasureName` → actual semantic model references
- Position values → actual layout coordinates

All templates use schema version `visualContainer/2.7.0`.

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
            "fontSize": { "expr": { "Literal": { "Value": "16D" } } },
            "bold": { "expr": { "Literal": { "Value": "true" } } }
          }
        }
      ],
      "categoryLabels": [
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
            "text": { "expr": { "Literal": { "Value": "'Card Title'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
            "bold": { "expr": { "Literal": { "Value": "true" } } },
            "alignment": { "expr": { "Literal": { "Value": "'center'" } } }
          }
        }
      ],
      "background": [
        {
          "properties": {
            "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
            "transparency": { "expr": { "Literal": { "Value": "0D" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

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
            "show": { "expr": { "Literal": { "Value": "true" } } }
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
            "mode": { "expr": { "Literal": { "Value": "'Basic'" } } }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

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

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "shape-VISUAL_NAME",
  "position": {
    "x": 0,
    "y": 0,
    "z": 0,
    "height": 720,
    "width": 1280,
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
                "color": { "expr": { "Literal": { "Value": "'#F2F2F2'" } } }
              }
            },
            "show": { "expr": { "Literal": { "Value": "false" } } }
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
    }
  }
}
```

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
    }
  }
}
```

---

## Action Button

Navigation or bookmark button. No data query.

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
