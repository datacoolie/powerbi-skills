# Azure Map Visual Authoring Guide

## Overview

Always use `azureMap` as the visual type for map visuals.

**Do not use `map` or `filledMap`** — they are legacy Bing Maps visuals and
must never be created. `powerbi-report-author validate` raises
`PBIR_VISUAL_TYPE_DEPRECATED` (warning) on these types.

### When a Map Fails to Render

Azure Maps can fail to geocode or render for a variety of reasons (unsupported
data format, ambiguous location names, missing coordinates). When this happens:

1. **Debug the problem** — check field names, data values, geocoding compatibility
2. **Try alternative geographic fields or coordinates** — try lat/lon columns, a
   more specific location column, or a different aggregation level (e.g., country
   instead of city)
3. **Ask the user for clarification** — if you cannot resolve the geocoding issue,
   use `ask_user` to describe the problem and ask which field to use or whether
   lat/lon columns are available
4. **Do not silently substitute a non-map visual** for data/geocoding issues — if
   the user explicitly requested a map and the underlying geography is workable,
   `ask_user` before changing visual types. Substituting a non-map visual for a
   resolvable data problem violates the design brief.
5. **When Azure Maps is unavailable in the environment** (e.g., disabled by tenant
   policy, unsupported region), fall back to a non-map encoding such as a
   `tableEx` of locations with conditional formatting or a `barChartClustered` by
   region — and tell the user why the map was replaced. Avoid the legacy `map`,
   `filledMap`, and `shapeMap` visuals as fallbacks. This matches the operational
   monitor archetype's map guidance
   ([archetype reference](../../powerbi-report-design/references/archetypes/operational-monitor.md)).

---

## Template

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
  "name": "<20hexchars>",
  "position": { "x": 20, "y": 20, "z": 0, "height": 400, "width": 610, "tabOrder": 0 },
  "visual": {
    "visualType": "azureMap",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "<TableName>" } },
                  "Property": "<LocationColumnName>"
                }
              },
              "queryRef": "<TableName>.<LocationColumnName>",
              "active": true
            }
          ]
        },
        "Size": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "<TableName>" } },
                  "Property": "<MeasureName>"
                }
              },
              "queryRef": "<TableName>.<MeasureName>",
              "active": true
            }
          ]
        }
      }
    },
    "objects": {}
  }
}
```

## Roles

| Role | Display Name | Kind | Required | Max |
|------|-------------|------|----------|-----|
| Category | Location | Grouping | ✅ | — |
| Size | Size | Measure | — | 1 |
| Series | Legend | Grouping | — | 1 |
| Y | Latitude | GroupingOrMeasure | — | 1 |
| X | Longitude | GroupingOrMeasure | — | 1 |
| Tooltips | Tooltips | Measure | — | — |

> **Tip**: Bind a geographic column (country, state, city) to `Category`.
> Azure Maps handles geocoding automatically — no explicit lat/lon needed
> unless you have coordinate data.
