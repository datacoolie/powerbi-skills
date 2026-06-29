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
  and navigation — that feeds into the `power-bi-report-authoring` skill for JSON generation.
  Do NOT use for generating PBIR JSON files, validating report structure, or building the
  semantic model. For JSON generation, use `power-bi-report-authoring`.
---

# Power BI Report Design

Plan and design Power BI reports before generating PBIR files. This skill transforms
business requirements and a semantic model into a structured **Design Spec** that the
`power-bi-report-authoring` skill consumes to produce the actual `.Report/` folder.

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
| `assets/layout-previews/` | SVG thumbnails (1 per layout) used in Seven Confirmations item #2 |
| `assets/chart-previews/` | SVG/PNG thumbnails (1 per chart recipe) used in Design Spec §5 |

### Legacy / cross-skill references

| Reference | When to Read |
|---|---|
| `references/tone-catalog.md` | **Tone catalog** — 12 named tones with typography, palette, density, gridline, border, signature, and iconography downstream choices. Remixing rules. Default tone by domain. |
| `references/signatures.md` | **Signature gallery** — 15 named signatures (typographic, chromatic, structural, iconographic) with tone-coherence matrix. Authoring fresh signatures. |
| `references/accessibility.md` | **Accessibility** — WCAG 2.1/2.2 checklist, 4 alt-text templates, keyboard nav reference, contrast formulas + worked examples, CVD guidance, PBI-specific a11y features, archetype priorities, 10-point testing checklist, DAX-driven alt text |
| `references/anti-patterns.md` | **Anti-patterns** — 6 clusters (visual noise, misleading encoding, cognitive overload, color misuse, interactivity theater, archetype mismatch) + LLM-specific failure modes + severity model |
| `references/visual-cookbook.md` | **Visual cookbook** — per-visual-type formatting rules, theme-vs-per-visual boundaries (what cascades from theme vs what must be instance-scoped) |
| `references/chart-selection-guide.md` | Deciding WHICH chart type to use — decision matrix, hard rules (why bar beats pie) |
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
| 1. Audience & Purpose | Five-question intake (WHO, WHAT, BIG IDEA, ACTION, STYLE) + tone selection | `references/strategist.md` Step 1 + `references/visual-design-principles.md` + `references/tone-catalog.md` + `references/signatures.md` |
| 2. Page Structure | Select pages by domain + page type | `references/domain-report-structures.md` + `references/page-layout-templates.md` |
| 3. Chart Selection | Start from analytical task → pick chart → pick recipe | `references/chart-selection-guide.md` + `references/visual-vocabulary.md` + `references/visual-cookbook.md` |
| 4. Layout & Positioning | Kirk's 5-layer process; Z/F-pattern; canvas 1664×936 | `references/visual-design-principles.md` + `references/layouts/` |
| 5. Theme & Colors | Brand or industry palette; 60/30/10 rule; 4.5:1 contrast | `references/theme-colors.md` + `references/shared-standards.md` §3 + `references/accessibility.md` |
| 6. Navigation & Filters | Pattern selection + slicer recipe binding | `references/navigation-patterns.md` + `references/slicer-filter-patterns.md` + `references/slicer-patterns/` |
| 7. Mobile Layout | Auto-create as starting point; refine for touch/single-column | `../power-bi-report-authoring/references/mobile-layout.md` |
| 8. Produce Design Spec | Fill all 11 sections of the contract template | `references/design-spec-reference.md` |

> **Hard rules** (no pie>5, no 3D, no rainbow, max visuals/page) are defined
> authoritatively in `references/shared-standards.md` §1. All roles load that file first.
> **Anti-patterns** are cataloged in `references/anti-patterns.md` with severity ratings.

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
