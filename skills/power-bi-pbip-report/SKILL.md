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
| `scripts/validate_report.py` | **Run after generation** — validates against official Microsoft JSON schemas, required properties, cross-references, bookmarks, naming conventions. Supports `--offline` for cached-only mode. |
| `scripts/validate_schemas.py` | **Proactive schema validator** — maps every PBIR file to its correct schema by filename pattern (not relying on `$schema` declarations). Supports `--sync` (download all schemas), `--sync-only` (CI cache prep), `--component <type> <file>` (single-file validation), `--check-versions` (detect outdated schema versions), `--offline`. |
| `scripts/finalize_pbir.py` | **Phase 4c polish** — snap_grid, align_kpi_row, apply_theme_tokens, normalize_fonts, ensure_alt_text. Supports `--dry-run`, `--skip`, `--only`. |
| `scripts/design_quality_check.py` | **Phase 4c lint** — 14 checks (E1-E4: contrast, drillthrough back button, bookmark targets, orphan pages; W1-W10: visual counts, pie slices, alt text, default page names, bad titles, hardcoded hex, 3D effects, rainbow palette, visual budget, alt text quality). Use `--style executive\|analytical\|operational` and `--write-report` to emit `design_report.md`. |
| `scripts/pbir_gate.py` | **Unified Phase 4c gate** — chains finalize → lint → validate into one pass/fail command. Supports `--dry-run`, `--skip-finalize`, `--skip-lint`, `--allow-warnings`, `--json`. Exit codes: `0` pass, `1` input error, `2` fail, `3` tool error. |

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

**If invoked from the `power-bi-developer` agent (Phase 4c), use the unified gate:**

```powershell
# Recommended — single command, one pass/fail verdict
python skills/power-bi-pbip-report/scripts/pbir_gate.py `
    --report <path-to-.Report-folder> `
    --style <style-from-design-spec>
```

The gate chains 4 stages: `finalize_pbir.py` → `design_quality_check.py` → `validate_report.py` → `validate_schemas.py`.
Exit codes: `0` = pass, `1` = input error, `2` = fail, `3` = tool error.
Add `--allow-warnings` to pass with warnings, `--json verdict.json` to save the result.
Flags: `--skip-finalize`, `--skip-lint`, `--skip-validate`, `--skip-schemas`.
See `../power-bi-report-design/references/polisher.md` for the full Phase 4c routing table.

<details><summary>Manual alternative (run each stage separately)</summary>

```powershell
# 1. Mechanical polish (snap grid, align KPIs, tokenize theme colors, unify fonts, alt text)
python skills/power-bi-pbip-report/scripts/finalize_pbir.py --report <path-to-.Report-folder>

# 2. Design-quality lint (style-aware: executive / analytical / operational)
python skills/power-bi-pbip-report/scripts/design_quality_check.py `
    --report <path-to-.Report-folder> `
    --style <style-from-design-spec> `
    --write-report

# 3. Structural validation (cross-refs, naming, required properties)
python skills/power-bi-pbip-report/scripts/validate_report.py <path-to-.Report-folder>

# 4. JSON Schema validation (proactive, path-based)
python skills/power-bi-pbip-report/scripts/validate_schemas.py <path-to-.Report-folder> --offline
```

Per-script exit codes: `0` = pass, `1` = warnings only, `2` = errors present (must fix).

</details>

**Standalone usage:**
```
python skills/power-bi-pbip-report/scripts/validate_report.py <path-to-.Report-folder>
python skills/power-bi-pbip-report/scripts/validate_schemas.py <path-to-.Report-folder> --offline
```

`validate_report.py` checks:
1. **JSON syntax** — every `.json` and `.pbir` file parses cleanly
2. **Required properties** — `$schema`, `name`, `position`, `themeCollection`, etc.
3. **Cross-references** — page folders match `pages.json`, custom visuals registered in `report.json`
4. **Naming conventions** — kebab-case for page and visual folders

`validate_schemas.py` checks: every file against its correct Microsoft JSON schema (by path pattern).

Fix all **errors** before delivering. **Warnings** are advisory (naming, unused registrations).  

If neither script is available, manually verify:
- Every JSON file parses (`json.loads()` succeeds)
- Every `visual.json` has `name`, `position` (with `x`, `y`, `height`, `width`), and either `visual` or `visualGroup`
- `pages.json` → `pageOrder` entries match actual page folder names
- `page.json` → `name` matches its parent folder name
- Custom visual types used in visuals are registered in `report.json` → `publicCustomVisuals`

---

## JSON Schema Reference

Schema URLs and versions are maintained in `scripts/validate_schemas.py` → `SCHEMA_REGISTRY`.
Run `python validate_schemas.py --check-versions` to detect outdated schema declarations.
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
