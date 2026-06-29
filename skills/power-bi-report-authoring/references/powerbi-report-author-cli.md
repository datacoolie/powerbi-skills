# `powerbi-report-author` CLI Reference

> Use this when the SKILL.md command table is not enough. The CLI is the source
> of truth for visual types, roles, formatting objects, property names, enum
> values, selectors, expression/value encodings, and PBIR validation.

## Setup

```bash
npm install -g @microsoft/powerbi-report-authoring-cli
powerbi-report-author --version
```

Prerequisite: Node.js 20+.

## Command Catalog

| Command | Purpose | When to Use |
|---|---|---|
| `--help` / `<cmd> --help` | Show syntax and available flags | Before using unfamiliar commands |
| `catalog list` | List all built-in visual types and deprecated entries | Choosing a visual type |
| `catalog describe <type>` | Roles, formatting keys, cardinality | Before creating/editing a visual |
| `formatting list-objects <type>` | Valid `objects.*` keys + VCO keys; flags objects needing id selectors | Before applying formatting |
| `formatting describe-object <type> <object>` | Property names, types, enum values, descriptions; `_selectorHint` | Finding exact property names |
| `formatting describe-property <type> <object> <prop>` | Focused single-property lookup | When you know the object, need one property |
| `formatting search <type> <regex>` | Regex search across formatting objects + VCOs | **When you don't know which object holds a property** |
| `formatting list-vcos` | Enumerate shared visualContainerObjects | Auditing chrome/container surface |
| `formatting effective-properties <type>` | Flattened visual objects + shared VCOs | One-shot snapshot of all formatting surfaces |
| `expr encode --kind <t> <v> [percent]` | Generate correct PBIR value encoding | Writing formatting values |
| `expr decode '<json>'` | Decode a PBIR expression to plain value | Inspecting existing values |
| `theme encode --kind <t> <v>` | Generate plain-JSON value for theme file | Editing theme JSON |
| `theme shade-color <hex> <percent>` | Apply ThemeDataColor shadeColor adjustment | Previewing tinted/shaded theme colors |
| `validate <path>` | Full validation of `.pbip` or `.Report` directory | **After every batch of PBIR edits** |
| `preview-visuals <path> [--with-derived]` | Enumerate every visual with summary + path | Auditing visuals across report |
| `preview-pages <path> [--with-derived]` | Page metadata summary | Quick page overview |
| `preview-filters <path>` | Enumerate report/page/visual filters | Filter audit |
| `preview-themes <path> [--with-derived]` | Registered custom theme summary | Theme audit |
| `doctor` | Environment self-check | First-run setup or troubleshooting |

## Validation Result Handling

Run `powerbi-report-author validate <path-to-.Report-dir>` after every logical
batch of PBIR edits.

- **Fix every error** before Desktop reload. Desktop may reject or misrender invalid PBIR.
- **Review warnings** before proceeding. Unknown visual types or theme visual keys
  usually mean a typo unless the report intentionally uses a custom `.pbiviz`.
- Diagnostics include file paths and JSON paths → jump directly to the broken node.
- For large diagnostics: `--pretty` for readable output, `--out <file>` for full results.

## Expression Encoding Examples

### PBIR (visual.json, page.json)

```bash
# Boolean
powerbi-report-author expr encode --kind bool true
# → {"expr":{"Literal":{"Value":"true"}}}

# Number (decimal)
powerbi-report-author expr encode --kind number 12
# → {"expr":{"Literal":{"Value":"12D"}}}

# Integer
powerbi-report-author expr encode --kind integer 3
# → {"expr":{"Literal":{"Value":"3L"}}}

# String (enum)
powerbi-report-author expr encode --kind text dotted
# → {"expr":{"Literal":{"Value":"'dotted'"}}}

# Color
powerbi-report-author expr encode --kind color "#118DFF"
# → {"solid":{"color":{"expr":{"Literal":{"Value":"'#118DFF'"}}}}}

# Theme color (index 0, no shade)
powerbi-report-author expr encode --kind themecolor 0 0
# → {"solid":{"color":{"expr":{"ThemeDataColor":{"ColorId":0,"Percent":0}}}}}
```

### Theme (theme.json)

```bash
powerbi-report-author theme encode --kind color "#118DFF"
# → "#118DFF" (plain) or {"solid":{"color":"#118DFF"}} (in visualStyles)

powerbi-report-author theme encode --kind number 12
# → 12

powerbi-report-author theme shade-color "#118DFF" -20
# → adjusted hex color
```

## Visual Type Quick Reference

### Modern Types (always use these)

| Type | Purpose |
|---|---|
| `cardVisual` | KPI cards (replaces legacy `card`) |
| `tableEx` | Data tables (replaces legacy `table`) |
| `pivotTable` | Matrices/pivot (replaces legacy `matrix`) |
| `azureMap` | Maps (replaces legacy `map`, `filledMap`) |
| `clusteredBarChart` | Horizontal bar charts |
| `clusteredColumnChart` | Vertical column charts |
| `lineChart` | Line/trend charts |
| `areaChart` | Area charts |
| `lineClusteredColumnComboChart` | Combo charts |
| `donutChart` | Donut/pie charts |
| `waterfallChart` | Waterfall charts |
| `treemap` | Treemaps |
| `funnel` | Funnel charts |
| `scatterChart` | Scatter plots |
| `decompositionTreeVisual` | Decomposition trees |
| `kpi` | KPI indicators |
| `shape` | Rectangles, dividers, containers |
| `textbox` | Static/dynamic text |
| `actionButton` | Navigation buttons |
| `slicer` | Filter slicers |
| `pageNavigator` | Page navigation |
| `image` | Image visuals |

### Never Create (Legacy)

| Legacy Type | Use Instead |
|---|---|
| `card` | `cardVisual` |
| `table` | `tableEx` |
| `matrix` | `pivotTable` |
| `map` | `azureMap` |
| `filledMap` | `azureMap` |

## Selector Pattern Quick Reference

| Type | Syntax | Use Case |
|---|---|---|
| **data** (scope) | `"data": [{"scopeId": {...}}]` | Color a specific category value |
| **data** (wildcard) | `"data": [{"dataViewWildcard": {"matchingOption": N}}]` | All instances (0), instances only (1), totals only (2) |
| **metadata** | `"metadata": "Table.Field"` | Target specific measure/column |
| **id** | `"id": "default"` | User-defined instance (cards, filter cards) |
| **none** (static) | *(no selector)* | Base formatting — lowest priority |
