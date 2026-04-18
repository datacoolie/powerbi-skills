# PBIP Git Diff Guide

PBIP is file-based — every change produces a readable diff. Use this guide to interpret and review PBIP commits.

## Branching Strategy

```
main          ← Production-ready reports (tagged releases)
├── dev       ← Integration branch for testing
│   ├── fix/<area>-<short-description>
│   ├── feat/<area>-<short-description>
│   └── perf/<area>-<short-description>
```

### Rules
- `main` is deploy-ready; never commit directly
- `dev` accepts merges from fix/feat/perf branches after review
- Feature branches are short-lived (merge within 1-3 days)
- Tag releases on `main` (`v1.0.0`, `v1.1.0`)

## Commit Message Convention

```
Pattern: <type>(<scope>): <description>

Types:
- fix:      Bug fix (data, visual, measure)
- feat:     New feature (page, measure, visual)
- perf:     Performance improvement
- style:    Cosmetic change (theme, formatting)
- refactor: Model restructuring without behavior change
- docs:     Documentation / changelog
- test:     Validation queries, UAT artifacts

Scopes:
- model  — TMDL changes
- dax    — measure / calc group changes
- report — PBIR changes
- theme  — theme file changes
- rls    — security role changes
- docs   — documentation
```

### Examples
```
fix(dax): correct YTD calculation for fiscal year start
feat(report): add supplier scorecard drillthrough page
perf(model): remove unused columns from FactSales
style(report): update theme to 2026 brand colors
refactor(model): split FactOrders into FactOrderHeader + FactOrderLine
```

## PBIP File Diff Map

When reviewing a diff, map changed files to the type of change:

| Change Type | Files Affected | What to verify |
|---|---|---|
| **New page** | `pages/pages.json` (list), `pages/<slug>/page.json`, `pages/<slug>/visuals/**` | Page slug matches display name; navigation updated |
| **Modified visual** | `pages/<page>/visuals/<visual>/visual.json` | Field refs still valid; position doesn't overlap |
| **New measure (report-level)** | `definition/reportExtensions.json` | Unique name; format string set |
| **New measure (model-level)** | `<Project>.SemanticModel/definition/tables/<Table>.tmdl` | Added to correct measure table |
| **Column change** | `tables/<Table>.tmdl` | DAX references updated; visual bindings updated |
| **New relationship** | `definition/relationships.tmdl` | Single direction; cardinality correct |
| **Theme change** | `StaticResources/RegisteredResources/*.json` + `report.json` | theme referenced by name in `report.json` |
| **Mobile layout** | `pages/<page>/mobileState.json` | Visual IDs match desktop |
| **Bookmark** | `report.json` (bookmarks array) | Display name unique; filter state captured |
| **Drillthrough** | `pages/<target-page>/page.json` (drillFilter properties) + target visuals | Drillthrough column defined; back button present |
| **RLS** | `<Project>.SemanticModel/definition/roles.tmdl` | Filter expression valid DAX |

## Reviewing a PBIP PR

### Before merging, verify:

```
□ Commit messages follow the convention
□ No binary files committed (.pbix, large exports) — only PBIP JSON / TMDL
□ cache.abf, .pbi, .localSettings.json NOT committed (add to .gitignore)
□ Schema validation passes (scripts/validate_report.py)
□ Diff scope matches commit message scope
□ Changelog updated if user-visible change
□ Test evidence attached (for Critical/High fixes)
```

### `.gitignore` essentials

```gitignore
# Power BI
*.pbix
*.pbit
.pbi/
.pbi-tools/
cache.abf
localSettings.json
.localSettings.json

# Project local
*.tmp
*.bak
```

## Reading Diffs — Common Patterns

### "Why does a small visual change touch many files?"
Position changes in Power BI cascade: changing a visual's `x, y` shifts Z-order, which can re-serialize neighboring visuals. Expected — verify by eyeballing the rendered report.

### "Why does a theme change show no report.json delta?"
Theme is referenced by name in `report.json.themeCollection`. Only the `StaticResources/RegisteredResources/<theme>.json` file changes. Report.json is unchanged unless the theme name changed.

### "Why does adding a measure touch `reportExtensions.json` but not the model?"
Report-level measures live in PBIR, not TMDL. They're scoped to the report only. If shared across reports, promote to a model-level measure in a `.tmdl` file.

### Merge conflict hotspots
- `pages/pages.json` — page ordering and visibility
- `report.json` — bookmarks array, theme, publicCustomVisuals
- Visual `position` properties — when two branches reposition the same visual

Resolve by understanding intent of both branches, then picking or combining manually. Avoid blind accept-current / accept-incoming.

## Tools

- **Validation:** `scripts/validate_report.py` (schema + structural checks)
- **Visual diff:** VS Code's built-in JSON diff works well for PBIR
- **TMDL diff:** VS Code TMDL extension provides syntax highlighting
- **Power BI Desktop:** always open the `.pbip` after a merge to verify render
