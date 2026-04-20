# Design Assets

Binary and SVG assets that Executor agents reference when building PBIR reports.
These are **companions** to the markdown recipes in
[`../references/`](../references/) — recipes describe composition; assets provide
the concrete artwork.

## Folder layout (mirrors `ppt-master/templates/`)

| Folder | Contents | Used by |
|---|---|---|
| [`icons/`](icons/) | SVG icons for KPI cards, status cells, nav buttons, slicer chiclets | Executor (all styles), Polisher |
| [`images/`](images/) | Raster art — backgrounds, banners, logos, section dividers _(catalog empty — supply per project)_ | Executor (executive + analytical layouts) |
| [`logos/`](logos/) | Industry placeholder logos (sales, finance, healthcare, manufacturing, …) | Executor (title-bar logo slot), Polisher (brand swap) |
| [`layout-previews/`](layout-previews/) | SVG schematics (1 base + annotated + dark per layout in `references/layouts/*.md`) | Strategist (Seven Confirmations item #2), Auditor |
| [`chart-previews/`](chart-previews/) | SVG thumbnails (1 per recipe in `references/chart-templates/*.md`) | Strategist Step 4, Design Spec §5 |
| [`slicer-previews/`](slicer-previews/) | SVG schematics (1 per recipe in `references/slicer-patterns/*.md`) | Design Spec §10 |
| [`pbi-themes/`](pbi-themes/) | Drop-in `theme.json` files (1 per theme in `references/themes/themes-index.json`) | Executor (theme application), Polisher |
| [`theme-swatches/`](theme-swatches/) | SVG palette swatches (normal + CVD-simulated per theme) | Strategist Phase 4a.5 item #5 (Palette) |
| [`tokens/`](tokens/) | W3C design tokens `.tokens.json` + compiled `.css` (per theme) | Web/HTML artifacts, Figma / Tokens Studio |

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
   - Chart previews: 320×180 SVG (16:9) — matches Design Spec §5 inline preview.
   - Slicer previews: 320×180 SVG (16:9).
   - Layout previews: 1664×936 SVG (desktop), 414×736 (mobile), 1920×1080 (TV),
     816×1056 (A4). Schematic only — no real data.
   - Backgrounds: ≤ 300 KB each; WebP preferred, JPEG fallback.
5. **Index files validate against JSON Schemas** in each folder. CI will fail if
   an asset file exists but is missing from the index (or vice-versa).

## Cross-references

- Recipe catalog (prose): [`../references/`](../references/)
- Theme JSON (canonical): [`../../power-bi-pbip-report/references/themes/`](../../power-bi-pbip-report/references/themes/)
- Visual-vocabulary intent map: [`../references/visual-vocabulary.md`](../references/visual-vocabulary.md)

## Seeding status (current)

| Folder | Files | Source | Coverage |
|---|---|---|---|
| `icons/tabler-outline/` | 74 SVG | [tabler/tabler-icons](https://github.com/tabler/tabler-icons) (MIT) | 10 categories — kpi-delta, chart, finance, status, navigation, action, domain, geo, data, comms |
| `icons/tabler-filled/` | 46 SVG | same (MIT) | Filled mirror for KPI tile leading marks |
| `icons/lucide/` | 64 SVG | [lucide-icons/lucide](https://github.com/lucide-icons/lucide) (ISC) | Alternate outline family for Strategist icon pinning |
| `icons/duotone/` | 20 SVG | Hand-authored (MIT) | Two-tone KPI / section-header marks |
| `icons/custom/` | — _(reserved)_ | — | Folder created on first project-specific icon |
| `chart-previews/` | 62 SVG | Hand-authored 320×180 schematics | Full coverage of 62 recipes; 10 recipes still uncharted (tracked in `chart-templates-index.json.gaps[]`) |
| `slicer-previews/` | 15 SVG | Hand-authored 320×180 schematics | Full coverage of 15 slicer patterns |
| `layout-previews/` | 258 SVG | Generated from `layouts-index.json` zones | Full coverage — 86 layouts × (base + annotated + dark) |
| `pbi-themes/` | 52 JSON | Hand-authored, validated | 16 domain (15 with dark pair) + 5 brand (all dark) + 3 design-system (all dark) + 2 accessibility + 3 seasonal |
| `theme-swatches/` | 104 SVG | Generated from theme JSON | 52 normal + 52 CVD (deuteranopia-simulated) |
| `tokens/` | 104 files | Generated from theme JSON | 52 `.tokens.json` (W3C DTCG) + 52 `.css` |
| `logos/` | 24 SVG | Hand-authored (CC0) | 24 industry placeholder marks |
| `images/` | 0 | — | Intentionally empty — supply per project (no stock art committed); planned seeds tracked in `images-index.json.gaps[]` |
