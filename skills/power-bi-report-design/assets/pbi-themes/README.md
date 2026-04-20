# Power BI theme JSON files

Drop-in `theme.json` files for every theme catalogued in
[`../../references/themes/themes-index.json`](../../references/themes/themes-index.json).

## How to apply

**Power BI Desktop** → View → Themes → Browse for themes → pick the `.json` here.

Or embed in PBIR at report level by placing the theme JSON under
`<report>.Report/StaticResources/SharedResources/BaseThemes/`.

## File naming

`<theme-id>.json` where `<theme-id>` matches the entry in `themes-index.json`.

52 themes total:

- **16 domain themes** (sales-growth, manufacturing-ops, finance/corporate-
  financial, healthcare-pharma, retail-fmcg, marketing-digital, hr-people-
  analytics, telecom-network, supply-chain-logistics, public-sector-gov,
  education-edtech, real-estate-hospitality, media-entertainment,
  sustainability-esg, consulting-authority, tech-monitoring) — **15 have
  dark pairs** (tech-monitoring is already dark-first, no pair)
- **5 brand-inspired themes** + 5 dark pairs (atlassian, google-material,
  ibm-carbon, salesforce, stripe)
- **3 design-system themes** + 3 dark pairs (microsoft-fluent, tailwind-slate,
  nord-frost)
- **2 accessibility themes** (accessible-okabe-ito CVD-safe, high-contrast-dark)
- **3 seasonal variants** (corporate-financial-q4, retail-fmcg-holiday,
  sustainability-esg-earthday)

Totals: 16 + 15 domain · 5 + 5 brand · 3 + 3 design-system · 2 accessibility ·
3 seasonal = **52**.

## Related assets

- Visual swatches: [`../theme-swatches/`](../theme-swatches/) (normal + CVD)
- W3C design-token pairs: [`../tokens/`](../tokens/) (.tokens.json + .css)
- Catalog index: [`../../references/themes/themes-index.json`](../../references/themes/themes-index.json)
- Theme × layout matrix: [`../theme-layout-matrix.svg`](../theme-layout-matrix.svg)

## Rules

1. Every theme must have a matching swatch SVG and tokens pair.
2. Text contrast ≥ 4.5:1 (WCAG AA). Dark variants ≥ 4.5:1 on dark background.
3. `dataColors` array has exactly 8 entries (`data0…data7`).
4. Semantic tokens (`good`, `bad`, `neutral`, `maximum`, `center`, `minimum`) set.
