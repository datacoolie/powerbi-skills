# Change-Impact Scoping

Before implementing a change, identify every file and artifact it touches. This prevents incomplete fixes and downstream regressions.

## Impact Scope Checklist

For each change, mark every box that applies:

```
□ Model only (no report changes needed)
□ DAX only (add/modify measures, no visual changes)
□ Report only (visual/layout changes, no model changes)
□ Theme only (colors/fonts, no structural changes)
□ Model + DAX (new column → new measure)
□ Model + Report (new relationship → visual interaction)
□ DAX + Report (new measure → visual that displays it)
□ Full stack (model + DAX + report)
□ Cross-project (shared dataset / paginated reports)
```

## Impact → files affected

| Scope | PBIP files touched |
|---|---|
| Model — new column | `<Project>.SemanticModel/definition/tables/<Table>.tmdl` |
| Model — new table | `<Table>.tmdl` + `relationships.tmdl` + `model.tmdl` (measure table list) |
| Model — relationship | `<Project>.SemanticModel/definition/relationships.tmdl` |
| Model — RLS | `<Project>.SemanticModel/definition/roles.tmdl` |
| DAX — new measure (reporting-level) | `<Project>.Report/definition/reportExtensions.json` |
| DAX — new measure (model-level) | Measure table `.tmdl` |
| Report — new page | `pages/pages.json` + new `pages/<slug>/page.json` + all child visuals |
| Report — modify visual | `pages/<page>/visuals/<visual>/visual.json` |
| Report — layout change | Multiple `visual.json` (position props only) |
| Report — theme | `StaticResources/RegisteredResources/*.json` + `report.json` |
| Report — navigation | `pages/<page>/visuals/<button>/visual.json` (actions) + bookmarks in `report.json` |
| Report — mobile | `pages/<page>/mobileState.json` (or `mobile.json`) |

## Downstream validation matrix

When you change X, verify Y:

| Changed | Verify |
|---|---|
| Model table name | All DAX references, all visual `queryState` bindings |
| Model column name | All DAX references, all visual field bindings, sort-by column refs |
| Relationship cardinality / direction | All cross-filtering still works; RLS still filters correctly |
| Storage mode | Refresh still works; DirectQuery compatibility of all DAX |
| Measure formula | All visuals using the measure; all tooltips using the measure |
| Measure name | All visuals, all bookmarks (stored filter refs), all field parameters |
| Theme colors | Every visual's custom color overrides (check hard-coded HEX) |
| Page name | Drillthrough targets, bookmark navigation, button actions |
| Visual position | Z-order; overlap with other visuals; mobile layout still valid |

## Risk assessment

Before implementing, score:

| Dimension | Low risk | High risk |
|---|---|---|
| Scope | Single file | > 5 files |
| Blast radius | 1 visual | Entire page or cross-page |
| Reversibility | Git revert is clean | DB schema change / data migration |
| Testability | Has validation query | Requires manual regression |
| Dependencies | No downstream consumers | Shared dataset / paginated reports |

**Rule:** If any dimension is **High risk**, run the change through a feature branch (see `ab-variant-testing.md`) and full validation (see `validation-checklist.md`).

## Scoping discipline

- ❌ Don't silently expand scope during implementation — re-scope and re-estimate
- ❌ Don't skip model validation after "pure report" changes that reference new columns
- ❌ Don't edit > 10 files in one change without a branch + review
- ✅ Do document every file touched in the commit message
- ✅ Do update the changelog for any user-visible change
