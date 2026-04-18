# Layouts — Catalog Reference

Page-layout recipes consumed by the Strategist (for selection) and the Executor
(for PBIR generation). Each recipe is **one markdown file** + **one SVG preview**
+ **one JSON index entry**.

## Files

| File | Role |
|---|---|
| `<id>.md` | Human-readable recipe: zones, slot coordinates, nav rules, theme guidance, when-NOT-to-use |
| `layouts-index.json` | Machine-readable catalog — single source of truth. Every layout must have an entry. |
| `layouts-index.schema.json` | JSON Schema (Draft 2020-12) that validates the index. |
| `../../assets/layout-previews/<id>.svg` | Wireframe preview thumbnail (monochrome, currentColor). Pointed to by the index `preview` field. |

See [`../../assets/layout-previews/README.md`](../../assets/layout-previews/README.md)
for the SVG contract.

## Structure decision: **flat filesystem, rich metadata**

The catalog is a **flat directory** (one `.md` per layout at the top level) — not
grouped into subfolders like `ppt-master/templates/layouts/`. This is
intentional.

### Why flat

1. **Multi-axis data, one folder tree.** Each layout has four independent axes —
   `style`, `canvas_class`, `domain`, `audience`. A folder tree can only express
   one axis; filtering on the others would force symlinks or cross-references.
2. **1-to-1 pairing stays trivial.** `<id>.md` ↔ `<id>.svg` is a simple
   coverage check. Nested paths would force every reader to parse a tree.
3. **Schema stays simple.** `"file": "^[a-z0-9\\-]+\\.md$"` — no slashes, no
   traversal risk.
4. **Works well up to ~30 items.** VS Code file list, `file_search`, and `ls`
   all show 13–30 items on a single screen without scrolling.

### Virtual grouping via index fields

Group by any axis at **query time**, not at filesystem time:

```jsonc
// "All analytical landscape finance layouts":
layouts.filter(l =>
  l.style === 'analytical' &&
  l.canvas_class === 'landscape-16x9' &&
  l.domain === 'finance')

// "All layouts tagged drillthrough-target":
layouts.filter(l => l.tags.includes('drillthrough-target'))

// "All stable mobile layouts":
layouts.filter(l => l.canvas_class === 'mobile-portrait' && l.status === 'stable')
```

### When to restructure

| Trigger | Proposed split |
|---|---|
| 30+ layouts | Group by `canvas_class/` on disk: `layouts/landscape/`, `layouts/mobile/`, `layouts/small/` |
| Coordinated multi-page brand kits (ppt-master model) | Populate the reserved top-level `collections` array (no file move needed — it's an ordered list of ids) |
| Per-industry catalogs fork (finance grows to 8+, sales to 10+) | Split index files: `layouts-index.finance.json` under a `catalogs/` key |

Do **not** restructure before one of these triggers actually fires.

## Index schema (scale-ready)

Every entry carries these axes so virtual grouping stays powerful:

| Field | Type | Purpose |
|---|---|---|
| `id` | kebab-case | Primary key (drives filenames `<id>.md`, `<id>.svg`) |
| `file` | `<id>.md` | Recipe markdown in this folder |
| `preview` | `<id>.svg` | Wireframe in `../../assets/layout-previews/` |
| `canvas` | `{width,height}` | Exact pixels |
| `canvas_class` | enum | Coarse form-factor bucket (`landscape-16x9`, `mobile-portrait`, `tooltip-small`, reserved: `print-a4`, `tv-wall`, `landscape-4x3`) |
| `style` | enum | `executive` \| `analytical` \| `operational` |
| `domain` | enum | Business area (`sales`, `finance`, `marketing`, `customer`, `operations`, `manufacturing`, `geography`, `hr`, `technology`, `healthcare`) or `cross-domain` |
| `audience` | string[] | Human roles |
| `visual_count` | int | Cardinality guide |
| `zones` | string[] | Named composition zones (matches recipe headings) |
| `tags` | kebab-case[] | Free-form multi-axis labels (`kpi-heavy`, `drillthrough-target`, `map`, `real-time`, …) |
| `use_when` | sentence | One-line selection guide |
| `status` | enum | `stable` \| `experimental` \| `deprecated` |
| `replaced_by` | id (optional) | Required when `status == 'deprecated'` |

### Reserved: `collections`

Top-level `collections: []` is reserved for ppt-master-style brand kits — an
ordered list of layout ids that form a coordinated multi-page set. Empty until
the skill starts shipping kits.

```jsonc
{
  "collections": [
    {
      "id": "finance-dark",
      "title": "Finance Dark Brand Kit",
      "description": "Cover + exec + waterfall + drillthrough, dark accent palette",
      "layouts": ["landing-navigation", "exec-overview-16x9",
                  "finance-pnl-waterfall", "drillthrough-detail"]
    }
  ]
}
```

## Canvas density tags

The `canvas_class` enum is a **form-factor** bucket — it doesn't distinguish
pixel density. Two landscape canvases are both `landscape-16x9`:

| Density | Tag | Status |
|---|---|---|
| 1664 × 936 | `canvas-1664x936` | **Current standard** — all landscape layouts in the catalog target this density |
| 1280 × 720 | `canvas-1280x720` | Legacy / Power BI-default — reserve if a consumer pins a layout to the smaller density; no catalog entry currently uses it |

Strategist uses these tags to match a layout to the project's target canvas
without forking the enum for every pixel resolution.

## Reflow vs. zoom (v0.6)

Moving from 1280 × 720 to 1664 × 936 adds ~70% of canvas area. A naïve ×1.3
**zoom** preserves layout proportions but also inflates fonts / padding and
leaves information density flat. **Reflow** keeps element sizes closer to
their 1280 × 720 tuning and spends the reclaimed space on additional slots
— more KPIs, narrative context, secondary panels, benchmark references, and
drill-adjacent detail.

| Mode | Visual count | When to choose |
|---|---|---|
| Zoom (baseline) | Unchanged | Migration-first; cross-team consistency; reports viewed at far distance (TV wall, kiosk) |
| Reflow (v0.6 tag `reflow-enhanced`) | +2 to +4 slots | Analyst/controller audiences; laptop/desktop viewing; pages that were info-sparse at 1280 × 720 |

Layouts that carry the `reflow-enhanced` tag include a **"## Reflow additions
(v0.6)"** section in their `.md` with new slot rows + an integration note
(which existing slot to shrink to make room). The base slot table is left
intact — consumers can opt in to reflow additions or stay on the zoom baseline.

**Not every layout should reflow.** Deliberately *not* reflow-enhanced:

- `full-page-map`, `qna-explore-page` — intentionally sparse; adding slots
  steals focus from the hero visual.
- `advanced-kpi-card-grid` (`vc=20`), `ultra-dense-kpi-scorecard` (`vc=60`)
  — already info-dense; more slots fight for the same attention.
- `dimension-nav-hub`, `what-if-parameter-page` — candidates for a future
  pass once live reports demonstrate concrete additions.

## Recommended themes (v0.7)

Each layout entry can carry a `recommended_themes[]` array referencing theme
ids from [`../themes/themes-index.json`](../themes/themes-index.json). Layout
is **structure**; theme is **brand**. They vary independently — one layout can
pair with multiple themes (e.g. `chiclet-nav-strip` works for both
`retail-fmcg` and `sales-growth`).

Visual swatches live in `assets/theme-swatches/<theme-id>.svg`. The Strategist
agent shortlists layouts by structural fit, then ranks the per-layout
`recommended_themes` against the target industry to present 2–3 complete
layout-plus-theme options to the user.

## Non-standard canvas classes

Some real reports use non-landscape canvases for specific interaction contexts.
Use these `canvas_class` values (enum widened in catalog v0.4) when the page
is *not* a full-screen landscape:

| canvas_class | Typical dimensions | Purpose |
|---|---|---|
| `tooltip-small` | 320 × 240 | Default Power BI tooltip page |
| `tooltip-wide` | 900–1200 × 240–350 | Panoramic hover enrichment (sparkline row) |
| `popup-compact` | 500–800 × 400–600 | Drill popup / Teams embed / intranet card |
| `mobile-portrait` | 390 × 844 | Mobile-layout page |

## Zone primitive vocabulary

These zone names appear across multiple real reports and are the recommended
spelling when adding `tags` on a new layout. Keep `zones[]` and `tags[]` in
sync where it makes sense so filter queries hit both.

| Primitive | Typical dimensions (px, on 1664×936) | Purpose | Recommended tag |
|---|---|---|---|
| `top-header-bar` | full-width × 62–104 tall | Brand / page title / period selector | `top-header-bar` |
| `left-rail-filter` | 234–312 wide × full height | Stacked slicers kept visible while reading body | `left-rail-filter` |
| `chiclet-slicer-strip` | full-width × ~73 tall, 4–6 buttons | Touch-friendly single-select filter, selected-state colour | `chiclet-slicer-strip` |
| `kpi-card-row` | full-width body × 104–156 tall, 3–6 cards | "What is it?" row immediately below header | `kpi-card-row` |
| `action-tab-nav` | row of `actionButton`, ~52 tall | Sibling-page wayfinding (selected-state variants) | `action-tab-nav` |
| `arrow-nav-tabs` | `arrowPentagonShape` row | Same intent as tabs, more decorative | `arrow-nav-tabs` |
| `bottom-detail-table` | full-width × 312–390 tall | Auditable detail under summary visuals | `bottom-detail-table` |
| `footer-data-strip` | full-width × 31–42 tall | Refresh timestamp, source, page owner | `footer-data-strip` |
| `hidden-filter-panel` | `visualGroup` with `isHidden:true` | Designer-only filter staging area | `hidden-filter-panel` |

## Versioning

`version` field at the top of the index is **SemVer**:

- **PATCH** (0.2.0 → 0.2.1): add/remove a single layout, no schema change
- **MINOR** (0.2 → 0.3): additive schema change (new optional field, widened enum) or a batch of new layouts that meaningfully changes catalog surface area
- **MAJOR** (0.x → 1.0): breaking schema change (remove field, narrow enum, rename id)

Consumers pin to a MAJOR version; Strategist logs a warning when the catalog
MINOR is newer than its last-tested value.

## Adding a new layout — checklist

1. Pick a kebab-case `id` (e.g. `hr-headcount-attrition`).
2. Write `references/layouts/<id>.md` following the exec-overview template.
3. Add a generator function to the preview script and emit
   `assets/layout-previews/<id>.svg` using the shared `currentColor` primitives.
4. Append an entry to `layouts-index.json` with all required fields
   (id, file, preview, canvas, canvas_class, style, domain, visual_count,
   zones, use_when, status). Pick tags from existing vocabulary first.
5. Run the enrichment / validation script — schema must pass and the preview
   must exist on disk.
6. Update the README's at-a-glance table (if you keep one).
7. Bump `version` per SemVer.

## Deprecating a layout

1. Change `status` to `deprecated`.
2. Set `replaced_by` to the id of the new layout (required by schema).
3. Keep the `.md` + `.svg` files on disk for one release cycle so old Design
   Specs still render previews.
4. Remove on the next MAJOR bump.

## v0.11 additions — domain diversification pack

Catalog grew 50 → **86 layouts** to close 0-coverage gaps in HR, Technology,
Healthcare and add thin-domain coverage for Sales, Supply Chain and ESG.

### New domain layouts (21)

| Domain | Layouts added |
|---|---|
| **hr** | `hr-headcount-attrition`, `hr-recruiting-funnel`, `hr-compensation-bands`, `hr-dei-scorecard`, `hr-engagement-survey`, `hr-org-chart-drill` |
| **technology** | `it-incident-postmortem`, `it-sla-heatmap`, `it-finops-cost-governance`, `it-release-train`, `it-service-catalog` |
| **healthcare** | `hc-patient-flow`, `hc-clinical-quality`, `hc-readmission-analysis` |
| **sales** | `sales-pipeline-forecast`, `sales-rep-leaderboard` |
| **supply-chain** | `supply-inventory-abc` |
| **esg** | `esg-carbon-scorecard` |
| **cross-domain** | `narrative-story-page`, `comparison-side-by-side`, `paginated-export-a4` |

### Auto-derived variants (15)

- **Mobile (8)**: `hr-headcount-attrition`, `hr-recruiting-funnel`, `hr-engagement-survey`, `it-incident-postmortem`, `it-finops-cost-governance`, `hc-patient-flow`, `hc-readmission-analysis`, `sales-pipeline-forecast`
- **A4 print (4)**: `hr-dei-scorecard`, `hr-compensation-bands`, `hc-clinical-quality`, `esg-carbon-scorecard`
- **TV-wall (3)**: `it-sla-heatmap`, `it-service-catalog`, `hc-patient-flow`

### New collections (4)

`hr-people-review`, `it-sre-war-room`, `hc-quality-review`, `esg-quarterly`.

### Schema updates

- Domain enum extended with `supply-chain`, `esg`.
- Canonical zone vocabulary extended with 51 new zone names (HR / IT / HC /
  sales / supply / ESG / cross-cutting primitives).

### Net effect

- Domains covered: **8 → 11** (3 formerly zero-coverage now populated).
- Matrix: **50×52 → 86×52** (4,472 cells, 527 pairings, 11.8%).
- Preview SVGs: **150 → 258** (base + dark + annotated per new/derived layout).
- Contact sheet regenerated for 86 layouts.

## v0.10 additions — structural enrichment, derivatives, collections, previews

Catalog grew 31 → 50 layouts and became a complete structural index:

| Addition | Where | Purpose |
|---|---|---|
| **`zones_detail[]`** | every layout | Precise grid coordinates per zone (`{name, x, y, w, h, role, visual_type}`). Executor emits PBIR JSON directly without re-parsing markdown. |
| **`density_score` (0..1)** | every layout | Derived from `visual_count` and canvas area. Intersect with `theme.personality_axes.spaciousness` for fit ranking. |
| **`interaction_model`** | 17 layouts | Explicit `drillthrough_target`, `tooltip_target`, `cross_filter_groups`, `bookmark_states`. Makes drill/tooltip wiring declarative. |
| **`data_requirements`** | every layout | `{min_rows, required_measures[], required_dimensions[], date_grain}`. Strategist rules out layouts the model can't feed. |
| **`avoid_when`** | every layout | Anti-pattern guidance — inverse of `use_when`. Prevents misuse (e.g. `ultra-dense-kpi-scorecard` is not for C-suite). |
| **`chart_patterns[]`** | every layout | Canonical chart-pattern ids per layout. Executor pulls spec from `assets/chart-previews/` instead of reinventing. |
| **`example_pbips[]`** | 16 layouts | Relative paths to reference `.pbip` files that exemplify the layout — turning `references-pbip/` into a living gallery. |
| **`last_reviewed_at` + `owner`** | every layout | Lifecycle metadata for 50-layer governance. |
| **`derived_from`** | 19 new layouts | Parent id for mobile/A4/TV variants. |
| **`preview_dark` + `preview_annotated`** | every layout | Dark-canvas preview + numbered-callout preview per layout. 100 new SVGs. |
| **Mobile companions** (×15) | new layouts `<id>-mobile` | Portrait 390×844 variants for top desktop layouts, zones remapped to single-column stacks with chip-rows and nav-tabs. |
| **Print/A4 variants** (×2) | `exec-overview-16x9-a4`, `finance-pnl-waterfall-a4` | Board-pack canvas (1169×826), recommends print-safe themes only. |
| **TV-wall variants** (×2) | `ops-single-screen-tv`, `mfg-line-status-tv` | 1920×1080, recommends dark companions only, adds `tv-headline` + `tv-alert-ticker`. |
| **`collections[]`** — 7 kits | finance-monthly-close, sales-qbr, ops-daily-standup, marketing-campaign-readout, board-deck-print, noc-wall-board, exec-cross-domain | Ordered multi-page recipes, ppt-master-style. |
| **Canonical zone vocabulary** (144) | schema enum | `zones[]` and `zones_detail[].name` lock to enum — typos become lint errors. |
| **Contact sheet** | `assets/layouts-contact-sheet.svg` | 6-column grid of all 50 layouts at ~240×135 each. |
| **Deprecation check** | automated | Every `status: deprecated` must have a valid `replaced_by` pointing at a `stable` layout. |

### Picking a layout pack (collections)

```jsonc
// "Give me a full month-end close pack"
doc.collections.find(c => c.id === "finance-monthly-close").layouts
// → ["landing-navigation", "exec-overview-16x9", "pl-statement-grid",
//    "finance-pnl-waterfall", "aging-bucket-page", "drillthrough-detail"]
```

### Using `zones_detail` in the Executor

```jsonc
{
  "id": "exec-overview-16x9",
  "canvas": { "width": 1664, "height": 936 },
  "zones_detail": [
    { "name": "title-bar", "x": 16, "y": 16, "w": 1632, "h": 56, "role": "frame" },
    { "name": "kpi-row", "x": 16, "y": 88, "w": 1632, "h": 121, "role": "kpi" },
    { "name": "hero-trend", "x": 16, "y": 225, "w": 946, "h": 393, "role": "hero", "visual_type": "trend" },
    { "name": "supporting-pair", "x": 978, "y": 225, "w": 670, "h": 393, "role": "supporting" }
  ]
}
```
