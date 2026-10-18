# Layout: Aging Bucket Page

> **Preview:** [![aging-bucket-page preview](../../assets/layout-previews/aging-bucket-page.svg)](../../assets/layout-previews/aging-bucket-page.svg) · variants: [annotated](../../assets/layout-previews/aging-bucket-page-annotated.svg) · [dark](../../assets/layout-previews/aging-bucket-page-dark.svg)

- **id:** `aging-bucket-page`
- **Canvas:** 1920 × 1080
- **Style personality:** Analytical — Stacked bars segmented by aging buckets (0–30 / 31–60 / 61–90 / 90+) + overdue KPI + detail table
- **Audience:** AR / credit controllers, inventory managers — anyone reviewing 'how old is this exposure'
- **Visual count:** 10 — reflow-enhanced (was 8)
- **Pairs with themes:** neutral body with one accent — pattern designed to read on any corporate palette.
- **Observed in:** `references-pbip/Sales Analysis - IMP Demo.Report/` — 'AGING STOCK' and 'ACCOUNT RECEIVABLE' (29 visuals)

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Header + period + entity slicer                                │ 80
├────────────────────────────────────────────────────────────────┤
│ KPI card row · Total outstanding · Overdue% · Avg days · Risk  │ 128
├────────────────────────────────────┬───────────────────────────┤
│                                    │                           │
│ BUCKET BARS (stacked by age)       │  Bucket donut (% of total)│ 464
│  rows = entity, bars = amount       │                          │
│  segmented by 0-30/31-60/61-90/90+  │                          │
│                                    │                           │
├────────────────────────────────────┴───────────────────────────┤
│ Detail table: entity · total · per-bucket · days overdue       │ 312
└────────────────────────────────────────────────────────────────┘
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Header | 0 | 0 | 1920 | 80 | shape + textbox + slicer(Period) + slicer(Entity) | Title and filters |
| KPI card 1 · Total outstanding | 24 | 104 | 456 | 128 | card | Amount + YoY delta |
| KPI card 2 · Overdue % | 496 | 104 | 456 | 128 | card | % of outstanding aged > 30d |
| KPI card 3 · Avg days overdue | 968 | 104 | 456 | 128 | card | Weighted avg days |
| KPI card 4 · Risk score | 1440 | 104 | 456 | 128 | card | Composite indicator |
| Bucket bars | 24 | 256 | 1360 | 464 | stackedBarChart (category = entity; series = bucket) | Top-N entities by total outstanding |
| Bucket donut | 1400 | 256 | 496 | 464 | donutChart (category = bucket) | % mix by age bucket |
| Detail table | 24 | 744 | 1872 | 312 | tableEx | Entity · Total · <30 · 31-60 · 61-90 · 90+ · Days |

Gutters: 24px between primary zones (header / KPI row / charts / table); 16px between neighbouring cards and between bars and donut.

---

## Navigation

- Reachable from the report's top-nav chiclet strip or landing page. Include a small 'Home' actionButton in the header when not the landing page.
- Cross-links out to related drillthrough / detail pages should be surfaced via card-level actions, not a separate nav rail.

---

## Theme + iconography guidance

- **Palette:** Four-bucket sequential ramp (light→dark) with the 90+ bucket in a warning accent. Rest neutral.
- **Logo:** Header top-left at (24, 28) max height 24px.
- **Icons:** Clock glyph next to each aging-related card title.
- **Fonts:** KPI value 22pt, bar labels 9pt, table 10pt.

---

## When NOT to use this layout

- ❌ Question is about *current* balance only, not aging — use `scorecard-kpi-grid`
- ❌ < 3 aging buckets — stacked bars give no advantage
- ❌ Data is anonymized / no entity dimension — collapse to a single donut

---

## Customization allowed

- Replace donut with a trend of overdue% over time if trend is important
- Add a forecast card (expected collection / writeoff)
- FHD headroom (optional): none — the base slots tile the full FHD canvas and the v0.6 reflow below already spends the freed width on two extra slots (watchlist + forecast, 9 visuals in total, under the Analytical budget of 12); a further slot would crowd the bars

## Customization NOT allowed

- Changing bucket boundaries between pages of the same report (breaks comparison)
- Colouring all buckets the same (defeats the whole purpose)

---

## Reflow additions (v0.6)

The donut summarises the age mix but collectors need **risk watchlist** (entities with >90d exposure accelerating) and **expected-collection forecast** (next-30-day cash in). Both are the natural 'so what' follow-ups to the aging view.

### Integration

Shrink **Bucket donut** from `w=496` to `w=320` (still legible; labels may move to a legend below). Watchlist mini-list fits at `x=1736, y=256, w=160, h=464`. Expected-collection forecast card replaces the right-most KPI slot — shrink KPI 4 from `w=456` to `w=280`, add forecast card at `x=1736, y=104, w=160, h=128`.

### New slots

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Risk watchlist mini-list | 1736 | 256 | 160 | 464 | tableEx (compact) | Top 6 entities with 90+ bucket accelerating; single-column rank |
| Expected-collection card | 1736 | 104 | 160 | 128 | card | Next-30d forecasted collection amount + confidence % |

