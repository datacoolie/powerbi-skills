# Theme & Color Guide

Comprehensive guide for choosing themes, color palettes, and semantic colors
in Power BI PBIR reports. Based on analysis of 25 production reference reports
and modern data visualization best practices.

> **Machine-readable companion:** the twenty-one themes documented or
> catalogued below are also available as a structured catalog at
> [`themes/themes-index.json`](themes/themes-index.json) with visual
> swatches in [`../assets/theme-swatches/`](../assets/theme-swatches/).
> Layouts reference themes via `recommended_themes[]` — see
> [`themes/README.md`](themes/README.md) for the full catalog map
> (16 domain themes + 4 design-system themes + 1 dark-mode).

> **Ready-to-use assets:**
> - Power BI theme JSON files: [`../assets/pbi-themes/`](../assets/pbi-themes/) (drop into Power BI Desktop → View → Themes → Browse)
> - W3C design-token pairs (.tokens.json + .css): [`../assets/tokens/`](../assets/tokens/) (52 theme pairs = 104 files)
> - Theme × layout compatibility matrix: [`../assets/theme-layout-matrix.svg`](../assets/theme-layout-matrix.svg)

---

## Color Usage Principles (v0.2)

The themes catalog encodes *palettes*. These principles govern *how a palette
is applied on a page*. They are consulting-grade rules borrowed from deck-design
practice and stored in `themes-index.json` under the top-level `principles` key.

### 1. 60-30-10 Proportion Rule

On any single page, color weight should split roughly **60% primary / 30%
secondary / 10% accent**. The primary is usually the first `data_colors` slot
(or `ui.table_accent`); the secondary is a neutral or muted variant; the
accent is reserved for the one thing the page is *about*.

Per-theme overrides live in `usage_rules.primary_share` / `secondary_share` /
`accent_share` — e.g. `consulting-authority` tightens to 70/20/10 for
executive restraint; `tech-monitoring` loosens to 50/30/20 because dashboards
legitimately use more hues.

### 2. Maximum 4 Colors per Page

Hard ceiling. Data series should use same-hue depth variations (see
`sequential.primary` ramp) rather than N distinct hues. If you need more than
four colors the chart is probably the wrong visual choice. Per-theme override:
`usage_rules.max_colors_per_page` (range 3–5 across the catalog).

### 3. Text Contrast ≥ 4.5:1 (WCAG AA)

Every theme stores a computed `ui.text_contrast` and `ui.contrast_rating`
(AAA / AA / AA-large / fail) for `foreground` on `background`. All nine
current themes rate **AAA** (≥ 7:1). When authoring a page, any text placed
on a non-default background (KPI card, callout, table header) must be
re-verified against the chosen background hex.

### 4. Monochromatic Depth for Data Series

Default encoding for multi-series charts:

| Role | Color | Source |
|------|-------|--------|
| Primary series | `sequential.primary[2]` (dark) at 100% opacity | primary ramp |
| Comparison series | same hue at 60% opacity | same ramp |
| Highlight | `data_colors[1]` or semantic accent at 100% | accent |

Avoid assigning a different hue per series (the "rainbow anti-pattern") except
when the series legitimately encode categorical identity (region, SKU family).

### 5. Focus-in-Color Pattern

The data point the page is *about* takes the primary or accent color;
**everything else uses `neutrals.muted` / `neutrals.gridline`**. Color
communicates attention, not decoration. Use `neutrals.muted` for
de-emphasized series, `neutrals.gridline` for axes and rule lines,
`neutrals.divider` for card separators, `neutrals.disabled` for
not-applicable states.

### 6. Sequential Ramps

Each theme provides 3-stop light → mid → dark ramps for `positive`,
`warning`, `negative`, and `primary`. Use them for:

- Trend heatmaps (conditional formatting)
- Choropleth / filled maps
- Gradient fills on area charts
- Stacked series where a single semantic dimension is varying intensity

The dark stop is *not* the same as the semantic base color — ramps are
computed to preserve hue while spanning a usable luminance range.

---

## Theme Architecture

Every report has a **base theme** (Microsoft built-in) and optionally a **custom theme**
(JSON file in `StaticResources/RegisteredResources/`). The custom theme overrides the base.

### report.json Theme Reference

```json
"themeCollection": {
  "baseTheme": {
    "name": "CY24SU10",
    "reportVersionAtImport": { "visual": "2.1.0", "report": "2.1.0", "page": "2.0.0" },
    "type": "SharedResources"
  },
  "customTheme": {
    "name": "<theme-filename>.json",
    "reportVersionAtImport": { "visual": "2.1.0", "report": "2.1.0", "page": "2.0.0" },
    "type": "RegisteredResources"
  }
}
```

The custom theme file must also be registered in `resourcePackages`:
```json
"resourcePackages": [
  {
    "name": "RegisteredResources",
    "type": "RegisteredResources",
    "items": [
      {
        "name": "<theme-filename>.json",
        "path": "<theme-filename>.json",
        "type": "Image"
      }
    ]
  },
  {
    "name": "SharedResources",
    "type": "SharedResources",
    "items": [
      { "name": "CY24SU10", "path": "BaseThemes/CY24SU10.json", "type": "BaseTheme" }
    ]
  }
]
```

**Note**: Custom theme files use `"type": "Image"` in `resourcePackages` even though they are JSON.

### Base Theme Selection

Use the latest stable base theme: **CY24SU10**.

---

## Semantic Colors

Semantic colors carry universal meaning. **Always** define these consistently in your theme.

### Status & Outcome Colors

| Meaning | Hex | Name | Usage |
|---|---|---|---|
| **Success / Good / Passed** | `#38B64B` | Emerald Green | KPIs above target, positive variance, completed status |
| **Failure / Bad / Failed** | `#EE1C25` | Signal Red | KPIs below target, negative variance, error status |
| **Warning / Caution** | `#F5A623` | Amber Orange | Approaching threshold, needs attention |
| **Neutral / Skipped / N/A** | `#949599` | Slate Gray | No status, skipped, not applicable, inactive |
| **In Progress / Pending** | `#0078D4` | Azure Blue | Running, in-flight, awaiting result |

### Variance & Comparison Colors

| Meaning | Hex | Name | Usage |
|---|---|---|---|
| **Above target / Positive** | `#38B64B` | Emerald Green | Exceeding expectation, growth |
| **Below target / Negative** | `#EE1C25` | Signal Red | Missing target, decline |
| **On target / Neutral** | `#949599` | Slate Gray | Within acceptable range |
| **Forecast / Projected** | `#808080` | Medium Gray | Projected values (dashed line) |
| **Budget / Target line** | `#404040` | Dark Gray | Reference lines, benchmarks |

### Conditional Formatting JSON (in visuals)

Positive/negative value color expression (e.g., for a KPI card or conditional measure):
```json
"color": {
  "solid": {
    "color": {
      "expr": {
        "Conditional": {
          "Cases": [
            {
              "Condition": { "Comparison": { "ComparisonKind": 1, "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "Measures" } }, "Property": "Variance%" } }, "Right": { "Literal": { "Value": "0D" } } } },
              "Value": { "Literal": { "Value": "'#38B64B'" } }
            }
          ],
          "Else": { "Literal": { "Value": "'#EE1C25'" } }
        }
      }
    }
  }
}
```

### Theme-Level Semantic Colors

Define these in the custom theme JSON — Power BI uses them for KPI visuals,
conditional formatting defaults, and gauge ranges:

```json
{
  "good": "#38B64B",
  "bad": "#EE1C25",
  "neutral": "#949599",
  "maximum": "#003052",
  "minimum": "#B2D7ED",
  "center": "#0078D4"
}
```

---

## Industry Color Palettes

Choose a palette that matches the report's domain. Each palette includes:
- **8 data colors** for chart series (primary → secondary → accent)
- **Semantic colors** (good/bad/neutral)
- **UI colors** (background, text, borders)

### Corporate / Financial

Dark, conservative palette conveying trust and authority.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#003052` | Navy |
| Secondary | `#0078D4` | Blue |
| Accent 1 | `#D4A846` | Gold |
| Accent 2 | `#6B7A8D` | Steel |
| Accent 3 | `#9B59B6` | Purple |
| Accent 4 | `#2ECC71` | Green |
| Accent 5 | `#E67E22` | Amber |
| Accent 6 | `#95A5A6` | Silver |

```json
"dataColors": ["#003052", "#0078D4", "#D4A846", "#6B7A8D", "#9B59B6", "#2ECC71", "#E67E22", "#95A5A6"],
"background": "#F8F9FA",
"foreground": "#1A1A2E",
"tableAccent": "#003052"
```

### Sales / Revenue / Growth

Vibrant, energetic palette with blue-green primary and warm accents.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#0078D4` | Azure Blue |
| Secondary | `#00B7C3` | Teal |
| Accent 1 | `#E74856` | Coral Red |
| Accent 2 | `#FF8C00` | Dark Orange |
| Accent 3 | `#107C10` | Forest Green |
| Accent 4 | `#5C2D91` | Royal Purple |
| Accent 5 | `#FFB900` | Marigold |
| Accent 6 | `#767676` | Neutral Gray |

```json
"dataColors": ["#0078D4", "#00B7C3", "#E74856", "#FF8C00", "#107C10", "#5C2D91", "#FFB900", "#767676"],
"background": "#FFFFFF",
"foreground": "#242424",
"tableAccent": "#0078D4"
```

### Manufacturing / Operations

Industrial palette with muted base and safety-accent colors.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#2B5797` | Industrial Blue |
| Secondary | `#7A7574` | Warm Gray |
| Accent 1 | `#E8980C` | Safety Yellow |
| Accent 2 | `#DF5022` | Safety Orange |
| Accent 3 | `#38B64B` | Process Green |
| Accent 4 | `#A4262C` | Stop Red |
| Accent 5 | `#8764B8` | Soft Purple |
| Accent 6 | `#00B294` | Teal |

```json
"dataColors": ["#2B5797", "#7A7574", "#E8980C", "#DF5022", "#38B64B", "#A4262C", "#8764B8", "#00B294"],
"background": "#F6F8F9",
"foreground": "#292E6B",
"tableAccent": "#2B5797"
```

### Healthcare / Pharma

Clean, clinical palette with calming blues and teals.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#0077B6` | Medical Blue |
| Secondary | `#48CAE4` | Sky Blue |
| Accent 1 | `#00B4D8` | Cyan |
| Accent 2 | `#90E0EF` | Pale Cyan |
| Accent 3 | `#023E8A` | Deep Blue |
| Accent 4 | `#38B64B` | Health Green |
| Accent 5 | `#E63946` | Alert Red |
| Accent 6 | `#457B9D` | Steel Blue |

```json
"dataColors": ["#0077B6", "#48CAE4", "#00B4D8", "#90E0EF", "#023E8A", "#38B64B", "#E63946", "#457B9D"],
"background": "#F8FFFE",
"foreground": "#1D3557",
"tableAccent": "#0077B6"
```

### Supply Chain / Logistics

Cool blue progression from dark to light, easy to read at a glance.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#012A4A` | Midnight Navy |
| Secondary | `#01497C` | Deep Ocean |
| Accent 1 | `#014F86` | Steel Blue |
| Accent 2 | `#2A6F97` | Medium Blue |
| Accent 3 | `#468FAF` | Cerulean |
| Accent 4 | `#8AD4EB` | Sky |
| Accent 5 | `#FE9666` | Peach |
| Accent 6 | `#A66999` | Mauve |

```json
"dataColors": ["#012A4A", "#01497C", "#014F86", "#2A6F97", "#468FAF", "#8AD4EB", "#FE9666", "#A66999"],
"background": "#E6ECF0",
"foreground": "#292E6B",
"tableAccent": "#012A4A"
```

### Retail / Consumer / FMCG

Fresh green palette with warm accents — organic and inviting.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#3CB043` | Fresh Green |
| Secondary | `#98BF64` | Sage |
| Accent 1 | `#74B72E` | Lime |
| Accent 2 | `#5DBB63` | Spring Green |
| Accent 3 | `#3599B8` | Ocean Teal |
| Accent 4 | `#F4D25A` | Honey |
| Accent 5 | `#FB8281` | Salmon |
| Accent 6 | `#5F6B6D` | Charcoal |

```json
"dataColors": ["#3CB043", "#98BF64", "#74B72E", "#5DBB63", "#3599B8", "#F4D25A", "#FB8281", "#5F6B6D"],
"background": "#EAF8EE",
"foreground": "#2D4A22",
"tableAccent": "#3CB043"
```

### Sustainability / ESG

Earth tones with organic greens and natural warmth.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#2D6A4F` | Forest |
| Secondary | `#52B788` | Moss |
| Accent 1 | `#95D5B2` | Seafoam |
| Accent 2 | `#D8F3DC` | Pale Mint |
| Accent 3 | `#8B5E3C` | Earth Brown |
| Accent 4 | `#D4A846` | Gold |
| Accent 5 | `#E76F51` | Terra Cotta |
| Accent 6 | `#264653` | Dark Teal |

```json
"dataColors": ["#2D6A4F", "#52B788", "#95D5B2", "#D8F3DC", "#8B5E3C", "#D4A846", "#E76F51", "#264653"],
"background": "#F5F5F0",
"foreground": "#1B4332",
"tableAccent": "#2D6A4F"
```

### Technology / IT / Monitoring

Dark-mode-friendly palette with electric accents for dashboards.

| Role | Hex | Swatch |
|---|---|---|
| Primary | `#0078D4` | Azure |
| Secondary | `#50E6FF` | Neon Cyan |
| Accent 1 | `#9B59B6` | Purple |
| Accent 2 | `#FF8C00` | Vivid Orange |
| Accent 3 | `#10893E` | Green |
| Accent 4 | `#E81123` | Red |
| Accent 5 | `#FFB900` | Yellow |
| Accent 6 | `#6B6B6B` | Gray |

```json
"dataColors": ["#0078D4", "#50E6FF", "#9B59B6", "#FF8C00", "#10893E", "#E81123", "#FFB900", "#6B6B6B"],
"background": "#F3F2F1",
"foreground": "#201F1E",
"tableAccent": "#0078D4"
```

---

## Custom Theme JSON Template

Complete template with all sections. Place in `StaticResources/RegisteredResources/`.

```json
{
  "name": "Custom Report Theme",
  "$schema": "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.121.json",
  "dataColors": [
    "#0078D4", "#00B7C3", "#E74856", "#FF8C00",
    "#107C10", "#5C2D91", "#FFB900", "#767676"
  ],
  "good": "#38B64B",
  "bad": "#EE1C25",
  "neutral": "#949599",
  "maximum": "#003052",
  "minimum": "#B2D7ED",
  "center": "#0078D4",
  "foreground": "#242424",
  "background": "#FFFFFF",
  "secondaryBackground": "#F3F2F1",
  "backgroundLight": "#FAFAFA",
  "foregroundNeutralSecondary": "#605E5C",
  "foregroundNeutralTertiary": "#A19F9D",
  "tableAccent": "#0078D4",
  "firstLevelElements": "#242424",
  "secondLevelElements": "#605E5C",
  "thirdLevelElements": "#A19F9D",
  "fourthLevelElements": "#D2D0CE",
  "textClasses": {
    "callout": { "fontFace": "Segoe UI", "color": "#242424" },
    "header":  { "fontFace": "Segoe UI", "color": "#242424" },
    "title":   { "fontFace": "Segoe UI", "color": "#242424", "fontSize": 10 },
    "largeTitle": { "fontFace": "Segoe UI", "color": "#242424", "fontSize": 14 },
    "label":   { "fontFace": "Segoe UI", "color": "#605E5C", "fontSize": 9 }
  },
  "visualStyles": {
    "*": {
      "*": {
        "background": [{ "color": { "solid": { "color": "#FFFFFF" } }, "transparency": 0 }],
        "border": [{ "color": { "solid": { "color": "#E1DFDD" } }, "radius": 8, "show": true, "transparency": 0 }],
        "dropShadow": [{ "show": true, "color": { "solid": { "color": "#000000" } }, "shadowSpread": 0, "shadowBlur": 6, "angle": 90, "shadowDistance": 3, "transparency": 85, "position": "Outer", "preset": "Custom" }],
        "padding": [{ "top": 8 }, { "bottom": 8 }, { "left": 10 }, { "right": 10 }],
        "categoryAxis": [{ "showAxisTitle": false }],
        "valueAxis": [{ "showAxisTitle": false, "gridlineShow": true, "gridlineStyle": "dotted", "gridlineThickness": 1 }],
        "legend": [{ "position": "TopCenter", "showTitle": false }],
        "subTitle": [{ "show": true }],
        "totals": [{ "show": true, "bold": true }]
      }
    },
    "page": {
      "*": {
        "background": [{ "color": { "solid": { "color": "#F3F2F1" } }, "transparency": 0 }]
      }
    },
    "tableEx": {
      "*": {
        "columnHeaders": [{ "backColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0.9 } } } } } }],
        "grid": [{ "gridHorizontal": true, "rowPadding": 3.5 }],
        "values": [{ "backColorPrimary": { "solid": { "color": "#F8F9FA" } }, "backColorSecondary": { "solid": { "color": "#FFFFFF" } } }]
      }
    },
    "pivotTable": {
      "*": {
        "grid": [{ "rowPadding": 5 }],
        "stylePreset": [{ "name": "Minimal" }]
      }
    }
  }
}
```

---

## Color Expression Patterns in Visuals

### Literal Color (hardcoded hex)
```json
"color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0078D4'" } } } } }
```

### Theme Data Color (references theme palette by index)
```json
"color": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } }
```
- `ColorId` = zero-based index into the theme's `dataColors` array
- `Percent` = lightness adjustment: `0` = original, positive = lighter, negative = darker
  Examples: `-0.5` = 50% darker, `0.4` = 40% lighter, `0.9` = very light (header background)

### When to Use Which

| Scenario | Method | Reason |
|---|---|---|
| Chart series default colors | `ThemeDataColor` | Respects theme changes — user can swap themes |
| Semantic colors (green/red for KPIs) | Literal hex | Meaning must not change with theme |
| Conditional formatting rules | Literal hex | Colors represent specific conditions |
| Background shapes | Either | `ThemeDataColor` for accent shapes; literal for fixed brand |
| Text/label colors | `ThemeDataColor` | Stays readable when theme changes |
| Header/navigation elements | Literal hex | Brand consistency across themes |

### Opacity / Transparency

All color properties can include transparency:
```json
"transparency": { "expr": { "Literal": { "Value": "30L" } } }
```
Value range: `0` = fully opaque, `100` = fully transparent.

---

## UI Color System

Consistent UI colors for structural elements (header bars, slicer panels, navigation):

| Element | Light Theme | Dark Accent | Notes |
|---|---|---|---|
| Page background | `#F3F2F1` | `#1B1A19` | Slightly off-white/off-black — never pure white/black |
| Visual background | `#FFFFFF` | `#292827` | Cards float on the page background |
| Header bar shape | Primary color | Primary color | Full-width shape at top; z-index 0 |
| Header text | `#FFFFFF` | `#FFFFFF` | White on dark header |
| Slicer panel background | `#E6ECF0` | `#323130` | Distinct from page bg |
| Visual border | `#E1DFDD` | `#484644` | Subtle, 1px, rounded |
| Gridlines | `#E8E8E8` | `#484644` | Dotted, minimal |
| Axis labels | `#605E5C` | `#A19F9D` | Never black; subtle gray |
| Title text | `#242424` | `#F3F2F1` | Near-black, not pure black |
| Body/label text | `#605E5C` | `#D2D0CE` | Secondary importance |
| Disabled/muted | `#A19F9D` | `#797775` | Ghosted elements |
| Divider lines | `#D2D0CE` | `#484644` | Section separators |

---

## Colorblind-Safe Alternatives

### Replace Red-Green with Blue-Orange

When red-green distinction is critical (KPIs, conditional formatting), also add a
secondary encoding (icons like ▲▼, bold, or +/- signs) beside the color.

| Standard | Colorblind-Safe | When |
|---|---|---|
| Green = Good | `#0078D4` Blue | If audience may include colorblind users |
| Red = Bad | `#FF6D00` Orange | Accessible contrast with blue |
| Yellow = Warning | `#A19F9D` Gray | Neutral warning |

### Color Oracle Test

Before finalizing a theme, verify with:
1. **Deuteranopia** (red-green, most common) — [colororacle.org](https://colororacle.org)
2. **Protanopia** (red-blind)
3. **Tritanopia** (blue-yellow, rare)

If any two semantic colors become indistinguishable, add secondary encoding (icons, patterns).

---

## Color Rules Summary

1. **Always define semantic colors** — `good`/`bad`/`neutral` in theme JSON; use literal hex in conditional formatting
2. **Match palette to industry** — use the industry palettes above as starting points
3. **Limit chart colors** — 1-2 accent colors + gray for most visuals; max 6-8 for categorical
4. **Use ThemeDataColor for defaults** — chart series, axis labels, gridlines reference the theme
5. **Use literal hex for meanings** — green/red KPIs, brand colors, conditional rules
6. **Define page background in theme** — `visualStyles.page.*.background` so all pages are consistent
7. **Set visual background to white** — `visualStyles.*.*.background` creates floating-card effect
8. **Add rounded corners + subtle shadow** — modern appearance via `border.radius: 8` + `dropShadow`
9. **Keep text hierarchy via theme** — `textClasses` for consistent font sizing across all visuals
10. **Test for accessibility** — verify color contrast ratios and colorblind safety
