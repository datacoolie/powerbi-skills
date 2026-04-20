# Recipe: KPI Banner Card

> **Preview:** [![kpi-banner preview](../../assets/chart-previews/kpi-banner.svg)](../../assets/chart-previews/kpi-banner.svg)

- **id:** `kpi-banner`
- **Visual type:** `card` (single value)
- **Typical size:** 320 × 120 (adjust width proportionally for 3-6 cards in a row)

---

## Composition

```
┌──────────────────────────────────┐
│ Label (11pt regular, muted)      │
│                                  │
│ $4.2M              [trend icon]  │  ← value 32pt Semibold
│                                  │
│ +12.4% YoY        [status icon]  │  ← delta 12pt Semibold (good/bad color)
└──────────────────────────────────┘
```

---

## Slots

| Slot | Content | Binding example |
|---|---|---|
| Label | Measure display name | Plain text on visual |
| Value | Primary measure | `[Total Revenue]` |
| Delta | Secondary measure (variance) | `[YoY Revenue %]` |
| Trend icon | Conditional format | `[YoY Direction]` → up/down/flat |
| Status icon | Threshold indicator | `[Revenue vs Plan Status]` → good/warn/bad |

---

## Formatting (theme-aware)

- **Background:** `background` (neutral) or `background2` (subtle gray)
- **Label color:** `foreground` muted (60% opacity) OR `neutral`
- **Value color:** `foreground`
- **Delta color:** conditional — `good` when positive, `bad` when negative
- **Border:** 1px `secondary` OR none (flat style)

Key visual.json fragments:
- `callout.value.color` → theme token
- `callout.value.font.size` → 32
- `dataLabels.labelPrecision` → 1 (for percent) or 0 (for currency in millions)

---

## Narrative frame by style

| Style | Delta label | Icon heaviness |
|---|---|---|
| Executive | "+12.4% vs. LY" | Always show trend + status |
| Analytical | "+12.4% YoY" | Show trend; status optional |
| Operational | "+12.4%" | Status icon dominant; traffic-light background |

---

## Do-NOT list

- ❌ Stack > 2 pieces of information vertically (value + one delta is max)
- ❌ Use 4-digit precision for money (`$4,234,192` → `$4.2M`)
- ❌ Show the measure's technical name ("Sum of SalesAmount" → "Revenue")
- ❌ Use red/green without icon (colorblind fail)
- ❌ Make cards different heights in the same row

---

## Data quality gotchas

- If measure returns `BLANK()`, card shows blank — not "0". Confirm desired behavior in DAX (Phase 3).
- For percent-based KPIs, check measure returns a number (0.124), not a percent-formatted string.
- Delta measure must handle the no-prior-period case.

---

## Checklist

- [ ] Label uses business terminology, not column name
- [ ] Value formatted with thousands separator + appropriate unit
- [ ] Delta shows vs. what (YoY, vs Plan, vs LW)
- [ ] Trend arrow direction matches sign of delta
- [ ] Status icon threshold documented in Design Spec
- [ ] Card height matches siblings in the row

---

## Card-family decision matrix

Five recipes compete for the "show a KPI" slot. Pick deliberately.

| Recipe | visualType | Best for | Avoid when |
|---|---|---|---|
| [`kpi-banner`](kpi-banner.md) | `card` | Single hero metric; 1 number + 1 delta + icon | Need trend axis / goal line / 3+ facets |
| [`multi-row-card`](multi-row-card.md) | `multiRowCard` | 4–8 related metrics at equal weight | Single hero; trend-per-row matters (→ `sparkline-table`) |
| [`kpi-indicator`](kpi-indicator.md) | `kpi` | Status vs target with trend context on one glyph | Multiple metrics; arbitrary comparison (not a target) |
| [`gauge-target`](gauge-target.md) | `gauge` | Operational board — one bounded metric vs target | Executive dashboards (wastes space); unbounded measures |
| [`bullet-chart`](bullet-chart.md) | `BulletChart...` ★ | IBCS-style dense actual vs target with range bands | No defined target; > 6 bullets in one visual |
| [`advance-card`](advance-card.md) | `advanceCard...` ★ | Rich KPI with conditional colors + icons + multiple rows | Simple single-metric case (`kpi-banner` is lighter) |

**Quick picker:**
- One number? → `kpi-banner`
- 4-8 numbers? → `multi-row-card`
- Status vs target? → `kpi-indicator` (static) or `gauge-target` (operational)
- Dense target + ranges? → `bullet-chart`
- Rich formatting needs? → `advance-card`

