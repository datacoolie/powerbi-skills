# Shared Standards (PBIR Non-Negotiables)

> **Applies to every role** — Strategist, Executor (all styles), Polisher.
> If a rule here conflicts with a style personality file, **this file wins**.

---

## 1. Banned Patterns (never ship these)

### Visual types
- ❌ **3D charts** of any kind
- ❌ **Pie / donut with > 5 slices** — use stacked bar or Top-N + "Other"
- ❌ **Dual-axis charts** unless both axes are the same unit and justified in the Design Spec
- ❌ **Stacked charts used to compare totals** — use clustered
- ❌ **Combo chart with > 2 series types** — one bar + one line only

### Data density
- ❌ **> 8 visuals per page** (Operational style allowed 8-12 — see `executor-operational.md`)
- ❌ **> 6 slicers per page**
- ❌ **Line chart with < 3 data points** — use a card instead
- ❌ **Table / matrix with > 20 rows visible at once** — add filter or drillthrough

### Color
- ❌ **Default Power BI blue theme** — every report must apply a named theme
- ❌ **Rainbow palettes** (> 5 distinct hues in one visual)
- ❌ **Red + green as the sole differentiator** — add pattern / icon / label for colorblind users
- ❌ **Hard-coded hex colors in visual.json** — must reference the theme's `data0…dataN` tokens
- ❌ **Contrast ratio < 4.5:1** on any text

### Typography
- ❌ **More than 2 font families** in one report
- ❌ **Axis labels < 10px** or **titles < 18px**
- ❌ **All-caps text > 5 words** (readability)

### Layout
- ❌ **Visuals overlapping** (unless intentional Z-order, documented)
- ❌ **Arbitrary x/y coordinates** — must snap to 8px grid
- ❌ **Inconsistent card heights in a KPI row** — all cards same height, same width

### Titles & labels
- ❌ **"Sum of <Column>"** auto-titles — always rename
- ❌ **Field names as visual titles** — titles must be Big-Idea phrasing ("Revenue leaders outperform by 40%")
- ❌ **Page names like "Page 1" / "Copy of Overview"**

### Navigation
- ❌ **Drillthrough page without a back button**
- ❌ **Bookmark without a Display Name**
- ❌ **Button action pointing to a deleted page**

### Accessibility
- ❌ **Missing alt text** on any visual
- ❌ **No tab order** defined for the page
- ❌ **Color-only semantics** without secondary cue (icon, pattern, label)

---

## 2. Canvas & Grid Rules

### Supported canvas sizes

| Canvas | Dimensions | When |
|---|---|---|
| Standard desktop | 1664 × 936 | Default for all new reports |
| 16:9 classic | 1280 × 720 | Legacy compatibility |
| Letter (portrait) | 816 × 1056 | Paginated-style reports |
| Tooltip | 320 × 240 | Hover tooltip pages (always this size) |
| Mobile (portrait) | 414 × 736 | `mobileState.json` only |

### Grid discipline
- **8px snap grid** — every `x`, `y`, `width`, `height` is a multiple of 8
- **Safe zone** — 16px margin on all four canvas edges (no visual touches the edge)
- **Gutter** — 16px between visuals (Executive style), 8px (Analytical / Operational)
- **KPI row** — all cards same height (120px standard); widths equal or follow a 2:1 / 3:1 rhythm

### Standard slot heights

| Slot | Height (1664×936) | Notes |
|---|---|---|
| Page title bar | 56 | Title + subtitle |
| KPI banner row | 120 | 4-6 cards |
| Hero visual | 320-400 | Single lead visual |
| Supporting grid (3 cols) | 380 | Three 555-wide visuals |
| Supporting grid (2 cols) | 380 | Two 824-wide visuals |
| Navigation bar | 48 | Top or left |

---

## 3. Color Rules

### 60 / 30 / 10 rule
- **60%** neutral (backgrounds, most text) — whites, light grays, deep navy for dark theme
- **30%** primary (most data) — theme's `data0` / `data1`
- **10%** accent (highlights, call-outs, critical-status indicators) — reserved

### Contrast minimums
- **4.5:1** for body text (WCAG AA)
- **3:1** for large text (≥ 18pt)
- **3:1** for non-text elements that convey meaning (icons, thin-line graphics)

### Semantic color
- Don't use color alone — pair with icon, label, or pattern
- Reserve red strictly for negative / critical
- Reserve green strictly for positive / on-target
- Amber for warning / off-target

### Theme tokens (always use these)
- `foreground` — primary text
- `background` — page background
- `data0…dataN` — series colors
- `good` / `bad` / `neutral` / `maximum` / `center` / `minimum` — semantic colors

No `"color": "#RRGGBB"` literal in any visual.json unless the Design Spec explicitly justifies it.

---

## 4. Typography Scale

| Element | Family | Size | Weight |
|---|---|---|---|
| Page title | Segoe UI | 24 | Semibold |
| Page subtitle | Segoe UI | 14 | Regular |
| Visual title | Segoe UI | 14 | Semibold |
| Visual subtitle | Segoe UI | 11 | Regular |
| Axis label | Segoe UI | 10 | Regular |
| Data label | Segoe UI | 12 | Semibold |
| Card value (KPI) | Segoe UI | 32 | Semibold |
| Card label | Segoe UI | 11 | Regular |
| Button text | Segoe UI | 12 | Semibold |
| Tooltip | Segoe UI | 11 | Regular |

**One font family per report.** Segoe UI default unless brand dictates otherwise.

---

## 5. Accessibility Checklist

Every page must pass:
- [ ] Every visual has alt text (set via `visualContainer.visual.objects.general.altText`)
- [ ] Tab order defined (not default top-to-bottom)
- [ ] Text contrast ≥ 4.5:1
- [ ] Color pairs with icon/pattern for meaning
- [ ] Line charts use markers (not color alone)
- [ ] Data labels visible where space permits

---

## 6. Performance Budget

| Metric | Max |
|---|---|
| Visuals per page (excluding slicers) | 8 (Analytical) / 12 (Operational) / 4 (Executive) |
| Slicers per page | 6 |
| Total visuals per report | 60 |
| Custom visuals per report | 4 |
| Image assets in Report/StaticResources | 20 |
| Theme file size | 500 KB |

---

## 7. PBIR Feature Compatibility

PBIR (the new JSON report format) supports features PBIX does not, and vice versa. Respect:
- **PBIR required for:** report-level measures (`reportExtensions.json`), granular source control, JSON generation
- **PBIX / Desktop required for:** some legacy visuals, interactive authoring for non-standard configs
- **Always generate PBIR** unless the project manifest says otherwise
- Target PBIR schema version 4.0 or latest

---

## 8. Referenced By

This file is read at the start of:
- `strategist.md` (Phase 4a)
- `executor-base.md` (Phase 4b)
- `polisher.md` (Phase 4c)
- `design_quality_check.py` (Phase 4c automated linter)

If you edit this file, re-run the design-QA script across all reports to flag newly-introduced violations.
