# Slicer previews

One SVG schematic per slicer recipe in
[`../../references/slicer-patterns/*.md`](../../references/slicer-patterns/).
Referenced from Design Spec §10 (Filters & Interactions) so reviewers can
recognise each recipe at a glance.

## File naming

Filename matches the recipe's `id` in
[`slicer-patterns-index.json`](../../references/slicer-patterns/slicer-patterns-index.json):

| Recipe id | File |
|---|---|
| `date-relative-rolling` | `date-relative-rolling.svg` |
| `chiclet-tile-slicer` | `chiclet-tile-slicer.svg` |
| `left-rail-global-panel` | `left-rail-global-panel.svg` |

## Rules

1. Size: **320 × 180 px** viewBox (matches chart-previews).
2. Dark-mode aware via embedded `<style id="preview-theme">` block with
   `@media (prefers-color-scheme: dark)`.
3. No real data — pure schematic so the control shape reads at a glance.
4. Every recipe in `slicer-patterns-index.json` must have a preview.

## Related references

- Decision guide: [`../../references/slicer-filter-patterns.md`](../../references/slicer-filter-patterns.md)
- Recipe catalog: [`../../references/slicer-patterns/`](../../references/slicer-patterns/)
