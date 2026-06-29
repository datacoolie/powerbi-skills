# Custom Visuals Reference

Custom visuals extend Power BI beyond built-in chart types. They require registration
in `report.json` → `publicCustomVisuals` array and use specific `visualType` identifiers.

---

## Registration Pattern

Every custom visual used in a report **must** be listed in `report.json`:

```json
{
  "publicCustomVisuals": [
    "ChicletSlicer1448559807354",
    "Sunburst1445472000808"
  ]
}
```

The `visualType` in `visual.json` must exactly match the registered identifier.

---

## Custom Visual Categories

### Enhanced KPI & Card Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Advance Card by JEYA** | `advanceCardE03760C5AB684758B56AA29F9E6C257B` | `Data` | Rich KPI card with conditional formatting, multiple data rows, icons, dynamic backgrounds |
| **KPI Indicator** | `payPalKPIDonutChart55A431AB15A540ED924ACD72ED8D259F` | `Indicator`, `TrendAxis`, `Goal` | Donut-style KPI with percentage fill, trend line, and target |
| **Multi KPI** | `multiKpiEA8DA325489E436991F0E411F2D85FF3` | `Values`, `Axis`, `WarningState` | Multiple KPIs with sparklines in a single compact visual |
| **Databar KPI** | `databarKPIB8060E2B144244C5A38807466893C9F5` | `Category`, `Values`, `Target` | Horizontal bar-style KPI with progress toward target |
| **Power KPI** | `powerKPI462CE5C2666F4EC8A8BDD7E5587320A3` | `Axis`, `Values`, `SecondaryValues` | KPI with full chart background (line/area) |
| **KPI Free** | `kpifree51D0292A0438427096AC459B59FEF2DE` | `Value`, `Goal`, `Indicator` | Free lightweight KPI card with trend and target |
| **KPI Table** | `kpiTable2FA7B4711C7C41C08129D5AB7A72D537` | `Category`, `Values`, `Target` | KPI metrics in a compact table layout |
| **KPI Ticker** | `kpiTicker492C9305B9464241B52382527F977DE1` | `Values`, `Axis` | Scrolling/marquee KPI banner for dashboards |
| **Zebra BI Cards** | `zebraBiCards2C860CFAA9944091B75F0DBD117F20FA` | `Category`, `Values`, `PY`, `AC`, `FC` | IBCS-compliant KPI cards — popular for financial reporting with variance indicators |
| **Multi Info Cards** | `multiInfoCards9D184BB3D4E44A139DA08142D76EFD36` | `Title`, `Description`, `Values` | Multiple informational cards with icons and descriptions |

**Advance Card** template (most popular custom visual — 379 instances in reference reports):
```json
{
  "visual": {
    "visualType": "advanceCardE03760C5AB684758B56AA29F9E6C257B",
    "query": {
      "queryState": {
        "Data": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "Measures" } },
                  "Property": "Revenue"
                }
              },
              "queryRef": "Measures.Revenue",
              "nativeQueryRef": "Revenue"
            }
          ]
        }
      }
    },
    "objects": {
      "conditionFormatting": [{ "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } }]
    }
  }
}
```

---

### Slicer & Filter Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Chiclet Slicer** | `ChicletSlicer1448559807354` | `Category`, `Values` | Button/tile-style slicer with images; great for category selection with visual icons |
| **Timeline Slicer** | `Timeline1447991079100` | `Time` | Interactive date range slider with granularity options (day/week/month/quarter/year) |
| **Text Filter / Search Slicer** | `textSearchSlicerF85E2E78BE4A4D7D9F99ED75B5D71C85` | `Values` | Free-text search box to filter visuals by typed string |
| **Hierarchy Slicer** | `HierarchicalFilterF39DAE8D57A743EF89F5C3809DEE2B67` | `Values` | Tree-view slicer for parent-child hierarchies with expand/collapse |
| **Advanced Toggle Switch** | `advancedtoggleswitch` | `Values` | Toggle/switch control for binary filter selections |

**Chiclet Slicer** template (221 instances):
```json
{
  "visual": {
    "visualType": "ChicletSlicer1448559807354",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DimCategory" } },
                  "Property": "CategoryName"
                }
              },
              "queryRef": "DimCategory.CategoryName"
            }
          ]
        },
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "Measures" } },
                  "Property": "TotalSales"
                }
              },
              "queryRef": "Measures.TotalSales"
            }
          ]
        }
      }
    },
    "objects": {
      "general": [{ "properties": {
        "columns": { "expr": { "Literal": { "Value": "4L" } } },
        "rows": { "expr": { "Literal": { "Value": "1L" } } },
        "orientation": { "expr": { "Literal": { "Value": "'horizontal'" } } },
        "showDisabled": { "expr": { "Literal": { "Value": "'bottom'" } } }
      }}],
      "header": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "false" } } }
      }}]
    }
  }
}
```

**Timeline Slicer** template:
```json
{
  "visual": {
    "visualType": "Timeline1447991079100",
    "query": {
      "queryState": {
        "Time": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DimDate" } },
                  "Property": "Date"
                }
              },
              "queryRef": "DimDate.Date"
            }
          ]
        }
      }
    },
    "objects": {
      "rangeHeader": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } }
      }}],
      "granularity": [{ "properties": {
        "granularity": { "expr": { "Literal": { "Value": "'month'" } } }
      }}]
    }
  }
}
```

---

### Gauge & Target Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Tachometer** | `Tachometer1474636471549` | `Y`, `StartValue`, `EndValue`, `TargetValue` | Semicircular gauge with needle, colored ranges, and target marker |
| **Bullet Chart (Microsoft)** | `BulletChart1443347686880` | `Category`, `Value`, `TargetValue`, `Minimum`, `NeedsImprovement`, `Satisfactory`, `Good`, `VeryGood`, `Maximum` | Compact bar with qualitative ranges and target line — preferred over gauge for density |
| **Bullet Chart (OKViz)** | `BulletChart832EC06300814F26921DEFC2DE8606BE` | `Category`, `Value`, `Target` | Simplified bullet with cleaner formatting options |
| **Vertical Bullet Chart** | `verticalbulletchartC92E3A05AD53C0B564B0C0333489BCC9` | `col_0` (Category), `col_2` (Value), `col_5` (Target) | Vertical orientation bullet — for actual vs. plan comparisons |
| **Linear Gauge** | `linearGauge2EBA8C0A99F94BF297BCCB1CF5427E68` | `Value`, `MinValue`, `MaxValue`, `TargetValue` | Horizontal linear gauge with fill and target |
| **Cylindrical Gauge** | `cylindricalGauge73A12A442345453EB69B593649C3A341` | `Y`, `MinValue`, `MaxValue` | 3D cylindrical tank-style gauge — fill level visualization |

**Tachometer** template (31 instances):
```json
{
  "visual": {
    "visualType": "Tachometer1474636471549",
    "query": {
      "queryState": {
        "Y": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "ActualValue"
              }
            },
            "queryRef": "Measures.ActualValue"
          }]
        },
        "TargetValue": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "TargetValue"
              }
            },
            "queryRef": "Measures.TargetValue"
          }]
        }
      }
    },
    "objects": {
      "target": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } }
      }}]
    }
  }
}
```

---

### Statistical & Distribution Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Box & Whisker** | `BoxWhiskerChart1455240051538` | `Groups`, `Values`, `Samples` | Show distribution (median, quartiles, outliers) across categories — manufacturing QC, salary ranges |
| **Histogram** | `histogramXY6E3D5691159E41859A007A262D4B0E9E` | `Values`, `Frequency` | Distribution of values in bins — delivery times, score distributions |
| **Violin Plot** | `ViolinPlot1445472000811` | `Category`, `Values`, `Sampling` | Combines box plot + kernel density — richer than box & whisker for showing distribution shape |

**Box & Whisker** template:
```json
{
  "visual": {
    "visualType": "BoxWhiskerChart1455240051538",
    "query": {
      "queryState": {
        "Groups": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimCategory" } },
                "Property": "Category"
              }
            },
            "queryRef": "DimCategory.Category",
            "nativeQueryRef": "Category"
          }]
        },
        "Values": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "MetricValue"
              }
            },
            "queryRef": "Measures.MetricValue",
            "nativeQueryRef": "MetricValue"
          }]
        },
        "Samples": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "FactTable" } },
                "Property": "RecordID"
              }
            },
            "queryRef": "FactTable.RecordID",
            "nativeQueryRef": "RecordID"
          }]
        }
      }
    }
  }
}
```

---

### Hierarchical & Part-of-Whole Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Sunburst** | `Sunburst1445472000808` | `Nodes`, `Values` | Multi-level ring chart for hierarchical data — org structure, product hierarchy, category drill-down |
| **Waffle Chart** | `WaffleChart1453776852267` | `Category`, `Values` | Grid of filled squares showing percentage — engagement rates, completion status, simple ratios |
| **Aster Plot** | `AsterPlot1443303142064` | `Category`, `Y` | Radial chart combining pie slice width with bar height — dual-encoded categorical comparison |

**Sunburst** template:
```json
{
  "visual": {
    "visualType": "Sunburst1445472000808",
    "query": {
      "queryState": {
        "Nodes": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DimRegion" } },
                  "Property": "Region"
                }
              },
              "queryRef": "DimRegion.Region"
            },
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "DimCity" } },
                  "Property": "City"
                }
              },
              "queryRef": "DimCity.City"
            }
          ]
        },
        "Values": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "Revenue"
              }
            },
            "queryRef": "Measures.Revenue"
          }]
        }
      }
    }
  }
}
```

**Waffle Chart** template:
```json
{
  "visual": {
    "visualType": "WaffleChart1453776852267",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimStatus" } },
                "Property": "Status"
              }
            },
            "queryRef": "DimStatus.Status"
          }]
        },
        "Values": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "CompletionRate"
              }
            },
            "queryRef": "Measures.CompletionRate"
          }]
        }
      }
    }
  }
}
```

---

### Comparison & Ranking Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Tornado Chart** | `TornadoChart1452517688218` | `Group`, `Values` | Side-by-side diverging bars — comparing two measures across categories (male vs female, plan vs actual) |
| **Lollipop Column Chart** | `lollipopcolumn216FD8C19B9DC0D953B3FAE4C3997742` | `Category`, `Values` | Column chart with circle marker on top — cleaner look for sparse category comparisons |
| **Merged Bar Chart** | `mergedBarChart7A702E6E03084979A73CC897E0D7E2EB` | `Category`, `Values` | Overlapping bars for direct comparison — actual vs budget side by side |
| **Clustered Column by Akvelon** | `clusteredColumnChartByAkvelonBE487DE8B8674A59A098B9B16C950BA1` | `Axis`, `Values`, `Legend` | Enhanced clustered column with small multiples built in |
| **Advanced Pie/Donut** | `advancedPieDonut812F760774854B428BA58A87279F6AF6` | `Category`, `Values` | Enhanced pie/donut with drill-down, percentage labels, and conditional colors |
| **Clustered Stacked Chart** | `clusteredstackedchartB0483D9875581356AF8B510BAAC9CFE4` | `Category`, `Values`, `Series` | Combines clustered and stacked bars in one visual — grouped comparison with composition |
| **Multiple Axes Chart** | `multipleAxesChartBC35C88E1D1A49DFA5A9240AFBB4E3BC` | `Axis`, `Values` | Multiple Y-axes on a single chart — for comparing metrics at different scales |
| **Nested Total Bar Chart** | `nestedTotalBarChartC2D32E67DFF64FDD9564CF2CFCD20141` | `Category`, `Values` | Overlapping bars showing part vs. total — compact actual-vs-budget view |

**Tornado Chart** template:
```json
{
  "visual": {
    "visualType": "TornadoChart1452517688218",
    "query": {
      "queryState": {
        "Group": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimCategory" } },
                "Property": "Category"
              }
            },
            "queryRef": "DimCategory.Category"
          }]
        },
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "Measures" } },
                  "Property": "MeasureA"
                }
              },
              "queryRef": "Measures.MeasureA"
            },
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "Measures" } },
                  "Property": "MeasureB"
                }
              },
              "queryRef": "Measures.MeasureB"
            }
          ]
        }
      }
    }
  }
}
```

---

### Flow & Relationship Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Sankey Diagram** | `SankeyDiagram1458048422238` | `Source`, `Destination`, `Weight` | Flow between categories — budget allocation, customer journey, supply chain paths |
| **Chord Chart** | `ChordChart1443052498688` | `From`, `To`, `Values` | Circular relationship diagram — inter-department transfers, trade flows between regions |

**Sankey Diagram** template:
```json
{
  "visual": {
    "visualType": "SankeyDiagram1458048422238",
    "query": {
      "queryState": {
        "Source": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "Flows" } },
                "Property": "SourceCategory"
              }
            },
            "queryRef": "Flows.SourceCategory"
          }]
        },
        "Destination": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "Flows" } },
                "Property": "DestCategory"
              }
            },
            "queryRef": "Flows.DestCategory"
          }]
        },
        "Weight": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "FlowAmount"
              }
            },
            "queryRef": "Measures.FlowAmount"
          }]
        }
      }
    }
  }
}
```

**Chord Chart** template:
```json
{
  "visual": {
    "visualType": "ChordChart1443052498688",
    "query": {
      "queryState": {
        "From": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "Relationships" } },
                "Property": "FromEntity"
              }
            },
            "queryRef": "Relationships.FromEntity"
          }]
        },
        "To": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "Relationships" } },
                "Property": "ToEntity"
              }
            },
            "queryRef": "Relationships.ToEntity"
          }]
        },
        "Values": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "RelationshipStrength"
              }
            },
            "queryRef": "Measures.RelationshipStrength"
          }]
        }
      }
    }
  }
}
```

---

### Waterfall & Variance Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **xViz Waterfall** | `waterfall6C9ED82ABD1F44C4A0D590CE01EB5EE7` | `Category`, `Values`, `Plan` | Enhanced waterfall with plan vs actual comparison line overlay |
| **Ultimate Variance** | `ultimateVariance9712E1351D4E4FA89077ED4D9351DC71` | `Category`, `Actual`, `Plan` | Integrated variance chart showing actual, plan, and variance in one visual |
| **Variance Chart** | `variance8E4BB1B41A8942A7B897C7014A6E1F56` | `Category`, `Values`, `Target` | Variance visualization with absolute and percentage deviation |
| **Growth Rate Chart** | `DjeeniGrowthRateChart_10300020A6CA2A4124B79C0FF6A4D9EE59` | `Category`, `Values` | Growth rate visualization with period-over-period comparison |

---

### Calendar Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **BCI Calendar** | `bciCalendarCC0FA2BFE4B54EE1ACCFE383B9B1DE61` | `category` (Date), `measure` | Heatmap calendar view — daily activity, attendance, production output by day |
| **Calendar by Datanau** | `CalendarByDatanau` | `Date`, `Values` | Alternative calendar visual with simpler configuration |

**BCI Calendar** template:
```json
{
  "visual": {
    "visualType": "bciCalendarCC0FA2BFE4B54EE1ACCFE383B9B1DE61",
    "query": {
      "queryState": {
        "category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimDate" } },
                "Property": "Date"
              }
            },
            "queryRef": "DimDate.Date",
            "nativeQueryRef": "Date"
          }]
        },
        "measure": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "DailyValue"
              }
            },
            "queryRef": "Measures.DailyValue",
            "nativeQueryRef": "DailyValue"
          }]
        }
      }
    },
    "objects": {
      "calendar": [{ "properties": {
        "weekStartDay": { "expr": { "Literal": { "Value": "1D" } } }
      }}]
    }
  }
}
```

---

### Specialty Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Radar Chart** | `RadarChart1423470498847` | `Category`, `Y` | Spider/web chart for multi-dimensional comparison — skill assessment, product scoring across attributes |
| **Mekko Chart** | `MekkoChart1513095496262` | `Category`, `Series`, `Y` | Variable-width stacked bar — market share across segments where segment sizes differ |
| **Table Heatmap** | `TableHeatmap1445497103790` | `Category`, `Y`, `Series` | Color-intensity matrix — correlation heatmap, time × category activity |
| **Packed Bubble** | `PackedBubbleChart1600694507780` | `Category`, `Values`, `Size` | Non-overlapping circles packed for part-of-whole — alternative to treemap with circular layout |
| **Lollipop Bar Chart** | `lollipopbar3906E14BA17BC92E464868265E6264D9` | `Category`, `Values` | Horizontal lollipop — cleaner alternative to bar chart for sparse data |
| **Flow Map** | `flowmap30CFDD5B92F848C88242B1E81C8C33C7` | `Origin`, `Destination`, `Value` | Geographic flow lines between locations on a map |
| **Drill Down Funnel** | `funnelDrilldownD423170ED341443BBDECDD3BA5FB49D2` | `Category`, `Values` | Enhanced funnel with drill-down into stages |
| **Sparkline by OKViz** | `sparklines50DB3783432B40A69C0B91926CE74CD9` | `Category`, `Values`, `Sparkline` | Standalone sparkline visual (not embedded in table) |
| **Icon Map Pro** | `iconMapProE938B1CED4834168A55864E1F8E7242E` | `Category`, `Latitude`, `Longitude`, `Size` | Map with custom icon markers per category |
| **Inforiver Charts** | `InforiverCharts582F6C55AB6442EF8FA129089285CB47` | *(varies by chart type)* | Enterprise charting suite — advanced charts, annotations, writeback |

---

## Other Popular Community Visuals

These visuals are widely used in the Power BI community but not present in the reference reports.
Verify `visualType` identifiers from AppSource before first use.

| Marketplace Name | Typical `visualType` | Use Case |
|---|---|---|
| **Deneb** | `Deneb6E97C82C58E5467CA7C3188B3E36ADE7` | Create any visualization using Vega / Vega-Lite declarative grammar — the most flexible custom visual |
| **Word Cloud** | `WordCloud1447959067750` | Word frequency / text analysis — word size proportional to frequency or measure |
| **Gantt Chart** | `Gantt1467746032498` | Project timeline with task bars, milestones, dependencies, and progress tracking |
| **Play Axis (Dynamic Slicer)** | `playAxis23F08FF12F11460BB525B1A3ADED385C` | Animated time axis — auto-plays through dates to animate scatter plots and maps |
| **HTML Content** | `htmlContent...` | Render custom HTML/CSS/SVG inside Power BI — for bespoke layouts or embedded content |
| **Charticulator** | `charticulator...` | Visual authoring tool — build fully custom chart types without code |
| **Card with States by OKViz** | `cardWithStates...` | Conditional card with dynamic background, icon, and color based on value thresholds |
| **Smart Filter by OKViz** | `smartFilter...` | Enhanced dropdown/search filter with multi-select and fuzzy matching |

> **Note:** Identifiers marked with `...` are abbreviated — look up the full identifier in
> [AppSource](https://appsource.microsoft.com/) when adding these to `report.json`.

**Radar Chart** template:
```json
{
  "visual": {
    "visualType": "RadarChart1423470498847",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimAttribute" } },
                "Property": "Attribute"
              }
            },
            "queryRef": "DimAttribute.Attribute"
          }]
        },
        "Y": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "Score"
              }
            },
            "queryRef": "Measures.Score"
          }]
        }
      }
    }
  }
}
```

**Mekko Chart** template:
```json
{
  "visual": {
    "visualType": "MekkoChart1513095496262",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimSegment" } },
                "Property": "Segment"
              }
            },
            "queryRef": "DimSegment.Segment"
          }]
        },
        "Series": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "DimProduct" } },
                "Property": "Product"
              }
            },
            "queryRef": "DimProduct.Product"
          }]
        },
        "Y": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "Measures" } },
                "Property": "MarketShare"
              }
            },
            "queryRef": "Measures.MarketShare"
          }]
        }
      }
    }
  }
}
```

---

## Additional Visuals Observed in Reference Reports

These identifiers appear in the reference PBIP reports and are verified from real usage. Add them
to `publicCustomVisuals` before use.

### Enterprise IBCS Suite — 3AG Systems

3AG Systems publishes an IBCS-compliant suite popular for financial reporting. Multiple variants
appear in the reference reports (table, chart, and card components):

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **3AG Systems Visual A** | `PBI_3AGSystems_0B9C9FBA_15A2_4A94_8AE4_8F778869B190` | `Category`, `Values` | IBCS-style chart with variance markers (5 reports) |
| **3AG Systems Visual B** | `PBI_3AGSystems_0B9C9FBA_15A2_4A94_8AE4_8F778869B191` | `Category`, `Values`, `PY` | IBCS-style with prior-year comparison |
| **3AG Systems Visual C** | `PBI_3AGSystems_0B9C9FBA_15A2_4A94_8AE4_8F778869B192` | `Category`, `Values`, `PY`, `PL` | IBCS tables/charts with plan and prior year (heavy usage: 5 reports) |

### Generic `PBI_CV_*` Identifiers

Microsoft's generic Custom Visual GUID pattern. These wrap various publishers' visuals — identify the
actual publisher via the AppSource lookup when encountered. The following appear in reference reports:

| `visualType` | Reports | Likely Category |
|---|---|---|
| `PBI_CV_9272D058_BEA0_476A_B090_A712545F92FA` | 14 (highest usage) | Card/KPI or slicer |
| `PBI_CV_7B952816_A48F_49B4_9E13_15E3BB2C0337` | 6 | Chart/data visual |
| `PBI_CV_25997FEB_F466_44FA_B562_AC4063283C4C` | 5 | Chart/data visual |
| `PBI_CV_0B9C9FBA_15A2_4A94_8AE4_8F778869B200` | 4 | Chart/data visual |
| `PBI_CV_3C80B1F2_09AF_4123_8E99_C3CBC46B23E0` | 3 | Chart/data visual |
| `PBI_CV_309E6B47_39A5_4681_808F_132AFB230872` | 2 | Chart/data visual |
| `PBI_CV_0B9C9FBA_15A2_4A94_8AE4_8F778869B190` | 2 | Chart/data visual |
| `PBI_CV_73744D90_4DC9_4F18_8BA5_EE8FA5C98035` | 1 | Specialty |
| `PBI_CV_815282F9_27F5_4950_9430_E910E0A8DB6A` | 1 | Specialty |

> **Tip:** When copying a visual from a reference PBIP, always copy its `publicCustomVisuals`
> entry from `report.json` along with the visual itself. Generic identifiers cannot be
> re-created from the identifier alone.

### Timeline & Slicer Variants

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Timeline Storyteller** | `timelineD7EACB3A04E64A5FA9D86F6E035F3523` | `Time`, `Values` | Storytelling-oriented timeline with events and labels |
| **Timeline Variation** | `timelineVariation3D7EACB3A04E64A5FA9D86F6E035F3524` | `Time`, `Values` | Alternative timeline layout — richer formatting options |
| **Custom Slicer** | `CustomSlicer` | `Category` | Generic third-party slicer identifier (publisher-specific; verify on AppSource) |
| **Slicer1448559807355** | `Slicer1448559807355` | `Category`, `Values` | Enhanced Microsoft slicer variant |

### Tree & Hierarchy Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **D3 JS Tree** | `D3JsTree2F7A67F154D04FA3A4CA3E01DE5AE54B` | `Node`, `ParentNode`, `Values` | D3-based hierarchical tree visualization — org chart, family tree, classification tree |
| **Hierarchical Tree** | `HierarchicalTreeF39DAE8D57A743EF89F5C3809DEE2B67` | `Nodes`, `Values` | Expanding tree view (note: shares identifier pattern with Hierarchy Slicer — verify on AppSource) |

### Calendar Variants

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Calendar Visual (MAQ Software)** | `calendarVisual74934D05B71F4C31B0F79D925EE89638` | `Date`, `Value` | Alternate calendar heatmap implementation |
| **Calendar Visual (Generic)** | `CalendarVisualA45056645E4E428B9D26EF971839A6B5` | `Date`, `Value` | Additional calendar heatmap variant |

### Process & Flow

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Process Mining** | `processMiningD4BFA18191D74FA5AEEEB307FC3EAED1` | `Case`, `Activity`, `Timestamp` | Discover and visualize process flows from event logs — manufacturing, customer journey, workflow analysis |
| **Informaxyz 3D BI Connected** | `Informaxyz3DBIConnected69f2181a7e5a44a9a709014959414bf0` | `Category`, `Values`, `Connections` | 3D connected BI visual — network-style data relationships in 3D space |

**Process Mining** template:
```json
{
  "visual": {
    "visualType": "processMiningD4BFA18191D74FA5AEEEB307FC3EAED1",
    "query": {
      "queryState": {
        "Case": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "EventLog" } },
                "Property": "CaseId"
              }
            },
            "queryRef": "EventLog.CaseId"
          }]
        },
        "Activity": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "EventLog" } },
                "Property": "Activity"
              }
            },
            "queryRef": "EventLog.Activity"
          }]
        },
        "Timestamp": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "EventLog" } },
                "Property": "Timestamp"
              }
            },
            "queryRef": "EventLog.Timestamp"
          }]
        }
      }
    }
  }
}
```

### Column & Bar Variants

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Advanced Column Bar Chart** | `AdvancedColumnBarChart149CBDF1945A4455952D90C68DD649AA` | `Category`, `Values`, `Series` | Combined column+bar chart with advanced formatting |
| **Clustered Stacked Bar Chart** | `ClusteredStackedBarChart39ECD6FE50G` | `Category`, `Series`, `Values` | Both clustered and stacked breakdown in one visual |
| **Horizontal Bullet Chart** | `horizontalbullechartAD848DB2E71C1BBC88C027512FD82044` | `Category`, `Value`, `Target` | Horizontal bullet chart variant — actual vs. target in compact rows |
| **Lipstick Column Chart** | `lipstickcolumnchartA0919059F5DBE50C75F3D8D6A166710D` | `Category`, `Values`, `Overlay` | Stacked column with thin overlay bar — actual vs. plan variance |
| **Lollipop Chart** | `lollipopChart50393786178B4137A75F3257CB590B96` | `Category`, `Values` | Alternate lollipop variant (different publisher) |
| **Lollipop Column Chart** | `lollipopColumnChart0D874BBC87DE40189C387BBA89739F6C` | `Category`, `Values` | Alternate vertical lollipop variant |

### KPI & Card Variants

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Multi-Card KPIs** | `multicardkpis` | `Values` | Compact grid of multiple KPI cards in one visual |
| **Data Goods 5 (`dg5...`)** | `dg5AAA90EFEFE747CB9357C4FC19B85A58` | *(varies)* | Generic data-goods identifier — verify exact capability on AppSource |

### Utility Visuals

| Marketplace Name | `visualType` | Query Roles | Use Case |
|---|---|---|---|
| **Dynamic Tooltip** | `dynamicTooltip1859AB39DB23051788ADF752BCB90749` | `Values` | Report-page tooltip that dynamically formats based on hover context |

**Lipstick Column Chart** template — common variance pattern:
```json
{
  "visual": {
    "visualType": "lipstickcolumnchartA0919059F5DBE50C75F3D8D6A166710D",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "Calendar" } },
                "Property": "Month"
              }
            },
            "queryRef": "Calendar.Month"
          }]
        },
        "Values": {
          "projections": [
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Measures" } }, "Property": "Plan" } }, "queryRef": "Measures.Plan" }
          ]
        },
        "Overlay": {
          "projections": [
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Measures" } }, "Property": "Actual" } }, "queryRef": "Measures.Actual" }
          ]
        }
      }
    }
  }
}
```

---

## When to Use Custom Visuals

### Scenarios Where Custom Visuals Add Clear Value

| Scenario | Built-in Limitation | Custom Visual Solution |
|---|---|---|
| Distribution analysis | No histogram or box plot built-in | Box & Whisker, Histogram, Violin Plot |
| Hierarchical breakdown | Treemap only shows 1-2 levels clearly | Sunburst for 3+ nested levels |
| Flow/relationship between nodes | No flow chart built-in | Sankey Diagram, Chord Chart |
| Comparing two measures diverging | Combo chart is awkward for this | Tornado Chart |
| Actual vs. target with ranges | KPI/gauge limited formatting | Bullet Chart, Tachometer |
| Date-based heatmap | No calendar view built-in | BCI Calendar |
| Multi-dimensional scoring | No radar/spider built-in | Radar Chart |
| Percentage as discrete units | No waffle built-in | Waffle Chart |
| Image-based category selection | Basic slicer has no images | Chiclet Slicer |
| Interactive date range picker | Date slicer basic | Timeline Slicer |
| Market size × composition | Stacked bar has equal widths | Mekko Chart |

### When to Avoid Custom Visuals

- **Performance**: Custom visuals render slower than built-in — avoid on pages with 15+ visuals
- **Mobile**: Many custom visuals have poor mobile layout support
- **Governance**: Organizations may restrict AppSource visuals — check admin policies
- **Maintenance**: Custom visuals can break on Power BI updates — built-in are always compatible
- **Certification**: Prefer **Microsoft-certified** custom visuals when available (marked with blue badge on AppSource)

---

## Quick Reference: visualType Identifiers

| Visual Name | `visualType` | Publisher |
|---|---|---|
| Advance Card | `advanceCardE03760C5AB684758B56AA29F9E6C257B` | JEYA |
| Chiclet Slicer | `ChicletSlicer1448559807354` | Microsoft |
| Timeline Slicer | `Timeline1447991079100` | Microsoft |
| Tachometer | `Tachometer1474636471549` | Microsoft |
| Bullet Chart | `BulletChart1443347686880` | Microsoft |
| Tornado Chart | `TornadoChart1452517688218` | Microsoft |
| Sunburst | `Sunburst1445472000808` | Microsoft |
| Box & Whisker | `BoxWhiskerChart1455240051538` | Microsoft |
| Waffle Chart | `WaffleChart1453776852267` | Microsoft |
| Radar Chart | `RadarChart1423470498847` | Microsoft |
| Chord Chart | `ChordChart1443052498688` | Microsoft |
| Sankey Diagram | `SankeyDiagram1458048422238` | Microsoft |
| Mekko Chart | `MekkoChart1513095496262` | Microsoft |
| Table Heatmap | `TableHeatmap1445497103790` | David Leung |
| Histogram | `histogramXY6E3D5691159E41859A007A262D4B0E9E` | OKViz |
| Violin Plot | `ViolinPlot1445472000811` | Daniel Marsh-Patrick |
| Packed Bubble | `PackedBubbleChart1600694507780` | Community |
| xViz Waterfall | `waterfall6C9ED82ABD1F44C4A0D590CE01EB5EE7` | xViz |
| Ultimate Variance | `ultimateVariance9712E1351D4E4FA89077ED4D9351DC71` | Community |
| BCI Calendar | `bciCalendarCC0FA2BFE4B54EE1ACCFE383B9B1DE61` | BCI |
| KPI Indicator | `payPalKPIDonutChart55A431AB15A540ED924ACD72ED8D259F` | Community |
| Multi KPI | `multiKpiEA8DA325489E436991F0E411F2D85FF3` | Community |
| Lollipop Column | `lollipopcolumn216FD8C19B9DC0D953B3FAE4C3997742` | Community |
| Merged Bar Chart | `mergedBarChart7A702E6E03084979A73CC897E0D7E2EB` | Community |
| Aster Plot | `AsterPlot1443303142064` | Microsoft |
| Vertical Bullet Chart | `verticalbulletchartC92E3A05AD53C0B564B0C0333489BCC9` | OKViz |
| Bullet Chart (OKViz) | `BulletChart832EC06300814F26921DEFC2DE8606BE` | OKViz |
| Databar KPI | `databarKPIB8060E2B144244C5A38807466893C9F5` | Community |
| Text Search Slicer | `textSearchSlicerF85E2E78BE4A4D7D9F99ED75B5D71C85` | Community |
| Hierarchy Slicer | `HierarchicalFilterF39DAE8D57A743EF89F5C3809DEE2B67` | Community |
| Flow Map | `flowmap30CFDD5B92F848C88242B1E81C8C33C7` | Community |
| Lollipop Bar | `lollipopbar3906E14BA17BC92E464868265E6264D9` | Community |
| KPI Free | `kpifree51D0292A0438427096AC459B59FEF2DE` | Community |
| KPI Table | `kpiTable2FA7B4711C7C41C08129D5AB7A72D537` | Community |
| KPI Ticker | `kpiTicker492C9305B9464241B52382527F977DE1` | Community |
| Zebra BI Cards | `zebraBiCards2C860CFAA9944091B75F0DBD117F20FA` | Zebra BI |
| Multi Info Cards | `multiInfoCards9D184BB3D4E44A139DA08142D76EFD36` | Community |
| Power KPI | `powerKPI462CE5C2666F4EC8A8BDD7E5587320A3` | Community |
| Advanced Toggle Switch | `advancedtoggleswitch` | Community |
| Cylindrical Gauge | `cylindricalGauge73A12A442345453EB69B593649C3A341` | Community |
| Linear Gauge | `linearGauge2EBA8C0A99F94BF297BCCB1CF5427E68` | Community |
| Advanced Pie/Donut | `advancedPieDonut812F760774854B428BA58A87279F6AF6` | Community |
| Clustered Stacked Chart | `clusteredstackedchartB0483D9875581356AF8B510BAAC9CFE4` | Community |
| Clustered Column by Akvelon | `clusteredColumnChartByAkvelonBE487DE8B8674A59A098B9B16C950BA1` | Akvelon |
| Multiple Axes Chart | `multipleAxesChartBC35C88E1D1A49DFA5A9240AFBB4E3BC` | Community |
| Nested Total Bar Chart | `nestedTotalBarChartC2D32E67DFF64FDD9564CF2CFCD20141` | Community |
| Variance Chart | `variance8E4BB1B41A8942A7B897C7014A6E1F56` | Community |
| Growth Rate Chart | `DjeeniGrowthRateChart_10300020A6CA2A4124B79C0FF6A4D9EE59` | Djeeni |
| Drill Down Funnel | `funnelDrilldownD423170ED341443BBDECDD3BA5FB49D2` | Community |
| Sparkline by OKViz | `sparklines50DB3783432B40A69C0B91926CE74CD9` | OKViz |
| Icon Map Pro | `iconMapProE938B1CED4834168A55864E1F8E7242E` | Community |
| Inforiver Charts | `InforiverCharts582F6C55AB6442EF8FA129089285CB47` | Inforiver |
| Calendar by Datanau | `CalendarByDatanau` | Datanau |
| Calendar Pro by OKViz | `calendarProByOKVIZ359F68153F3C4C1B84994D4D62ED4EAC` | OKViz |
| Deneb | `Deneb6E97C82C58E5467CA7C3188B3E36ADE7` | Daniel Marsh-Patrick |
| Word Cloud | `WordCloud1447959067750` | Microsoft |
| Gantt Chart | `Gantt1467746032498` | Microsoft |
| Play Axis | `playAxis23F08FF12F11460BB525B1A3ADED385C` | Community |
| 3AG Systems Visual A | `PBI_3AGSystems_0B9C9FBA_15A2_4A94_8AE4_8F778869B190` | 3AG Systems |
| 3AG Systems Visual B | `PBI_3AGSystems_0B9C9FBA_15A2_4A94_8AE4_8F778869B191` | 3AG Systems |
| 3AG Systems Visual C | `PBI_3AGSystems_0B9C9FBA_15A2_4A94_8AE4_8F778869B192` | 3AG Systems |
| Generic Custom Visual (9272D058) | `PBI_CV_9272D058_BEA0_476A_B090_A712545F92FA` | *(various)* |
| Generic Custom Visual (7B952816) | `PBI_CV_7B952816_A48F_49B4_9E13_15E3BB2C0337` | *(various)* |
| Generic Custom Visual (25997FEB) | `PBI_CV_25997FEB_F466_44FA_B562_AC4063283C4C` | *(various)* |
| Generic Custom Visual (0B9C9FBA_200) | `PBI_CV_0B9C9FBA_15A2_4A94_8AE4_8F778869B200` | *(various)* |
| Generic Custom Visual (3C80B1F2) | `PBI_CV_3C80B1F2_09AF_4123_8E99_C3CBC46B23E0` | *(various)* |
| Generic Custom Visual (309E6B47) | `PBI_CV_309E6B47_39A5_4681_808F_132AFB230872` | *(various)* |
| Generic Custom Visual (0B9C9FBA_190) | `PBI_CV_0B9C9FBA_15A2_4A94_8AE4_8F778869B190` | *(various)* |
| Generic Custom Visual (73744D90) | `PBI_CV_73744D90_4DC9_4F18_8BA5_EE8FA5C98035` | *(various)* |
| Generic Custom Visual (815282F9) | `PBI_CV_815282F9_27F5_4950_9430_E910E0A8DB6A` | *(various)* |
| Timeline Storyteller | `timelineD7EACB3A04E64A5FA9D86F6E035F3523` | Community |
| Timeline Variation | `timelineVariation3D7EACB3A04E64A5FA9D86F6E035F3524` | Community |
| Custom Slicer | `CustomSlicer` | *(various)* |
| Slicer 1448559807355 | `Slicer1448559807355` | Community |
| D3 JS Tree | `D3JsTree2F7A67F154D04FA3A4CA3E01DE5AE54B` | Community |
| Hierarchical Tree | `HierarchicalTreeF39DAE8D57A743EF89F5C3809DEE2B67` | Community |
| Calendar Visual (MAQ) | `calendarVisual74934D05B71F4C31B0F79D925EE89638` | MAQ Software |
| Calendar Visual (Generic) | `CalendarVisualA45056645E4E428B9D26EF971839A6B5` | Community |
| Process Mining | `processMiningD4BFA18191D74FA5AEEEB307FC3EAED1` | Community |
| Informaxyz 3D BI Connected | `Informaxyz3DBIConnected69f2181a7e5a44a9a709014959414bf0` | Informaxyz |
| Advanced Column Bar Chart | `AdvancedColumnBarChart149CBDF1945A4455952D90C68DD649AA` | Community |
| Clustered Stacked Bar Chart | `ClusteredStackedBarChart39ECD6FE50G` | Community |
| Horizontal Bullet Chart | `horizontalbullechartAD848DB2E71C1BBC88C027512FD82044` | Community |
| Lipstick Column Chart | `lipstickcolumnchartA0919059F5DBE50C75F3D8D6A166710D` | Community |
| Lollipop Chart (alt) | `lollipopChart50393786178B4137A75F3257CB590B96` | Community |
| Lollipop Column Chart (alt) | `lollipopColumnChart0D874BBC87DE40189C387BBA89739F6C` | Community |
| Multi-Card KPIs | `multicardkpis` | Community |
| Data Goods 5 (`dg5...`) | `dg5AAA90EFEFE747CB9357C4FC19B85A58` | Community |
| Dynamic Tooltip | `dynamicTooltip1859AB39DB23051788ADF752BCB90749` | Community |
