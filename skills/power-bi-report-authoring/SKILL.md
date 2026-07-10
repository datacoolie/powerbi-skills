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
|---|---|---|
| Using legacy visual types (`card`, `table`, `matrix`, `map`) | Deprecated; may break | Use `cardVisual`, `tableEx`, `pivotTable`, `azureMap` |
| Using `"Entity"` inside filter `Where` conditions | Filter silently fails | Use `"Source"` with alias from `From` |
| Omitting `nativeQueryRef` | Visual calculations may break | Always include `nativeQueryRef` |
| Reusing visual/filter names | Unpredictable behavior | Generate unique IDs |
| Wrong role name for visual type | Field ignored; visual blank | Match roles from `catalog describe <type>` |
| Mixing `Column` and `Measure` types | Query fails; visual error | Columns use `Column`, measures use `Measure` |
| Forgetting to add page to `pages.json` | Page invisible | Add to `pageOrder` array |
| Numbers without type suffix | Type mismatch | `D` for decimals, `L` for integers |
| Editing `$schema` version | Desktop may reject | Preserve existing version |
| Stringified JSON in `paragraphs` | Textbox shows nothing | `paragraphs` is a native JSON array |
| Using textbox as thin line/divider | Renders ~24px tall | Use `shape` visual (rectangle) |
| `visualContainerObjects` as sibling of `visual` | Schema error | Must be **inside** `visual` object |
| Using `tableEx` with dimensions+measures all in `Values` | No data rows | Use `pivotTable`; dimensions in `Rows`, measures in `Values` |
| Using PowerShell `ConvertTo-Json` to edit JSON | Nesting truncation | Use Node.js or always pass `-Depth 20` |
| Using regex/string replacement on JSON | Corrupts structure | Parse → modify → stringify |
| `dataPoint.fill` without selector on single-series | Bars invisible | Use `dataPoint.defaultColor` for base color |
| `dataPoint.defaultColor` on multi-series | All series same color | Use `dataPoint.fill` with `metadata` selectors |
| `ThemeDataColor` in explicit `dataPoint.fill` with metadata selector | Resolves to white/black | Use `Literal` hex values for explicit assignments |
| Colors without checking background contrast | Bars/lines invisible | Pick saturated hues contrasting with background |
| `show` property on page-level `background` | Schema error | Page background has no `show`; only VCO does |
| Guessing property names from memory | Silent failures | Always use `formatting describe-object` or `formatting search` |
| Formatting property has no effect (no error) | Missing id selector | Check `_selectorHint`; use dual-entry pattern |
| Theme JSON changes don't apply after reload | Desktop caches by name | Rename theme file + update `report.json` |
| `sortDefinition` outside of `query` | Sort ignored | Place in `visual.query.sortDefinition` |
| Partial VCO overrides | PBI resets omitted properties | Always set background + border + padding + visualHeader together |
| Dark theme but cards/tables still white | Need explicit overrides per visual type | Follow dark mode checklist: stylePreset, fillCustom, objects vs VCO |
| `tableEx`/`pivotTable` without `columnAdjustment: growToFit` | Columns shrink-wrap | Set `columnHeaders.columnAdjustment` to `growToFit` |
| Custom table colors with no effect | Style preset overrides | Set `stylePreset` VCO to `'None'` |

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
