# Themes catalog

Machine-readable companion to [`../theme-colors.md`](../theme-colors.md).
Where the prose guide explains *why* each palette exists, this catalog is the
structured index the Strategist / Executor agents consume to match a **theme**
to a chosen **layout**.

```
references/themes/
├── themes-index.json          # catalog (SemVer `version`)
├── themes-index.schema.json   # contract
├── theme-picker.json          # decision matrix for industry/audience/mode/CVD/print/motion → ranked themes (v0.7)
├── theme-picker.schema.json   # contract for the picker
└── README.md                  # (this file)

assets/theme-swatches/
├── <theme-id>.svg             # visual palette preview per theme
└── <theme-id>-cvd.svg         # colorblind-vision simulation (v0.4)

assets/pbi-themes/
└── <theme-id>.json            # native Power BI theme file, one-click import (v0.4)

assets/tokens/
├── <theme-id>.tokens.json     # W3C Design Tokens export (v0.7)
└── <theme-id>.css             # CSS custom-properties export (v0.7)

assets/theme-layout-matrix.svg # 31 × 52 compatibility matrix (v0.7)
```

## Catalog (v0.7 — 52 themes)

Catalog doubled from v0.6 by auto-generating **dark-mode companions** for
every light theme, adding **seasonal variants**, and closing the
brand-integration loop. Pick by **domain** for industry-specific reports,
by **design system** for neutral brand contexts, by **brand** for
enterprise ecosystems, or by **accessibility / dark / seasonal** for
specialized constraints.

### Domain-specific (14)

| Theme id | Primary industries | Character |
|---|---|---|
| `corporate-financial` | finance, banking, insurance, investor-relations | Dark navy authority |
| `sales-growth` | sales, retail, ecommerce, marketing | Vibrant forward motion |
| `manufacturing-ops` | manufacturing, operations, energy, utilities | Industrial steel + safety orange |
| `healthcare-pharma` | healthcare, pharma, life-sciences, public-health | Teal clinical trust |
| `supply-chain-logistics` | logistics, supply-chain, procurement, transportation | Navy + amber movement |
| `retail-fmcg` | retail, fmcg, grocery, consumer-goods | Fresh, consumer-facing |
| `sustainability-esg` | esg, sustainability, agriculture, non-profit | Earth-green balance |
| `tech-monitoring` | it-ops, devops, saas, cybersecurity | Console-glow cyans |
| `consulting-authority` | consulting, strategy, board-reporting | Deloitte/McKinsey/BCG restraint |
| `public-sector-gov` | government, civic-services, defense | Authoritative civic |
| `education-edtech` | education, academia, training, L&D | Scholarly warm purples |
| `media-entertainment` | streaming, broadcast, gaming, sports | Bold magenta + gold |
| `real-estate-hospitality` | real-estate, hotels, travel | Warm earth + champagne |
| `hr-people-analytics` | human-resources, talent, DEI, workforce | Human teal + coral |
| `marketing-digital` | digital-advertising, social-media, growth | Vivid gradient-friendly |
| `telecom-network` | telecom, ISP, mobile-carriers, 5G | Deep teal + orange alerts |

### Design-system community favorites (4)

| Theme id | Inspiration | When to use |
|---|---|---|
| `microsoft-fluent` | Fluent 2 / PBI CY24SU10 | Default-compatible; Microsoft 365 / Dynamics / Azure reports |
| `nord-frost` | [Nord](https://www.nordtheme.com/) Arctic palette | Muted calm cool tones; developer-tool dashboards |
| `tailwind-slate` | Tailwind CSS `slate` + `sky` | Modern SaaS/startup aesthetic |
| `accessible-okabe-ito` | [Okabe & Ito 2008](https://jfly.uni-koeln.de/color/) | Colorblind-safe reference (deuteranopia, protanopia, tritanopia) |

### Dark mode (1)

| Theme id | When to use |
|---|---|
| `high-contrast-dark` | NOC/SOC wall displays, monitoring consoles, 24/7 ops rooms; AAA contrast on deep canvas |

### Brand-extracted (5 — v0.6)

Palettes extracted from published enterprise design systems. Use when a
report lives in the consumer's brand ecosystem or targets their developers.

| Theme id | Inspiration | When to use |
|---|---|---|
| `brand-salesforce` | Salesforce Lightning Design System | Sales-ops, CRM-embedded dashboards, customer success reporting |
| `brand-ibm-carbon` | IBM Carbon Design System | Enterprise IT, research-grade analysis, B2B platforms |
| `brand-google-material` | Material Design 3 | Consumer web/mobile, Google Workspace-adjacent, productivity suites |
| `brand-stripe` | Stripe design system | Fintech, payments, founder-grade SaaS dashboards |
| `brand-atlassian` | Atlassian Design System | DevOps, project-management, Jira/Confluence-embedded |

> All 26 themes currently rate **WCAG AAA** (contrast ≥ 7:1) for `ui.foreground` on `ui.background`. The computed ratio is stored in each theme's `ui.text_contrast`.

## Entry shape (abridged, v0.3)

```jsonc
{
  "id": "sales-growth",
  "name": "Sales / Revenue / Growth",
  "personality": "Vibrant, energetic — forward motion",
  "industries": ["sales", "retail", "ecommerce", "marketing"],
  "mode": "light",                // "light" | "dark" | "dual"
  "data_colors": ["#0078D4", "#00B7C3", "#E74856", /* … 8 total */],
  "semantic":    { "good": "#38B64B", "bad": "#EE1C25", "neutral": "#949599",
                   "warning": "#F5A623", "info": "#0078D4" },
  "sequential":  { "positive": ["#B8E6BF", "#38B64B", "#1F7F2D"],
                   "warning":  ["#FCD9A6", "#F5A623", "#A36A0B"],
                   "negative": ["#F9B8BB", "#EE1C25", "#9F0E14"],
                   "primary":  ["#9ED0F5", "#0078D4", "#054D8A"] },
  "neutrals":    { "muted": "#A8A8A8", "disabled": "#D2D2D2",
                   "gridline": "#EDEDED", "divider": "#D0D0D0" },
  "ui":          { "background": "#FFFFFF", "foreground": "#242424",
                   "table_accent": "#0078D4",
                   "text_contrast": 15.52, "contrast_rating": "AAA" },
  "usage_rules": { "primary_share": 55, "secondary_share": 30,
                   "accent_share": 15, "max_colors_per_page": 4 },
  "base_theme":  "CY24SU10",
  "pairs_with_layouts": ["sales-performance", "customer-360", /* … */],
  "swatch": "sales-growth.svg"
}
```

### v0.2 additions (ppt-master-inspired)

Three optional but recommended fields were added alongside a top-level
`principles` block. All existing themes were backfilled:

| Field | Purpose | Rule in `theme-colors.md` |
|---|---|---|
| `sequential.{positive,warning,negative,primary}` | 3-stop ramps (light/mid/dark) for trends, heatmaps, gradients | §6 Sequential Ramps |
| `neutrals.{muted,disabled,gridline,divider}` | "Focus in color, rest in gray" tier | §5 Focus-in-Color Pattern |
| `usage_rules.{primary_share,secondary_share,accent_share,max_colors_per_page}` | Per-theme 60-30-10 override | §1 60-30-10 Rule, §2 Max 4 Colors |
| `ui.text_contrast` + `ui.contrast_rating` | Computed WCAG 2.1 AA ratio for fg on bg | §3 Contrast ≥ 4.5:1 |
| Top-level `principles` | Catalog-wide defaults all themes inherit | header of "Color Usage Principles" |

A ninth theme — **`consulting-authority`** (Deloitte/McKinsey/BCG family) —
was added for executive/board/strategic decks that want restrained
monochromatic authority rather than industry-specific palettes.

### v0.3 additions — diversity expansion

Catalog grew from 9 → **21 themes** to cover missing domains and the most
community-requested design systems:

- **Domain gaps (7):** `public-sector-gov`, `education-edtech`,
  `media-entertainment`, `real-estate-hospitality`, `hr-people-analytics`,
  `marketing-digital`, `telecom-network`.
- **Design-system favorites (4):** `microsoft-fluent` (PBI default aligned),
  `nord-frost`, `tailwind-slate`, `accessible-okabe-ito` (colorblind-safe
  reference palette).
- **Dark mode (1):** `high-contrast-dark` with neon accents on a `#0F1419`
  canvas — the most-requested missing piece for monitoring/NOC displays.

All new themes were authored with the full v0.2 field set (sequential /
neutrals / usage_rules / WCAG contrast). Layout `recommended_themes[]` was
regenerated across `layouts-index.json` (layouts v0.7 → v0.8) so the
reverse index is complete for 28 of 31 layouts.

### v0.4 additions — operationalization

Three upgrades turn the catalog from documentation into something directly
usable:

| Addition | Where | How to use |
|---|---|---|
| **Native Power BI theme files** — one per theme | [`assets/pbi-themes/*.json`](../../assets/pbi-themes/) | Import in Power BI Desktop: **View → Themes → Browse for themes**. Each file exposes `dataColors`, `foreground`, `background`, `tableAccent`, `good`/`bad`/`neutral`, `minimum`/`center`/`maximum` (from diverging ramp), and a minimal `visualStyles` block that applies `neutrals.gridline` / `neutrals.divider` to axes. |
| **`sequential.diverging` 5-stop ramp** | Every theme in `themes-index.json` | Structure: `[deep-negative, light-negative, neutral, light-positive, deep-positive]`. Use for variance KPIs, correlation heatmaps, red-green gain/loss conditional formatting. Maps directly to PBI's `minimum`/`center`/`maximum` in the PBI theme JSON. |
| **Colorblind-vision simulation sheets** | `assets/theme-swatches/<id>-cvd.svg` | Each theme gets a four-row sheet (normal vision, deuteranopia, protanopia, tritanopia) via Machado-Oliveira-Fernandes 2009 simulation matrices at severity 1.0. Open in a browser or VS Code preview to visually verify palette robustness — `accessible-okabe-ito` will show identical rows, saturated palettes like `media-entertainment` will not. |

### v0.5 additions — typography, gradients, CVD scoring

Three per-theme fields added so a theme is now a *full design token set*,
not just a color list. Schema updated; all 21 themes backfilled.

| Field | What it holds | Why it matters |
|---|---|---|
| **`typography`** | `{preset_id, title_font, body_font, mono_font, notes}` — aligned with ppt-master P1–P5 presets (`P1-editorial`, `P2-corporate`, `P3-technical`, `P4-warm`, `P5-minimal`). Fonts are CSS-style stacks with PBI-safe fallbacks (Segoe UI, Inter, Georgia, Consolas…). | A theme is only half the brand — typography carries the rest. Strategist can now pick font pairing alongside palette, Executor can emit matching `visualStyles.font` in PBI theme JSON downstream. |
| **`gradient_stops`** | `{hero, card_fill, subtle}` — each a `{stops[{offset,color}], angle_deg}` gradient derived from the theme's primary/secondary colors and mode-aware pale/dark mix. | Cover pages, KPI card fills, alternating table bands. Replaces the ad-hoc "just pick a lighter tint" pattern with deterministic, theme-consistent gradients. |
| **`cvd_safety`** | `{rating: safe\|caution\|unsafe, min_delta_e, worst_pair[], worst_under}` — computed: minimum Lab ΔE across all data_color pairs under normal + deuteranopia + protanopia + tritanopia simulation. Thresholds: `safe ≥ 15`, `caution 10–15`, `unsafe < 10`. | Turns the CVD preview sheets into a **numeric verdict**. Honest diagnostic: only `accessible-okabe-ito` rates `safe` at 8-color width (ΔE=15.11); others require limiting to 4–5 slots for CVD use. `worst_pair` tells you exactly which two colors collide. |

**Using `cvd_safety` in practice:**

- `safe` → use all 8 `data_colors` freely, even with CVD audiences.
- `caution` → limit to first 4–5 `data_colors`, or swap the `worst_pair` colors for semantic roles.
- `unsafe` → for accessibility-critical reports, either (a) switch to `accessible-okabe-ito`, or (b) restrict palette to the first 3–4 colors and rely on `neutrals.muted` for everything else.

### v0.6 additions — brand palettes, chart cookbook, personality axes, theme picker

Four new dimensions make the catalog operationally complete for automation:

| Addition | Where | Purpose |
|---|---|---|
| **5 brand-extracted themes** | `brand-salesforce`, `brand-ibm-carbon`, `brand-google-material`, `brand-stripe`, `brand-atlassian` | Cover the most-requested enterprise brand ecosystems. Each gets the full field set (sequential ramps, neutrals, CVD score, typography, gradients, chart_defaults, personality_axes). Native PBI theme JSON + swatch + CVD sheet generated per theme. |
| **`chart_defaults` per theme** | Every theme in `themes-index.json` | Recipe mapping `data_colors[i]` indices and semantic roles to specific visuals: `bar.primary`, `line.series`, `donut.series`, `kpi.positive_role`, `waterfall.increase_role`, `heatmap.ramp`, etc. Executor consumes this when emitting per-visual Power BI `visualStyles`, so "which color for a line chart" stops being ambiguous. |
| **`personality_axes` per theme** | Every theme in `themes-index.json` | Numeric 0–1 axes: `formality`, `spaciousness`, `warmth`, `boldness`. Enables quantitative matching by the Strategist: "find themes where `formality ≥ 0.75` AND `warmth ≤ 0.4`" → restrained authoritative set. |
| **`theme-picker.json`** | `references/themes/theme-picker.json` (+ schema) | Pre-built decision matrix: `by_industry`, `by_audience` (11 audiences: executive-board, operations-floor, sales-team, analyst-technical, external-customer, accessibility-first, public-civic, investor-relations, clinical-medical, monitoring-wall, marketing-campaign), `by_mode`, `by_cvd_requirement`, `by_formality`. Includes a 5-step `picking_algorithm` and worked `example_queries`. |

**Picking algorithm (encoded in `theme-picker.json`):**

1. Intersect `by_industry[<domain>]` with `by_audience[<audience>]`.
2. If CVD required, intersect with `by_cvd_requirement.strict_safe_only`.
3. Filter `by_mode` if user requires light/dark.
4. Within remaining set, sort by formality tier matching target.
5. Tiebreak: prefer domain-specific themes over brand/design-system.

**Example `chart_defaults` entry (all themes):**

```jsonc
"chart_defaults": {
  "bar":       { "primary": 0, "comparison": 1, "target_line": 3 },
  "line":      { "series": [0, 1, 2, 4], "highlight": 0 },
  "donut":     { "series": [0, 1, 2, 3, 4, 5], "center_label": 0 },
  "kpi":       { "positive_role": "good", "negative_role": "bad", "sparkline_color_index": 0 },
  "waterfall": { "increase_role": "good", "decrease_role": "bad", "total_role": "neutral" },
  "heatmap":   { "ramp": "sequential.diverging" },
  "table":     { "header_fill": "ui.table_accent", "row_stripe": "neutrals.gridline" }
}
```

### v0.7 additions — dark companions, tokens, print/motion/parenting, matrix

The catalog doubled and became a complete design-token system:

| Addition | Where | Purpose |
|---|---|---|
| **23 auto-generated dark companions** | `<id>-dark` entries in `themes-index.json` + `<id>-dark.svg` / `<id>-dark-cvd.svg` / `pbi-themes/<id>-dark.json` | For each light theme (except `accessible-okabe-ito` and the already-dark `high-contrast-dark`), lightness-remapped data colors, `#0F1419` canvas, regenerated ramps/neutrals/CVD score, boosted `boldness` axis. Catalog: 26 → 49 + 3 seasonal = 52. |
| **3 seasonal variants** | `corporate-financial-q4`, `retail-fmcg-holiday`, `sustainability-esg-earthday` | Hue-shifted variants for cyclical reports (year-end close, holiday campaigns, Earth Day messaging). Each carries `parent_theme` back to the base. |
| **W3C Design Tokens export** | `assets/tokens/<id>.tokens.json` + `<id>.css` (52 pairs = 104 files) | [W3C CG format](https://design-tokens.github.io/community-group/format/): `$type`/`$value` for colors, fontFamily, duration, cubicBezier. CSS file exposes `:root[data-theme="<id>"]` custom properties. Unblocks Figma, Storybook, non-PBI web dashboards. |
| **`motion` tokens per theme** | Every theme in `themes-index.json` | `{preset: snappy\|balanced\|quiet, tooltip_delay_ms, drill_transition_ms, fade_in_ms, easing}` — derived from `personality_axes.boldness`. Finance-grade themes get slow 400ms tooltips + standard easing; marketing themes get 150ms snappy cubic-bezier. |
| **`print_safe` + `cmyk`** | Every theme | `print_safe: boolean` flags themes suitable for board-pack printing (near-white bg, near-black fg, no data color with CMYK ink sum > 320%). `cmyk: {"#RRGGBB": [c,m,y,k]}` gives integer percentages for prepress. |
| **`parent_theme` (extends model)** | 31 derived themes | Brand themes descend from closest stock palette (`brand-salesforce` → `sales-growth`); dark companions extend their light parent; seasonal variants extend the base. Enables DRY inheritance for future customization. |
| **Layout × theme compatibility matrix** | `assets/theme-layout-matrix.svg` | 31-row × 52-column heat matrix; cells colored by theme `data_colors[0]` where pairing exists, grey otherwise. One-glance catalog audit. |
| **Layouts `recommended_themes[]` updated** | `layouts-index.json` v0.8 → v0.9 | 10 layouts now include the 5 brand themes in their recommendation list, closing the v0.6 loop. |
| **`theme-picker.json` v0.2** | Regenerated | Added `by_print_requirement`, `by_motion_preset`, 2 new audiences (`year-end-finance`, `dark-mode-ops`), updated 6-step picking algorithm to include print + light/dark tiebreaker. |

**Using motion tokens:**

```jsonc
// marketing-digital (boldness 0.85)
"motion": { "preset": "snappy", "tooltip_delay_ms": 150, "drill_transition_ms": 180, "easing": "cubic-bezier(0.2, 0, 0.2, 1)" }

// consulting-authority (boldness 0.25)
"motion": { "preset": "quiet", "tooltip_delay_ms": 400, "drill_transition_ms": 350, "easing": "cubic-bezier(0.4, 0, 0.6, 1)" }
```

**Using tokens in a web dashboard:**

```html
<link rel="stylesheet" href="./assets/tokens/corporate-financial.css">
<body data-theme="corporate-financial">
  <h1 style="color: var(--color-fg); font-family: var(--font-title);">Q4 Results</h1>
  <div style="background: var(--color-data-1); transition: opacity var(--motion-fade-in) var(--motion-easing);">...</div>
</body>
```

## Matching theme ↔ layout

Two-way relationship:

- `themes-index.json` → each theme lists `pairs_with_layouts[]`
- `layouts-index.json` → each layout carries `recommended_themes[]` (derived)

A strategist picking a layout for an FMCG sales report would:

1. Find a layout (e.g. `chiclet-nav-strip`).
2. Read its `recommended_themes` → `["retail-fmcg", "sales-growth"]`.
3. Preview each via `assets/theme-swatches/<id>.svg`.
4. Let the user / domain pick one.

## Why not one canonical theme per layout?

Real reports in `references-pbip/` prove the same layout serves multiple
industries — `exec-overview-16x9` appears in finance, manufacturing, ESG,
and retail reports, each with its own palette. The layout is structure;
the theme is brand. They vary independently.

## Relationship to `theme-colors.md`

| Artifact | Role |
|---|---|
| `theme-colors.md` | Human-readable guide: theme JSON structure, semantic rules, colorblind safety, base-theme selection, PBIR registration |
| `themes-index.json` | Machine-readable palette catalog for agents |
| `themes-index.schema.json` | Contract — enforces hex format, required fields, enum for `mode` |
| `assets/theme-swatches/*.svg` | Visual previews (dark-mode-aware chrome + literal brand hex swatches) |

When adding a new theme: add an entry to the JSON, add its prose explanation
to `theme-colors.md` under "Industry Color Palettes", and run the swatch
generator (kept in version control as a one-shot script in dev notes).

## Versioning

SemVer `version` field:

- **PATCH** — single theme added/removed, or a minor metadata fix
- **MINOR** — additive schema change (new optional field) or several themes at once
- **MAJOR** — breaking schema change (existing fields removed / retyped)

<!-- THEME-ASSET-NAV -->

## Asset navigation (all 52 themes)

Click any cell to open the asset directly. Total: 52 themes × 5 artifacts.

| Theme id | PBI theme | Swatch | CVD swatch | Tokens JSON | CSS |
|---|---|---|---|---|---|
| `accessible-okabe-ito` | [json](../../assets/pbi-themes/accessible-okabe-ito.json) | [svg](../../assets/theme-swatches/accessible-okabe-ito.svg) | [svg](../../assets/theme-swatches/accessible-okabe-ito-cvd.svg) | [json](../../assets/tokens/accessible-okabe-ito.tokens.json) | [css](../../assets/tokens/accessible-okabe-ito.css) |
| `brand-atlassian` | [json](../../assets/pbi-themes/brand-atlassian.json) | [svg](../../assets/theme-swatches/brand-atlassian.svg) | [svg](../../assets/theme-swatches/brand-atlassian-cvd.svg) | [json](../../assets/tokens/brand-atlassian.tokens.json) | [css](../../assets/tokens/brand-atlassian.css) |
| `brand-atlassian-dark` | [json](../../assets/pbi-themes/brand-atlassian-dark.json) | [svg](../../assets/theme-swatches/brand-atlassian-dark.svg) | [svg](../../assets/theme-swatches/brand-atlassian-dark-cvd.svg) | [json](../../assets/tokens/brand-atlassian-dark.tokens.json) | [css](../../assets/tokens/brand-atlassian-dark.css) |
| `brand-google-material` | [json](../../assets/pbi-themes/brand-google-material.json) | [svg](../../assets/theme-swatches/brand-google-material.svg) | [svg](../../assets/theme-swatches/brand-google-material-cvd.svg) | [json](../../assets/tokens/brand-google-material.tokens.json) | [css](../../assets/tokens/brand-google-material.css) |
| `brand-google-material-dark` | [json](../../assets/pbi-themes/brand-google-material-dark.json) | [svg](../../assets/theme-swatches/brand-google-material-dark.svg) | [svg](../../assets/theme-swatches/brand-google-material-dark-cvd.svg) | [json](../../assets/tokens/brand-google-material-dark.tokens.json) | [css](../../assets/tokens/brand-google-material-dark.css) |
| `brand-ibm-carbon` | [json](../../assets/pbi-themes/brand-ibm-carbon.json) | [svg](../../assets/theme-swatches/brand-ibm-carbon.svg) | [svg](../../assets/theme-swatches/brand-ibm-carbon-cvd.svg) | [json](../../assets/tokens/brand-ibm-carbon.tokens.json) | [css](../../assets/tokens/brand-ibm-carbon.css) |
| `brand-ibm-carbon-dark` | [json](../../assets/pbi-themes/brand-ibm-carbon-dark.json) | [svg](../../assets/theme-swatches/brand-ibm-carbon-dark.svg) | [svg](../../assets/theme-swatches/brand-ibm-carbon-dark-cvd.svg) | [json](../../assets/tokens/brand-ibm-carbon-dark.tokens.json) | [css](../../assets/tokens/brand-ibm-carbon-dark.css) |
| `brand-salesforce` | [json](../../assets/pbi-themes/brand-salesforce.json) | [svg](../../assets/theme-swatches/brand-salesforce.svg) | [svg](../../assets/theme-swatches/brand-salesforce-cvd.svg) | [json](../../assets/tokens/brand-salesforce.tokens.json) | [css](../../assets/tokens/brand-salesforce.css) |
| `brand-salesforce-dark` | [json](../../assets/pbi-themes/brand-salesforce-dark.json) | [svg](../../assets/theme-swatches/brand-salesforce-dark.svg) | [svg](../../assets/theme-swatches/brand-salesforce-dark-cvd.svg) | [json](../../assets/tokens/brand-salesforce-dark.tokens.json) | [css](../../assets/tokens/brand-salesforce-dark.css) |
| `brand-stripe` | [json](../../assets/pbi-themes/brand-stripe.json) | [svg](../../assets/theme-swatches/brand-stripe.svg) | [svg](../../assets/theme-swatches/brand-stripe-cvd.svg) | [json](../../assets/tokens/brand-stripe.tokens.json) | [css](../../assets/tokens/brand-stripe.css) |
| `brand-stripe-dark` | [json](../../assets/pbi-themes/brand-stripe-dark.json) | [svg](../../assets/theme-swatches/brand-stripe-dark.svg) | [svg](../../assets/theme-swatches/brand-stripe-dark-cvd.svg) | [json](../../assets/tokens/brand-stripe-dark.tokens.json) | [css](../../assets/tokens/brand-stripe-dark.css) |
| `consulting-authority` | [json](../../assets/pbi-themes/consulting-authority.json) | [svg](../../assets/theme-swatches/consulting-authority.svg) | [svg](../../assets/theme-swatches/consulting-authority-cvd.svg) | [json](../../assets/tokens/consulting-authority.tokens.json) | [css](../../assets/tokens/consulting-authority.css) |
| `consulting-authority-dark` | [json](../../assets/pbi-themes/consulting-authority-dark.json) | [svg](../../assets/theme-swatches/consulting-authority-dark.svg) | [svg](../../assets/theme-swatches/consulting-authority-dark-cvd.svg) | [json](../../assets/tokens/consulting-authority-dark.tokens.json) | [css](../../assets/tokens/consulting-authority-dark.css) |
| `corporate-financial` | [json](../../assets/pbi-themes/corporate-financial.json) | [svg](../../assets/theme-swatches/corporate-financial.svg) | [svg](../../assets/theme-swatches/corporate-financial-cvd.svg) | [json](../../assets/tokens/corporate-financial.tokens.json) | [css](../../assets/tokens/corporate-financial.css) |
| `corporate-financial-dark` | [json](../../assets/pbi-themes/corporate-financial-dark.json) | [svg](../../assets/theme-swatches/corporate-financial-dark.svg) | [svg](../../assets/theme-swatches/corporate-financial-dark-cvd.svg) | [json](../../assets/tokens/corporate-financial-dark.tokens.json) | [css](../../assets/tokens/corporate-financial-dark.css) |
| `corporate-financial-q4` | [json](../../assets/pbi-themes/corporate-financial-q4.json) | [svg](../../assets/theme-swatches/corporate-financial-q4.svg) | [svg](../../assets/theme-swatches/corporate-financial-q4-cvd.svg) | [json](../../assets/tokens/corporate-financial-q4.tokens.json) | [css](../../assets/tokens/corporate-financial-q4.css) |
| `education-edtech` | [json](../../assets/pbi-themes/education-edtech.json) | [svg](../../assets/theme-swatches/education-edtech.svg) | [svg](../../assets/theme-swatches/education-edtech-cvd.svg) | [json](../../assets/tokens/education-edtech.tokens.json) | [css](../../assets/tokens/education-edtech.css) |
| `education-edtech-dark` | [json](../../assets/pbi-themes/education-edtech-dark.json) | [svg](../../assets/theme-swatches/education-edtech-dark.svg) | [svg](../../assets/theme-swatches/education-edtech-dark-cvd.svg) | [json](../../assets/tokens/education-edtech-dark.tokens.json) | [css](../../assets/tokens/education-edtech-dark.css) |
| `healthcare-pharma` | [json](../../assets/pbi-themes/healthcare-pharma.json) | [svg](../../assets/theme-swatches/healthcare-pharma.svg) | [svg](../../assets/theme-swatches/healthcare-pharma-cvd.svg) | [json](../../assets/tokens/healthcare-pharma.tokens.json) | [css](../../assets/tokens/healthcare-pharma.css) |
| `healthcare-pharma-dark` | [json](../../assets/pbi-themes/healthcare-pharma-dark.json) | [svg](../../assets/theme-swatches/healthcare-pharma-dark.svg) | [svg](../../assets/theme-swatches/healthcare-pharma-dark-cvd.svg) | [json](../../assets/tokens/healthcare-pharma-dark.tokens.json) | [css](../../assets/tokens/healthcare-pharma-dark.css) |
| `high-contrast-dark` | [json](../../assets/pbi-themes/high-contrast-dark.json) | [svg](../../assets/theme-swatches/high-contrast-dark.svg) | [svg](../../assets/theme-swatches/high-contrast-dark-cvd.svg) | [json](../../assets/tokens/high-contrast-dark.tokens.json) | [css](../../assets/tokens/high-contrast-dark.css) |
| `hr-people-analytics` | [json](../../assets/pbi-themes/hr-people-analytics.json) | [svg](../../assets/theme-swatches/hr-people-analytics.svg) | [svg](../../assets/theme-swatches/hr-people-analytics-cvd.svg) | [json](../../assets/tokens/hr-people-analytics.tokens.json) | [css](../../assets/tokens/hr-people-analytics.css) |
| `hr-people-analytics-dark` | [json](../../assets/pbi-themes/hr-people-analytics-dark.json) | [svg](../../assets/theme-swatches/hr-people-analytics-dark.svg) | [svg](../../assets/theme-swatches/hr-people-analytics-dark-cvd.svg) | [json](../../assets/tokens/hr-people-analytics-dark.tokens.json) | [css](../../assets/tokens/hr-people-analytics-dark.css) |
| `manufacturing-ops` | [json](../../assets/pbi-themes/manufacturing-ops.json) | [svg](../../assets/theme-swatches/manufacturing-ops.svg) | [svg](../../assets/theme-swatches/manufacturing-ops-cvd.svg) | [json](../../assets/tokens/manufacturing-ops.tokens.json) | [css](../../assets/tokens/manufacturing-ops.css) |
| `manufacturing-ops-dark` | [json](../../assets/pbi-themes/manufacturing-ops-dark.json) | [svg](../../assets/theme-swatches/manufacturing-ops-dark.svg) | [svg](../../assets/theme-swatches/manufacturing-ops-dark-cvd.svg) | [json](../../assets/tokens/manufacturing-ops-dark.tokens.json) | [css](../../assets/tokens/manufacturing-ops-dark.css) |
| `marketing-digital` | [json](../../assets/pbi-themes/marketing-digital.json) | [svg](../../assets/theme-swatches/marketing-digital.svg) | [svg](../../assets/theme-swatches/marketing-digital-cvd.svg) | [json](../../assets/tokens/marketing-digital.tokens.json) | [css](../../assets/tokens/marketing-digital.css) |
| `marketing-digital-dark` | [json](../../assets/pbi-themes/marketing-digital-dark.json) | [svg](../../assets/theme-swatches/marketing-digital-dark.svg) | [svg](../../assets/theme-swatches/marketing-digital-dark-cvd.svg) | [json](../../assets/tokens/marketing-digital-dark.tokens.json) | [css](../../assets/tokens/marketing-digital-dark.css) |
| `media-entertainment` | [json](../../assets/pbi-themes/media-entertainment.json) | [svg](../../assets/theme-swatches/media-entertainment.svg) | [svg](../../assets/theme-swatches/media-entertainment-cvd.svg) | [json](../../assets/tokens/media-entertainment.tokens.json) | [css](../../assets/tokens/media-entertainment.css) |
| `media-entertainment-dark` | [json](../../assets/pbi-themes/media-entertainment-dark.json) | [svg](../../assets/theme-swatches/media-entertainment-dark.svg) | [svg](../../assets/theme-swatches/media-entertainment-dark-cvd.svg) | [json](../../assets/tokens/media-entertainment-dark.tokens.json) | [css](../../assets/tokens/media-entertainment-dark.css) |
| `microsoft-fluent` | [json](../../assets/pbi-themes/microsoft-fluent.json) | [svg](../../assets/theme-swatches/microsoft-fluent.svg) | [svg](../../assets/theme-swatches/microsoft-fluent-cvd.svg) | [json](../../assets/tokens/microsoft-fluent.tokens.json) | [css](../../assets/tokens/microsoft-fluent.css) |
| `microsoft-fluent-dark` | [json](../../assets/pbi-themes/microsoft-fluent-dark.json) | [svg](../../assets/theme-swatches/microsoft-fluent-dark.svg) | [svg](../../assets/theme-swatches/microsoft-fluent-dark-cvd.svg) | [json](../../assets/tokens/microsoft-fluent-dark.tokens.json) | [css](../../assets/tokens/microsoft-fluent-dark.css) |
| `nord-frost` | [json](../../assets/pbi-themes/nord-frost.json) | [svg](../../assets/theme-swatches/nord-frost.svg) | [svg](../../assets/theme-swatches/nord-frost-cvd.svg) | [json](../../assets/tokens/nord-frost.tokens.json) | [css](../../assets/tokens/nord-frost.css) |
| `nord-frost-dark` | [json](../../assets/pbi-themes/nord-frost-dark.json) | [svg](../../assets/theme-swatches/nord-frost-dark.svg) | [svg](../../assets/theme-swatches/nord-frost-dark-cvd.svg) | [json](../../assets/tokens/nord-frost-dark.tokens.json) | [css](../../assets/tokens/nord-frost-dark.css) |
| `public-sector-gov` | [json](../../assets/pbi-themes/public-sector-gov.json) | [svg](../../assets/theme-swatches/public-sector-gov.svg) | [svg](../../assets/theme-swatches/public-sector-gov-cvd.svg) | [json](../../assets/tokens/public-sector-gov.tokens.json) | [css](../../assets/tokens/public-sector-gov.css) |
| `public-sector-gov-dark` | [json](../../assets/pbi-themes/public-sector-gov-dark.json) | [svg](../../assets/theme-swatches/public-sector-gov-dark.svg) | [svg](../../assets/theme-swatches/public-sector-gov-dark-cvd.svg) | [json](../../assets/tokens/public-sector-gov-dark.tokens.json) | [css](../../assets/tokens/public-sector-gov-dark.css) |
| `real-estate-hospitality` | [json](../../assets/pbi-themes/real-estate-hospitality.json) | [svg](../../assets/theme-swatches/real-estate-hospitality.svg) | [svg](../../assets/theme-swatches/real-estate-hospitality-cvd.svg) | [json](../../assets/tokens/real-estate-hospitality.tokens.json) | [css](../../assets/tokens/real-estate-hospitality.css) |
| `real-estate-hospitality-dark` | [json](../../assets/pbi-themes/real-estate-hospitality-dark.json) | [svg](../../assets/theme-swatches/real-estate-hospitality-dark.svg) | [svg](../../assets/theme-swatches/real-estate-hospitality-dark-cvd.svg) | [json](../../assets/tokens/real-estate-hospitality-dark.tokens.json) | [css](../../assets/tokens/real-estate-hospitality-dark.css) |
| `retail-fmcg` | [json](../../assets/pbi-themes/retail-fmcg.json) | [svg](../../assets/theme-swatches/retail-fmcg.svg) | [svg](../../assets/theme-swatches/retail-fmcg-cvd.svg) | [json](../../assets/tokens/retail-fmcg.tokens.json) | [css](../../assets/tokens/retail-fmcg.css) |
| `retail-fmcg-dark` | [json](../../assets/pbi-themes/retail-fmcg-dark.json) | [svg](../../assets/theme-swatches/retail-fmcg-dark.svg) | [svg](../../assets/theme-swatches/retail-fmcg-dark-cvd.svg) | [json](../../assets/tokens/retail-fmcg-dark.tokens.json) | [css](../../assets/tokens/retail-fmcg-dark.css) |
| `retail-fmcg-holiday` | [json](../../assets/pbi-themes/retail-fmcg-holiday.json) | [svg](../../assets/theme-swatches/retail-fmcg-holiday.svg) | [svg](../../assets/theme-swatches/retail-fmcg-holiday-cvd.svg) | [json](../../assets/tokens/retail-fmcg-holiday.tokens.json) | [css](../../assets/tokens/retail-fmcg-holiday.css) |
| `sales-growth` | [json](../../assets/pbi-themes/sales-growth.json) | [svg](../../assets/theme-swatches/sales-growth.svg) | [svg](../../assets/theme-swatches/sales-growth-cvd.svg) | [json](../../assets/tokens/sales-growth.tokens.json) | [css](../../assets/tokens/sales-growth.css) |
| `sales-growth-dark` | [json](../../assets/pbi-themes/sales-growth-dark.json) | [svg](../../assets/theme-swatches/sales-growth-dark.svg) | [svg](../../assets/theme-swatches/sales-growth-dark-cvd.svg) | [json](../../assets/tokens/sales-growth-dark.tokens.json) | [css](../../assets/tokens/sales-growth-dark.css) |
| `supply-chain-logistics` | [json](../../assets/pbi-themes/supply-chain-logistics.json) | [svg](../../assets/theme-swatches/supply-chain-logistics.svg) | [svg](../../assets/theme-swatches/supply-chain-logistics-cvd.svg) | [json](../../assets/tokens/supply-chain-logistics.tokens.json) | [css](../../assets/tokens/supply-chain-logistics.css) |
| `supply-chain-logistics-dark` | [json](../../assets/pbi-themes/supply-chain-logistics-dark.json) | [svg](../../assets/theme-swatches/supply-chain-logistics-dark.svg) | [svg](../../assets/theme-swatches/supply-chain-logistics-dark-cvd.svg) | [json](../../assets/tokens/supply-chain-logistics-dark.tokens.json) | [css](../../assets/tokens/supply-chain-logistics-dark.css) |
| `sustainability-esg` | [json](../../assets/pbi-themes/sustainability-esg.json) | [svg](../../assets/theme-swatches/sustainability-esg.svg) | [svg](../../assets/theme-swatches/sustainability-esg-cvd.svg) | [json](../../assets/tokens/sustainability-esg.tokens.json) | [css](../../assets/tokens/sustainability-esg.css) |
| `sustainability-esg-dark` | [json](../../assets/pbi-themes/sustainability-esg-dark.json) | [svg](../../assets/theme-swatches/sustainability-esg-dark.svg) | [svg](../../assets/theme-swatches/sustainability-esg-dark-cvd.svg) | [json](../../assets/tokens/sustainability-esg-dark.tokens.json) | [css](../../assets/tokens/sustainability-esg-dark.css) |
| `sustainability-esg-earthday` | [json](../../assets/pbi-themes/sustainability-esg-earthday.json) | [svg](../../assets/theme-swatches/sustainability-esg-earthday.svg) | [svg](../../assets/theme-swatches/sustainability-esg-earthday-cvd.svg) | [json](../../assets/tokens/sustainability-esg-earthday.tokens.json) | [css](../../assets/tokens/sustainability-esg-earthday.css) |
| `tailwind-slate` | [json](../../assets/pbi-themes/tailwind-slate.json) | [svg](../../assets/theme-swatches/tailwind-slate.svg) | [svg](../../assets/theme-swatches/tailwind-slate-cvd.svg) | [json](../../assets/tokens/tailwind-slate.tokens.json) | [css](../../assets/tokens/tailwind-slate.css) |
| `tailwind-slate-dark` | [json](../../assets/pbi-themes/tailwind-slate-dark.json) | [svg](../../assets/theme-swatches/tailwind-slate-dark.svg) | [svg](../../assets/theme-swatches/tailwind-slate-dark-cvd.svg) | [json](../../assets/tokens/tailwind-slate-dark.tokens.json) | [css](../../assets/tokens/tailwind-slate-dark.css) |
| `tech-monitoring` | [json](../../assets/pbi-themes/tech-monitoring.json) | [svg](../../assets/theme-swatches/tech-monitoring.svg) | [svg](../../assets/theme-swatches/tech-monitoring-cvd.svg) | [json](../../assets/tokens/tech-monitoring.tokens.json) | [css](../../assets/tokens/tech-monitoring.css) |
| `telecom-network` | [json](../../assets/pbi-themes/telecom-network.json) | [svg](../../assets/theme-swatches/telecom-network.svg) | [svg](../../assets/theme-swatches/telecom-network-cvd.svg) | [json](../../assets/tokens/telecom-network.tokens.json) | [css](../../assets/tokens/telecom-network.css) |
| `telecom-network-dark` | [json](../../assets/pbi-themes/telecom-network-dark.json) | [svg](../../assets/theme-swatches/telecom-network-dark.svg) | [svg](../../assets/theme-swatches/telecom-network-dark-cvd.svg) | [json](../../assets/tokens/telecom-network-dark.tokens.json) | [css](../../assets/tokens/telecom-network-dark.css) |

See also the compatibility heat matrix: [`theme-layout-matrix.svg`](../../assets/theme-layout-matrix.svg) · contact sheet: [`layouts-contact-sheet.svg`](../../assets/layouts-contact-sheet.svg).
