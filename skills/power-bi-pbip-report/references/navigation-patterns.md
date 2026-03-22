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
