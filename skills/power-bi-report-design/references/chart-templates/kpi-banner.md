# Recipe: KPI Banner Card

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
