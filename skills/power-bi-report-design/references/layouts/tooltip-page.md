# Layout: Tooltip Page (hover detail)

- **id:** `tooltip-page`
- **Canvas:** 320 × 240 (Power BI default tooltip-page canvas)
- **Style personality:** Analytical — ultra-compact, single-context detail
- **Audience:** Any report user hovering over a visual mark
- **Visual count:** 3
- **Pairs with themes:** inherits host page theme; high contrast essential at small size

## Zone map

```
┌────────────────────────────┐ 0
│ Tooltip title (entity name │ 40
│ + secondary label)         │
├────────────────────────────┤
│ ┌──KPI A──┐ ┌──KPI B──┐    │ 80
│ │ value   │ │ value   │    │
│ │ delta   │ │ delta   │    │
│ └─────────┘ └─────────┘    │
├────────────────────────────┤
│                            │
│   Micro chart              │ 100
│   (sparkline or mini bar)  │
│                            │
└────────────────────────────┘ 240
```

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Tooltip title | 8 | 8 | 304 | 40 | textbox | Entity name 14pt Semibold + secondary label 10pt muted |
| KPI A | 8 | 56 | 148 | 72 | card | Big value + delta chip; no sparkline (too small) |
| KPI B | 164 | 56 | 148 | 72 | card | Paired KPI |
| Micro chart | 8 | 136 | 304 | 96 | line or bar | Remove axis labels; keep trend shape only |

## Authoring notes

1. In Power BI Desktop: **Format page** → Canvas settings → Type: **Tooltip** → Size: 320 × 240.
2. Visual on any other page: **Format visual** → Tooltip → Type: **Report page** → Page: this tooltip page.
3. The tooltip page can filter off the hovered mark by including the same fields in its page filters.
4. Keep to 3 visuals max — more causes slow rendering on hover and jittery popovers.

## Theme + iconography guidance

- **Palette**: host-page accent only; no new colors introduced
- **Logo**: **omit** — 320×240 is too small for a brand mark and the tooltip is a transient popover, not a standalone page. The host page already carries the logo.
- **Icons**: avoid — no space; text + numbers only
- **Fonts**: 10pt minimum — anything smaller is unreadable against visual hover-hit
- **Background**: solid fill with thin 1px border — gives a card-like detached feel

## When NOT to use this layout

- ❌ Need a full secondary analysis — route user to a drillthrough page instead
- ❌ Table-style detail — build a `drillthrough-detail` page (tooltip cannot scroll)
- ❌ Cross-entity comparison — tooltip is always single-context by design
