# Required Properties per File

Detailed required and optional properties for each PBIR JSON file.
The JSON template files show the complete structure — this file documents every field.

---

## report.json

- **Required**: `$schema`, `themeCollection`
- `themeCollection.baseTheme` needs: `name`, `reportVersionAtImport` (object with `visual`, `page`, `report` semver strings), `type`
- **Optional**: `settings`, `resourcePackages`, `publicCustomVisuals`, `filterConfig`, `annotations`

### Theme Selection

**Always apply a custom theme** that matches the report's topic, industry, or brand identity.
Ready-to-use theme JSON files are in `references/themes/`. Copy the appropriate file into
`StaticResources/RegisteredResources/` and reference it in `report.json`.

| Report Topic | Theme File | Primary Palette |
|---|---|---|
| Financial / P&L / Corporate | `corporate-financial.json` | Navy #003052, Gold #D4A846, Steel #6B7A8D |
| Sales / Revenue / CRM | `sales-revenue.json` | Azure #0078D4, Teal #00B7C3, Coral #E74856 |
| Manufacturing / Operations | `manufacturing-operations.json` | Industrial #2B5797, Safety #E8980C, Gray #7A7574 |
| Healthcare / Pharma | `healthcare-pharma.json` | Medical #0077B6, Cyan #48CAE4, Teal #00B4D8 |
| Supply Chain / Logistics | `supply-chain-logistics.json` | Navy #012A4A, Blue #2A6F97, Sky #468FAF |
| Retail / Consumer / FMCG | `retail-consumer.json` | Green #3CB043, Sage #98BF64, Accent #3599B8 |
| Sustainability / ESG | `sustainability-esg.json` | Forest #2D6A4F, Mint #52B788, Earth #D4A846 |
| Technology / IT Monitoring | `technology-it.json` | Fluent #0078D4, Cyan #50E6FF, Purple #9B59B6 |

> **Semantic colors** — all themes set: `good: #38B64B` (green), `bad: #EE1C25` (red), `neutral: #949599` (gray).
> Use these for status indicators (succeeded/failed/skipped, above/below target, on-track/at-risk/off-track).
> See `../../power-bi-report-design/references/theme-colors.md` for full semantic color tables, conditional formatting patterns, and colorblind-safe alternatives.

To apply a custom theme, place the theme JSON file in `StaticResources/RegisteredResources/`
and reference it in `report.json` → `themeCollection.customTheme`:

```json
"themeCollection": {
  "baseTheme": {
    "name": "CY24SU10",
    "reportVersionAtImport": { "visual": "2.1.0", "report": "2.1.0", "page": "2.0.0" },
    "type": "SharedResources"
  },
  "customTheme": {
    "name": "my-custom-theme.json",
    "reportVersionAtImport": { "visual": "2.1.0", "report": "2.1.0", "page": "2.0.0" },
    "type": "RegisteredResources"
  }
}
```

## page.json

- **Required**: `$schema`, `name`, `displayName`, `displayOption`
- `displayOption`: `"FitToPage"` | `"FitToWidth"` | `"ActualSize"`
- **Optional**: `height`, `width`, `type` (`"Drillthrough"` | `"Tooltip"`), `visibility` (`"HiddenInViewMode"`), `pageBinding`, `visualInteractions`, `filterConfig`, `objects`, `annotations`

## visual.json

- **Required**: `$schema`, `name`, `position` (needs `x`, `y`, `height`, `width`)
- Must have one of: `visual` or `visualGroup`
- `visual` requires only `visualType`; `query` with `queryState` needed for data-bound visuals
- **Optional**: `position.z`, `position.tabOrder`, `filterConfig`, `isHidden`, `parentGroupName`, `annotations`

## pages.json

- **Required**: `$schema`
- **Optional**: `pageOrder` (array of page name strings), `activePageName`

## version.json

- **Required**: `$schema`, `version` (pattern: `major.minor.0`, e.g. `"2.0.0"`)

## definition.pbir

- **Required**: `$schema`, `version`, `datasetReference`
- `datasetReference` uses either `byPath` (relative path) or `byConnection` (connection string)

## reportExtensions.json

- **Required**: `$schema`
- Contains report-level measures. Only present when the report defines report-level measures.
- **Optional**: `entities` (array of entity definitions with measures)

## mobile.json (per visual)

- **Required**: `$schema`
- Contains mobile layout overrides: position, size, formatting on mobile.
- Located alongside `visual.json` inside each visual's folder.

---

## Theme JSON: Visual Styles and Style Presets

To set **default formatting for all visuals of a given type** across the report, use the `visualStyles`
section in a custom theme JSON file (placed in `StaticResources/RegisteredResources/`):

```json
"visualStyles": {
  "<visualName>": {
    "*": {
      "<cardName>": [{
        "<propertyName>": <propertyValue>
      }]
    }
  }
}
```

- `"*"` as visualName targets **all** visual types
- `"*"` as stylePresetName is the **default** style
- Named presets (e.g., `"Demo Preset 1"`) appear in the Style dropdown on the visual

**Finding property names**: Save report as PBIP, enable "Copy object names" in Options → Report settings,
right-click a formatted visual → Copy object name, search in VS Code. The `objects` node in
PBIR files shows the property names; translate to theme format by removing the `expr`/`Literal` wrappers.

---

## Conditional Formatting (Tables/Matrices)

Conditional formatting applies to values in tables and matrices — not columns/rows.
Types: **Background color**, **Font color**, **Data bars**, **Icons**, **Web URLs**.

Format styles:
- **Gradient** (color scale): min/max color mapped to value range
- **Rules**: value ranges → specific colors (e.g., green/yellow/red thresholds)
- **Field value**: a field containing color names or hex codes drives colors directly

Icon sets: Directional (arrows, triangles), Shapes (traffic lights, circles), Indicators (flags, checkmarks), Ratings (stars, bars).

---

## Custom Format Strings

Format strings exist at three levels (higher overrides lower):
1. **Model** — set in Properties pane (VBA syntax: `m/d/yyyy`, `h:nn AM/PM`)
2. **Visual** — set in Format pane → Format data (**.NET syntax**: `M/d/yyyy`, `h:mm tt`)
3. **Element** — set on data labels/card elements (overrides both)

Common numeric formats: `#,##0` (thousands sep), `#,##0.00` (2dp), `0%` (percent), `$#,##0.00` (currency).
