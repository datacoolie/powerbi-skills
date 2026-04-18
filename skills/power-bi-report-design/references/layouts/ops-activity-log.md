# Layout: Ops Activity Log

- **id:** `ops-activity-log`
- **Canvas:** 1664 × 936
- **Style personality:** Operational — audit / troubleshooting
- **Audience:** Ops engineers, data platform owners, on-call responders
- **Visual count:** 9 (tab strip + status banner + trend + status matrix + log table + detail tooltip trigger) — reflow-enhanced (was 6)
- **Pairs with themes:** neutral / light with a single alert accent; dark mode friendly
- **Observed in:** `references-pbip/Monitoring_ADF_DB_v2.Report/` — "PipelineRuns"

---

## Zone map

```
┌────────────────────────────────────────────────────────────────┐ 0
│ Title bar                                                     │ 52
├────────────────────────────────────────────────────────────────┤
│ [Tab1] [Tab2] [Tab3] [Tab4]   (actionButton nav)              │ 52
├────────────────────────────────────────────────────────────────┤
│ STATUS BANNER — multiRowCard (Success / Failed / Running)     │ 94
├──────────────────────────────────┬─────────────────────────────┤
│                                  │                             │
│  Run trend (stacked area)        │  Pipeline × status matrix  │ 312
│                                  │                             │
├──────────────────────────────────┴─────────────────────────────┤
│                                                                │
│  Activity log (sortable table) — newest first                 │ 322
│                                                                │
└────────────────────────────────────────────────────────────────┘ 936
```

---

## Slot specifications

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Title | 31 | 10 | 1040 | 42 | textbox | 20pt Semibold |
| Refresh timestamp | 1300 | 16 | 333 | 31 | textbox | "Last refresh {ts}" right-aligned |
| Tab button 1–4 | 31 / 265 / 499 / 733 | 62 | 218 | 47 | actionButton | Shows selected-state variant |
| Status banner | 31 | 125 | 1602 | 83 | multiRowCard | 3 cells: success count, failed count, running count |
| Run trend (area) | 31 | 229 | 624 | 312 | stackedAreaChart | Hourly / daily stacked by status |
| Pipeline × status matrix | 676 | 229 | 957 | 312 | pivotTable | Rows=pipeline, cols=status, cells=count |
| Activity log table | 31 | 562 | 1602 | 343 | tableEx | Columns: ts, pipeline, trigger, status, duration, actor, id |

Gutters: 16px between trend and matrix, 16px between top row and bottom table. Status banner spans full body width to anchor the page.

---

## Navigation

Tab-strip IS the navigation — each button bookmarks to a sibling page (`PipelineRuns`, `TriggerRuns`, `DatasetExecutions`, `Alerts`). Use the selected-state button variant so users can see which page they're on.

---

## Theme + iconography guidance

- **Palette:** neutral grey base + one alert accent (red for failed). Success / running tint 4–8% opacity on banner cells.
- **Logo:** omit — this is an internal ops page, logo adds chrome without function. If branding is mandated, place at `(24, 8)` max height 24px and narrow title to 936w.
- **Icons:** status glyphs (check / cross / spinner / pause) on banner cells and in log-table `status` column; must match the ones used in the matrix legend.
- **Fonts:** monospace for the `id` column of the log table so hash/UUID values align.

---

## When NOT to use this layout

- ❌ Audience is exec — too dense, no narrative (use an exec `ops-single-screen` instead)
- ❌ No log-level data available — bottom table becomes filler
- ❌ Less than 3 pipelines — matrix is over-kill, collapse to a simple list

---

## Customization allowed

- Swap trend chart for a Gantt-style run duration view if duration matters more than count
- Collapse banner to 2 cells if only success / failed exists (no "running" state)
- Add an additional filter slicer row below the tab strip (pushes status banner to y=144)

## Customization NOT allowed

- Removing the tab strip if the page is part of a navigable log suite (breaks sibling-page wayfinding)
- Dropping the refresh timestamp — ops audiences need dataset freshness visible
- Using more than 1 alert colour (dilutes the failed / red signal)

---

## Reflow additions (v0.6)

The log table takes the full bottom width but responders also need **severity triage** and **top-failing pipelines** without scrolling. Reclaim a 300w right sidebar beside the log for those, plus a dismissible **incident banner** at the top of the body for active P1/P2.

### Integration

Shrink **Activity log table** from `w=1602` to `w=1286`. The sidebar occupies `x=1333–1633`. The incident banner appears only when `alerts > 0` — otherwise the status banner retains its full-width role.

### New slots

| Slot | x | y | w | h | Visual type | Notes |
|---|---|---|---|---|---|---|
| Incident banner | 31 | 115 | 1602 | 38 | shape + textbox + actionButton | Shown only when P1/P2 > 0; "Acknowledge" button right; pushes status banner down 42px |
| Severity triage card | 1333 | 562 | 300 | 160 | multiRowCard | P1 / P2 / P3 counts with trend arrow |
| Top-failing pipelines | 1333 | 735 | 300 | 170 | tableEx (compact) | Top 5 pipelines by failure count (last 24h) |

