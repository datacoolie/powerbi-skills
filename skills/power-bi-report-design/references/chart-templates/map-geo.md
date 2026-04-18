# Recipe: Map (Geographic)

- **id:** `map-geo`
- **Visual type:** `filledMap` (choropleth) OR `azureMap` (point overlay) OR `shapeMap`
- **Typical size:** 800 × 480

---

## Composition

```
     ┌──────────────────────────────────────────────────┐
     │                                                  │
     │        [[region shaded by metric intensity]]    │
     │                                                  │
     │   legend: low ░░░░▒▒▒▓▓▓███ high                │
     │                                                  │
     └──────────────────────────────────────────────────┘
```

Two distinct use cases — pick one:
1. **Choropleth** (filledMap / shapeMap): fill regions by magnitude (population, sales, etc.)
2. **Point overlay** (azureMap): plot individual locations, size by value, color by category

---

## Slots

| Slot | Choropleth binding | Point-overlay binding |
|---|---|---|
| Location | `Geography.Country` / `State` / `PostalCode` | `Location.City` or lat/lon pair |
| Category (optional) | — | `Location.Type` (color) |
| Size | `[Sales]` (fill intensity) | `[Revenue]` (bubble size) |
| Tooltip | KPI measures | KPI measures |

For `azureMap`, lat/lon categories must be marked as `Latitude` / `Longitude` in the model.

---

## Formatting (theme-aware)

- **Fill color ramp:** sequential (`data0` light → `data0` dark). Never rainbow; never diverging unless the metric has a meaningful midpoint
- **Zero / null:** render as `background2` (not white, not `good`)
- **Bubble color:** category colors from theme `data0..dataN` tokens (max 5 categories)
- **Zoom / pan:** enabled for filledMap; disable for shopfloor / kiosk displays (`Controls > Zoom = off`)
- **Base map:** neutral gray style — never photo-satellite unless terrain is genuinely relevant

---

## Narrative frame

- **Executive:** title the map with the insight ("West region drives 60% of growth"). Add a callout annotation on the highest region.
- **Analytical:** pair the map with a bar chart of the same dimension — map for pattern, bar for ranking
- **Operational:** point overlay with threshold-colored bubbles (`good` / `bad`) and site labels

---

## Do NOT

- Use a map when the geography isn't the story — a sorted bar chart is usually clearer for ranking
- Use rainbow color scales — misleading ordering signal
- Use bubble sizes proportional to radius (not area) — 2× radius = 4× area and viewers are deceived
- Use maps for < 5 locations (just use a bar chart with region labels)
- Rely on Bing map matching without validating — mis-geocoded points are common

---

## Data quality gotchas

- **Geocoding ambiguity:** "Portland" resolves to OR or ME — always include country/state columns and mark with Data Category
- **Missing shapes:** shapeMap requires a TopoJSON file in StaticResources for custom regions
- **Projection distortion:** Mercator exaggerates high latitudes — a map colored by Greenland looks overweighted
- **Density vs magnitude:** absolute values (total sales) inflate big regions — consider per-capita or per-store normalization

---

## Checklist

- [ ] Data category set on location columns (Country / City / State / ZIP)
- [ ] Single-hue sequential fill (not rainbow)
- [ ] Nulls rendered as `background2`, not green
- [ ] Accompanying ranked list (bar or table) on the same page
- [ ] Bubble size = area-scaled (Power BI default is correct — confirm not overridden)
- [ ] Alt text: "Map of <metric> by <geography>, highest in <top region>"
