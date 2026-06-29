# Mobile Layout

Guidelines and templates for mobile-optimized Power BI report layouts.
Based on *Power BI — Create Reports* (Microsoft, 2025).

---

## Mobile Design Rules

1. **Single column layout** — Stack visuals vertically, full width (max 323pt)
2. **KPIs first** — Most important numbers at the very top
3. **Reduce visual count** — Show only essential visuals; hide secondary charts
4. **Larger touch targets** — Slicers and buttons minimum 44px height
5. **Simplify tables** — Fewer columns, larger font
6. **Build desktop and mobile together** — Design both layouts at the same time for coherence
7. **No side-by-side visuals** — Except single-element visuals (cards, KPIs, buttons)
8. **6-8pt minimum spacing** — Between all elements, both vertically and horizontally
9. **Expand visuals to full width** — Use 323pt (max canvas width); a default margin is included
10. **Avoid nested scrollbars** — Set visual height so all elements are visible without internal scroll

---

## Auto-Create Mobile Layout

The auto-create feature generates a starting mobile view automatically:

- Reads the desktop layout **horizontally, left-to-right from the top**
- Stacks visuals vertically on the mobile canvas
- Cannot process **background images** — these are ignored
- Preserves functionality as much as possible
- Use as a **starting point**, then refine with manual formatting

---

## Mobile Formatting Best Practices

### Font Sizes
- Desktop font sizes are usually too large for mobile
- Reduce card/KPI font sizes to fit; use **display units** (M, K) to save space
- **Minimum font size: 9pt** — don't go smaller

### Visual Optimization
- Turn off **legends** and **X-axis labels** when they waste space
- Turn on **data labels** instead (centered on bars)
- Toggle off **responsive** mode if it interferes with formatting:
  `General > Properties > Advanced Options > Responsive = Off`

### Slicers for Mobile
- Make slicers **horizontal** instead of vertical
- Use **dropdown** mode to save space
- Responsive slicers shrink to a filter icon at small sizes
- **Important**: Slicer selections do NOT carry between mobile
  and web layout — they are independent filter contexts

### Page Navigators
- Change **Grid layout orientation** to horizontal in Visualizations pane
- Use a line shape underneath as a design accent

### Formatting Independence
- When you change a format setting in mobile layout, it **disconnects**
  from the desktop setting and becomes independent
- Use "Clear mobile changes" to re-sync with desktop values

---

## Minimum Recommended Visual Sizes

| Size Class | Min Width (pt) | Min Height (pt) | Visuals |
|---|---|---|---|
| **XL** | 323 | 270 | Map, Filled map, Matrix, Table, Multi-row card, Decomposition tree, Key influencers, Shape map |
| **L** | 323 | 180 | Bar chart, Column chart, Line chart, Area chart, Combo chart, Donut, Pie, Funnel, Ribbon, Scatter, Treemap, Waterfall, Stacked charts, List slicer, Card (New) |
| **M** | 323 | 100 | Continuous slicer, Tile slicer, Relative date slicer, Bookmark navigator, Page navigator, Dropdown slicer, Textbox |
| **S** | 158 | 100 | Button, Card, Gauge, KPI, Shape |

---

## Considerations and Limitations

- **Tooltips are disabled** on the mobile canvas — don't rely on tooltips for key info
- **Background images** are not supported in auto-create
- **Visual interactions** work on the mobile canvas (test during design)
- **Layering** must be adjusted in the Selection pane
- **Appearance** (show/hide) can only be changed in the desktop layout view
- Mobile layout is displayed **only in the Power BI mobile apps** (iOS/Android)
- Web browsers always show the standard desktop view
- When the phone is rotated to **landscape**, the non-optimized desktop view appears

---

## Mobile Layout Template

```
Phone Canvas (360×640):
┌──────────────────────┐
│ card-kpi-1 (0,0)     │  S-class: 158×100
│ card-kpi-2 (0,70)    │
│ card-kpi-3 (0,140)   │
├──────────────────────┤
│ dropdown-slicer      │  M-class: 323×100
│ (0,210 → 323×50)    │
├──────────────────────┤
│ lineChart-trend      │  L-class: 323×180
│ (0,270 → 323×180)   │
├──────────────────────┤
│ clusteredBarChart    │  L-class: 323×180
│ (0,460 → 323×180)   │
└──────────────────────┘
```

## mobile.json Example

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainerMobileState/2.3.0/schema.json",
  "position": {
    "x": 0,
    "y": 0,
    "width": 360,
    "height": 70,
    "z": 1000
  }
}
```

Place this file at `pages/<page>/visuals/<visual>/mobile.json` to define how
that visual appears in the mobile phone layout view.
