---
name: power-bi-business-analysis
description: >-
  Analyze business requirements and define BI strategy for Power BI projects.
  Use this skill whenever the user wants to analyze business requirements, identify KPIs,
  define what insights a report should deliver, propose dashboard structure for a business domain,
  or gather requirements before building a Power BI report or semantic model.
  Triggers include: "analyze business requirements", "what KPIs should we track",
  "what insights can we get", "business domain analysis", "requirements gathering",
  "what should we measure", "what problems can we solve", "propose a dashboard",
  "what reports do we need", "BI strategy", "define metrics".
  Do NOT use for actual model building (use power-bi-semantic-model),
  DAX writing (use power-bi-dax-development), or report generation (use power-bi-pbip-report).
---

# Power BI Business Analysis

This is **Phase 1** of the agent pipeline. Analyze the business request and
produce a **Requirements Document** that becomes the handoff contract to
Phase 2 (Semantic Model).

The skill itself runs as four internal **Steps** (to avoid colliding with the
agent's own Phase numbering):

```
Step 1 ── Step 2 ── Step 3 ── Step 4
CONTEXT   DOMAIN    INFO-ARCH OUTPUT
(WHO/     (KPIs by  (page     (Requirements
 WHAT/    industry)  plan)     Document +
 HOW)                          handoff JSON)
```

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
domain-specific Power BI guidance and best practices before making recommendations.

### Useful research queries

Run these at the start of each step, replacing `<domain>` with the business domain:

| Step | Sample query |
|---|---|
| Step 1 | `Power BI report archetype executive analytical operational` |
| Step 2 | `Power BI <domain> KPI best practices dashboard examples` |
| Step 2 | `DAX time intelligence year-over-year pattern` |
| Step 3 | `Power BI drillthrough tooltip page design guidelines` |
| Step 3 | `Power BI semantic model data source <source-type> limitations` |
| Step 4 | `Power BI row-level security RLS static dynamic patterns` |

Use `microsoft_docs_fetch` to read full articles when excerpts are insufficient.

## Reference Files (read in this order)

| Reference | Used in | Purpose |
|---|---|---|
| [stakeholder-interview-template.md](references/stakeholder-interview-template.md) | Step 1 | 15-question interview guide (WHO / WHAT / HOW) with recording template |
| [domain-kpi-templates.md](references/domain-kpi-templates.md) | Step 2 | KPI definitions, DAX patterns, dimensions, and analyses per industry |
| [information-architecture-patterns.md](references/information-architecture-patterns.md) | Step 3 | Archetype-specific page flows, navigation patterns, canvas sizing |
| [data-gap-analysis-template.md](references/data-gap-analysis-template.md) | Step 3/4 | Requirements-vs-data matrix, gap classification, resolution plan |
| [requirements-document-template.md](references/requirements-document-template.md) | Step 4 | 10-section document template — the Phase 1 → 2 handoff contract |

## When to Use This Skill vs. Others

| Say this → | Use this skill |
|---|---|
| "what should we measure", "define KPIs", "gather requirements" | power-bi-business-analysis (this skill) |
| "design the layout", "choose chart types", "pick a theme" | power-bi-report-design |
| "build the model", "create tables", "set up relationships" | power-bi-semantic-model |

Both this skill and `power-bi-report-design` handle "dashboard planning" — but
**this skill stops at the page plan**; `power-bi-report-design` turns that plan
into a Design Spec with specific layouts, recipes, and themes.

---

## Step 1 — Context Assessment (WHO / WHAT / HOW)

Before touching any data, run the stakeholder interview.

→ **Read [stakeholder-interview-template.md](references/stakeholder-interview-template.md)**
and record answers verbatim in the table at the bottom of that file.

The three question groups map to:

### WHO is the audience?

Map the interview answers (questions 1–5) to a report archetype:

| Audience | Report Archetype | Characteristics |
|---|---|---|
| C-suite / executives | **Executive** | 3-5 KPI cards, trend lines, exception alerts, minimal detail |
| Department managers | **Analytical** | Drill-down, period comparisons, target vs actual, filters |
| Analysts | **Exploration** | Many slicers, detail tables, export capability, multiple views |
| Operators / field staff | **Operational** | Real-time status, action items, mobile-optimized, alerts |

**Using the data-literacy score (interview Q5):**
- **1–2 (prefer summary)** → fewer slicers, larger fonts, more narrative titles, Big-Idea phrasing over raw numbers
- **3 (neutral)** → default Analytical archetype
- **4–5 (writes SQL)** → add detail tables, export buttons, richer slicer panel, expose grain

### WHAT decisions will this support?

Use interview answers 6–10 to capture:
- The **one question** the report must answer (→ Big-Idea title in §1 of the Requirements Document)
- The action the user takes after viewing (→ validates the report drives action, not just awareness)
- Comparisons that matter (→ time-intelligence measures in Step 2)
- Success criteria (→ UAT acceptance criteria in Phase 6)

### HOW does data support the story?

Use interview answers 11–15 to capture:
- Data sources, lowest grain, history depth, access restrictions, constraints
- These feed directly into Step 3's Data Gap Analysis and the Phase 2 storage-mode decision

### Skip Step 1 when…

- User provides a complete brief in one message (domain + KPIs + page plan) → go to Step 2 with their brief as input
- Model already exists AND has ≤ 5 measures AND user describes ≤ 3 pages → **Express Path**: condense Steps 1–3 into a single model-discovery pass (see agent.md §Express Path)

---

## Step 2 — Domain Analysis

Identify standard KPIs and analyses for the domain.

→ **Read [domain-kpi-templates.md](references/domain-kpi-templates.md)** — find the
matching section for your domain and lift the KPI table, dimensions, and analyses.

**Domain index** (pick one; see reference file for full KPI tables with DAX patterns):

| Domain | Typical audience | Hero metrics |
|---|---|---|
| Sales & Revenue | Sales ops, execs | Revenue, Growth YoY, AOV, Win Rate |
| FMCG | Brand/category mgrs | Net Revenue, Market Share, Trade ROI, OOS Rate |
| Manufacturing | Plant managers | OEE, Defect Rate, Downtime, Throughput |
| Supply Chain | Logistics / S&OP | OTIF, Inventory Turnover, Fill Rate, Supplier Score |
| Financial / P&L | CFO, controllers | Revenue, Gross Margin, EBITDA, Budget Variance |
| Retail | Store ops, merch | Sales/sqft, Basket Size, Same-Store Growth, Conversion |
| Procurement | Sourcing, category mgrs | Spend by category, Savings, PO Cycle Time, Maverick % |
| Healthcare / Pharma | Ops, clinical | Patient volume, Readmission, Avg LOS, Drug utilization |
| Technology / IT | IT ops, SRE | Uptime, MTTR, Ticket volume, Cost per user |

Storytelling principles (pre-attentive attributes, narrative structure) live in
the `power-bi-report-design` skill at
[visual-design-principles.md](../power-bi-report-design/references/visual-design-principles.md)
— do not duplicate them here.

---

## Step 3 — Information Architecture & Data Gaps

Design the report structure and verify the data exists to support it.

→ **Read [information-architecture-patterns.md](references/information-architecture-patterns.md)**
for archetype-specific page flows, canvas sizing, and navigation patterns.

### Page plan

Every report follows this universal layered progression:

1. **Overview** (Layer 1) — "How are we doing?" 3–5 KPI cards, hero trend visual
2. **Analysis** (Layer 2, 1–3 pages) — "Why is it happening?" broken down by key dimensions
3. **Detail / Drillthrough** (Layer 3, hidden) — "Show me the rows"
4. **Tooltip pages** (Layer 4, optional) — "More info on hover"

Minimum viable report = Layers 1 + 3. Full analytical report = all four layers.
For archetype-specific page counts and flows, use the reference file's diagrams.

### Filter requirements (not design)

At Phase 1, capture **which dimensions need to be filterable** and **who can
see what** (RLS). Do **not** decide slicer types, placement, sync groups, or
cross-filter behavior — those are Phase 4a design decisions owned by the
`power-bi-report-design` skill.

In [Requirements Document §6](references/requirements-document-template.md), list:
- Dimensions the audience must be able to filter by (Date, Region, Product, etc.)
- Whether each filter is **required** (must-have) or **nice-to-have**
- Expected scope hints (e.g. "Date is global", "Promotion only on the Promotion page")
- RLS requirements go in §7 (role, scoped column, rule expression)

### Data gap analysis

Before finalizing the page plan, verify every KPI has a data source.

→ **Read [data-gap-analysis-template.md](references/data-gap-analysis-template.md)**
and fill its requirements-vs-data matrix.

Each KPI ends up in one of three states:
- ✅ **Available** — data exists at the right grain → proceed
- ⚠️ **Partial** — needs transformation, different grain, or incomplete history → document ETL work in §4 of the Requirements Document
- ❌ **Missing** — no source → escalate, defer to backlog, or drop from v1

Gaps marked ❌ that block must-have KPIs are **blockers** for Phase 2 — do not
produce a handoff until they have a resolution plan.

---

## Step 4 — Output: Requirements Document + Handoff

Produce the formal deliverable.

→ **Use [requirements-document-template.md](references/requirements-document-template.md)**
as the structure. Fill all 10 sections (mark N/A where appropriate for Express Path).

The template's §5 Measure Inventory is the direct input to the
`power-bi-dax-development` skill — name each measure, its pattern, dependencies,
and priority.

### Handoff to Phase 2

The Phase 1 → Phase 2 transition emits a handoff JSON conforming to
[handoff.schema.json](../../agents/handoff.schema.json) with `from_phase: "phase-1"`.

See [handoff-phase1-to-phase2.json](../../agents/examples/handoff-phase1-to-phase2.json)
for the exact shape. The `artifacts["phase-1"]` payload must include:

| Key | Source |
|---|---|
| `requirements_document` | Requirements Document §1–§8 |
| `measures_inventory` | Requirements Document §5 |
| `page_plan` | Requirements Document §3 |
| `data_source_list` | Requirements Document §4 + gap analysis results |

Validate before handing off:
```powershell
python agents/validate_handoff.py <handoff-file>.json
```

---

## Exit Criteria — done when…

Phase 1 is complete when **every** item below is true:

- [ ] Requirements Document exists with all 10 sections filled (or marked N/A)
- [ ] Audience archetype selected (Executive / Analytical / Operational / Exploration)
- [ ] KPI list is complete, with business definitions and priority (Must / Should / Nice)
- [ ] Page plan has Overview + at least one Analysis page + Detail page
- [ ] Measures Inventory lists every measure with owner table and DAX pattern
- [ ] Required filter dimensions listed in §6 (design handled later in Phase 4a)
- [ ] Data Gap Analysis complete — no unresolved ❌ blockers on must-have KPIs
- [ ] Handoff JSON validates against the schema
- [ ] User has approved the Requirements Document

**Do not proceed to Phase 2 until the user approves.** If they request changes,
iterate within Step 4.

---

## Worked Example — FMCG Trade Analytics (Executive)

A one-page trace of the four Steps for a realistic brief:

> *"Our brand managers need to see how our trade-promotion spend is paying off
> across modern trade vs. general trade, by brand and by month."*

**Step 1 — Context**
- WHO: 8 brand managers + 2 commercial directors; data literacy 3; weekly cadence; desktop primary, mobile secondary
- WHAT: decide where to reallocate trade budget next quarter; Big-Idea = *"Trade ROI is highest in MT-Premium; shift 15% spend from GT-Mass by Q3"*; success = ≤ 2 hrs to assemble monthly review
- HOW: data in gold lakehouse (`gold.FactTradeSpend`, `gold.FactSales`, `gold.DimBrand`); daily grain; 36 months history; RLS by region
- **Archetype:** Analytical (managers + drill-down), leaning Executive at overview page

**Step 2 — Domain** (FMCG row from the index → [domain-kpi-templates.md §FMCG](references/domain-kpi-templates.md))
- Must-have KPIs: Net Revenue, Gross Margin %, Trade Spend ROI, Promotion Uplift, Market Share
- Nice-to-have: OOS Rate, Distribution Coverage
- Dimensions: Date, Brand, Channel (MT/GT/e-com), Promotion, Geography

**Step 3 — IA + Gaps**
- Page plan: Overview → Trade ROI by Channel → Brand Deep-dive → Promotion Post-mortem → Detail drillthrough (5 pages)
- Gap analysis: Market Share is ❌ (no Nielsen feed) → demote to backlog, keep 4 must-haves. Uplift is ⚠️ (baseline calculation needs 12-week pre-period assumption — document in §4)

**Step 4 — Output**
- Requirements Document filled; §5 Measure Inventory has 14 measures (4 base + 6 time-intel + 4 ratios)
- Handoff JSON emitted with `from_phase: "phase-1"`; validator passes
- User approves after one round of feedback (requested merging "Brand Deep-dive" + "Promotion Post-mortem" into a single page → updated §3)
- **Exit criteria: all 8 checkboxes satisfied → proceed to Phase 2**

---

## Related Skills

| Skill | Relationship | When it receives output from this skill |
|---|---|---|
| `power-bi-semantic-model` | Downstream (Phase 2) | §3 page plan + §4 data requirements drive table + relationship design |
| `power-bi-dax-development` | Downstream (Phase 3) | §5 Measure Inventory is the measure build list |
| `power-bi-report-design` | Downstream (Phase 4a) | Archetype + page plan + audience feed the Design Spec |
| `power-bi-feedback-iteration` | Loop-back | "Missing insight" / "new requirement" feedback routes back to Step 1 or 2 |

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do instead |
|---|---|
| Start with visuals before understanding the business question | Complete Step 1 (WHO/WHAT/HOW) first |
| Measure everything the data allows | Filter to KPIs the user confirmed in interview Q10 |
| Build "vanity metrics" that look impressive | Tie each KPI to a decision (interview Q7) |
| Create one report for all audiences | One archetype per report; split if stakeholders disagree |
| Present numbers without a "so what" | Every page has a Big-Idea title (interview Q6) |
| Cram every question into one report | Defer to backlog; one report = one focused narrative |
| Skip the data gap analysis | Run it before promising KPIs to the user |

