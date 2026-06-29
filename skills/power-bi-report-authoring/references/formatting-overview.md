# Formatting & Theming Overview

> **Read this first** before editing any visual appearance in a PBIR report.
> It explains the cascade model, value encoding rules, and which file to read next.

## Formatting Cascade

Power BI resolves formatting in a layered cascade (highest priority wins):

| Priority | Layer | File | Encoding |
|---|---|---|---|
| 1 (highest) | Conditional formatting | `visual.json` objects (FillRule, rules) | PBIR expressions |
| 2 | Per-visual objects | `visual.json → visual.objects` | PBIR expressions |
| 3 | Visual container objects | `visual.json → visual.visualContainerObjects` | PBIR expressions |
| 4 | Page objects | `page.json → objects` (background, filter pane) | PBIR expressions |
| 5 | Custom theme (type-specific) | `theme.json → visualStyles[type]["*"][obj]` | Theme encoding |
| 6 | Custom theme (wildcard) | `theme.json → visualStyles["*"]["*"][obj]` | Theme encoding |
| 7 | Base theme | `SharedResources/BaseThemes/` | Theme encoding |
| 8 (lowest) | System defaults | Built into PBI Desktop | — |

A property set at layer 2 overrides the same property at layers 3–8.
When a cascade result matters visually, verify in Desktop with screenshots.

> **Theme changes require sweeping all cascade layers.** The theme file only
> controls layers 5–6. Hardcoded colors in `page.json` (layer 4) and
> `visual.json` (layers 2–3) override the theme and must be updated in the
> same operation. See re-theming patterns in the formatting-patterns reference.

## VCO Per-Visual Requirements

These `visualContainerObjects` properties must be set **per-visual** — they do
not cascade reliably from theme `visualStyles`:

- `border` (including `radius`) — for rounded corners
- `background` (show, color, transparency)
- `padding` — must accompany any other VCO override
- Card-specific: `accentBar`, `outline`, `layout` (require `selector: { id: "default" }`)

**Rule**: When setting any `visualContainerObjects` per-visual, always set
`background`, `border` (with `radius`), `padding`, and `visualHeader` together.
Partial VCO overrides cause PBI to reset omitted properties to system defaults.

## Value Encoding — Three Formats

**Critical**: Theme files and PBIR files encode the same properties differently.
Using the wrong encoding is the #1 formatting error.

| Value | Theme JSON (plain) | Theme visualStyles (hybrid) | PBIR visual.json (expression-wrapped) |
|---|---|---|---|
| Boolean | `true` | `true` | `{"expr":{"Literal":{"Value":"true"}}}` |
| Number | `12` | `12` | `{"expr":{"Literal":{"Value":"12D"}}}` |
| Integer | `3` | `3` | `{"expr":{"Literal":{"Value":"3L"}}}` |
| String | `"dotted"` | `"dotted"` | `{"expr":{"Literal":{"Value":"'dotted'"}}}` |
| Color | `"#118DFF"` | `"#118DFF"` or `{"solid":{"color":"#118DFF"}}` | `{"solid":{"color":{"expr":{"Literal":{"Value":"'#118DFF'"}}}}}` |
| Theme color | — | — | `{"solid":{"color":{"expr":{"ThemeDataColor":{"ColorId":0,"Percent":0}}}}}` |

**Rules:**
- **theme.json** top-level keys (dataColors, good/bad, structural): plain JSON
- **theme.json** `visualStyles` properties: plain JSON (some color props need `{"solid":{"color":"#hex"}}`)
- **visual.json** and **page.json** objects: always PBIR expression wrappers
- Use `powerbi-report-author expr encode --kind <t> <v>` for PBIR encodings
- Use `powerbi-report-author theme encode --kind <t> <v>` for theme values
- Use `powerbi-report-author expr decode '<json>'` to inspect existing values

## Selector Types (Quick Reference)

Selectors control which data a formatting entry targets. Five types, in
descending priority:

| Type | Syntax | Use Case |
|---|---|---|
| **data** (scope identity) | `"data": [{"scopeId": {...}}]` | Color a specific category value |
| **data** (wildcard) | `"data": [{"dataViewWildcard": {"matchingOption": N}}]` | All instances (0), instances only (1), totals only (2) |
| **metadata** | `"metadata": "Table.Field"` | Target specific measure/column |
| **id** | `"id": "default"` | User-defined instance (cards, filter cards) |
| **none** (static) | *(no selector)* | Base formatting — lowest priority |

Within each priority row, **first match in array order wins**.

See `formatting-patterns.md` for full selector patterns and examples.

## Which File to Read Next

| You are editing… | Read this |
|---|---|
| `visual.json` — chart colors, labels, axes, data points, VCOs, conditional formatting | `formatting-patterns.md` |
| `visual.json` — reusable components (KPI rows, slicers, nav) | `common-patterns.md` |
| Theme JSON — dataColors, textClasses, visualStyles | Themes in `themes/` directory |
| Screenshots after Desktop reload | `screenshot-review.md` |
| Desktop verification loop | `powerbi-desktop.md` |
| CLI metadata lookup | `powerbi-report-author-cli.md` |
