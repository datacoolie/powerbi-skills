# Design Assets

Binary and SVG assets that Executor agents reference when building PBIR reports.
These are **companions** to the markdown recipes in
[`../references/`](../references/) — recipes describe composition; assets provide
the concrete artwork.

## Folder layout (mirrors `ppt-master/templates/`)

| Folder | Contents | Used by |
|---|---|---|
| [`icons/`](icons/) | SVG icons for KPI cards, status cells, nav buttons, slicer chiclets | Executor (all styles), Polisher |
| [`images/`](images/) | Raster art — backgrounds, banners, logos, section dividers | Executor (executive + analytical layouts) |
| [`logos/`](logos/) | Industry placeholder logos (sales, finance, healthcare, manufacturing, …) | Executor (title-bar logo slot), Polisher (brand swap) |
| [`layout-previews/`](layout-previews/) | PNG thumbnails (1 per layout in `references/layouts/*.md`) | Strategist (Seven Confirmations item #2), Auditor |
| [`chart-previews/`](chart-previews/) | SVG/PNG thumbnails (1 per recipe in `references/chart-templates/*.md`) | Strategist Step 4, Design Spec §5 |

Each subfolder has its own `README.md` and a machine-readable `*-index.json`
manifest (see per-folder docs for schema).

## Rules

1. **No PII / no proprietary logos.** Ship only Apache-2 / MIT / CC0 / CC-BY assets.
   Every asset's license is recorded in its folder index.
2. **SVG prefers `currentColor`.** So the Executor can recolor via theme tokens
   without re-authoring.
3. **File names kebab-case, no spaces, ASCII only.** Matches the catalog `id`
   convention.
4. **Sizes:**
   - Icons: 24×24 SVG viewBox (scale via CSS/PBIR format pane).
   - Thumbnails: 480×270 PNG (16:9) — matches Power BI page-preview ratio.
   - Backgrounds: ≤ 300 KB each; WebP preferred, JPEG fallback.
5. **Index files validate against JSON Schemas** in each folder. CI will fail if
   an asset file exists but is missing from the index (or vice-versa).

## Cross-references

- Recipe catalog (prose): [`../references/`](../references/)
- Theme JSON (canonical): [`../../power-bi-pbip-report/references/themes/`](../../power-bi-pbip-report/references/themes/)
- Visual-vocabulary intent map: [`../references/visual-vocabulary.md`](../references/visual-vocabulary.md)

## Seeding status (from ppt-master reuse)

| Folder | Files | Source | Coverage |
|---|---|---|---|
| `icons/tabler-outline/` | 34 SVG | `.agents/skills/ppt-master/templates/icons/tabler-outline/` (MIT) | KPI starter set — 6 categories |
| `icons/tabler-filled/` | 21 SVG | `.agents/skills/ppt-master/templates/icons/tabler-filled/` (MIT) | Filled-style mirror of KPI set (21 of 34 available upstream) |
| `icons/lucide/` | 27 SVG | `.agents/skills/ppt-master/templates/icons/chunk/` (lucide-style, ISC) | Lucide-inspired 27-icon set (adds `map`, `map-pin`, `funnel`) |
| `icons/custom/` | 0 | — | Empty — drop project-specific marks here |
| `chart-previews/` | 13 SVG | `.agents/skills/ppt-master/templates/charts/` + 2 hand-authored | Full coverage of all 13 recipes |
| `images/` | 0 | — | Empty — supply per project (no stock art committed) |
| `logos/` | 12 SVG | Hand-authored (CC0) | 12 industry placeholder marks: sales, finance, healthcare, manufacturing, retail, logistics, marketing, hr, technology, energy, education, hospitality |
| `layout-previews/` | 13 SVG | Generated from `layouts-index.json` zones (ppt-master style) | Full coverage: 6 core + 7 Tier-1 community layouts |
