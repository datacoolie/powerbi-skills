# W3C design tokens

W3C [Design Tokens Community Group](https://www.w3.org/community/design-tokens/)
format tokens + compiled CSS variables for every theme catalogued in
[`../../references/themes/themes-index.json`](../../references/themes/themes-index.json).

## File naming

For each theme id, two files:

| Pattern | Example | Format |
|---|---|---|
| `<theme-id>.tokens.json` | `sales-growth.tokens.json` | W3C design tokens (JSON) |
| `<theme-id>.css` | `sales-growth.css` | CSS custom properties (`--color-data0`, …) |

52 theme ids × 2 files = **104 files**.

## How to use

### In web / HTML artifacts

```css
@import url("./sales-growth.css");

.card {
  color: var(--color-foreground);
  background: var(--color-background);
  border-color: var(--color-neutrals-divider);
}
```

### In design tooling

Import `<theme-id>.tokens.json` into Figma / Tokens Studio / Style Dictionary
to generate platform-specific variables (iOS, Android, Tailwind, …).

## Token categories

Every tokens file emits:

- `color.data.0` … `color.data.7` — categorical series
- `color.foreground`, `color.background` — canvas
- `color.good`, `color.bad`, `color.neutral`, `color.maximum`, `color.center`,
  `color.minimum` — semantic
- `color.neutrals.muted`, `color.neutrals.gridline`, `color.neutrals.divider`,
  `color.neutrals.disabled` — UI
- `color.sequential.primary.light|mid|dark` — 3-stop ramps (primary, positive,
  warning, negative)

## Rules

1. Every theme in `themes-index.json` has a `.tokens.json` AND a `.css`.
2. Token paths follow W3C DTCG spec (`$value`, `$type: "color"`).
3. The CSS file is generated from the tokens file — don't edit the CSS by hand.

## Related assets

- Power BI theme JSON: [`../pbi-themes/`](../pbi-themes/)
- Visual swatches: [`../theme-swatches/`](../theme-swatches/)
- Theme catalog + principles: [`../../references/theme-colors.md`](../../references/theme-colors.md)
- Color discipline: [`../../references/shared-standards.md`](../../references/shared-standards.md) §3
