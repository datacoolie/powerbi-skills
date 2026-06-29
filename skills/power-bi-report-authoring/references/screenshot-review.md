# Screenshot Review

> Read this after `powerbi-desktop` screenshot capture and before reporting
> completion for any rendered-output change.

## Review Workflow

1. Capture screenshots via `powerbi-desktop screenshot` or `screenshot-all`.
2. Review each screenshot against the Design Spec / expected outcome.
3. Use the checklist below to identify issues.
4. Fix any problems in PBIR JSON, then repeat the validate → reload → screenshot loop.

Do not rely only on structural validation. Fix any issue found in screenshots.

> **Screenshot scope:** Each screenshot captures the report page **AND** the
> right-hand filter pane (`outspacePane`) when enabled. Filter pane and filter
> card chrome are formattable surfaces — review them alongside on-page visuals.

## Checklist

### Layout and Visibility

- [ ] All visuals fully visible with no edge clipping or unintentional overlap
- [ ] Each page has a visible descriptive title/header
- [ ] Top-bar slicers sit to the right of the title (not replacing it)
- [ ] Titles, labels, values, subtitles, and legends are readable and not truncated
- [ ] Cards and KPIs show complete values (no ellipses or missing digits)
- [ ] Textboxes render without scrollbars
- [ ] Slicers are fully visible including lower portions and dropdown areas
- [ ] Spacing is intentional with no accidental large gaps

### Data Rendering

- [ ] Charts show actual bars, lines, or points (not empty frames)
- [ ] Tables and matrices have data rows (not just headers)
- [ ] No visuals showing error icons, "Can't display", or "Requires X fields"
- [ ] Blank/null values are expected (if present)
- [ ] Slicers show selectable values

### Formatting and Theming

- [ ] Background colors and theme applied (not default white/gray)
- [ ] Font colors contrast against their backgrounds
- [ ] Chart colors contrast with card/page backgrounds and distinguish series
- [ ] Each measure follows the color_map consistently across visuals
- [ ] Card gutters/padding are intentional (no accidental white from wildcard styles)
- [ ] Conditional formatting visually present where expected
- [ ] Border radius, shadows, and effects render as intended
- [ ] Filter pane styling matches theme (background, font, border colors)

## Common Screenshot Problems

| Symptom | Likely Cause | Fix |
|---|---|---|
| Visual shows error icon | Wrong entity/property names in `queryState` | Check TMDL for correct table/column names |
| Chart frame with no data | Missing or wrong role bindings | Verify with `powerbi-report-author catalog describe <type>` |
| Card/KPI value shows `...` or cutoff | Font too large for visual size | Increase size or reduce fontSize; check padding |
| Textbox shows scrollbar or clipped | Height didn't account for padding | Increase height: `max(18, ceil(fontSize * 25/16)) + padding` |
| Redundant subtitle appears | Auto-generated subtitle repeats title | Hide it or replace with useful context (date range, units) |
| Text invisible on dark background | Font color matches background | Set explicit contrasting `fontColor` |
| Visual overlaps another | Position coordinates conflict | Recalculate `x`, `y`, `width`, `height` |
| Slicer hidden behind chart | Header band overlaps, or slicer height too small | Re-read slicer ref, recompute height, reserve full band |
| Card has white gutters/padding | Wildcard theme padding applied to cards | Add card-specific padding/background overrides |
| Same measure uses different colors | Color map not applied consistently | Re-read design brief, set each visual to mapped color |
| Blank page | No visuals, or visuals with `z < 0` | Check visual directories and z-order |
| Slicer shows no items | Wrong column binding or filter conflict | Verify slicer's `queryState` column has data |
| Bars/columns invisible despite data | `dataPoint.fill` without selector | Use `defaultColor` for base color, or add `metadata` selector |
| Theme JSON didn't apply | Desktop caches by file name | Rename theme file + update `report.json`, or reopen Desktop |
| Table cells white despite dark VCO bg | VCO only controls outer container | Set colors in `objects.values.backColorPrimary/Secondary` |

## When to Take Screenshots

| Change Type | Screenshot Scope |
|---|---|
| Single visual edit | `screenshot <page-id>` for that page |
| New page added | `screenshot <new-page-id>` |
| Theme change | `screenshot-all` (affects every page) |
| Navigation/bookmark | `screenshot-all` |
| Page order change | `screenshot-all` |
| Filter pane styling | `screenshot <any-page-with-filters>` |
| Font change | `screenshot-all` (fonts are report-wide) |
| Report-wide formatting | `screenshot-all` |
