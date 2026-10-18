---
name: power-bi-report-authoring
description: >-
  Create, edit, validate, preview, and screenshot Power BI reports in PBIR/PBIP format with the
  official `powerbi-report-author` CLI (scaffold, catalog, formatting, expr, theme, validate,
  preview, pack/unpack); generate visuals from a layout recipe with `build_report_from_layout.py`.
  Covers the `authoring` mode of Microsoft's `powerbi-report-cli` skill. Use when the user wants to
  implement an approved report spec or Design Brief, add or edit pages, visuals, filters, slicers,
  bookmarks, buttons, themes, field parameters, conditional formatting, custom visuals or formatting,
  or validate PBIR and verify rendering in Desktop or the Fabric service. For visual design use
  `power-bi-report-design` first; for requirements/approval use `power-bi-business-analysis`;
  for publishing use `power-bi-management`. Triggers: "edit PBIR", "create Power BI report page",
  "add visual to PBIP", "format report visual", "validate Power BI report", "preview PBIP",
  "screenshot report page", "scaffold a new report".
---

# Power BI PBIR/PBIP Report Authoring

Owns **PBIR file mechanics**: pages, visuals, bindings, filters, slicers,
navigation, bookmarks, themes, formatting, validation, preview, and screenshots.
It produces and edits the `<Report>.Report/` folder. Semantic model/DAX work
belongs to `power-bi-semantic-model` / `power-bi-dax-development`; Fabric
transport belongs to `power-bi-management`.

**Input:** an approved Design Spec (`power-bi-report-design`), a `Design Brief:`
block / `_brief/report-spec.md` (`power-bi-business-analysis` planning), or a
concrete edit request.

Canvas: **1920 × 1080 (FHD)** is the default for new pages (layout recipes are authored on it; for another
16:9 canvas rescale with `../power-bi-report-design/scripts/rescale_layout.py`); preserve existing page
sizes unless resizing is approved. Tooltip pages **320 × 240**.

> **Official source.** This skill mirrors the `authoring` mode of
> [microsoft/skills-for-fabric `powerbi-report-cli`](https://github.com/microsoft/skills-for-fabric)
> (MIT). `references/authoring.md` (+ `-part-02/03/04`) is the official mode
> guide and `references/authoring/*.md` are the official topic files — verbatim.
> On any conflict between an official file and a repo-specific note, **the
> official file wins**.
>
> **Mode → skill map** (official docs use mode names):
> `planning` → `power-bi-business-analysis` · `design` → `power-bi-report-design`
> · `authoring` → this skill · `management` → `power-bi-management` ·
> `semantic-model-authoring` → `power-bi-semantic-model`.

## Tool choice — CLI first

| Need | Use (CLI) | Do not use |
|---|---|---|
| Visual roles, formatting objects, enums, selectors, value encoding | `powerbi-report-author catalog / formatting / expr / theme / text` | memory, doc examples, MCP |
| New report shell | `powerbi-report-author scaffold` | hand-written `.pbip`/`definition.pbir`/`report.json` |
| Schema + cross-file validation | `powerbi-report-author validate` | — |
| Rendered check (Desktop **or** service) | `powerbi-report-author preview --host desktop\|service` | calling `powerbi-desktop` directly, `--pid` |
| Read-only audit | `powerbi-report-author preview-visuals/-pages/-filters/-themes` | regex over JSON |
| Local ⇄ Fabric payload | `powerbi-report-author pack / unpack` (then `power-bi-management`) | `jq`/`base64` loops |

MCP is only for the semantic model (table/column/measure names, DAX checks) —
see `power-bi-semantic-model`. If a CLI capability and an MCP tool both fit, the
CLI wins.

## Authoring completion gate — MANDATORY

Schema validation is never the end. Any task that creates or modifies rendered
content is incomplete until **all** of these are true:

1. `powerbi-report-author validate "<.Report folder>"` succeeds.
2. The latest PBIR is loaded into the selected host (`preview … --status` first,
   then open/attach or `--reload`).
3. Every affected page is captured (`--screenshot`, `--page`/`--all-pages`;
   `--all-pages` for theme/global/navigation/page-order changes).
4. Screenshots are reviewed with `references/authoring/screenshot-review.md`.
5. Visible issues are fixed and the loop repeats.

If load/capture/review is blocked, report screenshot validation as **blocked** —
do not claim completion. On the **service** host, after review passes, open the
validated report in a visible (non-headless) preview and leave it open. Load and
capture are separate CLI invocations (never `--reload` + `--screenshot` together).
Read `references/authoring/preview.md` (+ `-part-02/03/04`) before the first
preview command; it owns safety gates, `hasUnsavedChanges` hard-stop, the one-retry
`correction` rule, screenshot artifact lifecycle, and semantic-model reload.

```text
edit → validate → status → open/reload → screenshot → review → (fix → repeat)
```

Preview essentials (full rules in `preview.md`):

| Operation | Sequence |
|---|---|
| Open/attach, reload | `--status` first, then the operation |
| Screenshot | screenshot only — never status first |
| Desktop | always `--host desktop`; never `--pid`; failure without a machine-readable `correction` ends the turn |
| Service | always `--group <workspace-guid> --dataset <semantic-model-guid>`; never infer either ID; `--headless` for agent runs |
| TMDL changed | `--reload-with-model` + model processing per `preview-part-04.md` |

Preview is inspection. **Never publish** as part of authoring — publishing needs
an explicit request and goes to `power-bi-management`.

## Must / Prefer / Avoid

**MUST**
- Look up roles/formatting/enums/selectors with the CLI before writing them.
- Scaffold new reports with `powerbi-report-author scaffold`; preserve every existing `$schema`.
- Use modern visuals only: `cardVisual`, `tableEx`, `pivotTable`, `azureMap`.
- Validate after each logical batch, then run the completion gate above.
- Edit JSON with structured tools (Node `JSON.parse`/`stringify` or exact-match edits) — never regex or PowerShell `ConvertTo-Json`.
- Read `references/authoring/formatting-overview.md` before any appearance change.

**PREFER**
- Start from an approved Design Spec / `Design Brief:` / `_brief/report-spec.md`.
- Route design uncertainty to `power-bi-report-design`.
- A deterministic Node.js generator for large builds; do not hand a whole PBIP to a subagent (split by page/visual family and integrate yourself).

**AVOID**
- Guessing PBIR JSON from memory; copying property names from examples without `formatting describe-object`.
- Scaffolding-only completion: every requested page needs data-bound visuals.
- Treating a stale screenshot as validation when the host reports unsaved changes.

## Quick start

0. **Route** — greenfield → planning first (`power-bi-business-analysis`); look & feel → `power-bi-report-design`; come back here with an approved brief.
1. **CLI setup** — Node ≥ 20, then `npm install -g @microsoft/powerbi-report-authoring-cli@latest` (it bundles the Desktop bridge; no separate `powerbi-desktop` install). Check `powerbi-report-author --version` and `powerbi-report-author doctor`.
2. **Know the model** — TMDL files or the semantic-model MCP for exact table/column/measure names. Missing measures → Phase 3 first.
3. **Scaffold** new reports (`references/authoring-part-02.md` → *Greenfield*), bind the model (`references/authoring/model-binding.md`).
4. **Route by intent** with the topic table below; read the topic file before editing.
5. **Author**, then validate → preview → review (gate above).
6. **Report back** — concise summary of what changed, issues, and screenshot status.

## Reference map

### Official mode guide (read in order as needed)

| File | Content |
|---|---|
| `references/authoring.md` | Mode rules, preview critical notes, quick-start workflow |
| `references/authoring-part-02.md` | Topic routing table, large-build execution, CLI setup, PBIR layout, **greenfield scaffold** |
| `references/authoring-part-03.md` | Metadata CLI commands, guardrails (modern visuals), preview commands, validation |
| `references/authoring-part-04.md` | Anti-patterns & pitfalls table (read before touching visuals/bindings/filters/formatting) |

### Official topic files (`references/authoring/`)

| File | Read when |
|---|---|
| `authoring-workflows.md` | Add/modify pages, visuals, drillthrough, interactions (full JSON) |
| `model-binding.md` | Create/repoint/repair `definition.pbir` (`byPath` vs `byConnection`) |
| `preview.md` → `-part-02/03/04` | Desktop/service preview, status, screenshots, lifecycle, model reload |
| `screenshot-review.md` | Reviewing captured pages |
| `powerbi-report-author-cli.md` (+`-part-02`) | Full CLI command catalog (catalog/formatting/expr/theme/text/scaffold/pack/unpack/preview-*) |
| `powerbi-desktop.md` | Desktop routing summary (always via `preview`) |
| `formatting-overview.md` → `formatting.md` (+`-part-02`) | Cascade, selectors, encoding, dual-entry pattern |
| `color-strategy.md` | Data-point colors, cross-visual measure colors |
| `conditional-formatting.md` (+`-part-02…07`) | Gradients, rules, icons, data bars, URLs, field-driven colors |
| `page-formatting.md`, `filter-pane.md` | Page canvas/wallpaper; filter pane & card chrome |
| `theming.md` (+`-part-02`), `re-theming.md` (+`-part-02/03`) | Theme JSON; switching themes on existing reports, dark mode |
| `expressions.md` | Column/Measure/Aggregation/Hierarchy refs, visual calcs, sort |
| `filters.md`, `slicers.md` (+`-part-02`), `field-parameters.md` | Filters, slicers, metric-selector parameters |
| `bookmark.md` | Bookmarks, toggles, groups, button actions |
| `cartesian.md` (+`-part-02/03/04`), `map.md`, `card.md` (+`-part-02/03`), `kpi.md`, `table.md` | Chart, map, card/KPI, table/matrix visuals |
| `button.md` (+`-part-02/03`), `image.md`, `shape.md`, `textbox.md` | Buttons & navigation, images, shapes, text |
| `custom-visuals.md` | AppSource / org-store / private `.pbiviz` registration |
| `version-control.md` | Git branching, commit, rollback |

### Repo-specific supplements (non-authoritative; verify with the CLI)

| File | Use |
|---|---|
| `references/visual-templates.md` | Complete `visual.json` templates per visual type |
| `references/formatting-patterns.md`, `references/common-patterns.md` | Rounded corners, shadows, KPI rows, slicer panels, sync slicers, interactions |
| `references/bookmark-patterns.md` | Toggle/reset/tab bookmark recipes |
| `references/mobile-layout.md` | `mobile.json` rules and template |
| `references/required-properties.md`, `references/folder-structure.md` | Property cheat sheet, folder layout |
| `references/custom-visuals-catalog.md` | Catalog of `visualType` identifiers seen in reference reports |
| `references/page-template.json` | `page.json` for adding pages (shell files come from `scaffold`) |
| `references/themes/*.json` | 8 ready-made industry themes → copy to `StaticResources/RegisteredResources/` |
| `scripts/*.py` | Phase 4c polish/lint/gate (see below); `build_report_from_layout.py` (recipe + slot spec → visuals + layout manifest), `check_layout_drift.py` (built vs approved layout) |
| `references/layout-spec-example.json` | Example slot spec for `build_report_from_layout.py` |

## Naming convention (this repo)

- lowercase-kebab-case for page and visual folders; prefix visual folders with `visualType`.
- Pages: `overview`, `sales-analysis`, `product-detail` (drillthrough), `customer-tooltip`.
- Visuals: `card-kpi-revenue`, `clusteredBarChart-top-10`, `lineChart-monthly-trend`, `slicer-date-range`, `shape-header-bg`, `textbox-page-title`, `actionButton-back`, `pivotTable-sales-by-region`.
- Bookmarks: `tab-{section}`, `reset-{scope}`.
- CLI-scaffolded page IDs are opaque; rename only with `pages.json`, bookmark and navigation references updated together, then validate.

## Generating pages from layout recipes

For pages built from a `power-bi-report-design` recipe, do not hand-place visuals. Write a slot spec
(`references/layout-spec-example.json`) and run:

```powershell
python skills/power-bi-report-authoring/scripts/build_report_from_layout.py --report <.Report> --spec spec.json
```

It positions every slot at the recipe's coordinates on the spec's canvas (default FHD; rescaled for others),
validates roles with `powerbi-report-author catalog describe` (unknown or missing required roles, and legacy
types `card`/`multiRowCard`/`table`/`matrix`/`map`/`filledMap`, are errors), writes theme-driven textboxes and
alt text, runs `powerbi-report-author validate`, and records the approved slots in `_brief/layout-manifest.json`
(outside the `.Report` folder so it never enters a Fabric upload). Recipe slots missing from the spec are
skipped and reported. Rows a recipe expresses as ranges (`160…1584`) are not generated — place those by hand.
Afterwards the gate's drift stage (`check_layout_drift.py`) flags any visual moved or removed from the approved
layout, plus new overlaps. Generation is only the layout half: formatting, conditional formatting, filters,
bookmarks and navigation still follow the official topic files, and the completion gate (validate → preview →
screenshot → review) still applies.

## Phase 4c gate (power-bi-developer pipeline)

Run after authoring and before hand-off:

```powershell
python skills/power-bi-report-authoring/scripts/pbir_gate.py --report <path-to-.Report> --style <executive|analytical|operational> [--apply]
```

**Read-only by default.** Without `--apply` the finalize stage is a dry run and `design_report.md` goes to a temp
evidence dir (`--evidence-dir` overrides). Use `--apply` only on a report generated in this session; never on a
brownfield report whose layout must be preserved (finalize snaps positions, rewrites fonts/colors, adds alt text).
`--apply` is also guarded: inside a git work tree it refuses when the report folder has uncommitted changes
(commit/stash first so the polish rewrite is its own revertable diff; `--force-apply` overrides); outside git it
copies the report to `<temp>/pbir-gate-backup/` before writing.

Chains `finalize_pbir.py` (snap grid, align KPI row, theme tokens, fonts, alt text)
→ `design_quality_check.py` (E1–E4 errors, W1–W10 warnings) → `validate_report.py`
(cross-refs, naming, advisories) → `powerbi-report-author validate` (schema, source
of truth) → `check_layout_drift.py` (vs `_brief/layout-manifest.json`; skipped without one). Exit `0` pass, `1` input error, `2` fail, `3` tool error;
`--allow-warnings`, `--json verdict.json`, `--skip-finalize|lint|validate|schemas|drift`, `--manifest`, `--drift-tolerance`.
The gate does **not** replace the preview/screenshot completion gate above — run it,
then capture and review screenshots. See `../power-bi-report-design/references/polisher.md`.

## Related skills

| Skill | Relationship |
|---|---|
| `power-bi-business-analysis` | Upstream: planning, `_brief/report-spec.md`, approval barrier |
| `power-bi-report-design` | Upstream (Phase 4a): Design Spec / `Design Brief:` drives all generation |
| `power-bi-semantic-model`, `power-bi-dax-development` | Upstream: exact table/column/measure names; Measures Gate |
| `power-bi-management` | Downstream: publish/download/rebind in Fabric (`pack`/`unpack` + `az rest`) |
| `power-bi-performance-troubleshooting` | Cross-cutting: visual count, slicer cardinality, query reduction |
| `power-bi-feedback-iteration` | Downstream (Phase 5): formatting/JSON fixes route back here |
