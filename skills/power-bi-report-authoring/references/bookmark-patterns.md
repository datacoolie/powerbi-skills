# Bookmark Patterns (PBIR JSON)

Complete bookmark implementation patterns for PBIP/PBIR format reports,
covering toggle visibility, page navigation, slicer state capture,
and spotlight/focus mode bookmarks.

---

## Bookmark Architecture in PBIR

Bookmarks in PBIR format are stored as individual JSON files:

```
<Report>.Report/
└── definition/
    ├── bookmarks.json              ← Bookmark registry (list + groups)
    └── bookmarks/
        ├── bookmark-id-1.bookmark.json
        ├── bookmark-id-2.bookmark.json
        └── ...
```

### bookmarks.json — Registry

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarks/1.0.0/schema.json",
    "bookmarkGroups": [
        {
            "displayName": "Navigation Tabs",
            "name": "BookmarkGroup_nav"
        },
        {
            "displayName": "Toggle Views",
            "name": "BookmarkGroup_toggle"
        }
    ],
    "bookmarks": [
        {
            "displayName": "Tab - Sales",
            "name": "Bookmark_tab_sales",
            "explorationState": {
                "report": {
                    "activeSection": "ReportSection_sales"
                }
            }
        },
        {
            "displayName": "Tab - Finance",
            "name": "Bookmark_tab_finance",
            "explorationState": {
                "report": {
                    "activeSection": "ReportSection_finance"
                }
            }
        }
    ]
}
```

---

## Toggle Visibility Bookmarks

Toggle between two visual states (e.g., chart view vs table view)
on the same page.

### Pattern: Chart/Table Toggle

Create two bookmarks — one showing the chart, one showing the table.
Both capture only visual visibility (not filters or slicers).

**Bookmark file: `show-chart.bookmark.json`**

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/1.0.0/schema.json",
    "name": "Bookmark_show_chart",
    "displayName": "Show Chart View",
    "explorationState": {
        "report": {
            "activeSection": "ReportSection_analysis"
        },
        "sections": {
            "ReportSection_analysis": {
                "visualContainers": {
                    "visual_chart_1": {
                        "singleVisual": {
                            "display": {
                                "mode": "visible"
                            }
                        }
                    },
                    "visual_table_1": {
                        "singleVisual": {
                            "display": {
                                "mode": "hidden"
                            }
                        }
                    },
                    "btn_show_chart": {
                        "singleVisual": {
                            "display": {
                                "mode": "hidden"
                            }
                        }
                    },
                    "btn_show_table": {
                        "singleVisual": {
                            "display": {
                                "mode": "visible"
                            }
                        }
                    }
                }
            }
        }
    },
    "options": {
        "targetVisualType": "unchanged",
        "applyData": false,
        "applyDisplay": true,
        "applyCurrentFilters": false,
        "applyAllSlicers": false,
        "applySelectedBookmarkSlicers": false,
        "isDisabledSpotlight": true,
        "includeSelectedBookmarkSlicers": []
    }
}
```

**Bookmark file: `show-table.bookmark.json`**

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/1.0.0/schema.json",
    "name": "Bookmark_show_table",
    "displayName": "Show Table View",
    "explorationState": {
        "report": {
            "activeSection": "ReportSection_analysis"
        },
        "sections": {
            "ReportSection_analysis": {
                "visualContainers": {
                    "visual_chart_1": {
                        "singleVisual": {
                            "display": {
                                "mode": "hidden"
                            }
                        }
                    },
                    "visual_table_1": {
                        "singleVisual": {
                            "display": {
                                "mode": "visible"
                            }
                        }
                    },
                    "btn_show_chart": {
                        "singleVisual": {
                            "display": {
                                "mode": "visible"
                            }
                        }
                    },
                    "btn_show_table": {
                        "singleVisual": {
                            "display": {
                                "mode": "hidden"
                            }
                        }
                    }
                }
            }
        }
    },
    "options": {
        "targetVisualType": "unchanged",
        "applyData": false,
        "applyDisplay": true,
        "applyCurrentFilters": false,
        "applyAllSlicers": false,
        "applySelectedBookmarkSlicers": false,
        "isDisabledSpotlight": true,
        "includeSelectedBookmarkSlicers": []
    }
}
```

### Key Options Explained

| Option | Value | Effect |
|---|---|---|
| `applyData` | `false` | Don't change data bindings |
| `applyDisplay` | `true` | Apply visibility changes |
| `applyCurrentFilters` | `false` | Don't capture filter state |
| `applyAllSlicers` | `false` | Don't capture slicer state |
| `isDisabledSpotlight` | `true` | Don't apply spotlight/focus mode |

---

## Slicer State Bookmarks

Capture specific slicer selections to create "preset views."

### Pattern: Pre-configured Filter Presets

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/1.0.0/schema.json",
    "name": "Bookmark_preset_north",
    "displayName": "North Region Preset",
    "explorationState": {
        "report": {
            "activeSection": "ReportSection_sales"
        },
        "sections": {
            "ReportSection_sales": {
                "visualContainers": {
                    "slicer_region": {
                        "singleVisual": {
                            "objects": {
                                "data": [{
                                    "properties": {
                                        "filterValues": {
                                            "filter": {
                                                "Where": [{
                                                    "Condition": {
                                                        "In": {
                                                            "Expressions": [{
                                                                "Column": {
                                                                    "Expression": {
                                                                        "SourceRef": { "Entity": "Geography" }
                                                                    },
                                                                    "Property": "Region"
                                                                }
                                                            }],
                                                            "Values": [
                                                                [{ "Literal": { "Value": "'North'" } }]
                                                            ]
                                                        }
                                                    }
                                                }]
                                            }
                                        }
                                    }
                                }]
                            }
                        }
                    }
                }
            }
        }
    },
    "options": {
        "targetVisualType": "unchanged",
        "applyData": false,
        "applyDisplay": false,
        "applyCurrentFilters": false,
        "applyAllSlicers": true,
        "applySelectedBookmarkSlicers": false,
        "isDisabledSpotlight": true
    }
}
```

---

## Reset All Filters Bookmark

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/1.0.0/schema.json",
    "name": "Bookmark_reset_all",
    "displayName": "Reset All Filters",
    "explorationState": {
        "report": {
            "activeSection": "ReportSection_sales"
        }
    },
    "options": {
        "targetVisualType": "unchanged",
        "applyData": false,
        "applyDisplay": false,
        "applyCurrentFilters": true,
        "applyAllSlicers": true,
        "applySelectedBookmarkSlicers": false,
        "isDisabledSpotlight": true
    }
}
```

---

## Bookmark Groups

Group related bookmarks in the bookmarks.json registry:

```json
{
    "bookmarkGroups": [
        {
            "displayName": "Navigation",
            "name": "BookmarkGroup_nav"
        },
        {
            "displayName": "View Toggle",
            "name": "BookmarkGroup_views"
        },
        {
            "displayName": "Presets",
            "name": "BookmarkGroup_presets"
        }
    ],
    "bookmarks": [
        {
            "displayName": "Tab - Sales",
            "name": "Bookmark_tab_sales",
            "bookmarkGroup": "BookmarkGroup_nav",
            "explorationState": { "..." : "..." }
        },
        {
            "displayName": "Show Chart",
            "name": "Bookmark_show_chart",
            "bookmarkGroup": "BookmarkGroup_views",
            "explorationState": { "..." : "..." }
        },
        {
            "displayName": "North Region",
            "name": "Bookmark_preset_north",
            "bookmarkGroup": "BookmarkGroup_presets",
            "explorationState": { "..." : "..." }
        }
    ]
}
```

---

## Button → Bookmark Binding

Assign a bookmark action to a button in `visual.json`:

```jsonc
// Button visual.json excerpt
{
    "visual": {
        "visualType": "actionButton",
        "objects": {
            "icon": [{
                "properties": {
                    "shapeType": { "expr": { "Literal": { "Value": "'Blank'" } } }
                }
            }],
            "action": [{
                "properties": {
                    "type": {
                        "expr": { "Literal": { "Value": "'Bookmark'" } }
                    },
                    "bookmark": {
                        "expr": { "Literal": { "Value": "'Bookmark_show_chart'" } }
                    }
                }
            }],
            "text": [{
                "properties": {
                    "text": { "expr": { "Literal": { "Value": "'Chart View'" } } },
                    "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } }
                }
            }],
            "fill": [{
                "properties": {
                    "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#2B579A'" } } } } }
                }
            }]
        }
    }
}
```

---

## Quick Reference

| Pattern | Options to Set |
|---|---|
| Tab navigation | `applyDisplay: false`, navigate via `activeSection` |
| Toggle visibility | `applyDisplay: true`, all others `false` |
| Filter presets | `applyAllSlicers: true`, all others `false` |
| Reset filters | `applyCurrentFilters: true`, `applyAllSlicers: true` |
| Spotlight mode | `isDisabledSpotlight: false`, target specific visual |
| Combined (nav + filter) | `applyDisplay: true`, `applyAllSlicers: true` |

| File | Purpose |
|---|---|
| `bookmarks.json` | Registry of all bookmarks + groups |
| `bookmarks/<name>.bookmark.json` | Individual bookmark state definition |
| Button `visual.json` | Bookmark action binding on buttons |
