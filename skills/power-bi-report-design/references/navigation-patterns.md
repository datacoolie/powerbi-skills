# Navigation Patterns

Reusable navigation patterns for Power BI PBIR reports.

---

## Page Navigation Buttons

Use `actionButton` visuals to navigate between report pages:

```json
{
  "name": "actionButton-go-to-detail",
  "position": { "x": 10, "y": 680, "width": 120, "height": 30, "z": 5000, "tabOrder": 9000 },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "icon": [{ "properties": {
        "shapeType": { "expr": { "Literal": { "Value": "'ArrowRight'" } } }
      }}],
      "text": [{ "properties": {
        "text": { "expr": { "Literal": { "Value": "'View Details →'" } } }
      }}],
      "action": [{ "properties": {
        "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
        "destination": { "expr": { "Literal": { "Value": "'detail-page'" } } }
      }}]
    }
  }
}
```

## Bookmark Navigation (Tab Selector)

Use bookmarks to create tab-like navigation within a single page. Each
bookmark shows/hides a group of visuals to simulate tabbed content.

1. Create a bookmark for each "tab state" in `bookmarks/`
2. Add `actionButton` visuals styled as tabs
3. Each button's action points to a bookmark

```json
// bookmarks/bookmarks.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json",
  "bookmarkOrder": ["tab-sales", "tab-profit", "tab-orders"]
}

// bookmarks/tab-sales.bookmark.json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json",
  "name": "tab-sales",
  "displayName": "Sales Tab",
  "explorationState": {
    "version": "2.0",
    "activeSection": "analysis-page",
    "sections": {
      "analysis-page": {
        "visualContainers": {
          "group-sales-visuals": { "isHidden": false },
          "group-profit-visuals": { "isHidden": true },
          "group-orders-visuals": { "isHidden": true }
        }
      }
    }
  }
}
```

## Back Button (for Drillthrough Pages)

Always include a back button on drillthrough pages:

```json
{
  "name": "actionButton-back",
  "position": { "x": 10, "y": 10, "width": 80, "height": 30, "z": 5000 },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "icon": [{ "properties": {
        "shapeType": { "expr": { "Literal": { "Value": "'Back'" } } }
      }}],
      "text": [{ "properties": {
        "text": { "expr": { "Literal": { "Value": "'← Back'" } } }
      }}],
      "action": [{ "properties": {
        "type": { "expr": { "Literal": { "Value": "'Back'" } } }
      }}]
    }
  }
}
```

## Reset Filters Button

A button that resets all slicer selections via a bookmark:

```json
// Create a "reset" bookmark with all slicers at default state
// Then create a button pointing to that bookmark:
{
  "name": "actionButton-reset-filters",
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "text": [{ "properties": {
        "text": { "expr": { "Literal": { "Value": "'Reset Filters'" } } }
      }}],
      "action": [{ "properties": {
        "type": { "expr": { "Literal": { "Value": "'Bookmark'" } } },
        "bookmark": { "expr": { "Literal": { "Value": "'reset-all-filters'" } } }
      }}]
    }
  }
}
```

---

## Multi-Level Navigation (Hub-and-Spoke)

For reports with many pages, use a hub page that links to section landing
pages, which then link to detail pages.

```
┌─────────────────────────────────────────────┐
│                  Hub Page                    │
│  [Sales]  [Finance]  [Operations]  [HR]     │
└──┬──────────┬───────────┬──────────┬────────┘
   │          │           │          │
   ▼          ▼           ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Sales  │ │Finance │ │  Ops   │ │  HR    │
│Overview│ │Overview│ │Overview│ │Overview│
│[Detail]│ │[Detail]│ │[Detail]│ │[Detail]│
│[Trend] │ │[P&L]  │ │[Shift] │ │[Head-  │
│        │ │        │ │        │ │ count] │
└────────┘ └────────┘ └────────┘ └────────┘
```

### Hub Page Navigation Buttons

Style buttons as cards with icons and descriptions:

```json
{
  "name": "actionButton-nav-sales",
  "position": { "x": 50, "y": 200, "width": 350, "height": 200, "z": 5000 },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "icon": [{ "properties": {
        "shapeType": { "expr": { "Literal": { "Value": "'Blank'" } } }
      }}],
      "text": [{ "properties": {
        "text": { "expr": { "Literal": { "Value": "'Sales Analytics\\nRevenue, growth, and customer insights'" } } },
        "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
        "fontSize": { "expr": { "Literal": { "Value": "14D" } } }
      }}],
      "fill": [{ "properties": {
        "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#2B579A'" } } } } }
      }}],
      "action": [{ "properties": {
        "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
        "destination": { "expr": { "Literal": { "Value": "'sales-overview'" } } }
      }}]
    }
  }
}
```

---

## Breadcrumb Navigation

Show the user's current location in the report hierarchy using a text
visual + navigation buttons.

### Breadcrumb Pattern

```
[Home] > [Sales] > Product Detail
```

Implement with a row of action buttons + separator text visuals:

```json
// Breadcrumb "Home" link
{
  "name": "actionButton-breadcrumb-home",
  "position": { "x": 10, "y": 8, "width": 50, "height": 24, "z": 10000 },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "text": [{ "properties": {
        "text": { "expr": { "Literal": { "Value": "'Home'" } } },
        "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } } } },
        "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
        "fontUnderline": { "expr": { "Literal": { "Value": "true" } } }
      }}],
      "fill": [{ "properties": {
        "transparency": { "expr": { "Literal": { "Value": "100L" } } }
      }}],
      "outline": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "false" } } }
      }}],
      "action": [{ "properties": {
        "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
        "destination": { "expr": { "Literal": { "Value": "'hub-page'" } } }
      }}]
    }
  }
}
```

Place separator shapes (text: " > ") between breadcrumb links. The last
item is plain text (not a button) showing the current page name.

---

## Page Navigator (Built-In)

Power BI's built-in page navigator creates automatic buttons for all pages.
In PBIR, it's a visual of type `pageNavigator`:

```json
{
  "name": "page-navigator",
  "position": { "x": 0, "y": 880, "width": 1664, "height": 56, "z": 15000 },
  "visual": {
    "visualType": "pageNavigator",
    "objects": {
      "general": [{ "properties": {
        "orientation": { "expr": { "Literal": { "Value": "'Horizontal'" } } },
        "showHiddenPages": { "expr": { "Literal": { "Value": "false" } } },
        "showTooltipPages": { "expr": { "Literal": { "Value": "false" } } }
      }}],
      "buttonShape": [{ "properties": {
        "roundEdge": { "expr": { "Literal": { "Value": "8L" } } }
      }}],
      "selectedButton": [{ "properties": {
        "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#2B579A'" } } } } },
        "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } }
      }}],
      "unselectedButton": [{ "properties": {
        "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F2F2F2'" } } } } },
        "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#333333'" } } } } }
      }}]
    }
  }
}
```

### When to Use Each Pattern

| Pattern | Best For |
|---|---|
| Page Navigator | Simple reports, 3-7 pages, all pages visible |
| Bookmark tabs | Multi-view on single page, toggle chart/table |
| Hub-and-spoke | Large reports, 10+ pages, multiple domains |
| Breadcrumbs | Deep hierarchies, drillthrough chains |
| Back button | Drillthrough pages (required) |
| Reset filters | Any page with slicers |
