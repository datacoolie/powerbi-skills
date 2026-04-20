# Layout previews

One SVG per layout in
[`../../references/layouts/*.md`](../../references/layouts/) plus its variants
(`-annotated`, `-dark`, `-mobile`, `-tv`, `-a4`). Referenced from Design Spec §4
and from Phase 4a.5 Seven Confirmations so stakeholders can preview spatial
arrangement before any JSON is generated.

## File naming

`<layout-id>[-variant][-dark|-annotated].svg`

| Pattern | Example |
|---|---|
| Base | `exec-overview-16x9.svg` |
| Annotated | `exec-overview-16x9-annotated.svg` |
| Dark mode | `exec-overview-16x9-dark.svg` |
| Mobile variant | `exec-overview-16x9-mobile.svg` |
| Mobile · dark | `exec-overview-16x9-mobile-dark.svg` |
| TV variant | `mfg-line-status-tv.svg` |
| A4 variant | `finance-pnl-waterfall-a4.svg` |

Derived variants (`-mobile`, `-tv`, `-a4`) are themselves layout ids in
[`../../references/layouts/layouts-index.json`](../../references/layouts/layouts-index.json).
Their `.svg` files are the **base preview** for those ids.

## Rules

1. Size: **1664 × 936** viewBox for desktop, **414 × 736** for mobile,
   **1920 × 1080** for TV, **816 × 1056** for A4. Schematic only — no real data.
2. Dark variants use the theme-aware `<style id="preview-theme">` block with
   `@media (prefers-color-scheme: dark)` switching.
3. Annotated variants add callouts over the base layout to explain zones.
4. Every layout id in `layouts-index.json` must have a base preview here.

## Related assets

- [`../../assets/layouts-contact-sheet.svg`](../layouts-contact-sheet.svg) —
  one-page catalog overview of all 86 base layouts.
- [`../../assets/theme-layout-matrix.svg`](../theme-layout-matrix.svg) —
  theme × layout compatibility grid.

## Provenance

All previews are hand-authored schematics following the 8 px grid from
[`../../references/shared-standards.md`](../../references/shared-standards.md).
