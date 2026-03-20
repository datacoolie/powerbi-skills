---
name: power-bi-pbip-report
description: >-
  Create Power BI reports in PBIP/PBIR format by generating the complete .Report/ folder structure
  with all required JSON files (report.json, page.json, visual.json, pages.json, etc.).
  Use this skill whenever the user asks to create, scaffold, or generate a Power BI report,
  PBIP project report, PBIR report pages, report visuals, or asks to build a Power BI dashboard
  from scratch using file-based format. Also use when the user wants to add pages or visuals
  to an existing PBIP report, copy report structures, or convert report requirements into
  PBIR folder output. This skill covers the report layer only (not the semantic model).
---

# Power BI PBIP Report Generator

Generate Power BI reports in the **PBIR (Power BI Enhanced Report)** format — the modern,
file-based report definition where each page, visual, and bookmark is a separate JSON file
inside a structured folder. This format is ideal for version control, code review, and
programmatic report generation.

**This skill generates the `.Report/` folder only.** It assumes a semantic model already exists
(either as a `.SemanticModel/` sibling folder or a remote connection).

## Quick Reference: Folder Structure

Read `references/folder-structure.md` for the complete annotated tree. The essential structure:

```
<ProjectName>.Report/
├── definition.pbir                    # Links report to semantic model
├── definition/
│   ├── report.json                    # Report config: themes, settings, resources
│   ├── reportExtensions.json          # Report-level measures (optional)
│   ├── version.json                   # PBIR version metadata
│   ├── pages/
│   │   ├── pages.json                 # Page order and active page
│   │   ├── <page-slug>/              # Human-readable folder name
│   │   │   ├── page.json             # Page config: display, dimensions, interactions
│   │   │   └── visuals/
│   │   │       ├── <visual-slug>/    # Human-readable folder name
│   │   │       │   ├── visual.json   # Visual: type, position, query, formatting
│   │   │       │   └── mobile.json   # Mobile layout override (optional)
│   │   │       └── ...
│   │   └── ...
│   └── bookmarks/                     # Optional
│       ├── bookmarks.json
│       └── <bookmark-slug>.bookmark.json
├── StaticResources/
│   ├── RegisteredResources/           # Custom themes, images
│   └── SharedResources/
│       └── BaseThemes/
│           └── CY24SU10.json          # Base theme (shipped with Power BI)
└── .platform                          # Git integration metadata
```

## Naming Convention

PBIR supports renaming page/visual/bookmark folders and `name` properties to human-readable
values. The `name` property inside each JSON file **must match** its folder (or file) name.

### Rules (per PBIR spec)
- Names must consist of **word characters (letters, digits, underscores) or hyphens** only
- Maximum **50 characters**
- Must be **unique** within their scope (pages unique across report, visuals unique within page)

### Page Naming — Slugified Display Name
Convert the `displayName` to a URL-style slug:
1. Lowercase the display name
2. Replace spaces and special characters with hyphens
3. Remove consecutive hyphens
4. Strip leading/trailing hyphens
5. Truncate to 50 characters

| displayName | Folder name (`name`) |
|---|---|
| Overview | `overview` |
| Sales Performance | `sales-performance` |
| P&L Detail | `pl-detail` |
| 1. BC Tổng quan NVL | `1-bc-tong-quan-nvl` |
| Tooltip Card | `tooltip-card` |

### Visual Naming — Type-Prefixed Description
Pattern: `{visualType}-{brief-description}`

| Visual | Folder name (`name`) |
|---|---|
| Card showing total revenue | `card-total-revenue` |
| Clustered bar chart of sales by region | `clusteredBarChart-sales-by-region` |
| Date range slicer | `slicer-date-range` |
| Matrix of order details | `pivotTable-order-details` |
| Background shape | `shape-background` |
| Area chart of completion rate | `areaChart-completion-rate` |

Use the actual Power BI `visualType` string as the prefix (see Visual Type Reference below).

### Bookmark Naming
Pattern: `{slugified-display-name}`  
File: `{slug}.bookmark.json`

## Workflow

Follow these steps when generating a report:

### Step 1: Gather Requirements
Before generating files, understand:
- **Semantic model**: What tables and measures are available? (Ask if not provided)
- **Pages needed**: How many pages, what purpose (overview, detail, tooltip, drillthrough)?
- **KPIs and visuals**: What metrics and charts per page?
- **Target audience**: Executive dashboard vs. analytical report vs. operational?
- **Canvas size**: Default 1280×720 (standard), or custom?
- **Story**: What is the one-sentence insight each page should communicate? (If the user
  cannot state it, help them clarify before designing visuals.)
- **Action**: What should the viewer do after seeing each page? (Filter, drill, decide, escalate?)
- **Theme**: Choose or create a color theme that matches the report's topic and brand
  (see Theme Selection below).

### Step 2: Design Page Layout

Before generating coordinates, confirm the design intent:
- **Select chart types using `references/chart-selection-guide.md`** — never default to
  pie/donut; never place a chart before deciding what insight it must communicate.
- **Apply design principles from `references/visual-design-principles.md`** — pre-attentive
  attributes, Gestalt grouping, color intent, and clutter reduction checklist.
- **Write the visual title first** — if you cannot write a statement or question title for
  a visual, the visual's purpose is not clear enough to design it.

Plan each page with:
- Visual placement using the 1280×720 grid (x, y, width, height coordinates)
- Z-order (higher z = on top; use increments of 1000 for clean layering)
- Tab order for keyboard accessibility
- Visual interactions (cross-filter, cross-highlight, or none)
- **Headline titles** for each visual (state the insight, not just a label)
- **Accent color assignment** — which series/element gets the one accent color?
  All others are grey.

Follow the **Z-pattern** reading flow and **information hierarchy** — the audience's eye
enters at the top-left and scans right, then diagonally down:

```
┌──────────────────────────────────────────────────────────┐
│ HEADER BAR  (y: 0–60)                                    │
│ Page title (headline), Key KPI cards, Date range slicer  │
├──────────────────────────────────────────────────────────┤
│ PRIMARY INSIGHT AREA  (y: 60–420)                        │
│ ┌──────────────────────┐  ┌────────────────────────────┐ │
│ │  Main Visual         │  │  Supporting Context        │ │
│ │  (largest chart —    │  │  (2-3 smaller visuals      │ │
│ │   the story's hero)  │  │   that provide comparison  │ │
│ │                      │  │   or breakdown)            │ │
│ └──────────────────────┘  └────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│ SECONDARY ANALYSIS  (y: 420–640)                         │
│ Detail table, drill-down matrix, or trend breakdown      │
├──────────────────────────────────────────────────────────┤
│ FILTERS & NAVIGATION  (y: 640–720)                       │
│ Category slicers, page navigation buttons, reset button  │
└──────────────────────────────────────────────────────────┘
```

**Pixel Guidelines** (1280×720 canvas):

| Zone | y range | Height | Purpose |
|---|---|---|---|
| Header | 0–60 | ~60 | Title, KPI cards, date slicer |
| Primary insight | 60–420 | ~360 | Main visual (60% width) + supporting (40%) |
| Secondary analysis | 420–640 | ~220 | Detail table or breakdown chart |
| Filters / nav | 640–720 | ~80 | Slicers, navigation buttons |

The primary insight area gets the most vertical space because it carries the main
story. Supporting visuals provide context but should not compete for attention.
Use **one accent color** for the most important data series; render everything
else in gray to direct focus (see Data Storytelling Principles below).

### Step 3: Generate the Folder Structure
Create all folders and files. Use the reference templates:
- `references/report-template.json` → base report.json
- `references/page-template.json` → base page.json
- `references/visual-templates.md` → visual.json patterns per type
- `references/pages-metadata-template.json` → pages.json
- `references/definition-pbir-template.json` → definition.pbir
- `references/version-template.json` → version.json

### Step 4: Validate Cross-References
Run through this checklist before finishing:

- [ ] Every page folder name matches its `page.json` → `name` property
- [ ] Every visual folder name matches its `visual.json` → `name` property
- [ ] `pages.json` → `pageOrder` lists every page folder name in display order
- [ ] `pages.json` → `activePageName` is a valid page folder name
- [ ] `visualInteractions` → `source` and `target` reference valid visual names on that page
- [ ] All `$schema` URLs use correct versions
- [ ] Naming convention: only word chars, digits, underscores, hyphens; max 50 chars
- [ ] `definition.pbir` → `datasetReference.byPath.path` points to correct semantic model
- [ ] Required files all present: `definition.pbir`, `definition/report.json`, `definition/version.json`

## JSON Schema Reference

Each PBIR file declares a `$schema` for validation. Use these exact URLs:

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

**Finding the latest version:** Schema URLs follow the pattern
`https://developer.microsoft.com/json-schemas/fabric/item/report/definition/{schemaName}/{version}/schema.json`.
Browse available versions at the [GitHub json-schemas repository](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition)
and pick the highest version number for each schema.

## Required Properties per File

### report.json
- **Required**: `$schema`, `themeCollection`
- `themeCollection.baseTheme` needs: `name`, `reportVersionAtImport` (object with `visual`, `page`, `report` semver strings), `type`
- **Optional**: `settings`, `resourcePackages`, `publicCustomVisuals`, `filterConfig`, `annotations`

#### Theme Selection

Choose a **custom theme that matches the report's topic, industry, or brand identity**.
A well-chosen theme reinforces the narrative and gives the report a professional, cohesive look.

Examples:
| Report Topic | Theme Palette Direction |
|---|---|
| Financial / P&L | Dark navy, gold accents, conservative neutrals |
| Sales / Revenue | Vibrant blues, greens for growth, reds for decline |
| Manufacturing / Operations | Industrial grays, safety orange/yellow accents |
| Healthcare | Clean whites, calming blues and teals |
| Sustainability / ESG | Earth tones, greens, natural palette |
| Retail / Consumer | Brand-aligned colors, warm and inviting |

To apply a custom theme, place a theme JSON file in `StaticResources/RegisteredResources/`
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

The custom theme JSON file follows the [Power BI report theme schema](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes)
and defines `dataColors`, `background`, `foreground`, `tableAccent`, font families, and
visual-specific style overrides. Always keep the `baseTheme` as the fallback.

### page.json
- **Required**: `$schema`, `name`, `displayName`, `displayOption`
- `displayOption`: `"FitToPage"` | `"FitToWidth"` | `"ActualSize"`
- **Optional**: `height`, `width` (required unless displayOption is DeprecatedDynamic), `type` (`"Drillthrough"` | `"Tooltip"`), `visibility` (`"HiddenInViewMode"`), `pageBinding`, `visualInteractions`, `filterConfig`, `objects`, `annotations`

### visual.json
- **Required**: `$schema`, `name`, `position` (needs `x`, `y`, `height`, `width`)
- Must have one of: `visual` or `visualGroup`
- `visual` requires only `visualType`; `query` with `queryState` needed for data-bound visuals
- **Optional**: `position.z`, `position.tabOrder`, `filterConfig`, `isHidden`, `parentGroupName`, `annotations`

### pages.json
- **Required**: `$schema`
- **Optional**: `pageOrder` (array of page name strings), `activePageName`

### version.json
- **Required**: `$schema`, `version` (pattern: `major.minor.0`, e.g. `"2.0.0"`)

### definition.pbir
- **Required**: `$schema`, `version`, `datasetReference`
- `datasetReference` uses either `byPath` (relative path) or `byConnection` (connection string)

### reportExtensions.json
- **Required**: `$schema`
- Contains report-level measures (report extensions). Only present when the report defines report-level measures.
- **Optional**: `entities` (array of entity definitions with measures)

### mobile.json (per visual)
- **Required**: `$schema`
- Contains mobile layout overrides for a visual: position, size, and formatting on mobile.
- Located alongside `visual.json` inside each visual's folder.
- **Optional**: `position` (x, y, width, height, z for mobile canvas), `config`

## Custom Visuals

When a visual uses a **custom visual** (`publicCustomVisuals` in report.json or a pbiviz in
`CustomVisuals/`), you **must** inform the user:

1. **State the visual's marketplace name** — the exact name as listed on the
   [Power BI Visuals Marketplace](https://appsource.microsoft.com/en-us/marketplace/apps?product=power-bi-visuals)
2. **Explain why** this custom visual was chosen over a built-in alternative
3. **Provide the `publicCustomVisuals` identifier** to add to `report.json`

Example notification to user:
> This report uses the custom visual **"Deneb"** (identifier: `Deneb64BBF0D4C1BD4B06B84DD1B16028ED63`)
> from the Power BI Visuals Marketplace. Please install it via:
> Insert → More visuals → From AppSource → search "Deneb".

Always prefer built-in visuals when they meet the requirement. Only recommend custom
visuals when the built-in alternatives cannot achieve the needed visualization.

## Visual Type Reference

**Full chart selection guidance** (including hard rules for when to avoid specific chart types,
common mistakes, and audience-based guidance) is in `references/chart-selection-guide.md`.
Use that reference when deciding WHICH chart to use. Use this section to look up HOW to
generate that chart's JSON.

### Query Role Names by Visual Type

Each visual type uses different "role" keys in `queryState`. Read `references/visual-templates.md`
for complete JSON templates. Quick reference:

| visualType | Query Roles | When to Use |
|---|---|---|
| `card` | `Values` | Single hero KPI — the most important metric on the page |
| `multiRowCard` | `Values` | 4-8 related KPIs at equal visual weight |
| `slicer` | `Values` | Filter control — date, category, or hierarchy |
| `clusteredBarChart` | `Category`, `Y` | **Default for category comparison** — horizontal; labels read naturally |
| `clusteredColumnChart` | `Category`, `Y` | Vertical bars — only when time is on the x-axis or ≤8 categories |
| `barChart` | `Category`, `Y` | Stacked horizontal — part-of-whole across categories |
| `columnChart` | `Category`, `Y` | Stacked vertical — part-of-whole with time on x-axis |
| `lineChart` | `Category`, `Y` | **Default for trends over time** — continuous data |
| `areaChart` | `Category`, `Y` | Filled area — only for single series where volume matters; avoid stacked |
| `lineClusteredColumnComboChart` | `Category`, `Y`, `Y2` | Combo chart — only when two scales are truly needed and clearly labeled |
| `pieChart` | `Category`, `Y` | **⚠ Avoid by default** — use `clusteredBarChart` instead; see chart-selection-guide.md |
| `donutChart` | `Category`, `Y` | **⚠ Avoid** — arc-length comparison is harder than bar; no practical advantage |
| `waterfallChart` | `Category`, `Y` | Cumulative additions/subtractions showing start, deltas, end |
| `treemap` | `Group`, `Values` | Part-of-whole with many segments (10+) or hierarchical data |
| `pivotTable` | `Rows`, `Columns`, `Values` | Matrix — detail analysis with row and column groupings |
| `tableEx` | `Values` | Flat table — row-level or summary detail view |
| `funnel` | `Category`, `Y` | Sequential pipeline stages — only when stages are truly sequential |
| `scatterChart` | `Category`, `X`, `Y`, `Size` | Correlation between two metrics; bubble size = third dimension |
| `map` | `Category`, `Size` | Geographic patterns — normalize data to rate/% for regional comparisons |
| `gauge` | `Y`, `TargetValue`, `MinValue`, `MaxValue` | Single metric vs. target — prefer `kpi` for density |
| `kpi` | `Indicator`, `TrendAxis`, `Goal` | KPI status with trend over time and target — rich in small space |
| `shape` | *(none — decorative)* | Background rectangles for visual grouping (low z-order) |
| `textbox` | *(none — static content)* | Page title, section headings, callout annotations |
| `actionButton` | *(none)* | Page navigation buttons |
| `image` | *(none)* | Static image — logo, illustration |

### Field Expression Patterns

Fields in `queryState` projections reference semantic model entities:

**Column reference** (dimension field):
```json
{
  "field": {
    "Column": {
      "Expression": { "SourceRef": { "Entity": "TableName" } },
      "Property": "ColumnName"
    }
  },
  "queryRef": "TableName.ColumnName",
  "nativeQueryRef": "ColumnName"
}
```

**Measure reference** (calculated measure):
```json
{
  "field": {
    "Measure": {
      "Expression": { "SourceRef": { "Entity": "MeasureTable" } },
      "Property": "MeasureName"
    }
  },
  "queryRef": "MeasureTable.MeasureName",
  "nativeQueryRef": "MeasureName"
}
```

**Aggregation reference** (inline aggregation of a column):
```json
{
  "field": {
    "Aggregation": {
      "Expression": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "TableName" } },
          "Property": "ColumnName"
        }
      },
      "Function": 0
    }
  },
  "queryRef": "Sum(TableName.ColumnName)",
  "nativeQueryRef": "Total ColumnName",
  "displayName": "Total ColumnName"
}
```

Aggregation `Function` values: `0` = Sum, `1` = Avg, `2` = Count, `3` = Min, `4` = Max, `5` = CountNonNull, `6` = Median, `7` = StdDev, `8` = Var.

## Formatting Patterns

### Visual Container Objects (title, background, border)
These apply to the visual's container (the box around the chart):

```json
"visualContainerObjects": {
  "title": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "text": { "expr": { "Literal": { "Value": "'My Chart Title'" } } },
      "fontSize": { "expr": { "Literal": { "Value": "12D" } } },
      "bold": { "expr": { "Literal": { "Value": "true" } } },
      "fontFamily": { "expr": { "Literal": { "Value": "'Segoe UI'" } } },
      "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#333333'" } } } } }
    }
  }],
  "background": [{
    "properties": {
      "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } } },
      "transparency": { "expr": { "Literal": { "Value": "0D" } } }
    }
  }],
  "border": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } }
    }
  }]
}
```

### Color Expression Patterns

**Literal color** (hex):
```json
{ "solid": { "color": { "expr": { "Literal": { "Value": "'#FF5733'" } } } } }
```

**Theme color** (references theme palette):
```json
{ "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } }
```
`ColorId` 0-9 maps to the theme's data color palette. `Percent` adjusts lightness (0 = base, negative = darker, positive = lighter).

### Literal Value Patterns
- String: `"'my string'"`  (single quotes inside double quotes)
- Number: `"10D"` (D suffix for decimal)
- Boolean: `"true"` or `"false"`
- Null: `"null"`

## Page Types

### Standard Page
Normal visible page — the default. No `type` or `visibility` needed.

### Tooltip Page
Hidden page used as a custom tooltip for visuals on other pages:
```json
{
  "type": "Tooltip",
  "visibility": "HiddenInViewMode",
  "height": 240,
  "width": 320
}
```
Standard tooltip canvas size is 320×240.

### Drillthrough Page
Page accessed via right-click drillthrough from other visuals:
```json
{
  "type": "Drillthrough",
  "pageBinding": {
    "name": "unique-binding-name",
    "type": "Drillthrough",
    "parameters": [{
      "name": "param-name",
      "boundFilter": "filter-name"
    }]
  }
}
```

## Data Storytelling Principles

Apply these principles (derived from *Storytelling with Data* by Cole Nussbaumer Knaflic,
and *Data Visualization: A Handbook for Data Driven Design* by Andy Kirk) when designing
report pages. Full reference material is in `references/visual-design-principles.md`
and `references/chart-selection-guide.md`.

### Before Creating Any Visual

Answer these three questions — in order — before placing a single visual:

1. **WHO** is the audience?
   - Executive/leadership: needs the conclusion in ≤30 seconds; statement titles, 3-5 KPIs,
     one hero chart, minimal annotation.
   - Analyst: needs drill-down and exploration capability; scatter plots, detail tables, and
     interactive slicers are appropriate.
   - Operational user: checks status repeatedly; prioritize KPI cards with vs-target
     indicators and threshold reference lines.

2. **WHAT** should they know or do after seeing this page?
   - Complete the sentence: *"I want my audience to ___."*
   - Every page must drive toward a specific decision or action — not just "show data."
   - If you cannot complete this sentence, the page design is not ready.

3. **WHAT** data supports that specific point?
   - Select only data that advances the message. Omit the rest.
   - Showing all 100 data points when 2 are the actual story is a common mistake.
     Communicate the pearls, not all the oysters.

### The Big Idea
Before designing a page or a report, articulate the **Big Idea** as a single sentence
that: (a) states a unique point of view, (b) conveys what's at stake, and (c) is complete.

> *"Enterprise revenue grew 42% YoY, but SMB declined 18% — if this trend continues,
> SMB will cease to be profitable by Q3."*

If you cannot write this sentence for a report page, the page needs more scoping before
it gets visuals.

### Chart Type Selection

**Chart type follows the data relationship, not preference or novelty.** See
`references/chart-selection-guide.md` for the full decision matrix. Core rules:

| Data Relationship | Preferred Chart | `visualType` |
|---|---|---|
| Change over time | Line chart | `lineChart` |
| Comparing categories | Horizontal bar chart | `clusteredBarChart` |
| Ranking by value | Sorted horizontal bar | `clusteredBarChart` |
| Part-to-whole (few parts) | Stacked bar | `barChart` / `columnChart` |
| Part-to-whole (many parts) | Treemap | `treemap` |
| Waterfall / delta tracking | Waterfall | `waterfallChart` |
| Correlation | Scatter plot | `scatterChart` |
| Single KPI | Card | `card` |
| KPI vs. target + trend | KPI visual | `kpi` |

**Absolute prohibitions — never generate these by default:**
- **❌ Pie charts** (`pieChart`): Humans compare areas/angles very poorly. Use a sorted
  horizontal bar instead. The only acceptable exception is ≤3 clearly distinct segments
  summing to exactly 100%.
- **❌ Donut charts** (`donutChart`): Arc-length comparison is even harder than area
  comparison. No practical justification over a bar chart.
- **❌ 3D charts** (any type): 3D distorts all 2D data. Always use the flat equivalent.
  The only legitimate exception is interactive charts with true 3D spatial data.
- **❌ Secondary Y-axis** (combo charts with dual axes): Implies a relationship that may
  not exist; makes the chart hard to read. If two series must appear together, pull the
  chart into two vertically-aligned charts sharing the same x-axis.

When the user asks for a pie or donut chart, generate a sorted horizontal bar chart instead
and briefly explain why it communicates more clearly.

### Visual Focus and Emphasis (Pre-Attentive Attributes)

The brain processes **pre-attentive attributes** — color, size, position, shape, intensity —
in under 250ms, before conscious reading. Use them to direct the audience's eye to the
key insight before they process any text.

**Practical rules:**
1. **One accent color per visual** — apply the accent color only to the data series or
   data point carrying the key message. Everything else is grey.
2. **Grey is the canvas, not absence** — a grey bar is not "unimportant data"; it is the
   baseline that makes the accent color pop.
3. **Do not use multiple pre-attentive signals simultaneously** — bold color AND larger size
   AND a callout box on the same element is redundant and diminishes each signal.
4. **Apply in explanatory mode only** — on exploratory/interactive dashboards, avoid heavy
   pre-attentive emphasis (it hides other trends); on analytical/story pages, use it fully.

**"3-second test"**: After designing a visual, cover the title and show it for 3 seconds.
The viewer's first fixation should land on the key insight. If it lands on a gridline,
the legend, or an unimportant bar — redesign.

### Clutter Reduction

> "Every element you add to a page takes up cognitive load on the part of your audience.
> Humans have a finite amount of mental processing power." — *Storytelling with Data*

**Remove these by default — add back only if there is a specific reason:**

| Element | Default Action | Reason |
|---|---|---|
| Chart border / visual border | Remove | Closure principle — brain groups the visual without it |
| Plot area background color | Remove (white/transparent) | Background colors compete with data |
| Heavy gridlines | Lighten to `#E8E8E8` or remove | Let data stand out; reduce visual noise |
| Vertical gridlines on bar charts | Remove | Bar length is the encoding; gridlines re-encode |
| Axis lines (spines) | Remove top and right; often remove all | Continuity principle — eyes align naturally |
| Legend when direct labeling is possible | Remove legend; label series directly | Eliminates cognitive round-trips |
| Value labels on every bar / point | Show only on highlighted series | Labeling everything = labeling nothing |
| Trailing zeros (`1,000,000` vs. `1M`) | Simplify | False precision adds visual weight |
| Diagonal axis labels | Rotate chart to horizontal bar | Diagonal text reads 40% slower |
| Secondary y-axis | Separate into two charts | Dual axes imply false correlation |
| Color variation for novelty | Single consistent palette | Too much variety prevents anything from standing out |

**Cognitive load test**: If the visual looks "busy," it is. Start removing elements until
the data-to-ink ratio feels high — data should occupy the majority of the visual's ink.

### Color with Intent

1. **Design in grey first** — build the entire chart without color, then apply the accent
   color only where it earns its place (the key insight, the highlighted series, the
   outlier data point).
2. **One bold color against a grey palette** is the single most powerful emphasis technique.
3. **Consistency across the entire report** — if blue = Enterprise, blue = Enterprise on
   every page. Changing colors forces re-learning and creates false signals.
4. **Colorblind-safe defaults**: Avoid red + green as opposing signals. Use blue + orange
   or add secondary encoding (icons, bold labels, + / − symbols) alongside color.
5. **Color conveys emotion**: Blues/teals = calm/analytical; reds/oranges = urgency/warning;
   greens = growth/positive. Choose palettes that reinforce the report's tone.

See `references/visual-design-principles.md` → *Color Theory* section for scale types
(sequential, diverging, categorical) and recommended hex palettes.

### Gestalt Principles Applied to Layout

Use these perceptual grouping laws to make the layout legible without extra labels:

- **Proximity**: Place related items close together; separate unrelated items with white space.
  Put data labels directly next to their data series — this eliminates the legend.
- **Similarity**: Use the same color for the same metric across all pages. Same visual type
  for the same kind of data across all pages.
- **Enclosure**: A background shape behind a group of visuals groups them without borders.
  Light grey shading separates the filter panel from the data area.
- **Closure**: Remove chart borders — the brain completes the rectangle without them.
  Bonus: data stands out more against a clean background.
- **Continuity**: Aligned bars imply a common baseline even without the y-axis line.
  Use dashed lines for forecasts and solid lines for actuals — the eye reads both as
  one continuous series.

### Titles as Headlines

> "Takeaway titles orient the audience immediately. Descriptive titles make the audience do work."
> — *Storytelling with Data*

| Title Pattern | Use When | Example |
|---|---|---|
| **Statement title** (takeaway) | Analytical pages with a specific finding | *"Enterprise revenue grew 42% YoY while SMB declined"* |
| **Question title** | Interactive dashboards; viewer explores | *"Which regions are driving growth this quarter?"* |
| **Descriptive title** | Operational dashboards with familiar metrics | *"Monthly Revenue by Region"* |

**Rules:**
- Use statement titles by default on analytical report pages
- The visual title must be a sentence or meaningful phrase — never just a metric name
- Titles are upper-left justified (Z-pattern reading flow starts top-left)
- Visual title font: Bold, 11-13px, dark color (`#333333`)
- Page title: Bold, 18-24px, darkest color (`#1F1F1F`)

### Page Narrative Structure
Each page should follow an implicit arc:
- **Top (header):** Establish context — what metric, what period, what's the headline insight?
- **Middle (primary):** Present the evidence — the main visual that proves the headline.
- **Bottom (secondary):** Support with detail — breakdown tables, comparisons, drill-down.
- **Call to action:** Make it clear what the viewer should do next (navigate, filter, decide).

## Integration with Design Skills

For **chart selection methodology** and **layout design patterns**, refer to the
`power-bi-report-design-consultation` skill. Use that skill first to gather requirements
and select appropriate visual types, then return here to generate the PBIR files.

This skill's own design references:
- `references/chart-selection-guide.md` — decision matrix, hard rules (no pie/donut/3D),
  common mistakes by chart type, audience modifiers
- `references/visual-design-principles.md` — pre-attentive attributes, Gestalt principles,
  color theory, typography hierarchy, clutter reduction checklist, title patterns,
  narrative structure, audience design guide

## Common Patterns

### KPI Header Row
A row of 3-5 card visuals across the top of a page:
- Position: y=10, height=70, evenly spaced across width
- Each card: `visualType: "card"`, single measure in `Values`

### Slicer Panel
Date and category slicers, typically at the top or left:
- Top row slicers: y=0, height=50, x spread across top
- Left panel slicers: x=0, width=200, stacked vertically

### Sync Slicers Across Pages

When slicers should apply consistently across multiple pages (e.g., a global date range
or department filter), use **sync slicers** via `reportExtensions.json`. This is the
**default recommendation** for multi-page reports — it prevents users from having to
re-select filters on each page.

Sync slicers are configured in `reportExtensions.json` at the report level. The file
defines which slicer visual syncs across which pages:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/reportExtension/1.0.0/schema.json",
  "entities": []
}
```

In practice, sync slicers work by placing identical slicer visuals on each page (same field,
same configuration) and Power BI synchronizes their selection state. To set this up in PBIR:
1. Add the same slicer visual (same field and configuration) to each page that needs it
2. Use consistent naming: e.g., `slicer-date-range` on every page
3. The sync behavior is managed by Power BI Desktop when the report is opened

**Default rule:** For any multi-page report, always include sync slicers for date range
and primary category filters unless the user explicitly requests independent page filtering.

### Background Shape
A colored rectangle behind a group of visuals for visual grouping:
- Use `visualType: "shape"` with no query
- Set low z-order (e.g., 0) so it appears behind data visuals
- Configure fill color via visual `objects.line` and `objects.fill`

---

## Page Type Templates

Use these templates as starting points for common page types. Adjust dimensions
and visuals to match specific requirements.

### Overview Page Template

The landing page — executive summary with navigation to detail pages.

```
Layout (1280×720):
┌─────────────────────────────────────────────────────┐
│ shape-header-bg (0,0 → 1280×60) z:0                │
│   textbox-title (10,10) "Report Title"              │
│   slicer-date-range (900,10 → 370×40)              │
├─────────────────────────────────────────────────────┤
│ KPI Row (y:70, h:80)                                │
│  card-kpi-1  card-kpi-2  card-kpi-3  card-kpi-4    │
│  (x:10,w:305) (x:325,w:305) (x:640,w:305) (x:955) │
├─────────────────────────────────────────────────────┤
│ Primary (y:160, h:300)                              │
│  ┌─────────────────────┐ ┌────────────────────────┐ │
│  │ lineChart-trend     │ │ clusteredBarChart-top-n │ │
│  │ (10,160 → 750×300)  │ │ (770,160 → 500×300)    │ │
│  └─────────────────────┘ └────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ Secondary (y:470, h:200)                            │
│  pivotTable-summary (10,470 → 1260×200)             │
├─────────────────────────────────────────────────────┤
│ Navigation (y:680, h:30)                            │
│  actionButton-detail  actionButton-drillthrough     │
└─────────────────────────────────────────────────────┘
```

### Detail / Analysis Page Template

Deep-dive page with filters and detailed breakdowns.

```
Layout (1280×720):
┌────────┬────────────────────────────────────────────┐
│ Filter │ shape-header-bg (200,0 → 1080×50)          │
│ Panel  │   textbox-title  slicer-date-range          │
│ (0,0)  ├────────────────────────────────────────────┤
│ w:190  │ KPI Row (y:55, h:65)                       │
│ h:720  │  card-kpi-1  card-kpi-2  card-kpi-3        │
│        ├────────────────────────────────────────────┤
│ slicer │ Main Chart Area (y:130, h:280)             │
│ -cat1  │  lineClusteredColumnComboChart-main         │
│ slicer │  (210,130 → 1060×280)                      │
│ -cat2  ├────────────────────────────────────────────┤
│ slicer │ Detail Table (y:420, h:260)                │
│ -cat3  │  tableEx-detail (210,420 → 1060×260)       │
│        ├────────────────────────────────────────────┤
│ action │ Nav: actionButton-back (210,690 → 100×25)  │
│ Button │                                             │
│ -reset │                                             │
└────────┴────────────────────────────────────────────┘
```

### Drillthrough Page Template

Target page for right-click drillthrough — shows entity-level detail.

```json
// page.json additions:
{
  "type": "Drillthrough",
  "visibility": "HiddenInViewMode"
}
```

```
Layout (1280×720):
┌─────────────────────────────────────────────────────┐
│ Header: textbox-entity-name + actionButton-back     │
│ (actionButton with "Back" navigation type)          │
├─────────────────────────────────────────────────────┤
│ Entity Summary (y:60, h:100)                        │
│  card-attr-1  card-attr-2  card-attr-3  card-attr-4 │
├─────────────────────────────────────────────────────┤
│ Trend (y:170, h:250)                                │
│  lineChart-entity-trend (10,170 → 1260×250)         │
├─────────────────────────────────────────────────────┤
│ Detail (y:430, h:280)                               │
│  tableEx-entity-transactions (10,430 → 1260×280)    │
└─────────────────────────────────────────────────────┘
```

The drillthrough parameter filter is automatically applied by Power BI
when the user right-clicks a record and selects "Drillthrough."

### Tooltip Page Template

Custom tooltip — small canvas shown on hover.

```json
// page.json:
{
  "type": "Tooltip",
  "visibility": "HiddenInViewMode",
  "width": 320,
  "height": 240
}
```

```
Layout (320×240):
┌───────────────────────────┐
│ textbox-title (5,5)       │
├───────────────────────────┤
│ card-primary (5,30 → 150) │
│ card-secondary (165,30)   │
├───────────────────────────┤
│ clusteredBarChart-detail  │
│ (5,100 → 310×130)        │
└───────────────────────────┘
```

Keep tooltip pages minimal — max 3-4 visuals. Load time is critical since
tooltips appear on hover.

---

## Navigation Patterns

### Page Navigation Buttons

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

### Bookmark Navigation (Tab Selector)

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

### Back Button (for Drillthrough Pages)

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

### Reset Filters Button

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

## Domain-Specific Report Structures

Recommended page sets and visual compositions by industry domain.

### Sales / Revenue Analytics
| Page | Type | Key Visuals |
|---|---|---|
| Overview | Standard | KPI cards (Revenue, Growth, Target%), trend line, top-N bar |
| Regional Breakdown | Standard | Map, clustered bar by region, matrix by region×product |
| Product Analysis | Standard | Treemap by category, combo chart (revenue + margin), table |
| Customer Analysis | Standard | Scatter (value vs. frequency), top-10 table, cohort trend |
| Sales Rep Performance | Standard | Bar chart ranked, KPI cards per rep, target gauge |
| Order Detail | Drillthrough | Entity cards, transaction table, trend line |
| Product Tooltip | Tooltip | Card (sales), card (margin%), mini bar chart |

### Manufacturing / Operations
| Page | Type | Key Visuals |
|---|---|---|
| Production Overview | Standard | KPI cards (OEE, yield, downtime), line chart (daily output) |
| Quality Control | Standard | Control chart (defect rate), Pareto bar, trend |
| Equipment Status | Standard | Card matrix per machine, gauge (utilization), timeline |
| Inventory | Standard | Stacked bar (stock levels), line (consumption rate), alerts |
| Shift Analysis | Detail | Matrix (shift×metric), combo chart, filter by line/shift |
| Machine Drillthrough | Drillthrough | Machine details, downtime history, maintenance log |

### Financial / P&L
| Page | Type | Key Visuals |
|---|---|---|
| Executive Summary | Standard | KPI cards (Revenue, EBITDA, Net Income), waterfall chart |
| Income Statement | Standard | Matrix (account hierarchy), variance bar chart |
| Balance Sheet | Standard | Clustered bar (assets vs liabilities), trend |
| Cash Flow | Standard | Waterfall (operating→investing→financing), line trend |
| Budget vs Actual | Detail | Combo chart (bars=actual, line=budget), variance table |
| Account Drillthrough | Drillthrough | Account transactions, monthly trend, annotations |

### Supply Chain / Logistics
| Page | Type | Key Visuals |
|---|---|---|
| Overview | Standard | KPI cards (fill rate, on-time%, lead time), trend lines |
| Inventory Levels | Standard | Stacked bar (by warehouse), line (days of supply), alerts |
| Supplier Performance | Standard | Scatter (quality vs delivery), ranked bar chart |
| Logistics Tracking | Standard | Map (shipment routes), table (order status), funnel |
| Demand Planning | Detail | Line (forecast vs actual), variance chart, accuracy KPI |
| Shipment Drillthrough | Drillthrough | Shipment milestones, carrier detail, timeline |

### Retail / FMCG
| Page | Type | Key Visuals |
|---|---|---|
| Store Performance | Standard | Map, ranked bar (revenue by store), KPI cards |
| Category Analysis | Standard | Treemap, combo chart (sales + margin), matrix |
| Basket Analysis | Standard | Scatter (basket size vs frequency), top combos table |
| Promotion Effectiveness | Standard | Before/after bar chart, ROI card, trend |
| Store Drillthrough | Drillthrough | Store details, daily trend, product mix pie/bar |

---

## Mobile Layout

For mobile-optimized reports, create `mobile.json` alongside `visual.json`
in each visual folder. The mobile layout repositions visuals for a phone
canvas (typically 360×640).

### Mobile Design Rules

1. **Single column layout** — Stack visuals vertically, full width
2. **KPIs first** — Most important numbers at the very top
3. **Reduce visual count** — Show only essential visuals; hide secondary charts
4. **Larger touch targets** — Slicers and buttons minimum 44px height
5. **Simplify tables** — Fewer columns, larger font

### Mobile Layout Template

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

### mobile.json Example

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
