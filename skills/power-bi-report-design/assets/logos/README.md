# Industry Logos

Brand-neutral placeholder logos for common verticals. Used by the Executor when
a project hasn't yet supplied the customer's actual brand mark, and by demo
reports bundled with this skill.

## Files

24 industries × 1 combined-mark SVG each (viewBox `0 0 160 48`).

| Industry | File | Glyph | Suggested layouts |
|---|---|---|---|
| Sales | [logo-sales.svg](logo-sales.svg) | trend-arrow + bars | exec-overview, sales-performance, scorecard |
| Finance | [logo-finance.svg](logo-finance.svg) | coin with dollar | finance-pnl-waterfall, scorecard |
| Healthcare | [logo-healthcare.svg](logo-healthcare.svg) | medical cross tile | ops-single-screen, customer-360 |
| Manufacturing | [logo-manufacturing.svg](logo-manufacturing.svg) | gear with hub | mfg-line-status, ops-single-screen |
| Retail | [logo-retail.svg](logo-retail.svg) | storefront with awning | sales-performance, geo-territory-map |
| Logistics | [logo-logistics.svg](logo-logistics.svg) | delivery truck | ops-single-screen, geo-territory-map |
| Marketing | [logo-marketing.svg](logo-marketing.svg) | megaphone with waves | marketing-funnel |
| HR / People | [logo-hr.svg](logo-hr.svg) | two silhouettes | scorecard, drillthrough-detail |
| Technology | [logo-technology.svg](logo-technology.svg) | circuit chip | ops-single-screen, scorecard |
| Energy / Utilities | [logo-energy.svg](logo-energy.svg) | lightning bolt | mfg-line-status, ops-single-screen |
| Education | [logo-education.svg](logo-education.svg) | graduation cap | exec-overview, scorecard |
| Hospitality | [logo-hospitality.svg](logo-hospitality.svg) | cup with steam | sales-performance, geo-territory-map |
| Automotive | [logo-automotive.svg](logo-automotive.svg) | car silhouette | sales-performance, mfg-line-status |
| Pharma / Life Sciences | [logo-pharma.svg](logo-pharma.svg) | pill capsule | scorecard, customer-360 |
| Telecom | [logo-telecom.svg](logo-telecom.svg) | antenna with signal | ops-single-screen, geo-territory-map |
| Real Estate | [logo-real-estate.svg](logo-real-estate.svg) | house with roof | sales-performance, geo-territory-map |
| Construction | [logo-construction.svg](logo-construction.svg) | hard hat | ops-single-screen, mfg-line-status |
| Food & Beverage | [logo-food-beverage.svg](logo-food-beverage.svg) | leaf + fork | sales-performance, scorecard |
| Media / Streaming | [logo-media.svg](logo-media.svg) | play tile | exec-overview, marketing-funnel |
| Government / Public Sector | [logo-government.svg](logo-government.svg) | classical building | exec-overview, drillthrough-detail |
| Insurance | [logo-insurance.svg](logo-insurance.svg) | shield with check | scorecard, drillthrough-detail |
| Agriculture | [logo-agriculture.svg](logo-agriculture.svg) | wheat stalk | geo-territory-map, scorecard |
| Aviation / Aerospace | [logo-aviation.svg](logo-aviation.svg) | airplane | ops-single-screen, geo-territory-map |
| E-commerce | [logo-ecommerce.svg](logo-ecommerce.svg) | shopping bag | marketing-funnel, customer-360 |

## Anatomy

Every file is a **combined mark** with two zones packed into one 160×48 SVG:

```
┌──────────────┬───────────────────────────────────┐
│              │  ACME Sales                       │  <- wordmark (14pt bold)
│   [GLYPH]    │  · SALES · REVENUE                │  <- tag (8pt, letter-spaced)
│              │                                   │
└──────────────┴───────────────────────────────────┘
     48x48                    108x48
     badge_crop              wordmark zone
```

- **Badge region `[0,0]-[48,48]`** is a rounded square filled with `currentColor`
  (88% opacity) and a white glyph. Crop to this region for a monogram mark on
  mobile / compact headers.
- **Wordmark region `[48,0]-[160,48]`** uses `currentColor` text — replace the
  `<text>` elements with the customer's real company name at hand-off.

## Rules

1. **Recolor via theme** — all non-glyph strokes/fills are `currentColor`; set
   CSS `color:` or PBIR theme accent to recolor the badge.
2. **Glyph is white on filled badge** for contrast; if you invert the badge
   (transparent bg), edit the `<g>` glyph attributes to use `currentColor`.
3. **No real trademarks.** These are synthetic placeholder marks. Do NOT ship
   a report to a customer still showing "ACME" — the Strategist must flag this
   in the Design Spec and the Executor must swap in the real brand asset.
4. **Mobile use:** crop to the 48×48 badge (use `logos-index.json` →
   `badge_crop`). The full 160×48 wordmark doesn't fit the 390px mobile
   portrait header.

## Index + validation

- `logos-index.json` — catalog (24 entries).
- `logos-index.schema.json` — JSON Schema Draft 2020-12.
- All SVGs are XML-valid and use only `currentColor` / white inks.

## How the Executor uses these

1. Strategist's page spec says: `logo_slot: {industry: "finance", position: "title-bar-left"}`.
2. Executor reads `logos-index.json`, matches `industry == "finance"`, reads the
   file, embeds it in the PBIR page at the coordinates from the layout's
   `**Logo:**` bullet (see `../../references/layouts/<layout-id>.md`).
3. At customer hand-off the placeholder `<text>` is replaced with the real
   company name (Polisher step) — the glyph may stay if it fits the industry,
   or be swapped with the customer's supplied brand mark.

## Adding a new industry

1. Draft a 24×24 glyph using white strokes on a transparent background.
2. Add a generator function + catalog tuple, regenerate, validate XML.
3. Append an entry to `logos-index.json` (must pass schema).
4. Add a row to the table above.
