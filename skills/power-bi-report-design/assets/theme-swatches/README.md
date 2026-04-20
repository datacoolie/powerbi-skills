# Theme swatches

SVG palette swatches for every theme catalogued in
[`../../references/themes/themes-index.json`](../../references/themes/themes-index.json).
Used by the Strategist during Phase 4a.5 Seven Confirmations (item 5 — Palette)
to show stakeholders the approved color palette before any JSON is written.

## File naming

| Pattern | Example | Purpose |
|---|---|---|
| `<theme-id>.svg` | `sales-growth.svg` | Normal-vision swatch |
| `<theme-id>-cvd.svg` | `sales-growth-cvd.svg` | CVD-simulated (deuteranopia) swatch |

For every theme there are two SVGs: the normal palette and a color-vision-
deficiency simulated version so designers can verify categorical bars remain
distinguishable.

## Rules

1. Swatch viewBox: fixed across all themes for easy side-by-side comparison.
2. Each swatch shows: `data0…data7`, `foreground`, `background`, `good`, `bad`,
   `neutral`, `maximum`, `center`, `minimum`.
3. Contrast ratings (AAA/AA/fail) are annotated on the swatch.

## Related assets

- Drop-in PBI themes: [`../pbi-themes/`](../pbi-themes/)
- W3C design tokens: [`../tokens/`](../tokens/)
- Catalog + principles: [`../../references/theme-colors.md`](../../references/theme-colors.md)
- Machine-readable index: [`../../references/themes/themes-index.json`](../../references/themes/themes-index.json)
