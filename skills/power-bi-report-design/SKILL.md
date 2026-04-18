---
name: power-bi-report-design
description: >-
  Design Power BI report layouts, select chart types, plan page structures, choose themes,
  and apply data storytelling principles BEFORE generating PBIR JSON files.
  Use this skill whenever the user asks to design a report, plan a dashboard layout,
  choose visualizations, decide on chart types, apply storytelling to data, select a theme
  or color palette, plan page navigation, or structure report pages for a Power BI project.
  Also use when the user provides requirements and needs a report design spec before generation,
  or when reviewing/improving an existing report's visual design, layout, or UX.
  This skill produces a Design Spec — a structured plan of pages, visuals, layout, theme,
  and navigation — that feeds into the `power-bi-pbip-report` skill for JSON generation.
  Do NOT use for generating PBIR JSON files, validating report structure, or building the
  semantic model. For JSON generation, use `power-bi-pbip-report`.
---

# Power BI Report Design

Plan and design Power BI reports before generating PBIR files. This skill transforms
business requirements and a semantic model into a structured **Design Spec** that the
`power-bi-pbip-report` skill consumes to produce the actual `.Report/` folder.

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
the latest visualization guidance before recommending chart types or patterns.

## Reference Files

### Role files (phase-driven workflow)

These role files correspond to the `power-bi-developer` agent's design phases. Load the
one matching the current phase.

| Role File | Used In | Purpose |
|---|---|---|
| `references/strategist.md` | Phase 4a | 5-question intake, style selection, layout/chart picks, produces the Design Spec |
| `references/executor-base.md` | Phase 4b | Shared two-pass (Layout → Narrative) rules inherited by all executors |
| `references/executor-executive.md` | Phase 4b | Executive personality — ≤4 visuals, Big-Idea titles, high whitespace |
| `references/executor-analytical.md` | Phase 4b | Analytical personality — 5-8 visuals, KPI + hero + 3-col grid, direct labels |
| `references/executor-operational.md` | Phase 4b | Operational personality — 8-12 visuals, traffic-light status, large fonts |
| `references/polisher.md` | Phase 4c | Drives `finalize_pbir.py` + `design_quality_check.py`, Design Spec reconciliation |

### Shared standards & templates

| Reference | When to Read |
|---|---|
| `references/shared-standards.md` | **Non-negotiable PBIR design rules** — banned patterns, grid, typography scale, color 60/30/10, accessibility, performance budgets. All roles must load this. |
| `references/design-spec-reference.md` | 11-section Design Spec contract template + Seven Confirmations sign-off table |
| `references/layouts/layouts-index.json` | Index of starter page layouts (slot coordinates, style tags) |
| `references/layouts/*.md` | Individual layout recipes (exec-overview-16x9, sales-performance, drillthrough-detail, …) |
| `references/chart-templates/chart-templates-index.json` | Index of chart recipes (composition + slots + gotchas) |
| `references/chart-templates/*.md` | Individual chart recipes (kpi-banner, bar-comparison, trend-line, yoy-variance, waterfall-bridge, …) |
| `assets/icons/` | SVG icon library (Tabler / Lucide / custom sets). Strategist binds a **set** in Seven Confirmations item #6. |
| `assets/images/` | Raster artwork — backgrounds, banners, dividers, demo logos. |
| `assets/layout-previews/` | PNG thumbnails (1 per layout) used in Seven Confirmations item #2 |
| `assets/chart-previews/` | SVG/PNG thumbnails (1 per chart recipe) used in Design Spec §5 |

### Legacy / cross-skill references

| Reference | When to Read |
|---|---|
| `references/chart-selection-guide.md` | Deciding WHICH chart type to use — decision matrix, hard rules (why bar beats pie) |
| `references/visual-vocabulary.md` | **Intent-first** catalog: 9 data-relationship categories × ~70 charts (FT Visual Vocabulary / Gramener edition) mapped to Power BI `visualType`s |
| `references/visual-design-principles.md` | Pre-attentive attributes, Gestalt principles, color theory, typography, narrative structure, Kirk's 5-layer design process, **accessibility design** (alt text, tab order, markers, contrast, checklist) |
| `references/page-layout-templates.md` | Starting layouts: Overview, Detail, Drillthrough, Tooltip, Grid, Sidebar, Scorecard, Tab-Nav |
| `references/domain-report-structures.md` | Industry page sets: Sales, Manufacturing, Financial, Supply Chain, Retail, Healthcare, Technology |
| `references/theme-colors.md` | Theme architecture, semantic colors, industry palettes, custom theme JSON patterns, colorblind-safe alternatives |
| `../power-bi-pbip-report/references/common-patterns.md` | Reusable components: KPI rows, slicer panels, background shapes, page navigator, visual interactions, TOP N chart (shared with pbip-report) |
| `references/navigation-patterns.md` | Navigation buttons, bookmark tabs, back button, reset filters, hub-and-spoke, breadcrumbs, page navigator |
| `../power-bi-pbip-report/references/mobile-layout.md` | Mobile design rules, auto-create, minimum visual sizes, formatting, slicer behavior, limitations |
| `../power-bi-pbip-report/references/themes/*.json` | Ready-to-use custom theme files (8 industries) — canonical source |

## Design Workflow

### Step 1: Understand the Audience and Purpose

Before choosing any chart, answer these questions (from Knaflic's "Storytelling with Data"):

```
Pre-Design Questions:
□ WHO is the audience? (Executive, Analyst, Operational user)
□ WHAT decisions will this report support?
□ What is the BIG IDEA — one sentence that captures the main insight?
□ What ACTION should the audience take after seeing this report?
```

Read `references/visual-design-principles.md` → Audience Design Guide for audience-specific
density, interaction, and update frequency guidance.

### Step 2: Plan Page Structure

Determine the pages needed. Every report starts with an Overview page.

```
Page Planning Template:
| Page | Type | Purpose | Key Visuals |
|------|------|---------|-------------|
| Overview | Normal | Landing — headline KPIs + top trends | KPI cards, hero trend line, Top-N bar |
| [Domain] Analysis | Normal | Deep dive into [domain] | Breakdown charts, matrix |
| [Entity] Detail | Drillthrough | Single-entity detail | Cards, table, mini trend |
| [Entity] Tooltip | Tooltip | Hover context | 2-3 compact visuals |
```

For industry-specific page sets, read `references/domain-report-structures.md`.
For layout starting points, read `references/page-layout-templates.md`.

### Step 3: Select Chart Types

Start from the **analytical task**, not from a chart name. Read
`references/chart-selection-guide.md` for the full decision matrix.

Quick decision tree:

```
What is the analytical task?
├── Compare categories     → Horizontal bar chart (sorted desc)
├── Show trend over time   → Line chart
├── Show parts of whole    → Stacked bar or treemap
├── Show distribution      → Histogram or box plot
├── Show correlation       → Scatter chart
├── Show geographic data   → Filled map or Azure map
├── Show flow / pipeline   → Funnel, Sankey (custom visual)
├── Show ranking changes   → Ribbon chart
└── Show single KPI value  → Card or KPI visual
```

**Hard rules:**
- Bar charts beat pie charts for comparison (human eye reads length > angle)
- Line charts require a continuous axis (time or sequential numeric)
- Limit pie/donut to ≤ 5 slices (merge the rest into "Other")
- Maximum 6-8 non-slicer visuals per page (more causes performance and cognitive overload)
- Dual-axis charts only when the two series are genuinely related and need different scales

### Step 4: Design Layout and Positioning

Follow Kirk's 5-layer design process (read `references/visual-design-principles.md`):

1. **Data Representation** — Choose the encoding (Layer 1 = chart types from Step 3)
2. **Interactivity** — Decide slicers, drillthrough, cross-filtering, bookmarks
3. **Annotation** — Titles, subtitles, direct labels, reference lines, callouts
4. **Color** — Start gray, add ONE accent for the insight, then category/magnitude hues
5. **Composition** — Z-pattern flow, KPIs at top, hero visual below, filters at left/top

Layout rules:
- **Z-pattern reading flow**: top-left (headline) → top-right → bottom-left → bottom-right
  — Best for **executive dashboards** and overview pages with distinct visual blocks
- **F-pattern reading flow**: top (full-width header) → left column scan → selective right reads
  — Best for **text-heavy analytical pages**, tables/matrices, and detail pages where users scan
  down the left side for labels then read right for values
- **KPI row** at the top: 3-6 card visuals showing the most important numbers
- **Hero visual** immediately below the KPI row: the largest chart on the page
- **Supporting visuals** fill the remaining space in a balanced grid
- **Slicers**: left sidebar (vertical) or top strip (horizontal)
- **White space**: separate logical groups using proximity (Gestalt principle)

**Data-Ink Ratio** (Tufte principle): Maximize the share of ink devoted to data.
- Remove chart borders, gridlines, and axis lines that don't aid comprehension
- Use direct labels instead of legends when ≤ 5 series
- Remove unnecessary background fills (set to transparent)
- Hide field headers on slicers when the title is sufficient

Canvas: **1664 × 936** (standard). Tooltip pages: **320 × 240**.

**Mobile Design Decision:**
- **Design mobile layout** when ≥ 30% of audience uses phone/tablet (ask stakeholders)
- **Desktop-only** is acceptable for internal analyst reports viewed on desktops
- For mobile: prioritize KPI cards + 1-2 key visuals per page; hide complex matrices
- See `../power-bi-pbip-report/references/mobile-layout.md` for generation details

### Step 5: Choose Theme and Colors

Read `references/theme-colors.md` for the full theme architecture.

Decision process:
1. Check if the client has brand colors → build a custom theme
2. If no brand → pick an industry-appropriate theme from `references/themes/`
3. Ensure accessible contrast (4.5:1 minimum for text)
4. Test with colorblind simulation (avoid red/green as the only differentiator)

Available industry themes:
| Theme File | Industry |
|---|---|
| `themes/sales-revenue.json` | Sales & Revenue |
| `themes/manufacturing-operations.json` | Manufacturing & Operations |
| `themes/corporate-financial.json` | Corporate / Financial |
| `themes/supply-chain-logistics.json` | Supply Chain & Logistics |
| `themes/retail-consumer.json` | Retail / Consumer |
| `themes/healthcare-pharma.json` | Healthcare & Pharma |
| `themes/sustainability-esg.json` | Sustainability / ESG |
| `themes/technology-it.json` | Technology / IT |

### Step 6: Plan Navigation

Choose a navigation pattern based on report complexity:

| Report Size | Navigation Pattern | Reference |
|---|---|---|
| 1-3 pages | No explicit navigation — default tab strip | — |
| 4-8 pages | Page navigator visual or button bar | `references/navigation-patterns.md` |
| 9+ pages | Bookmark-based tab groups + landing page | `references/navigation-patterns.md` |

Also decide:
- Which pages need **drillthrough** (detail pages accessed from summary visuals)
- Which visuals need **report page tooltips** (hover cards for extra context)
- Whether **reset filters** button is needed (recommended for 3+ slicers)
- Whether **back button** is needed on drillthrough pages (always yes)

### Step 7: Produce the Design Spec

Compile all decisions into a structured Design Spec. This is the handoff artifact
for the `power-bi-pbip-report` skill.

```
Design Spec Structure:
═══════════════════════════════════════════
REPORT DESIGN SPEC: [Report Name]
═══════════════════════════════════════════

## Audience & Purpose
- Primary audience: [role]
- Key decisions supported: [list]
- Big Idea: [one sentence]

## Theme
- Theme file: [path or "custom"]
- Brand colors: [hex codes if custom]

## Pages
### Page 1: [page-name] (Overview)
- Layout template: [from page-layout-templates.md]
- Visuals:
  | Visual Name | Type | Data (Table.Column/Measure) | Position |
  |-------------|------|----------------------------|----------|
  | card-kpi-revenue | card | _Measures.Total Revenue | top-left |
  | lineChart-monthly-trend | lineChart | DimDate.Month, _Measures.Total Revenue | center |
  | ... | ... | ... | ... |
- Slicers: [date range, category, ...]
- Interactions: [cross-filter / cross-highlight rules]

### Page 2: [page-name] (Detail)
[same structure]

### Page N: [page-name] (Drillthrough)
- Drillthrough field: [Table.Column]
[same structure]

## Navigation
- Pattern: [tab strip / page navigator / bookmarks]
- Drillthrough: [list source → target pages]
- Tooltips: [list visual → tooltip page]
- Reset filters: [yes/no]

## Notes
- [any special requirements, constraints, deviations]
═══════════════════════════════════════════
```

The `power-bi-pbip-report` skill uses this spec to generate all PBIR JSON files
without re-making design decisions.

---

## Phase-Driven Workflow (agent-aligned)

The seven-step workflow above is the classic, skill-internal flow. When invoked
from the `power-bi-developer` agent, follow the role-based phase gates instead:

| Agent Phase | Role to load | Output |
|---|---|---|
| 4a Design Strategy | `references/strategist.md` + `shared-standards.md` + layouts/chart-templates indexes | Filled `design-spec-reference.md` |
| 4a.5 Seven Confirmations (Plan-mode Q&A, non-blocking) | *(no role file — `vscode_askQuestions` panel with recommended defaults; single-message summary as fallback)* | Recorded user decision on Canvas / Pages / Audience / Style / Palette / Iconography / Navigation (accepted defaults or inline edits) |
| 4b Generation | `references/executor-base.md` + one of `executor-executive.md` / `executor-analytical.md` / `executor-operational.md` | PBIR files (Pass 1 Layout → Pass 2 Narrative) |
| 4c Polish & Design QA | `references/polisher.md` | `finalize_pbir.py` → `design_quality_check.py` → `validate_report.js` → evidence package |

Phase 4a.5 is a **non-blocking Plan-mode review**: a single `vscode_askQuestions`
call presents the seven decisions with the Strategist's recommended defaults,
and the user can accept the whole panel in one click or via a chat reply of
`"proceed"` / `"go"` / `"looks good"`. Inline edits update only the changed
items; a full redesign loops back to 4a. Do NOT run 4b without a Design Spec,
and every 4b regeneration MUST be followed by 4c.
