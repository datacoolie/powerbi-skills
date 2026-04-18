# Layout: Customer 360

- **id:** `customer-360`
- **Canvas:** 1664 × 936
- **Style personality:** Analytical — dense, diagnostic, comparison-ready
- **Audience:** Account managers, CX analysts, retention teams
- **Visual count:** 9
- **Pairs with themes:** neutral analytical themes; semantic status colors (good/warn/bad)

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Title bar: "Customer 360 — {CustomerName}"                    │ 56
├────────────────────────────────────────────────────────────────┤
│ Profile header (avatar / logo, tier chip, tenure, owner)      │ 96
├────────────────────────────────────────────────────────────────┤
│ ┌──KPI1──┐ ┌──KPI2──┐ ┌──KPI3──┐ ┌──KPI4──┐                   │ 120
│ │ LTV    │ │ NPS    │ │ Churn% │ │ Open $ │                   │
│ └────────┘ └────────┘ └────────┘ └────────┘                   │
├────────────────────────────────────────────────────────────────┤
│ Cohort retention matrix       │ Retention curve               │ 320
│ (months-since-signup × month) │ (overlay: cohort vs all)      │
├────────────────────────────────────────────────────────────────┤
│ Top segments / product mix / recent activity (grid of 3)      │ 220
└────────────────────────────────────────────────────────────────┘ 936
```

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Title bar | 32 | 16 | 1600 | 56 | textbox | 24pt Semibold |
| Profile header | 32 | 80 | 1600 | 96 | card/shape | Avatar 64px + company + tier chip + owner |
| KPI 1–4 | 32/432/832/1232 | 192 | 384/384/384/400 | 120 | card | LTV / NPS / Churn% / Open Pipeline |
| Cohort matrix | 32 | 328 | 792 | 320 | matrix | Color-scale background by retention % |
| Retention curve | 840 | 328 | 792 | 320 | line | Cohort vs. all-customers overlay |
| Segment 1 | 32 | 664 | 520 | 248 | bar / donut | Product mix |
| Segment 2 | 572 | 664 | 520 | 248 | bar | Top categories |
| Segment 3 | 1112 | 664 | 520 | 248 | table | Recent activity |

## Navigation

Typically the **drillthrough target** from a customer hub page. Include Back button at (32, 16, 48, 32) if drillthrough.

## Theme + iconography guidance

- **Palette:** neutral + 1 semantic triad (good/warn/bad)
- **Logo:** **two logos** on this layout. (1) Corporate wordmark top-left of title bar, 24px (small — not the focus). (2) Customer avatar / logo inside the profile-header block at `(48, 80)`, 48px circle — this is the identity anchor for the page.
- **Icons:** tier badge (crown / star / bronze), trend up/down on KPIs
- **Cohort color:** sequential single-hue scale; legend on retention curve

## When NOT to use this layout

- ❌ Account list / search — use a sortable table page
- ❌ Product-centric analysis (flip to `sales-performance` or a product-360 variant)
- ❌ You don't have cohort-capable data — drop cohort matrix, use plain trend
