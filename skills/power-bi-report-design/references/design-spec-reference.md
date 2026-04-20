# Design Spec — 11-Section Reference Template

> **Output of Phase 4a (Strategist). Input of Phase 4a.5 (Seven Confirmations) and Phase 4b (Executor).**

The Design Spec is the **contract**: once it is approved, the Executor builds exactly what it says — no design judgment required during JSON generation.

Fill every section. Use "N/A" explicitly for sections that don't apply — don't leave blanks.

---

## Template

```markdown
# Design Spec — <Report Name>

Version: <v0.1 | v0.2 …>
Author: <strategist / AI agent>
Date: <YYYY-MM-DD>

---

## 1. Brief Capture (5-Question Intake)

| # | Question | Answer (verbatim from user) |
|---|---|---|
| 1 | WHO — primary readers + role | |
| 2 | WHAT — decision this enables | |
| 3 | BIG IDEA — one-sentence takeaway | |
| 4 | ACTION — what they do differently | |
| 5 | STYLE — boardroom / analyst / ops | |

## 2. Audience & Purpose

- **Primary audience:** <role, seniority>
- **Secondary audience:** <role, if any>
- **Decision it drives:** <one sentence>
- **Frequency of use:** <daily / weekly / monthly / ad-hoc>
- **Delivery channel:** <Power BI Service / Teams / Embedded / Print>

## 3. Style Personality

**Chosen:** <Executive | Analytical | Operational>

Justification: <1-2 sentences tying it to WHO + STYLE answers>

Reference file: `executor-<executive|analytical|operational>.md`

## 4. Page Plan

| # | Page name | Slug | Purpose (1 sentence) | Layout file | Canvas |
|---|---|---|---|---|---|
| 1 | Overview | `overview` | | `layouts/exec-overview-16x9.md` | 1664×936 |
| 2 | … | | | | |

For each page, the Big-Idea title that will appear at the top:

| Page | Big-Idea title (draft) |
|---|---|
| Overview | "Revenue momentum steady; North lags plan" |
| … | |

## 5. Visual Inventory (per page)

For each page, list every visual:

### Page 1: Overview

| Visual # | Type | Chart template | Position (x,y,w,h) | Measure(s) | Column(s) | Annotation |
|---|---|---|---|---|---|---|
| V1 | textbox title | — | 0,0,1664,56 | — | — | Big-Idea title |
| V2 | card | `chart-templates/kpi-banner.md` | 0,64,236,120 | `[Total Revenue]` | — | target indicator |
| V3 | card | `chart-templates/kpi-banner.md` | 240,64,236,120 | `[YoY Revenue %]` | — | trend arrow |
| V4 | line chart | `chart-templates/trend-line.md` | 0,200,1664,320 | `[Total Revenue]` | `DimDate[Date]` | plan reference line |
| V5 | bar chart | `chart-templates/bar-comparison.md` | 0,536,555,380 | `[Total Revenue]` | `DimProduct[Category]` | top performer highlight |
| … | | | | | | |

### Page 2: …

(repeat the table)

## 6. Theme & Color

- **Theme file:** `themes/<name>.json` (existing) OR **Custom** (new)
- **Primary brand HEX:** #______
- **Accent HEX:** #______
- **Semantic good/bad/neutral HEX:** #______ / #______ / #______
- **Font family:** Segoe UI (default) OR <brand font>

If custom: attach the theme JSON draft as §6a.

## 7. Iconography

Chosen: <None | KPI set | Domain set | Custom>

If KPI / Domain / Custom, list the specific icons:

| Icon | Usage | Source |
|---|---|---|
| trend-up | KPI cards (YoY positive) | `icons/kpi/trend-up.svg` |
| target-hit | KPI cards (on plan) | `icons/kpi/target.svg` |
| warning | Cards below threshold | `icons/kpi/warning.svg` |
| … | | |

## 8. Navigation

Chosen pattern: <None | Button bar top | Bookmark tabs | Hub-and-spoke | Page navigator>

- **Button locations:** <e.g., top-right bar, 4 buttons>
- **Bookmark list (if any):** <name, filter state, target>
- **Drillthrough:** <source column → target page>
- **Sync slicer groups:** <which slicers, which pages>

## 9. Mobile Strategy

For each page:

| Page | Mobile? | Layout approach |
|---|---|---|
| Overview | Yes | Stack KPI cards vertically; hide grid; keep trend hero |
| Detail | No | Desktop-only |

## 10. Interactions & State

- **Default filters on load:** <per page>
- **Cross-filter rules:** <which visuals filter which>
- **RLS impact:** <how report behaves under each role>
- **Tooltip pages:** <which visuals have custom tooltip pages>

## 11. Backlog / Open Questions / Gaps

Anything not fully resolved — gaps against the template libraries, unresolved user questions, or deferred scope:

- [ ] <gap> — e.g., "No chart-template exists for sankey-flow; using funnel-conversion as stand-in"
- [ ] <open question> — e.g., "User has not provided the fiscal-year start month"
- [ ] <deferred scope> — e.g., "Mobile layout for Detail page deferred to v1.1"

---

## Sign-off (Phase 4a.5 Seven Confirmations)

To be filled after bundled recommendation is presented to the user:

| # | Confirmation | Recommended | User confirmed? |
|---|---|---|---|
| 1 | Canvas | 1664×936 | ☐ |
| 2 | Page plan | 4 pages as above | ☐ |
| 3 | Audience | Sales leadership | ☐ |
| 4 | Style personality | Analytical | ☐ |
| 5 | Color palette | themes/sales-revenue.json | ☐ |
| 6 | Iconography | KPI set | ☐ |
| 7 | Navigation | Button bar top | ☐ |

All seven must be ☑ before Phase 4b begins.
```

---

## Filling the template — guardrails

### Do
- ✅ Put one page per row in §4
- ✅ Put one visual per row in §5 (Visual Inventory)
- ✅ Quote user answers verbatim in §1 — don't paraphrase the brief
- ✅ Always reference a chart-template by file path in §5
- ✅ Always reference a layout by file path in §4
- ✅ Use the exact measure syntax `[Measure Name]` in §5 (matches DAX output from Phase 3)
- ✅ State explicit HEX values in §6 so the theme can be generated deterministically

### Don't
- ❌ Fill §1 after the fact — it's the intake record
- ❌ Write "various KPIs" in §5 — list them explicitly
- ❌ Merge §4 and §5 — page plan is strategic, visual inventory is tactical
- ❌ Leave §11 empty unless truly no gaps exist (rare)
- ❌ Include any JSON — this is a spec, not an implementation

---

## Why 11 sections, not fewer?

Each section answers a question the Executor would otherwise have to improvise:
- §1-3 → which style, audience, voice?
- §4-5 → what to build, in what order?
- §6-7 → how does it look?
- §8-10 → how does it behave?
- §11 → what's deferred, so expectations are explicit

Fewer sections → more improvisation → less predictable output.

---

## Referenced by

- [`strategist.md`](strategist.md) — output format
- Agent Phase 4a.5 — reads §4-8 to build Seven Confirmations bundle
- Agent Phase 4b — Executor reads every section to generate JSON
- Agent Phase 4c — Polisher verifies output against §6 (theme tokens), §7 (icons), §9 (mobile)
