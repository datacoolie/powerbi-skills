---
name: power-bi-pbip-report
description: >-
  Generate Power BI reports in PBIP/PBIR format by producing the complete .Report/ folder
  structure with all required JSON files (report.json, page.json, visual.json, pages.json, etc.).
  Use this skill whenever a Design Spec is ready and the user asks to generate, scaffold, or
  build the actual PBIR JSON files for a Power BI report. Also use when adding pages or visuals
  to an existing PBIP report, or converting a design into PBIR folder output.
  This skill handles JSON generation and validation only — not design decisions.
  For report design (chart selection, layout, theme, storytelling), use `power-bi-report-design` first.
---

# Power BI PBIP Report Generation

Generate Power BI reports in **PBIR (Power BI Enhanced Report)** format — the file-based
report definition used in PBIP projects. This skill produces the complete `.Report/` folder
with all JSON files that Power BI Desktop and the Power BI service can open directly.

**Input:** A Design Spec from the `power-bi-report-design` skill (or equivalent user instructions)
specifying pages, visuals, layout positions, theme, and navigation.

Canvas size: **1664 × 936** (standard Power BI canvas). Tooltip pages: **320 × 240**.

## Reference Files

| Reference | When to Read |
|---|---|
| `references/folder-structure.md` | Understanding the full PBIR folder layout |
| `references/visual-templates.md` | Generating `visual.json` — complete JSON templates per visual type, field expression patterns |
| `references/custom-visuals.md` | Custom visual identifiers, JSON templates, and query roles |
| `references/formatting-patterns.md` | Advanced formatting: rounded corners, shadows, conditional colors, axis/legend/filter/sort patterns, TOP N filter, drillthrough config, conditional formatting rules (color scales, gradient fills) |
| `references/common-patterns.md` | Reusable components: KPI rows, slicer panels, background shapes, page navigator, visual interactions, TOP N chart, sync slicers (reportExtensions), page-level filters |
| `references/bookmark-patterns.md` | Bookmark JSON: toggle visibility, slicer state capture, reset filters, bookmark groups, button→bookmark binding |
| `references/mobile-layout.md` | Mobile phone layout rules and `mobile.json` template |
| `references/required-properties.md` | Required/optional properties per file, theme selection, conditional formatting, format strings |
| `references/report-template.json` | JSON template for `report.json` |
| `references/page-template.json` | JSON template for `page.json` |
| `references/pages-metadata-template.json` | JSON template for `pages.json` |
| `references/version-template.json` | JSON template for `version.json` |
| `references/definition-pbir-template.json` | JSON template for `definition.pbir` |
| `references/themes/*.json` | Ready-to-use custom theme files (8 industries) — copy to `StaticResources/RegisteredResources/` |
| `scripts/validate_report.js` | **Run after generation** — validates against official Microsoft JSON schemas (preferred) |
| `scripts/validate_report.py` | **Fallback** — validates JSON syntax, required properties, cross-references, naming |
| `scripts/finalize_pbir.py` | **Phase 4c polish** — snap_grid, align_kpi_row, apply_theme_tokens, normalize_fonts, ensure_alt_text. Supports `--dry-run`, `--skip`, `--only`. |
| `scripts/design_quality_check.py` | **Phase 4c lint** — 8 checks (visual counts, drillthrough back button, pie slices, alt text, default page names, bad titles, hardcoded hex, bookmark targets). Use `--style executive\|analytical\|operational` and `--write-report` to emit `design_report.md`. |

## Quick Reference: Folder Structure

```
<ReportName>.Report/
├── definition/
│   ├── report.json              ← Report settings, theme, custom visuals
│   ├── pages/
│   │   ├── <page-name>/
│   │   │   ├── page.json        ← Page config (name, size, type, filters)
│   │   │   └── visuals/
│   │   │       ├── <visual-name>/
│   │   │       │   ├── visual.json   ← Visual type, query, formatting
│   │   │       │   └── mobile.json   ← Mobile layout overrides (optional)
│   │   │       └── ...
│   │   └── ...
│   ├── pages.json               ← Page ordering metadata
│   ├── version.json             ← Schema version metadata
│   ├── bookmarks/               ← Bookmark definitions (optional)
│   │   ├── bookmarks.json       ← Bookmark ordering
│   │   └── <name>.bookmark.json ← Individual bookmark state
│   └── reportExtensions.json    ← Report-level extensions (optional)
├── definition.pbir              ← Dataset binding reference
├── StaticResources/
│   └── RegisteredResources/     ← Images, custom themes, icons
└── CustomVisuals/               ← Embedded custom visual packages (optional)
```

## Naming Convention

### Rules
- Use **lowercase-kebab-case** for all folder and file names (page folders, visual folders)
- Prefix visual folder names with `visualType` for scanability
- Keep names short but descriptive: `card-kpi-revenue`, `lineChart-monthly-trend`

### Page Naming
```
overview                    # Landing/summary page
sales-analysis              # Domain + "analysis"
product-detail              # Entity + "detail" (drillthrough)
customer-tooltip            # Entity + "tooltip" (tooltip page)
```

### Visual Naming
```
card-kpi-revenue            # card + "kpi" + metric
clusteredBarChart-top-10    # visualType + description
lineChart-monthly-trend     # visualType + time grain + metric
slicer-date-range           # slicer + field description
shape-header-bg             # shape + purpose
textbox-page-title          # textbox + purpose
actionButton-back           # actionButton + action
pivotTable-sales-by-region  # pivotTable + dimension breakdown
```

### Bookmark Naming
```
tab-sales                   # tab-{section} for tab navigation
tab-profit
reset-all-filters           # reset-{scope} for reset bookmarks
```

## Workflow

### Step 1: Generate Report-Level Files

These files define the report container. Create them first because page and visual files
reference the theme and settings established here.

1. `definition.pbir` — dataset reference
2. `report.json` — theme, settings, custom visuals registration
3. `pages.json` — page ordering
4. `version.json` — schema version

Use JSON templates from `references/report-template.json`, `references/pages-metadata-template.json`,
`references/version-template.json`, `references/definition-pbir-template.json`.
See `references/required-properties.md` for property details and theme selection guidance.

### Step 2: Generate Pages and Visuals

For each page:
1. Create `page.json` from `references/page-template.json`
2. For each visual, create `visual.json` — read `references/visual-templates.md` for
   complete JSON templates per visual type (includes field expression patterns)
3. Apply formatting — see Formatting Patterns section below; read
   `references/formatting-patterns.md` for advanced patterns
4. Set up visual interactions in `page.json` — see `references/common-patterns.md`

### Step 3: Generate Supporting Files

As needed:
- **Bookmarks**: Create `bookmarks/bookmarks.json` + individual `.bookmark.json` files
  — see `references/bookmark-patterns.md` and `../power-bi-report-design/references/navigation-patterns.md`
- **Mobile**: Add `mobile.json` alongside `visual.json` — see `references/mobile-layout.md`
- **Custom themes**: Place theme JSON in `StaticResources/RegisteredResources/`
- **Images**: Place logos, icons in `StaticResources/RegisteredResources/`
- **Report extensions**: `reportExtensions.json` for report-level measures

### Step 4: Validate Before Completion

Power BI Desktop rejects files with JSON syntax errors silently or with cryptic messages.
**Always validate before telling the user the report is ready.**

**If invoked from the `power-bi-developer` agent (Phase 4c), run the full polish chain first:**

```powershell
# 1. Mechanical polish (snap grid, align KPIs, tokenize theme colors, unify fonts, alt text)
python skills/power-bi-pbip-report/scripts/finalize_pbir.py --report <path-to-.Report-folder>

# 2. Design-quality lint (style-aware: executive / analytical / operational)
python skills/power-bi-pbip-report/scripts/design_quality_check.py `
    --report <path-to-.Report-folder> `
    --style <style-from-design-spec> `
    --write-report

# 3. Schema validation (always last)
node skills/power-bi-pbip-report/scripts/validate_report.js <path-to-.Report-folder>
```

Exit codes: `0` = pass, `1` = warnings only, `2` = errors present (must fix). See
`../power-bi-report-design/references/polisher.md` for the full Phase 4c routing table.

**Preferred** (schema-driven, validates against official Microsoft JSON schemas):
```
node skills/power-bi-pbip-report/scripts/validate_report.js <path-to-.Report-folder>
```

**Fallback** (no Node.js):
```
python skills/power-bi-pbip-report/scripts/validate_report.py <path-to-.Report-folder>
```

Both check:
1. **JSON syntax** — every `.json` and `.pbir` file parses cleanly
2. **Schema validation** — structure matches Microsoft's published JSON schemas (Node.js only)
3. **Required properties** — `$schema`, `name`, `position`, `themeCollection`, etc.
4. **Cross-references** — page folders match `pages.json`, custom visuals registered in `report.json`
5. **Naming conventions** — kebab-case for page and visual folders

Fix all **errors** before delivering. **Warnings** are advisory (naming, unused registrations).  

If neither script is available, manually verify:
- Every JSON file parses (`json.loads()` succeeds)
- Every `visual.json` has `name`, `position` (with `x`, `y`, `height`, `width`), and either `visual` or `visualGroup`
- `pages.json` → `pageOrder` entries match actual page folder names
- `page.json` → `name` matches its parent folder name
- Custom visual types used in visuals are registered in `report.json` → `publicCustomVisuals`

---

## JSON Schema Reference

| File | Schema URL |
|---|---|
| report.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.2.0/schema.json` |
| page.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json` |
| visual.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json` |
| pages.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json` |
| version.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json` |
| definition.pbir | `https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json` |
| bookmark.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json` |
| bookmarks.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json` |
| reportExtensions.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/reportExtension/1.0.0/schema.json` |
| mobile.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainerMobileState/2.3.0/schema.json` |

**Finding the latest version:** Browse available versions at the
[GitHub json-schemas repository](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition).

## Required Properties (Quick Reference)

Each JSON file has a `$schema` property. Beyond that:

| File | Key Required Properties |
|---|---|
| `report.json` | `themeCollection` (with `baseTheme.name`, `reportVersionAtImport`, `type`) |
| `page.json` | `name`, `displayName`, `displayOption` (`"FitToPage"` / `"FitToWidth"` / `"ActualSize"`) |
| `visual.json` | `name`, `position` (`x`, `y`, `height`, `width`), plus `visual` or `visualGroup` |
| `pages.json` | *(only `$schema`)* — `pageOrder` array is optional |
| `version.json` | `version` (e.g. `"2.0.0"`) |
| `definition.pbir` | `version`, `datasetReference` (`byPath` or `byConnection`) |

For full property details, theme selection guidance, conditional formatting, and format strings,
read `references/required-properties.md`. For JSON structure, use the template files.

## Custom Visuals

When a visual uses a **custom visual**, you **must**:

1. **State the marketplace name** and explain why it was chosen over built-in —
   custom visuals add rendering overhead and dependency risk, so the benefit must be clear
2. **Register** the `visualType` identifier in `report.json` → `publicCustomVisuals` array
3. **Use correct query roles** — custom visuals have unique role names (not standard `Category`/`Y`)

Prefer built-in visuals when they can achieve the visualization. Custom visuals shine when
built-in alternatives lack the chart type entirely (e.g., no built-in histogram, Sankey, or
calendar heatmap). Read `references/custom-visuals.md` for all templates, query roles, and identifiers.

### Key Custom Visuals

| visualType | Name | Query Roles | When to Use |
|---|---|---|---|
| `advanceCardE03760C5AB...` | Advance Card | `Data` | Rich KPI with conditional formatting |
| `ChicletSlicer14485...` | Chiclet Slicer | `Category`, `Values` | Image/tile category selection |
| `Timeline1447991079100` | Timeline Slicer | `Time` | Interactive date range slider |
| `BulletChart14433476...` | Bullet Chart | `Category`, `Value`, `TargetValue` | Actual vs target with ranges |
| `TornadoChart14525176...` | Tornado Chart | `Group`, `Values` | Diverging bar (A vs B) |
| `BoxWhiskerChart1455...` | Box & Whisker | `Groups`, `Values`, `Samples` | Distribution analysis |
| `Sunburst1445472000808` | Sunburst | `Nodes`, `Values` | Multi-level hierarchy ring |
| `SankeyDiagram14580...` | Sankey Diagram | `Source`, `Destination`, `Weight` | Flow between categories |
| `RadarChart14234704...` | Radar Chart | `Category`, `Y` | Multi-dimensional scoring |
| `WaffleChart14537768...` | Waffle Chart | `Category`, `Values` | Percentage as discrete blocks |
| `bciCalendarCC0FA2B...` | BCI Calendar | `category`, `measure` | Heatmap calendar view |
| `zebraBiCards2C860C...` | Zebra BI Cards | `Category`, `Values`, `PY`, `AC` | IBCS financial variance cards |
| `Deneb6E97C82C58E5...` | Deneb | *(Vega spec)* | Fully custom Vega/Vega-Lite chart |
| `Gantt1467746032498` | Gantt Chart | `Task`, `StartDate`, `Duration` | Project timeline |
| `WordCloud1447959067750` | Word Cloud | `Category`, `Values` | Word frequency display |

## Visual Type Reference

Read `references/chart-selection-guide.md` for WHICH chart to use — it explains why
certain charts work better than others (bar charts beat pie charts for comparison because
the human eye reads length more accurately than angle/area).

Read `references/visual-templates.md` for complete JSON templates per visual type.
Read `references/custom-visuals.md` for custom visual identifiers, templates, and query roles.

### Query Role Names by Visual Type

| visualType | Query Roles | When to Use |
|---|---|---|
| `card` | `Values` | Single hero KPI |
| `cardVisual` | `Data` | New-style card with reference labels |
| `multiRowCard` | `Values` | 4-8 related KPIs at equal weight |
| `slicer` | `Values` | Filter control — date, category, hierarchy |
| `advancedSlicerVisual` | `Values` | Tile-based visual slicer |
| `clusteredBarChart` | `Category`, `Y` | **Default for category comparison** — horizontal |
| `clusteredColumnChart` | `Category`, `Y` | Vertical bars — time on x-axis or ≤8 categories |
| `barChart` | `Category`, `Y` | Stacked horizontal — part-of-whole |
| `columnChart` | `Category`, `Y` | Stacked vertical — part-of-whole with time |
| `lineChart` | `Category`, `Y` | **Default for trends over time** |
| `areaChart` | `Category`, `Y` | Filled area — single series where volume matters |
| `lineClusteredColumnComboChart` | `Category`, `Y`, `Y2` | Combo — only when two scales truly needed |
| `waterfallChart` | `Category`, `Y` | Cumulative additions/subtractions |
| `treemap` | `Group`, `Values` | Part-of-whole with many segments (10+) |
| `pivotTable` | `Rows`, `Columns`, `Values` | Matrix — row and column groupings |
| `tableEx` | `Values` | Flat table — row-level detail |
| `funnel` | `Category`, `Y` | Sequential pipeline stages |
| `scatterChart` | `Category`, `X`, `Y`, `Size` | Correlation between two metrics |
| `map` | `Category`, `Size` | Geographic patterns |
| `gauge` | `Y`, `TargetValue`, `MinValue`, `MaxValue` | Single metric vs. target |
| `kpi` | `Indicator`, `TrendAxis`, `Goal` | KPI with trend and target |
| `ribbonChart` | `Category`, `Series`, `Y` | Ranking changes over time |
| `stackedAreaChart` | `Category`, `Y`, `Series` | Cumulative composition over time |

Non-data visuals (no query): `shape`, `basicShape`, `textbox`, `actionButton`, `image`, `pageNavigator`.

### Field Expressions

Three patterns for binding data to visuals: **Column** (dimension), **Measure** (DAX measure),
**Aggregation** (inline Sum/Avg/Count on a column). Each uses `SourceRef.Entity` + `Property`.
See `references/visual-templates.md` → "Field Expression Patterns" for the full JSON templates.

Aggregation `Function` codes: `0`=Sum, `1`=Avg, `2`=Count, `3`=Min, `4`=Max, `5`=CountNonNull.

## Formatting Patterns

### Literal Value Suffixes

All property values in PBIR use `{ "expr": { "Literal": { "Value": "<value>" } } }` format.
The value string has type-specific suffixes:

| Suffix | Type | Example |
|---|---|---|
| `D` | Double/numeric | `"12D"`, `"0.5D"` |
| `L` | Long/integer | `"4L"`, `"0L"` |
| *(none)* | String | `"'text'"` (single-quoted) |
| *(none)* | Boolean | `"true"` or `"false"` |

For advanced formatting (rounded corners, shadows, conditional colors, axis/legend/sort,
theme visual styles, conditional formatting in tables, format strings),
read `references/formatting-patterns.md` and `references/required-properties.md`.

## Slicer Types

| Slicer | visualType | Description |
|---|---|---|
| Original slicer | `slicer` | Vertical list, tile, dropdown styles |
| Button slicer | `advancedSlicerVisual` | Interactive buttons with grid layout, image support, conditional formatting |
| List slicer (preview) | `listSlicer` | Vertical list with hierarchy, search, conditional formatting |
| Text slicer (preview) | `textSlicer` | Free-form text input for exact string matching |

Button slicers support: `Single select`, `Force selection`, conditional formatting on background/border/text,
paste values to select. List slicers support: hierarchical drilling, `Restrict to leaf nodes`, conditional formatting.

## Page Types

| Type | `page.json` config | Typical Size |
|---|---|---|
| Normal page | *(default — no special type)* | 1664×936 (standard) |
| Drillthrough | `"type": "Drillthrough"` + `drillthrough` filter fields in `filterConfig` | Standard canvas |
| Tooltip | `"type": "Tooltip"`, `"visibility": "HiddenInViewMode"` | Use Tooltip canvas preset (small) |
| Hidden page | `"visibility": "HiddenInViewMode"` | Standard canvas |

### Drillthrough Pages

1. Set `"type": "Drillthrough"` in `page.json`
2. Add drillthrough filter fields to the page's `filterConfig`
3. Power BI auto-creates a back button; add `actionButton-back` visual
4. Design visuals for single-entity detail (card + table + trend chart pattern)
5. **Cross-report drillthrough**: both reports must be in the same workspace; enable in report settings; field names/types must match exactly

### Report Page Tooltips

1. Set page `"type": "Tooltip"` and `"visibility": "HiddenInViewMode"` in `page.json`
2. Use the Tooltip page size preset (small canvas)
3. Add tooltip fields to the page's configuration
4. Assign tooltip to visuals: visual's `Tooltip > Type = Report page`, select the tooltip page
5. Keep tooltip pages small — they hover over the report canvas

## Field Parameters

Field parameters let users dynamically switch which fields appear in visuals via a slicer.
In the semantic model: a DAX table expression:

```dax
Parameter = {
    ("Customer", NAMEOF('Customer'[Customer]), 0),
    ("Category", NAMEOF('Product'[Category]), 1),
    ("Color", NAMEOF('Product'[Color]), 2)
}
```

**Limitations**: Can't use as drillthrough/tooltip linked fields. Not supported with AI visuals or Q&A.
Use explicit DAX measures (not implicit aggregations) for measure parameters.

## Sparklines in Tables/Matrices

Add sparklines on numeric fields in tables/matrices — up to **5 per visual**, max **52 data points** each.
Available as **line** or **column** type. Configurable markers (highest, lowest, first, last).

## Visual Grouping

Set `parentGroupName` in `visual.json` to group visuals. Groups can nest, support background color,
and use `isHidden` to toggle all members. Organize via Selection pane.

## Bookmarks

Stored in `definition/bookmarks/` — `bookmarks.json` (metadata) + `<name>.bookmark.json` (state).
Captures: page, filters, slicers, visibility, sort, drill state. Scopes: **Data**, **Display**,
**Current page**, **All vs Selected visuals**. Use for tab navigation, toggle views, reset filters.
See `references/bookmark-patterns.md` for complete bookmark JSON patterns
and `../power-bi-report-design/references/navigation-patterns.md` for navigation design patterns.
