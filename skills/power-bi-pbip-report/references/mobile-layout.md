# Mobile Layout

Guidelines and templates for mobile-optimized Power BI report layouts.

---

## Mobile Design Rules

1. **Single column layout** — Stack visuals vertically, full width
2. **KPIs first** — Most important numbers at the very top
3. **Reduce visual count** — Show only essential visuals; hide secondary charts
4. **Larger touch targets** — Slicers and buttons minimum 44px height
5. **Simplify tables** — Fewer columns, larger font

## Mobile Layout Template

```
Phone Canvas (360×640):
┌──────────────────────┐
│ card-kpi-1 (0,0)     │
│ card-kpi-2 (0,70)    │
│ card-kpi-3 (0,140)   │
├──────────────────────┤
│ lineChart-trend      │
│ (0,220 → 360×200)   │
├──────────────────────┤
│ clusteredBarChart    │
│ (0,430 → 360×200)   │
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
