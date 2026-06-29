# Card Visual Authoring Guide

Cards (`cardVisual`) display one or more headline metrics. `card` (legacy) is
deprecated — always use `cardVisual`.

- [Single-Value Template](#single-value-template)
- [Multi-Value Template](#multi-value-template)
- [Key Formatting Rules](#key-formatting-rules)
- [Multi-Value Formatting](#multi-value-formatting)
- [When to Consolidate vs. Keep Separate](#when-to-consolidate-vs-keep-separate)
- [Theme Approach](#theme-approach)
- [Discovering Properties](#discovering-properties)
- [References](#references)

---

## Single-Value Template

The `Data` role accepts one or more measures. For a single headline KPI:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
  "name": "<20hexchars>",
  "position": { "x": 24, "y": 56, "z": 1000, "height": 80, "width": 296, "tabOrder": 1000 },
  "visual": {
    "visualType": "cardVisual",
    "query": {
      "queryState": {
        "Data": {
          "projections": [{
            "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<Table>" } }, "Property": "<Measure>" } },
            "queryRef": "<Table>.<Measure>",
            "nativeQueryRef": "<Measure>"
          }]
        }
      }
    }
  }
}
```

---

## Multi-Value Template

Add multiple projections to the `Data` role. PBI renders them as a horizontal
row of callouts inside one visual. Use this instead of placing multiple
single-value cards side by side when they share the same container styling.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
  "name": "<20hexchars>",
  "position": { "x": 24, "y": 56, "z": 1000, "height": 120, "width": 900, "tabOrder": 1000 },
  "visual": {
    "visualType": "cardVisual",
    "query": {
      "queryState": {
        "Data": {
          "projections": [
            {
              "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<Table>" } }, "Property": "<Measure1>" } },
              "queryRef": "<Table>.<Measure1>",
              "nativeQueryRef": "<Measure1>"
            },
            {
              "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<Table>" } }, "Property": "<Measure2>" } },
              "queryRef": "<Table>.<Measure2>",
              "nativeQueryRef": "<Measure2>"
            },
            {
              "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<Table>" } }, "Property": "<Measure3>" } },
              "queryRef": "<Table>.<Measure3>",
              "nativeQueryRef": "<Measure3>"
            }
          ]
        }
      }
    }
  }
}
```

> **Sizing tip:** Multi-value cards need more width. Allow ~250–300 px per
> callout. For 3 measures a width of 900 px works well. Height of 100–120 px
> accommodates value + label without clipping.

---

## Key Formatting Rules

### Instance selectors required

Most `cardVisual` formatting objects require `selector: { "id": "default" }`.
Without it, properties silently fail to apply.

Objects that need the `id` selector: `value`, `label`, `accentBar`, `outline`,
`padding`, `spacing`, `divider`, `fillCustom`, `shadowCustom`, `glowCustom`,
`image`, `layout`, `referenceLabelTitle`, `referenceLabelValue`,
`referenceLabelDetail`.

Objects that do **NOT** need a selector: `cardCalloutArea`, `referenceLabel`,
`referenceLabelLayout`.

### Remove the internal border

The `outline` object controls the internal rectangular border inside the card.
To remove it (recommended):

```json
"outline": [{
  "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } },
  "selector": { "id": "default" }
}]
```

> ⚠️ This does **NOT** cascade from theme `visualStyles` — must be set
> per-visual. The outer container border (VCO `border`) is separate and
> does cascade from theme.

### Override the category label text

By default the card shows the raw measure name from the model. Override
with `label.text`:

```json
"label": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "text": { "expr": { "Literal": { "Value": "'Total Revenue'" } } }
  },
  "selector": { "id": "default" }
}]
```

### Font sizing and clipping

> **Applies to both creation and resizing.** Whenever a card is created or its
> `position.height` / `position.width` changes, re-evaluate font sizes against
> the new dimensions before proceeding.

The default callout font is 45 pt (from `textClasses.callout`), which overflows
cards shorter than ~250 px. Scale `value.fontSize` with card height, and also
check `label.fontSize` and VCO `padding` top/bottom margins — they consume
vertical space too. Confirm the final card with a Desktop screenshot because
schema-valid font and padding choices can still clip rendered content.

| Card height | Recommended `value.fontSize` |
|-------------|------------------------------|
| 72 px | `28D` |
| 80 px | `32D` |
| 120 px | `36D` |
| 200+ px | `45D` (default) |

### Accent bar

Adds a colored edge bar. Match color to the card's accent from the palette:

```json
"accentBar": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "position": { "expr": { "Literal": { "Value": "'Left'" } } },
    "width": { "expr": { "Literal": { "Value": "4D" } } },
    "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0072B2'" } } } } }
  },
  "selector": { "id": "default" }
}]
```

> **Tip:** When using an accent bar, set VCO `padding` to all zeros so the
> bar spans the full card height. Set `layout` outer margins to all zeros
> so the accent bar is flush against the card border. Set `padding`
> `topMargin: 0L`, `bottomMargin: 0L` (content sits tight against top),
> `leftMargin: 12L` (breathing room from the bar), `rightMargin: 8L`.

---

## Multi-Value Formatting

These formatting objects only take effect when the card has **2 or more**
measures in the `Data` role. On single-value cards they validate but have
no visible effect.

### cardCalloutArea

Controls per-callout tile styling — padding, corner radius, background fill.
Does **not** need an `id` selector.

```json
"cardCalloutArea": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "paddingUniform": { "expr": { "Literal": { "Value": "8L" } } },
    "rectangleRoundedCurve": { "expr": { "Literal": { "Value": "6L" } } },
    "backgroundFillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F5F5F5'" } } } } },
    "backgroundTransparency": { "expr": { "Literal": { "Value": "0D" } } }
  }
}]
```

### layout (gridlines between callouts)

Draws vertical separator lines between each callout tile. Use the `layout`
object — `cardVisual` does have a `grid` object that validates, but it does
**not** render the inter-callout separators in PBI Desktop. The working path
is `layout` with `style: "Table"` plus `customizeLines: true`, which unlocks
the `gridline*` properties below.

```json
"layout": [{
  "properties": {
    "style": { "expr": { "Literal": { "Value": "'Table'" } } },
    "customizeLines": { "expr": { "Literal": { "Value": "true" } } },
    "gridlineWidth": { "expr": { "Literal": { "Value": "1D" } } },
    "gridlineColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
    "gridlineTransparency": { "expr": { "Literal": { "Value": "0D" } } },
    "gridlineStyle": { "expr": { "Literal": { "Value": "'solid'" } } }
  },
  "selector": { "id": "default" }
}]
```

### divider

Horizontal divider line between value and label within each callout. Property
names are prefixed with `divider*` (the unprefixed `width/color/style/...`
belong to the visual-container `divider` object, not `cardVisual`'s own).

```json
"divider": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "dividerWidth": { "expr": { "Literal": { "Value": "1D" } } },
    "dividerColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#E0E0E0'" } } } } },
    "dividerTransparency": { "expr": { "Literal": { "Value": "0D" } } },
    "dividerLineStyle": { "expr": { "Literal": { "Value": "'solid'" } } },
    "dividerIgnorePadding": { "expr": { "Literal": { "Value": "true" } } }
  },
  "selector": { "id": "default" }
}]
```

> **Note:** `value` and `label` formatting (font, size, color, alignment)
> applies uniformly to all callouts — you cannot style individual callouts
> differently within the same multi-value card.

---

## When to Consolidate vs. Keep Separate

**Use one multi-value card** when adjacent KPI cards:
- Share the same container styling (border, background, shadow)
- Need uniform font sizes and label formatting
- Are a cohesive metric group (e.g., Revenue, Profit, Units)
- Benefit from built-in `layout` gridlines and per-callout `divider` lines

**Keep separate single-value cards** when you need:
- Per-card accent bar colors (each card gets its own accent color)
- Different background colors or conditional formatting per metric
- Different font sizes per metric (e.g., hero card larger than supporting cards)
- Individual card click/drill-through behavior

---

## Theme Approach

These `cardVisual` defaults can be applied report-wide via theme
`visualStyles` (plain JSON, not PBIR `expr` wrappers):

```json
"cardVisual": {
  "*": {
    "value": [{ "bold": true, "$id": "default" }],
    "label": [{ "show": true, "$id": "default" }],
    "cardCalloutArea": [{ "paddingUniform": 0 }],
    "border": [{ "show": true, "color": { "solid": { "color": "#E8E8E8" } }, "radius": 8 }],
    "title": [{ "show": false }],
    "spacing": [{ "verticalSpacing": -6 }],
    "padding": [{ "top": 0, "bottom": 0, "left": 0, "right": 0 }]
  }
}
```

> ⚠️ `outline`, `accentBar`, `layout`, visual-level `padding` (with `leftMargin` etc.),
> `value.fontColor`, and `label.text` do **NOT** cascade from theme — they
> must be set per-visual.
>
> **VCO mixing caveat**: If you set ANY VCO property per-visual (background,
> border, visualHeader), also set `padding` per-visual in the same
> `visualContainerObjects` block. Otherwise PBI may reset padding to its
> default (~5px) instead of inheriting from the theme.

**Layout outer margins** — To eliminate the gap between the card border and
content (so the accent bar sits flush), set `layout` with `id: "default"`:

```json
"layout": [{
  "properties": {
    "topOuterMargin": { "expr": { "Literal": { "Value": "0L" } } },
    "bottomOuterMargin": { "expr": { "Literal": { "Value": "0L" } } },
    "leftOuterMargin": { "expr": { "Literal": { "Value": "0L" } } },
    "rightOuterMargin": { "expr": { "Literal": { "Value": "0L" } } },
    "paddingUniform": { "expr": { "Literal": { "Value": "0L" } } }
  },
  "selector": { "id": "default" }
}]
```

---

## Discovering Properties

```bash
# List all formatting objects for cardVisual
powerbi-report-author formatting list-objects cardVisual

# Inspect a specific object
powerbi-report-author formatting describe-object cardVisual value
powerbi-report-author formatting describe-object cardVisual accentBar
powerbi-report-author formatting describe-object cardVisual outline
powerbi-report-author formatting describe-object cardVisual referenceLabel

# Search across all objects for a property
powerbi-report-author formatting search cardVisual "padding|margin"
```

---

## References

- [formatting.md § Selectors](formatting.md#selectors-targeting-specific-data) — id selector pattern
- [theming.md § Visual Styles](theming.md#6-visual-styles-visualstyles) — theme defaults

