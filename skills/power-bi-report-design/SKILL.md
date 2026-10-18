---
name: power-bi-report-design
description: >-
  Design Power BI report layouts, select chart types, plan page structures, choose themes, and apply
  data storytelling BEFORE generating PBIR JSON. Produces a Design Spec plus the official canonical
  `Design Brief:` contract (design identity, page archetypes, mechanical layout_contract) that feeds
  `power-bi-report-authoring`. Covers the `design` mode of Microsoft's `powerbi-report-cli` (tone,
  signature, archetype router, chart selection, color, typography, layout, interactivity,
  accessibility, brownfield redesign, pre-flight checklist). Use whenever the user asks to design a
  report, plan a dashboard layout, choose visualizations or chart types, select a theme or palette,
  plan navigation, redesign or critique an existing report, or needs a design spec from requirements.
  Do NOT use to generate PBIR JSON, validate report structure, or build the semantic model
  (use `power-bi-report-authoring` / `power-bi-semantic-model`).
---

# Power BI Report Design

Plan and design Power BI reports before generating PBIR files. This skill transforms
business requirements and a semantic model into a structured **Design Spec** (+ the
canonical **`Design Brief:`** YAML contract) that the
`power-bi-report-authoring` skill consumes to produce the actual `.Report/` folder.
This skill never edits PBIR or calls Fabric APIs.

> **Official source.** `references/design.md` + `references/design/**` mirror the
> `design` mode of [microsoft/skills-for-fabric `powerbi-report-cli`](https://github.com/microsoft/skills-for-fabric)
> (MIT) verbatim; they win on conflict. Mode → skill map: `planning` →
> `power-bi-business-analysis`, `authoring` → `power-bi-report-authoring`,
> `management` → `power-bi-management`.

**Docs lookup.** For the latest Microsoft visualization guidance, search Microsoft
Learn (the `microsoft-learn-mcp` tools — docs have no CLI equivalent, so MCP is the
right tool here) before recommending chart types or patterns.

## Reference Files

### Role files (phase-driven workflow)

These role files correspond to the `power-bi-developer` agent's design phases. Load the
one matching the current phase.

| Role File | Used In | Purpose |
|---|---|---|
| `references/strategist.md` | Phase 4a | 5-question intake, style selection, layout/chart picks, produces the Design Spec |
| `references/executor-base.md` | Phase 4b | Shared two-pass (Layout → Narrative) rules inherited by all executors |
| `references/executor-executive.md` | Phase 4b | Executive personality — ≤6 visuals (3–6 KPIs), Big-Idea titles, high whitespace |
| `references/executor-analytical.md` | Phase 4b | Analytical personality — 8-12 visuals, KPI + hero + 3-col grid, direct labels |
| `references/executor-operational.md` | Phase 4b | Operational personality — 10-14 visuals, traffic-light status, large fonts |
| `references/polisher.md` | Phase 4c | Drives `finalize_pbir.py` + `design_quality_check.py`, Design Spec reconciliation |

### Shared standards & templates

| Reference | When to Read |
|---|---|
| `references/shared-standards.md` | **Non-negotiable PBIR design rules** — banned patterns, grid, typography scale, color 60/30/10, accessibility, performance budgets. All roles must load this. |
| `references/design-spec-reference.md` | 11-section Design Spec contract template + Seven Confirmations sign-off table |
| `references/layouts/layouts-index.json` | Index of starter page layouts (slot coordinates, style tags) — all landscape recipes are FHD 1920×1080 |
| `references/layouts/archetype-map.md` | Maps the official archetypes/variants (Executive A/B/C, Analytical A/B/C, …) to library recipes; lists gaps; FHD space-allocation + visual-budget rules |
| `../power-bi-report-authoring/scripts/build_report_from_layout.py` | Turns an approved recipe + slot spec into PBIR visuals (the Executor's Pass 1 for recipe pages) |
| `scripts/rescale_layout.py` | Rescale a layout's slots to another 16:9 canvas (1280×720, 2560×1440, a brownfield size); `--check` validates a recipe slot table (grid, bounds, overlaps, margins) |
| `references/layouts/*.md` | Individual layout recipes (exec-overview-16x9, sales-performance, drillthrough-detail, …) |
| `references/chart-templates/chart-templates-index.json` | Index of chart recipes (composition + slots + gotchas) |
| `references/chart-templates/*.md` | Individual chart recipes (kpi-banner, bar-comparison, trend-line, yoy-variance, waterfall-bridge, …) |
| `assets/icons/` | SVG icon library (Tabler / Lucide / custom sets). Strategist binds a **set** in Seven Confirmations item #6. |
| `assets/images/` | Raster artwork — backgrounds, banners, dividers, demo logos. |
| `assets/layout-previews/` | SVG thumbnails (1 per layout) used in Seven Confirmations item #2 |
| `assets/chart-previews/` | SVG/PNG thumbnails (1 per chart recipe) used in Design Spec §5 |

### Official design mode (verbatim from Microsoft `powerbi-report-cli`)

`references/design.md` is the official mode guide (workflow Steps 0–7, archetype
router, gotchas, canonical `Design Brief:` contract). Topic files live in
`references/design/`. **Official files win on conflict with repo notes below.**

| Reference | When to Read |
|---|---|
| `references/design.md` | Entry point — workflow, archetype router, design contract, gotchas |
| `references/design/tone-catalog.md` | **Tone catalog** — named tones with typography, palette, density, gridline, border, signature, iconography downstream choices; remixing rules |
| `references/design/signatures.md` | **Signature gallery** — named signatures with tone-coherence matrix; authoring fresh signatures |
| `references/design/archetypes/*.md` | Per-page layout variants: executive-summary, operational-monitor, analytical-canvas, narrative-story, comparative-benchmark |
| `references/design/archetype-composition.md` | Multi-page compositions and cross-page variant rotation |
| `references/design/chart-selection.md` | Encoding hierarchy, purpose → chart matching |
| `references/design/visual-cookbook.md` (+`-part-02`) | Per-visual-type sort/color/label/CF rules; theme-vs-per-visual boundaries |
| `references/design/layout.md`, `color.md`, `typography.md`, `interactivity.md` | Grid/composition, palette & semantics, type scale, drill/bookmark/cross-filter/navigation model |
| `references/design/brownfield.md` | Redesign, restyle, theme swap, brand application of an existing report |
| `references/design/accessibility.md`, `anti-patterns.md`, `pre-flight-checklist.md` | Final audit before hand-off |
| `references/design/design-brief.md` (+`-part-02`) | **Read before hand-off** — `Design Brief:` template, `layout_contract` schema, validation checklist |
| `references/design/assets/base.json` | Base theme with per-type safeguards (textbox/card/table) to adapt for custom themes |

### Repo cross-skill references

| Reference | When to Read |
|---|---| | Deciding WHICH chart type to use — decision matrix, hard rules (why bar beats pie) |
| `references/visual-vocabulary.md` | **Intent-first** catalog: 9 data-relationship categories × ~70 charts (FT Visual Vocabulary / Gramener edition) mapped to Power BI `visualType`s |
| `references/visual-design-principles.md` | Pre-attentive attributes, Gestalt principles, color theory, typography, narrative structure, Kirk's 5-layer design process, **accessibility design** (alt text, tab order, markers, contrast, checklist) |
| `references/page-layout-templates.md` | Starting layouts: Overview, Detail, Drillthrough, Tooltip, Grid, Sidebar, Scorecard, Tab-Nav |
| `references/domain-report-structures.md` | Industry page sets: Sales, Manufacturing, Financial, Supply Chain, Retail, Healthcare, Technology |
| `references/theme-colors.md` | Theme architecture, semantic colors, industry palettes, custom theme JSON patterns, colorblind-safe alternatives |
| `../power-bi-report-authoring/references/common-patterns.md` | Reusable components: KPI rows, slicer panels, background shapes, page navigator, visual interactions, TOP N chart (shared with pbip-report) |
| `references/navigation-patterns.md` | Navigation buttons, bookmark tabs, back button, reset filters, hub-and-spoke, breadcrumbs, page navigator |
| `references/slicer-filter-patterns.md` | **Decision guide** for filter scope, slicer type selection, sync groups, cross-filter vs. highlight, default state, filter-vs-drillthrough, pane visibility, RLS interaction |
| `references/slicer-patterns/` | **Recipe cookbook** — 14 slicer/filter composition recipes (ASCII mockup + slots + property snippet + defaults + anti-patterns) in 7 families: date, category, numeric, search, architecture, governance, parameter. Index: `slicer-patterns/slicer-patterns-index.json` |
| `../power-bi-report-authoring/references/mobile-layout.md` | Mobile design rules, auto-create, minimum visual sizes, formatting, slicer behavior, limitations |
| `../power-bi-report-authoring/references/themes/*.json` | Ready-to-use custom theme files (8 industries) — canonical source |

## Design Workflow (Summary)

The full workflow is driven by the **Strategist** role (`references/strategist.md`).
Each step below links to the detailed reference — load the reference, don't re-derive.

| Step | Action | Primary Reference |
|---|---|---|
| 1. Audience & Purpose | Data-first investigation, five-question intake (WHO, WHAT, BIG IDEA, ACTION, STYLE), tone + signature | `references/strategist.md` Steps 0–2 + `references/visual-design-principles.md` + `references/design/tone-catalog.md` + `references/design/signatures.md` |
| 2. Page Structure | Select pages by domain + page type; route each page to an archetype + variant | `references/domain-report-structures.md` + `references/page-layout-templates.md` + `references/design/archetypes/*.md` + `references/design/archetype-composition.md` |
| 3. Chart Selection | Start from analytical task → pick chart → pick recipe | `references/design/chart-selection.md` + `references/chart-selection-guide.md` + `references/visual-vocabulary.md` + `references/design/visual-cookbook.md` |
| 4. Layout & Positioning | Kirk's 5-layer process; Z/F-pattern; 8-px grid | `references/design/layout.md` + `references/visual-design-principles.md` + `references/layouts/` |
| 5. Theme & Colors | Brand or industry palette; 60/30/10 rule; 4.5:1 contrast | `references/design/color.md` + `references/theme-colors.md` + `references/shared-standards.md` §3 + `references/design/accessibility.md` + `references/design/assets/base.json` |
| 6. Navigation & Filters | Pattern selection + slicer recipe binding | `references/design/interactivity.md` + `references/navigation-patterns.md` + `references/slicer-filter-patterns.md` + `references/slicer-patterns/` |
| 7. Mobile Layout | Auto-create as starting point; refine for touch/single-column | `../power-bi-report-authoring/references/mobile-layout.md` |
| 8. Produce Design Spec + `Design Brief:` | Fill all 11 sections, then emit the canonical `Design Brief:` YAML; run the pre-flight checklist | `references/design-spec-reference.md` + `references/design/design-brief.md` + `references/design/pre-flight-checklist.md` |

> **Hard rules** (no pie>5, no 3D, no rainbow, max visuals/page) are defined
> authoritatively in `references/shared-standards.md` §1. All roles load that file first.
> **Anti-patterns** are cataloged in `references/design/anti-patterns.md` with severity ratings.

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-report-authoring` | Downstream (Phase 4b) | Design Spec is consumed to generate PBIR JSON files |
| `power-bi-dax-development` | Upstream (Phase 3) | Measure catalog provides data bindings for visuals |
| `power-bi-business-analysis` | Upstream (Phase 1) | Page plan, audience, KPIs, and domain from requirements |
| `power-bi-performance-troubleshooting` | Cross-cutting | Report-level optimization (visual count, slicer design, query reduction) |
| `power-bi-feedback-iteration` | Loop-back | Chart/layout redesign feedback routes through this skill |

---

## Phase-Driven Workflow (agent-aligned)

The seven-step workflow above is the classic, skill-internal flow. When invoked
from the `power-bi-developer` agent, follow the role-based phase gates instead:

| Agent Phase | Role to load | Output |
|---|---|---|
| 4a Design Strategy | `references/strategist.md` + `shared-standards.md` + layouts/chart-templates indexes | Filled `design-spec-reference.md` |
| 4a.5 Seven Confirmations (Plan-mode Q&A, non-blocking) | *(no role file — `vscode_askQuestions` panel with recommended defaults; single-message summary as fallback)* | Recorded user decision on Canvas / Pages / Audience / Style / Palette / Iconography / Navigation (accepted defaults or inline edits) |
| 4b Generation | `references/executor-base.md` + one of `executor-executive.md` / `executor-analytical.md` / `executor-operational.md` | PBIR files (Pass 1 Layout → Pass 2 Narrative) |
| 4c Polish & Design QA | `references/polisher.md` | `finalize_pbir.py` → `design_quality_check.py` → `validate_report.py` → evidence package |

Phase 4a.5 is a **non-blocking Plan-mode review**: a single `vscode_askQuestions`
call presents the seven decisions with the Strategist's recommended defaults,
and the user can accept the whole panel in one click or via a chat reply of
`"proceed"` / `"go"` / `"looks good"`. Inline edits update only the changed
items; a full redesign loops back to 4a. Do NOT run 4b without a Design Spec,
and every 4b regeneration MUST be followed by 4c.
