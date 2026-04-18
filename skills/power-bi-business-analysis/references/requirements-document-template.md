# Requirements Document Template

Structured output template for Phase 1. Fill every section before handing off
to Phase 2 (Semantic Model). Sections marked *(optional)* can be left as N/A
for small projects or Express Path engagements.

---

```markdown
# BI Requirements: [Project Name]

**Date:** [YYYY-MM-DD]
**Author:** [agent / analyst name]
**Stakeholders:** [list of interviewed roles]
**Domain:** [Sales / Manufacturing / Financial / Supply Chain / Retail / Procurement / Healthcare / Technology]
**Report Archetype:** [Executive / Analytical / Operational]

---

## §1 Business Context

| Field | Value |
|---|---|
| Primary audience | [role + seniority] |
| Data literacy | [high / medium / low] |
| Consumption mode | [desktop / mobile / embedded / presentation] |
| Cadence | [real-time / daily / weekly / monthly / ad-hoc] |
| Big-Idea statement | *"[one sentence — the key takeaway the report must deliver]"* |
| Success criteria | [measurable outcome, e.g. "reduce reporting prep from 4 hrs to 0"] |

## §2 KPIs and Metrics

| # | KPI | Business Definition | DAX Pattern | Format | Target Logic | Priority |
|---|---|---|---|---|---|---|
| 1 | Total Revenue | Sum of net sales amount | `SUM(Sales[NetAmount])` | $#,##0 | vs. budget | Must-have |
| 2 | … | … | … | … | … | … |

*Use the domain-kpi-templates.md shortlist as a starting point. Only include KPIs
the stakeholder confirmed in the interview (question 10).*

## §3 Report Structure (Page Plan)

| Page | Purpose (one sentence) | Audience | Hero Visual | Supporting Visuals | Key Measures | Filters / Slicers |
|---|---|---|---|---|---|---|
| Overview | How are we doing overall? | All | Trend line | 4 KPI cards, bar chart | Revenue, Growth YoY, Margin, Orders | Date range, Region |
| … | … | … | … | … | … | … |

*Follow the standard progression: Overview → Analysis (1-3) → Detail/Drillthrough → Tooltip.*

## §4 Data Requirements

| Table / Entity | Fact or Dim | Grain | Key Columns | Source System | Storage Mode |
|---|---|---|---|---|---|
| Sales | Fact | Transaction | OrderID, Date, Amount, ProductID | SQL / Lakehouse | Import |
| DimDate | Dim | Day | DateKey, Year, Quarter, Month | Generated | Import |
| … | … | … | … | … | … |

## §5 Measure Inventory

| Measure Name | Owner Table | Pattern | Column Dependencies | Page(s) Used | Priority |
|---|---|---|---|---|---|
| Total Revenue | _Sales KPI | SUM | Sales[NetAmount] | Overview, Trend | Must-have |
| Revenue YoY % | _Sales KPI | Time intelligence | Sales[NetAmount], Date | Overview | Must-have |
| … | … | … | … | … | … |

*This inventory feeds directly into the power-bi-dax-development skill (Phase 3).*

## §6 Filters and Interactions

| Scope | Filter / Slicer | Type | Default |
|---|---|---|---|
| Global | Date range | Between slicer | Last 12 months |
| Global | Region | Dropdown | All |
| Page: Product Analysis | Product category | Dropdown | All |
| Cross-filter | All visuals | Highlight (not filter) | — |

## §7 Access and Security

| Aspect | Requirement |
|---|---|
| RLS roles | [e.g. Region Manager sees own region only] |
| Data sensitivity | [public / internal / confidential] |
| Distribution | [workspace / Power BI app / embedded / export-to-PDF] |
| Licensing | [Pro / PPU / Premium / Fabric capacity] |

## §8 Constraints and Assumptions *(optional)*

- Data refresh window: [e.g. nightly 02:00 UTC]
- Model size budget: [e.g. < 500 MB for Pro license]
- Branding: [corporate theme required / flexible]
- Deadline: [e.g. UAT by 2026-05-15]
- Known data gaps: [list any metrics that lack source data]

## §9 Open Questions / Backlog

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | Is forecast data available in the gold layer? | Data Engineering | Open |
| … | … | … | … |

## §10 Sign-Off

| Role | Name | Date | Status |
|---|---|---|---|
| Business Owner | | | ☐ Approved |
| Data Steward | | | ☐ Approved |
| Agent / Analyst | | | ☐ Drafted |
```

---

## Usage Notes

- The agent fills this template during Phase 1; the user approves before Phase 2 begins.
- For **Express Path** (small projects), sections §6-§9 may be auto-filled with sensible
  defaults and marked "auto — confirm or edit".
- §5 (Measure Inventory) becomes the input contract for Phase 3. Every row must have
  a `Measure Name` and `Owner Table` before handoff.
- §3 (Page Plan) becomes the input contract for Phase 4a (Strategist). Every row must
  have a `Purpose` and `Hero Visual` before handoff.
