---
name: power-bi-report-authoring
description: >-
  Create and modify Power BI report files in PBIR/PBIP format using the
  `powerbi-report-author` and `powerbi-desktop` CLIs. Use when the user wants
  to: (1) implement an approved report spec or design brief, (2) add or edit
  pages, visuals, filters, slicers, bookmarks, themes, or formatting, (3)
  validate PBIR and verify rendering in Power BI Desktop. For open-ended visual
  design, use `power-bi-report-design` first. For end-to-end requirements and
  approval workflow, use `powerbi-report-planning` first. Triggers: "edit PBIR",
  "create Power BI report page", "add visual to PBIP", "format report visual",
  "validate Power BI report", "reload Desktop screenshot", "implement an
  approved PBIP report spec", "edit PBIR pages/visuals".
---

# Power BI PBIP Report Authoring

Create and modify Power BI reports in **PBIR (Power BI Enhanced Report)** format — the
file-based report definition used in PBIP projects. This skill produces and edits the
`.Report/` folder with all JSON files that Power BI Desktop and the Power BI service can
open directly. It also handles live Desktop verification via screenshot workflows.

**Input:** A Design Spec from the `power-bi-report-design` skill (or equivalent user instructions)
specifying pages, visuals, layout positions, theme, and navigation.

Canvas size: **1664 × 936** (standard Power BI canvas). Tooltip pages: **320 × 240**.

## Must/Prefer/Avoid

### MUST

- Use CLI capability lookup (`powerbi-report-author catalog/formatting`) before writing
  visual roles, formatting objects, enum values, selectors, or expression encodings.
- Validate PBIR with `powerbi-report-author validate` after each logical batch of edits.
- Use `powerbi-desktop` reload/screenshot workflows for rendered-output changes.
- Never guess PBIR JSON from memory when CLI metadata or reference files are available.

### PREFER

- Start from an approved Design Spec or `Design Brief:` for greenfield report builds.
- Route visual-design uncertainty to `power-bi-report-design` before writing files.
- Use the Edit → Validate → Reload → Screenshot loop for any visual change.

### AVOID

- Do not create legacy visual types (`card`, `table`, `matrix`, `map`, `filledMap`).
- Do not hardcode property names without CLI confirmation.
- Do not skip Desktop verification for visual changes.

## Reference Files

| Reference | When to Read |
|---|---|
| `references/folder-structure.md` | Understanding the full PBIR folder layout |
| `references/powerbi-desktop.md` | **Desktop verification** — open, reload, screenshot, PID selection, troubleshooting |
| `references/screenshot-review.md` | **Screenshot review** — checklist, common problems, fix patterns after capture |
| `references/powerbi-report-author-cli.md` | **CLI metadata** — catalog, formatting, expr encode/decode, validate, preview commands |
| `references/formatting.md` | **Core formatting patterns** — JSON structure, selectors (precedence rules, dual-entry pattern), VCOs, color routing |
| `references/formatting-overview.md` | **Read first for appearance changes** — cascade model, encoding rules, selectors, routing |
| `references/authoring.md` | **Authoring workflows** — add pages, add visuals, layout templates, theme registration, drillthrough, interactions |
| `references/card.md` | Card visual (`cardVisual`) — single/multi-value templates, instance selectors, accent bar, font scaling |
| `references/cartesian.md` | Bar/column/line/area/scatter charts — query roles, combo charts, lineStyles, markers, drill hierarchies |
| `references/table.md` | Table/matrix visuals (`pivotTable`) — row banding, style presets, column formatting, subtotals |
| `references/slicers.md` | Slicer visual authoring — 9 slicer types, sizing formulas, fill variant, selection config, mode reference |
| `references/filters.md` | Filter authoring — 8 filter types, TopN rules, relative dates, inverted selection, filter pane layout |
| `references/color-strategy.md` | Cross-visual measure-color mapping — theme dataColors, defaultColor, per-series metadata selectors |
| `references/conditional-formatting.md` | Data-driven formatting — 6 types (FillRule gradients, rules, icons, data bars, web URLs, field values) |
| `references/re-theming.md` | Re-theming workflow — dark mode, polarity changes, 4-step theme swap procedure |
| `references/page-formatting.md` | Page-level formatting — canvas background, wallpaper (outspace), background images |
| `references/filter-pane.md` | Filter pane appearance — outspacePane styling, filter card states (Applied/Available) |
| `references/textbox.md` | Textbox visuals — paragraphs JSON, dynamic text, rich formatting |
| `references/shape.md` | Shape visuals — dual-entry selector pattern, available shapes, rotation, text caveat |
| `references/image.md` | Image visuals — 3 source types, ResourcePackageItem registration, plot area backgrounds |
| `references/map.md` | Map visuals — Azure Map template, geocoding, ArcGIS |
| `references/theming.md` | Theme JSON authoring — dataColors, textClasses, visualStyles, dark-mode checklist |
| `references/expressions.md` | Field expressions — Column, Measure, Aggregation patterns, filter definitions, sort specs |
| `references/version-control.md` | Git workflows for PBIR — branching, reverting, merge strategies |
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
| `scripts/validate_report.py` | **Run after generation** — validates cross-references, bookmarks, naming conventions |
| `scripts/finalize_pbir.py` | **Phase 4c polish** — snap_grid, align_kpi_row, apply_theme_tokens, normalize_fonts, ensure_alt_text |
| `scripts/design_quality_check.py` | **Phase 4c lint** — 14 checks (E1-E4 critical, W1-W10 warnings). Use `--style executive\|analytical\|operational` |
| `scripts/pbir_gate.py` | **Unified Phase 4c gate** — chains finalize → lint → validate → CLI validate into one pass/fail command |
| `scripts/pbir_utils.py` | Internal shared helper (constants, logging, console fix) — imported by the 4 scripts above, not run directly |

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
│   │   ├── pages.json           ← Page ordering metadata
│   │   └── ...
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

### Step 0: CLI Setup & Desktop Context

**Prerequisite: Node.js 20+.** Check with `node --version`.

Install both CLIs globally:
```bash
npm install -g @microsoft/powerbi-report-authoring-cli @microsoft/powerbi-desktop-bridge-cli
```

Confirm availability:
```bash
powerbi-report-author --version
powerbi-desktop --version
```

Before authoring, understand the model (TMDL files or Semantic Model MCP) and
check Desktop status:
```bash
powerbi-desktop status
```

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
2. For each visual, create `visual.json` — use `powerbi-report-author catalog describe <type>`
   for exact roles, then read `references/visual-templates.md` for JSON templates
3. Apply formatting — use `powerbi-report-author formatting list-objects <type>` for valid objects,
   then read `references/formatting-overview.md` and `references/formatting-patterns.md`
4. Set up visual interactions in `page.json` — see `references/common-patterns.md`

### Step 3: Generate Supporting Files

As needed:
- **Bookmarks**: Create `bookmarks/bookmarks.json` + individual `.bookmark.json` files
  — see `references/bookmark-patterns.md` and `../power-bi-report-design/references/navigation-patterns.md`
- **Mobile**: Add `mobile.json` alongside `visual.json` — see `references/mobile-layout.md`
- **Custom themes**: Place theme JSON in `StaticResources/RegisteredResources/`
- **Images**: Place logos, icons in `StaticResources/RegisteredResources/`
- **Report extensions**: `reportExtensions.json` for report-level measures

### Step 4: Validate

Power BI Desktop rejects files with JSON syntax errors silently or with cryptic messages.
**Always validate before telling the user the report is ready.**

Run CLI validation after every logical batch of PBIR edits:
```bash
powerbi-report-author validate "<path-to-.Report-dir>"
```

- Fix every **error** before Desktop reload.
- Review **warnings** — unknown visual types usually mean a typo.
- Diagnostics include file paths and JSON paths for direct navigation.

**If invoked from the `power-bi-developer` agent (Phase 4c), use the unified gate:**

```powershell
# Recommended — single command, one pass/fail verdict
python skills/power-bi-report-authoring/scripts/pbir_gate.py `
    --report <path-to-.Report-folder> `
    --style <style-from-design-spec>
```

The gate chains 4 stages: `finalize_pbir.py` → `design_quality_check.py` → `validate_report.py` → `powerbi-report-author validate` (CLI).
Exit codes: `0` = pass, `1` = input error, `2` = fail, `3` = tool error.
Add `--allow-warnings` to pass with warnings, `--json verdict.json` to save the result.
Flags: `--skip-finalize`, `--skip-lint`, `--skip-validate`, `--skip-schemas`.
See `../power-bi-report-design/references/polisher.md` for the full Phase 4c routing table.

<details><summary>Manual alternative (run each stage separately)</summary>

```powershell
# 1. Mechanical polish (snap grid, align KPIs, tokenize theme colors, unify fonts, alt text)
# 3. Structural validation (cross-refs, naming, advisories — not schema)
python skills/power-bi-report-authoring/scripts/validate_report.py <path-to-.Report-folder>

# 4. CLI Schema validation
npx powerbi-report-author validate <path-to-.Report-folder>
```

Per-script exit codes: `0` = pass, `1` = warnings only, `2` = errors present (must fix).

</details>

**Standalone usage:**
```
python skills/power-bi-report-authoring/scripts/validate_report.py <path-to-.Report-folder>
npx powerbi-report-author validate <path-to-.Report-folder>
```

`validate_report.py` checks (schema validation is intentionally NOT duplicated here —
that is the CLI's job):
1. **JSON syntax** — every `.json` and `.pbir` file parses cleanly (needed to run the checks below)
2. **Cross-references** — page folders match `pages.json`, bookmarks reference real pages,
   custom visuals registered in `report.json`
3. **Naming conventions** — kebab-case for page and visual folders
4. **Query semantics** — visual query `From` items reference a valid `Entity`/`Name`
5. **Drillthrough/tooltip advisories** — missing drillthrough filters, oversized tooltip pages

`powerbi-report-author validate` checks: every file against its correct Microsoft JSON schema
(required properties, `$schema`, position shape, `displayOption` enum values, `visual` vs
`visualGroup` presence, etc.) — always run this as the source of truth for schema correctness.

Fix all **errors** before delivering. **Warnings** are advisory (naming, unused registrations).

If the CLI is not available, `validate_report.py` alone is not a substitute for schema
validation — install the CLI (Step 0) before delivering a report.

---

## JSON Schema Reference

Schema validation is handled by the `powerbi-report-author validate` CLI command.
Browse available versions at the [GitHub json-schemas repository](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition).

## Required Properties (Quick Reference)

Each JSON file must have a `$schema` property. For full property details, theme selection,
conditional formatting, and format strings, read `references/required-properties.md`.

| File | Key Required Properties |
|---|---|
| `report.json` | `themeCollection` (with `baseTheme.name`, `reportVersionAtImport`, `type`) |
| `page.json` | `name`, `displayName`, `displayOption` |
| `visual.json` | `name`, `position` (`x`, `y`, `height`, `width`), plus `visual` or `visualGroup` |
| `definition.pbir` | `version`, `datasetReference` (`byPath` or `byConnection`) |

## Custom Visuals

When a visual uses a **custom visual**, you **must**:

1. **State the marketplace name** and explain why it was chosen over built-in —
   custom visuals add rendering overhead and dependency risk, so the benefit must be clear
2. **Register** the `visualType` identifier in `report.json` → `publicCustomVisuals` array
3. **Use correct query roles** — custom visuals have unique role names (not standard `Category`/`Y`)

Prefer built-in visuals when they can achieve the visualization. Custom visuals shine when
built-in alternatives lack the chart type entirely (e.g., no built-in histogram, Sankey, or
calendar heatmap). Read `references/custom-visuals.md` for all identifiers, templates, and query roles.

## Visual Type Reference

Read `../power-bi-report-design/references/chart-selection-guide.md` for WHICH chart to use.
Read `references/visual-templates.md` for complete JSON templates per visual type.
Read `references/custom-visuals.md` for custom visual identifiers, templates, and query roles.

Non-data visuals (no query): `shape`, `basicShape`, `textbox`, `actionButton`, `image`, `pageNavigator`.

### Field Expressions

Three patterns for binding data to visuals: **Column** (dimension), **Measure** (DAX measure),
**Aggregation** (inline Sum/Avg/Count on a column). Each uses `SourceRef.Entity` + `Property`.
See `references/visual-templates.md` → "Field Expression Patterns" for the full JSON templates.

Aggregation `Function` codes: `0`=Sum, `1`=Avg, `2`=Count, `3`=Min, `4`=Max, `5`=CountNonNull.

## Formatting Patterns

All property values in PBIR use `{ "expr": { "Literal": { "Value": "<value>" } } }` format.
Literal suffixes: `D` (double), `L` (long/integer), single-quoted strings, bare booleans.

For advanced formatting (rounded corners, shadows, conditional colors, axis/legend/sort,
theme visual styles, conditional formatting in tables, format strings),
read `references/formatting-patterns.md` and `references/required-properties.md`.

## Page Types

| Type | `page.json` config | Typical Size |
|---|---|---|
| Normal page | *(default — no special type)* | 1664×936 (standard) |
| Drillthrough | `"type": "Drillthrough"` + drillthrough filter fields in `filterConfig` | Standard canvas |
| Tooltip | `"type": "Tooltip"`, `"visibility": "HiddenInViewMode"` | Tooltip canvas preset (small) |
| Hidden page | `"visibility": "HiddenInViewMode"` | Standard canvas |

For drillthrough and tooltip page setup details, read `references/common-patterns.md`.

## Bookmarks

Stored in `definition/bookmarks/` — `bookmarks.json` (metadata) + `<name>.bookmark.json` (state).
Captures: page, filters, slicers, visibility, sort, drill state. Scopes: **Data**, **Display**,
**Current page**, **All vs Selected visuals**. Use for tab navigation, toggle views, reset filters.
See `references/bookmark-patterns.md` for complete bookmark JSON patterns
and `../power-bi-report-design/references/navigation-patterns.md` for navigation design patterns.

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-report-design` | Upstream (Phase 4a) | Design Spec drives all JSON generation decisions |
| `power-bi-semantic-model` | Upstream (Phase 2) | Model schema needed for queryState column/measure bindings |
| `power-bi-dax-development` | Upstream (Phase 3) | Measure names and tables needed for visual data bindings |
| `power-bi-performance-troubleshooting` | Cross-cutting | Report-level perf (visual count, slicer cardinality, query reduction) |
| `power-bi-feedback-iteration` | Downstream (Phase 5) | Visual formatting fixes and JSON corrections route here |

---

## Edit → Validate → Reload → Screenshot Loop

For rendered-output changes, follow this loop. Do not report completion until
validation, reload, and screenshot review are clean.

```text
┌──────────────────────────────────────────────────────────┐
│  1. Edit PBIR files                                      │
│  2. Validate           → errors? fix and go to 1         │
│  3. Desktop status     → choose the correct bridge PID   │
│  4. Desktop reload     → error? fix PBIR and go to 1     │
│  5. Screenshot/review  → issues? fix and go to 1         │
│  6. Clean              → report completion               │
└──────────────────────────────────────────────────────────┘
```

**Rules:**
- **Step 2** — `powerbi-report-author validate <path-to-.Report-dir>`. Pass the
  report definition directory (e.g., `Sales.Report`), not the `.pbip` file.
- **Steps 3–5** — use `powerbi-desktop` CLI: `status` → choose PID → `reload --pid <pid>`
  → `screenshot` or `screenshot-all` → review.
- `reload` covers report/PBIR changes only. For model/TMDL changes, use
  semantic-model skill and reopen the PBIP.
- **Theme cache:** Theme JSON files are cache-keyed by name — Desktop may not
  pick up edits on reload. Rename with a random suffix and update `report.json`.
- Run reload and screenshot operations **serially** per PID — never in parallel.

**Desktop CLI commands:**

| Command | Purpose | When |
|---|---|---|
| `open "<path.pbip>"` | Launch Desktop for a PBIP | Starting Desktop |
| `status` | List instances and bridge state | Before reload/screenshot |
| `reload --pid <pid>` | Reload current PBIP report files | After validated PBIR edits |
| `screenshot <page-id> --pid <pid> --output <file>` | Capture one page | Isolated page changes |
| `screenshot-all --pid <pid> --output-dir <dir>` | Capture every page | Report-wide changes |

**Common outcomes:**

| Output/error | Action |
|---|---|
| `"not_connected"` | Open report: `powerbi-desktop open "<path.pbip>"` |
| `AMBIGUOUS_DESKTOP_INSTANCE` | Run `status`, choose PID, retry with `--pid` |
| `Timeout` | Confirm `connected`, retry once; persist → `--wait-seconds 120` |
| `Cancelled` | Serialize operations per PID, retry |
| `ReportDefinitionValidationFailed` | Fix PBIR, validate, reload again |
| `REPORT_DIR_REQUIRED` | Select correct PID or open target PBIP |

Read `references/powerbi-desktop.md` for full command reference and troubleshooting.
Read `references/screenshot-review.md` for the visual review checklist.

---

## Authoring Metadata & Validation CLI

Use `powerbi-report-author` whenever you need PBIR facts that should not be
guessed: visual types, data roles, formatting objects, property names, enum
values, selectors, expression/value encodings.

| Command | Purpose | When |
|---|---|---|
| `catalog list` | List built-in visual types | Choosing visual type |
| `catalog describe <type>` | Roles, formatting keys, cardinality | Before creating/editing a visual |
| `formatting list-objects <type>` | Valid `objects.*` keys + VCO keys | Before applying formatting |
| `formatting describe-object <type> <obj>` | Property names, types, enums; `_selectorHint` | Finding exact property names |
| `formatting search <type> <regex>` | Regex search across all objects | **Don't know which object holds a property** |
| `formatting effective-properties <type>` | Flattened visual objects + VCOs | Full formatting surface snapshot |
| `expr encode --kind <t> <v>` | Generate PBIR value encoding | Writing formatting values |
| `expr decode '<json>'` | Decode PBIR expression to plain value | Inspecting existing values |
| `validate <path>` | Full PBIR validation | **After every batch of changes** |
| `preview-visuals <path>` | Visual inventory across report | Auditing all visuals |
| `preview-pages <path>` | Page metadata summary | Quick page overview |

Read `references/powerbi-report-author-cli.md` for full command catalog and encoding examples.

---

## Anti-Patterns and Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Using `"Entity"` inside filter `Where` conditions | Filter silently fails | Use `"Source"` with the alias from `From` |
| Omitting `nativeQueryRef` | Visual calculations may break | Always include `nativeQueryRef` |
| Reusing visual/filter names | Unpredictable behavior | Generate unique IDs |
| Setting `visualType` to invalid string | Visual renders as error box | Run `powerbi-report-author catalog describe <type>` or `powerbi-report-author catalog list` |
| Wrong role name for visual type | Field is ignored; visual blank | Match role names from `powerbi-report-author catalog describe <type>` |
| Mixing `Column` and `Measure` types | Query fails; visual error | Columns use `Column`, measures use `Measure` |
| Forgetting to add page to `pages.json` | Page invisible | Add to `pageOrder` array |
| Booleans without correct format | Wrong type | `"true"` / `"false"` (no suffix, unquoted in Value) |
| Numbers without type suffix | Type mismatch | `D` for decimals, `L` for integers |
| Editing `$schema` version | PBI Desktop may reject | Preserve existing version |
| Stringified JSON in `paragraphs` | Textbox shows nothing | `paragraphs` is a native JSON array |
| Using textbox as a thin line/divider | Renders ~24px tall regardless of `height` | Use a `shape` visual (rectangle) instead — shapes respect small dimensions |
| `visualContainerObjects` as sibling of `visual` | Schema validation error in PBI Desktop | Must be **inside** `visual` object, as sibling of `objects` |
| Partial VCO overrides | PBI resets omitted properties | Always set background + border + padding + visualHeader together |
| Using `tableEx` with dimension columns and measures all in `Values` | Headers render but no data rows even when DAX confirms data exists | Use `pivotTable`; put dimensions in `Rows` and measures in `Values` |
| Using PowerShell `ConvertTo-Json` to edit visual JSON | Property reordering, nesting depth truncation (`-Depth` default is 2) | Use Node.js for JSON manipulation, or always pass `-Depth 20` and verify structure |
| Using regex or string replacement to modify JSON files | Corrupts nesting structure — properties end up inside sibling values, braces misalign | Read file → `JSON.parse` → modify object → `JSON.stringify` → write back. Or use the `edit` tool with exact old/new string matching |
| `dataPoint.fill` without a selector on single-series charts | Bars/columns invisible despite data in tooltips | Use `dataPoint.defaultColor` for a base color without a selector; `fill` requires a `metadata` selector |
| Using `dataPoint.defaultColor` on multi-series charts | All series/categories get the same color — no visual differentiation | Use theme `dataColors` for consistent palette across visuals, or `dataPoint.fill` with `metadata` selectors for per-series overrides — see [color-strategy.md § Color Strategy Quick Reference](references/color-strategy.md#color-strategy-quick-reference) |
| Clustered bar/column chart colors collapse into one legend color | The visual has a Series role but all bars and legend markers share the same hue | Use per-series `dataPoint.fill` selectors or a theme `dataColors` palette; do not use `defaultColor` on clustered charts |
| Relying on theme `dataColors` alone for cross-visual measure consistency | Same measure gets different colors on different visuals (index-based assignment varies with projection order) | Maintain a measure→color mapping and apply explicit `dataPoint.fill`/`defaultColor` per visual — see [color-strategy.md § Cross-Visual Measure-Color Consistency](references/color-strategy.md#pattern-cross-visual-measure-color-consistency) |
| Using `ThemeDataColor` for explicit per-measure `dataPoint.fill` with metadata selectors | Colors silently resolve to white or black instead of expected palette color | Use `Literal` hex values for explicit color assignments with metadata selectors — `ThemeDataColor` is unreliable in this context |
| Choosing bar/series colors without checking background contrast | Bars or lines invisible against page/card background (e.g., white bars on white canvas) | Always pick saturated, mid-to-dark hues that contrast with the page and VCO background colors |
| `show` property on page-level `background` | Schema error — page `background` only supports `color`, `image`, `transparency` | Only VCO `background` (on visuals) has `show`; page background is always visible |
| Copying property names from doc examples without verifying | Warnings or silent failures — property names vary by visual type | Always run `powerbi-report-author formatting describe-object <type> <object>` for exact property names |
| Guessing which object a property belongs to | Wasted calls checking wrong objects one by one | Run `powerbi-report-author formatting search <type> <regex>` to grep across all objects at once |
| Formatting property has no effect (no error) | Setting `show: false` on cardVisual outline without an id selector — validates but renders unchanged | Check `powerbi-report-author formatting describe-object <type> <object>` for `_selectorHint`; use the dual-entry pattern (static + id selector entries) |
| Using `cardCalloutArea` on a single-value card | Properties validate but have no visible effect — `cardCalloutArea` only renders on multi-value cards (2+ measures in Data) | Use `outline`/`accentBar`/`fillCustom` with `{ id: "default" }` selector for single-value cards. For multi-value cards, `cardCalloutArea` controls per-callout tile styling — see [card.md § Multi-Value Formatting](references/card.md#multi-value-formatting) |
| Using `"Fields"` as the `queryState` role for `cardVisual` | Cards render empty — PBI Desktop cannot resolve the binding. Validator reports `Unknown role "Fields"` and `Required role "Data" missing` | `cardVisual`'s only data role is `"Data"`. `"Fields"` is the legacy `card` visual's role name — never carry it over. Always verify role names with `powerbi-report-author catalog describe cardVisual` — see [card.md § Single-Value Template](references/card.md#single-value-template) |
| Creating separate single-value `cardVisual` instances for multiple related KPIs | Wastes canvas space and misuses the visual type — `cardVisual` natively supports multiple projections in one tile | Default to one multi-value `cardVisual` with all measures as `Data` projections when ≥2 related KPIs are requested. Only use separate cards when per-card styling differences are required — see [card.md § When to Consolidate vs. Keep Separate](references/card.md#when-to-consolidate-vs-keep-separate) |
| Adding multiple fields to button slicer Values or Label roles | Slicer breaks or shows unexpected results — each role accepts only 1 field | Put one field in Values, one in Label; additional fields go to Tooltips |
| Looking at `filterConfig` on other visuals to understand slicer selections | Wrong location — selections live **only** inside the slicer's own `visual.json` via `expansionStates` + `objects.general.filter` | Always read `references/slicers.md` first when modifying slicers |
| Creating an image visual without prompting for the source type | Wrong visual structure — URL vs local file vs data field each have different schemas and expression types | Always ask the user for the image source (local file / URL / data field) before creating the visual — see [image.md § Source Types Overview](references/image.md#source-types-overview) |
| Creating a data-bound image visual with a field that lacks `dataCategory: ImageUrl` | Visual renders blank or error | **Warn the user first** — present alternatives (other ImageUrl fields, local file, URL) and confirm before creating — see [image.md § Select from data](references/image.md#3-select-from-data) |
| Placing background image on page canvas instead of visual plot area | Background image lands on `page.json → objects.background` when a visual context was intended | When a background image is requested in the context of a specific visual, default to `plotArea.image`. Only use page-level `background.image` when the user explicitly says "page/canvas background" — see [image.md § Plot Area Background Image](references/image.md#plot-area-background-image-plotareaimage) |
| Creating a `multiRowCard` visual | Legacy multi-row card — deprecated; `powerbi-report-author validate` warns with `PBIR_VISUAL_TYPE_DEPRECATED` | Always use `cardVisual`. For multiple KPIs, use a single multi-value `cardVisual` with all measures as projections in the `Data` role — see [card.md](references/card.md#multi-value-template) |
| Using `map` or `filledMap` instead of `azureMap` for map visuals | Legacy Bing Maps visuals — deprecated and must not be created; `powerbi-report-author validate` warns with `PBIR_VISUAL_TYPE_DEPRECATED` | Always use `azureMap` — see [map.md](references/map.md). If the map fails to geocode, debug fields or ask the user — do **not** silently substitute a non-map visual |
| Using legacy `card`/`table`/`matrix` | Deprecated; may break | Use `cardVisual`, `tableEx`, `pivotTable` |
| Creating `tableEx`/`pivotTable` without `columnAdjustment: growToFit` | Columns shrink-wrap to content, leaving unused whitespace | Always set `columnHeaders.columnAdjustment` to `growToFit` and `autoSizeColumnWidth` to `true` — see [table.md](references/table.md#default-rule--grow-to-fit) |
| Custom table/matrix row colors with no effect (white background) | Default style preset overrides `objects`-level `backColorPrimary`/`backColorSecondary` | Set `stylePreset` VCO to `'None'` on every `tableEx`/`pivotTable` with custom colors — see [table.md § Style Presets](references/table.md#style-presets-for-tables) |
| Table cells white despite dark VCO background | `visualContainerObjects.background` only controls outer container — table cells paint on top | Set dark colors in `objects.values.backColorPrimary/Secondary` and `objects.columnHeaders.backColor`, not in VCO — see [re-theming.md § Dark Mode Checklist](references/re-theming.md#dark-mode-authoring-checklist) |
| Dark theme applied but cards/tables/slicers still white | Dark mode triggers every formatting trap simultaneously | Follow the full [re-theming.md § Dark Mode Authoring Checklist](references/re-theming.md#dark-mode-authoring-checklist) — covers stylePreset, fillCustom+id selector, objects vs VCO, and contrast audit |
| Theme JSON changes do not appear after Desktop reload | Desktop caches theme files by file name | Rename the theme JSON with a small random suffix, update the theme registration in `report.json`, then reload; otherwise close and reopen Desktop |
| Placing `sortDefinition` inside `visual` or at root of `visual.json` | Schema validation error; sort silently ignored — chart falls back to alphabetical | `sortDefinition` is a property of **`query`** — use `visual.query.sortDefinition`. Supported since `visualConfiguration/2.2.0` |
| Container shape fill doesn't match reference | Text invisible or wrong background color | Match fill color and transparency to the reference. If the page background already provides the color, skip the shape. If the shape must be invisible, verify text still contrasts with the canvas — see [shape.md § Container Shapes](references/shape.md#container-shapes) |
| Shape text invisible after re-theme | Shape `text` object has no explicit `fontColor` — inherited foreground vanishes against a light fill on a light canvas | Always set explicit `fontColor` on shape `text` objects (in the `{ selector: { id: "default" } }` entry). During re-theming, audit all shapes with `text.show: true` |
| Enabling `logAxisScale` on data with zero or negative values | PBI Desktop silently falls back to linear scale — log of zero/negative is undefined | **Warn the user before applying.** Present alternatives (filter negatives, switch measure, use `labelDisplayUnits`). Apply only after all bound values are positive — see [cartesian.md § Log Scale](references/cartesian.md#log-scale-logaxisscale) |
| Changing theme without sweeping inline overrides | Old colors remain on shapes, page backgrounds, nav buttons, textboxes — theme-only change has no effect on hardcoded `Literal` hex at Priority 2 | Follow [re-theming.md § Re-theming Workflow](references/re-theming.md#re-theming-an-existing-report) Steps 0–3: build a color mapping, update theme JSON, then bulk-sweep `definition/` files for old hex before reload |
| Changing only `dataColors` in theme without sweeping | Shapes, accent bars, nav button borders retain old accent colors — they use hardcoded Literal hex from the old `dataColors` array, not `ThemeDataColor` references | Sweep ALL old `dataColors[N]` hex values across `definition/` files. Even same-polarity "just change the data colors" requests need the full sweep |

---

## Visual Capability Guardrails

### Modern Visual Types (always use)

| Do not create | Use instead |
|---|---|
| `card` | `cardVisual` |
| `table` | `tableEx` |
| `matrix` | `pivotTable` |
| `map`, `filledMap` | `azureMap` |

### Instance Selectors

Some formatting objects need `{ id: ... }` selectors. Run `formatting list-objects`
and `formatting describe-object`; follow `_selectorHint` and the dual-entry pattern
in `references/formatting-patterns.md`.
