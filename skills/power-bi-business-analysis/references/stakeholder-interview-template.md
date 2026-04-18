# Stakeholder Interview Template

Structured interview guide for gathering Power BI project requirements from
business stakeholders. Run this before defining KPIs or page structures.

## Pre-Interview Preparation

```
Before the interview:
□ Identify the stakeholder's role and seniority
□ Review any existing reports they currently use
□ List known data sources and availability
□ Prepare domain-specific KPI shortlist (from domain-kpi-templates.md)
```

## Interview Questions

### Section 1 — WHO (Audience Profiling)

| # | Question | Why It Matters |
|---|---|---|
| 1 | What is your role, and what decisions do you make weekly/monthly? | Maps to report archetype (Executive / Analytical / Operational) |
| 2 | Who else will use this report? List roles and approximate count. | Determines if multiple style personalities are needed |
| 3 | How do you consume reports today? (Desktop, mobile, Teams embed, presentation) | Drives canvas size and mobile layout decisions |
| 4 | How often will you look at this? (Real-time, daily, weekly, monthly, ad-hoc) | Affects storage mode and refresh strategy |
| 5 | Rate your comfort with data tools: 1 (prefer summary) to 5 (write SQL). | Sets detail level, slicer complexity, export needs |

### Section 2 — WHAT (Decisions & Outcomes)

| # | Question | Why It Matters |
|---|---|---|
| 6 | What is the **one question** this report must answer? | Becomes the Big-Idea title on the overview page |
| 7 | What action do you take after seeing the data? (e.g. reallocate budget, escalate, reorder) | Validates the report drives action, not just awareness |
| 8 | What comparisons matter most? (vs. target, vs. last year, vs. budget, vs. benchmark) | Determines time-intelligence and variance measures |
| 9 | What would make you say "this report is a success"? | Defines acceptance criteria for UAT |
| 10 | Are there any existing KPIs or metrics you already track? List them. | Avoids reinventing; ensures continuity |

### Section 3 — HOW (Data & Constraints)

| # | Question | Why It Matters |
|---|---|---|
| 11 | What data sources are available? (SQL Server, Lakehouse, Excel, API, etc.) | Drives storage mode (Import / DQ / DirectLake) |
| 12 | What is the lowest grain of the data? (Transaction, daily summary, monthly) | Sets fact-table design and drill-down depth |
| 13 | How far back do you need historical data? (1 yr, 3 yr, all-time) | Affects model size and incremental refresh |
| 14 | Are there data-access restrictions? (Roles that see only their region/team) | Triggers RLS design in Phase 2 |
| 15 | Any deadlines, compliance, or branding constraints? | Scopes timeline and theme selection |

## Recording the Answers

Capture answers verbatim in a simple table:

```markdown
| # | Stakeholder Answer | Agent Notes |
|---|---|---|
| 1 | "I'm VP Sales, I decide weekly pipeline focus" | Executive archetype, weekly cadence |
| 2 | … | … |
```

## Post-Interview Checklist

```
After the interview:
□ Map audience → report archetype (Executive / Analytical / Operational)
□ Draft the Big-Idea statement from question 6
□ Select matching domain template from domain-kpi-templates.md
□ Identify data gaps (questions 11-13 vs. required KPIs)
□ Feed answers into the Requirements Document template
```

## Multiple-Stakeholder Projects

When more than one stakeholder is involved:

1. Interview each role separately (answers often conflict)
2. Build a **stakeholder map**: role × decisions × frequency × data literacy
3. If archetypes clash (e.g. C-suite wants Executive, analysts want Operational),
   propose separate report sections or pages targeted to each audience
4. Resolve conflicts by deferring to the primary decision-maker
