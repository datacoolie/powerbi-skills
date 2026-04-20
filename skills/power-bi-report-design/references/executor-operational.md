# Role: Executor — Operational Style Personality

> **Inherits from [`executor-base.md`](executor-base.md).** Read that first; this file overrides density, font sizes, and status encoding only.

---

## When this personality applies

- **Audience:** Shop-floor supervisors, ops center, call-center monitors, logistics dispatchers
- **Reading context:** Always-on wall displays or large monitors; at-a-glance scan
- **Goal:** Know status right now; identify what needs intervention
- **STYLE brief answer:** "wall display", "ops center", "monitoring screen", "control room"

---

## Density — the deliberate exception

Operational style **intentionally breaks** the ≤ 8 visuals rule. An ops dashboard is a **status board**, not a narrative.

| Element | Operational rule |
|---|---|
| Visuals per page (excl. slicers) | **8-12** (up to 16 on ultra-wide canvas) |
| Slicers per page | **1-2 max** (usually zero — no human is filtering live) |
| KPI cards | 6-12, often multi-row |
| Pages per report | **1-3** (usually one primary screen) |
| Refresh cadence | Near real-time (DirectQuery or frequent import refresh) |

---

## Status encoding (the core discipline)

Every visual answers "is this OK, warning, or critical?" via:

1. **Traffic-light color** — but never color alone
2. **Icon** — ✓ / ⚠ / ✕ paired with color
3. **Label** — "On target" / "Watch" / "Action required"
4. **Threshold** — explicit numeric boundary shown on the visual

Semantic token mapping:
- `good` → green, ✓ icon, "On target"
- `neutral` → gray, – icon, "No data" / "Paused"
- `bad` → red, ✕ icon, "Action required"
- Amber (via `minimum` or custom token) → warning

---

## Page structure (typical)

```
┌─────────────────────────────────────────────────────────────┐
│ Site status + last refresh timestamp             (56 h)    │
├─────────────────────────────────────────────────────────────┤
│ [KPI][KPI][KPI][KPI][KPI][KPI]                  (120 h)    │
│ [KPI][KPI][KPI][KPI][KPI][KPI]                  (120 h)    │
├─────────────────────────────────────────────────────────────┤
│ [Line 1 status] [Line 2 status] [Line 3 status] (220 h)    │
├─────────────────────────────────────────────────────────────┤
│ [Alert feed / exceptions table]                 (300 h)    │
└─────────────────────────────────────────────────────────────┘
```

Or — for call-center / logistics — replace "Line N status" row with geographic / queue-depth visuals.

---

## Font sizes (larger than other styles)

Ops screens are read from **2-5 meters away**.

| Element | Operational size | (vs standard) |
|---|---|---|
| Page title | 32pt | (24pt) |
| KPI card value | 48pt | (32pt) |
| KPI card label | 14pt | (11pt) |
| Visual title | 16pt | (14pt) |
| Axis label | 12pt | (10pt) |
| Data label | 14pt | (12pt) |

---

## Essential elements

### Multi-row KPI grid
- 6-12 cards, arranged in a grid that fills the top third of the screen
- Each card encodes status via background color or border color
- All cards equal size (uniformity aids scan)

### Target / threshold visuals
- Linear gauges or bullet charts for target attainment
- Donut progress (0-100%) acceptable here *(exception to the general pie-chart ban, justified)*

### Exception feed
- Table or matrix of current exceptions / alerts
- Sorted by severity, then recency
- Red row background for critical alerts

### Refresh timestamp
- **Always visible** (top-right or bottom-right)
- Textbox bound to `[Last Refresh Time]` measure
- Red flag if refresh > N minutes old

---

## Color discipline

- High-contrast palette (ops screens combat glare)
- Dark background often preferred for 24/7 screens (reduces burn-in)
- Saturated red/amber/green for status — these are semantic, not decorative
- Reserve 1-2 hues for non-status accents only

---

## Interaction

Ops screens are **mostly non-interactive**:
- No drillthrough (operator can't click)
- No bookmarks
- Cross-filter **disabled** on most pairs (one slicer click shouldn't scramble the status board)
- Tooltip pages optional

If the screen is hybrid (operator supervises, occasionally investigates):
- Allow click-to-drillthrough on the exception feed only

---

## Whitespace

- **Minimal** — the whole screen is working real estate
- Gutter 8px between visuals
- Safe zone 8-16px
- KPI cards touch (or have 4px gutter) for a seamless grid

---

## Titles & subtitles

- **Title:** short, noun-phrase, no Big-Idea
  - "Line 3 — utilization"
  - "North warehouse — queue depth"
- **Subtitle:** optional; used only for threshold / unit
  - "Target: 85%" / "Tickets"

---

## What NOT to do in Operational style

- ❌ Narrative page titles (save them for Executive style)
- ❌ Complex trend charts with 5+ series — ops is about now, not history
- ❌ Heavy annotations
- ❌ Custom visuals that are slow to render — ops needs sub-1s load
- ❌ Tooltips with bloated content
- ❌ Multi-page navigation requiring clicks — single-page preferred

---

## Special considerations

### DirectQuery / frequent refresh
- Design measures carefully — avoid iterators over large fact tables
- Consider aggregations table for the most-used metrics
- Polisher should flag any visual that relies on slow DAX

### Screen size & resolution
- Confirm in Design Spec §2 the actual screen resolution (1920×1080 vs 3840×2160)
- Canvas may need to be 1920×1080 with custom size, not standard 1664×936
- Test at true resolution before sign-off

---

## Checklist before Polisher

- [ ] Every status visual pairs color with icon + label
- [ ] KPI values are ≥ 32pt (48pt preferred)
- [ ] Refresh timestamp is visible on screen
- [ ] Cross-filter behavior disabled where appropriate (preserves status)
- [ ] Exception feed present (or explicit justification why not)
- [ ] Single-page design (or ≤ 3 pages) — avoid navigation where possible
