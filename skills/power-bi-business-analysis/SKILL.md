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

Analyze business user requests to define a clear BI strategy before any model or report is built.
The output is a **structured requirements document** that feeds into downstream skills
(semantic model → DAX → report).

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
domain-specific Power BI guidance and best practices before making recommendations.

## Quick Reference

| Task | Approach |
|---|---|
| New project intake | Run full Context Assessment (WHO/WHAT/HOW) |
| Domain-specific KPIs | Use Domain Templates below + detailed reference (references/domain-kpi-templates.md) |
| Page/report structure | Propose pages using Information Architecture framework |
| Data gap analysis | Compare required metrics vs. available data sources |
| Stakeholder alignment | Generate Requirements Document for sign-off |

## Phase 1: Context Assessment (WHO / WHAT / HOW)

Before touching any data, answer three questions (from *Storytelling with Data* principles):

### WHO is the audience?

```
Audience Profiling:
□ Role and seniority (C-suite, manager, analyst, operator)
□ Data literacy level (high, medium, low)
□ Decision-making authority (strategic, tactical, operational)
□ How they consume reports (desktop, mobile, presentation, embedded)
□ Frequency of use (daily, weekly, monthly, ad-hoc)
```

Map the audience to a report archetype:

| Audience | Report Type | Characteristics |
|---|---|---|
| C-suite / executives | Executive dashboard | 3-5 KPI cards, trend lines, exception alerts, minimal detail |
| Department managers | Analytical report | Drill-down, period comparisons, target vs actual, filters |
| Analysts | Exploration workbook | Many slicers, detail tables, export capability, multiple views |
| Operators / field staff | Operational report | Real-time status, action items, mobile-optimized, alerts |

### WHAT decisions will this support?

```
Decision Mapping:
□ What specific decisions does the audience make with this data?
□ What action should they take after viewing the report?
□ What question should each page answer in one sentence?
□ What would "success" look like for this report?
```

### HOW does data support the story?

```
Data-to-Insight Mapping:
□ What data sources are available? (gold layer, existing models, external)
□ What is the data granularity? (transaction-level, daily, monthly)
□ What time periods are needed? (real-time, historical, forecast)
□ What comparisons matter? (YoY, budget vs actual, target vs actual, benchmark)
□ Are there hierarchies to support drill-down? (geography, product, time, org)
```

## Phase 2: Domain Analysis

Based on the business domain, identify standard KPIs, common analyses, and typical report structures.

### Domain Templates

Storytelling principles (pre-attentive attributes, narrative structure, audience design)
are in the `power-bi-report-design` skill at
`../power-bi-report-design/references/visual-design-principles.md`.

For detailed KPI definitions with DAX patterns, format strings, and target logic,
see `references/domain-kpi-templates.md`.

#### Sales & Revenue
```
Key KPIs:
- Revenue (total, by product/region/channel)
- Growth rate (YoY, MoM, QoQ)
- Average order value (AOV)
- Customer acquisition cost (CAC)
- Customer lifetime value (CLV)
- Sales pipeline / conversion rate
- Revenue per employee / per unit

Common Analyses:
- Sales trend over time (line chart)
- Revenue by product category (bar chart)
- Geographic distribution (map)
- Top N customers / products (ranked bar)
- Sales vs. target (bullet chart / gauge)
- Cohort analysis (retention heatmap)

Typical Pages: Overview → Sales Trend → Product Analysis → Regional Breakdown →
               Customer Analysis → Target Tracking → Detail / Drillthrough
```

#### FMCG (Fast-Moving Consumer Goods)
```
Key KPIs:
- Net revenue, gross margin
- Volume (units sold, cases, weight)
- Distribution (numeric, weighted)
- Market share
- Trade spend effectiveness (ROI)
- Promotion uplift
- Out-of-stock rate
- Days of inventory

Common Analyses:
- Brand/SKU performance comparison
- Promotion effectiveness (pre/during/post)
- Channel mix (modern trade, general trade, e-commerce)
- Price point analysis
- Seasonal demand patterns
- Distributor/retailer performance

Typical Pages: Overview → Brand Performance → Channel Analysis → Promotion ROI →
               Distribution Coverage → Inventory Status → Detail
```

#### Manufacturing & Operations
```
Key KPIs:
- OEE (Overall Equipment Effectiveness)
- Production volume / yield rate
- Defect rate / quality index
- Downtime (planned vs. unplanned)
- Cycle time / throughput
- Scrap rate / waste percentage
- Energy consumption per unit
- Safety incidents

Common Analyses:
- Production trend by plant/line (line chart)
- OEE breakdown: availability × performance × quality
- Defect Pareto analysis (top causes)
- Downtime analysis by category
- Capacity utilization heatmap
- Material consumption vs. plan

Typical Pages: Overview → Production KPIs → Quality Analysis → Downtime Analysis →
               Plant Comparison → Material Usage → Detail
```

#### Supply Chain & Logistics
```
Key KPIs:
- On-time delivery (OTD) / OTIF
- Lead time (average, variability)
- Inventory turnover / days on hand
- Fill rate / order accuracy
- Freight cost per unit
- Warehouse utilization
- Supplier performance score
- Demand forecast accuracy

Common Analyses:
- Delivery performance trend
- Inventory aging analysis
- Supplier scorecard comparison
- Route/lane cost analysis
- Demand vs. supply gap
- Warehouse capacity utilization

Typical Pages: Overview → Delivery Performance → Inventory Health → Supplier Scorecard →
               Logistics Cost → Demand Planning → Detail
```

#### Financial / P&L
```
Key KPIs:
- Revenue, COGS, gross profit, gross margin
- Operating expenses (OPEX) by category
- EBITDA, net income, net margin
- Budget vs. actual variance
- Cash flow (operating, investing, financing)
- Working capital ratios
- Cost per unit / cost allocation

Common Analyses:
- P&L waterfall (revenue → costs → profit)
- Budget vs. actual variance (bar + variance %)
- Expense trend by category
- Department/entity comparison
- Month-over-month / YoY P&L comparison
- Rolling forecast vs. actual

Typical Pages: Overview → P&L Statement → Revenue Analysis → Cost Breakdown →
               Budget Variance → Cash Flow → Department Detail
```

#### Retail
```
Key KPIs:
- Sales per square foot / per store
- Basket size / items per transaction
- Conversion rate (foot traffic → purchase)
- Same-store sales growth
- Shrinkage / loss prevention
- Customer satisfaction (NPS)
- Loyalty program metrics

Common Analyses:
- Store performance ranking
- Category contribution analysis
- Hourly/daily sales patterns (heatmap)
- Promotion effectiveness
- Customer segmentation
- Product affinity / market basket

Typical Pages: Overview → Store Performance → Category Analysis → Customer Insights →
               Promotion Tracking → Inventory → Detail
```

#### Procurement
```
Key KPIs:
- Total spend / spend by category
- Savings achieved vs. target
- Supplier count / consolidation ratio
- PO cycle time
- Contract compliance rate
- Cost avoidance
- Maverick spend percentage

Common Analyses:
- Spend analysis by category/supplier/region
- Supplier performance comparison
- Price trend analysis
- Contract utilization rate
- Savings waterfall
- Procurement process efficiency

Typical Pages: Overview → Spend Analysis → Supplier Performance → Contract Management →
               Savings Tracking → Process Metrics → Detail
```

## Phase 3: Information Architecture

Design the report structure before any visual is created.

### Page Planning Framework

For each proposed page, define:

```
Page Definition Template:
┌────────────────────────────────────────────┐
│ Page Name: [name]                          │
│ Purpose: [one-sentence question it answers]│
│ Audience: [who primarily uses this page]   │
│ Key Metrics: [3-5 measures displayed]      │
│ Main Visual: [the "hero" chart type]       │
│ Supporting Visuals: [2-3 context charts]   │
│ Filters/Slicers: [what the user controls]  │
│ Drill Actions: [drillthrough targets]      │
│ Data Source: [tables/entities needed]       │
└────────────────────────────────────────────┘
```

### Standard Page Patterns

Every report should follow this progression:

1. **Overview page** — The executive summary. 3-5 KPI cards at top, one hero visual
   (usually a trend line), 1-2 supporting visuals. Answers: "How are we doing overall?"
2. **Analysis pages** (1-3) — Break down the overview by key dimensions (product, region,
   time, category). Each page answers one specific analytical question.
3. **Detail / Drillthrough page** — Transaction-level or item-level data. Hidden from
   navigation; accessed via drillthrough from analysis pages.
4. **Tooltip pages** (optional) — Small 320×240 pages that appear on hover.
   Show contextual detail without leaving the current page.

### Measure Planning

List all measures needed, grouped by purpose:

```
Measure Inventory Template:
| Measure Name | Formula Type | Tables Needed | Page(s) Used |
|---|---|---|---|
| Total Revenue | SUM aggregation | Sales[Amount] | Overview, Sales Trend |
| Revenue YoY % | Time intelligence | Sales, Date | Overview, Trend |
| Gross Margin % | Ratio (DIVIDE) | Sales, Costs | P&L, Overview |
| Running Total | Window function | Sales, Date | Trend |
```

This inventory feeds directly into the `power-bi-dax-development` skill.

## Phase 4: Output — Requirements Document

Generate a structured document with these sections:

```
# BI Requirements: [Project Name]

## 1. Business Context
- Domain: [industry/function]
- Audience: [roles and data literacy]
- Key decisions supported: [list]
- Success criteria: [measurable outcomes]

## 2. KPIs and Metrics
| KPI | Definition | Target | Data Source |
|---|---|---|---|

## 3. Report Structure
| Page | Purpose | Key Visuals | Measures |
|---|---|---|---|

## 4. Data Requirements
| Table/Entity | Type (Fact/Dim) | Key Columns | Source |
|---|---|---|---|

## 5. Measure Inventory
| Measure | Pattern | Dependencies | Priority |
|---|---|---|---|

## 6. Filters and Interactions
- Global filters: [date range, entity]
- Page-level slicers: [per page]
- Cross-filter behavior: [highlight vs filter]

## 7. Access and Security
- RLS requirements: [roles and rules]
- Data sensitivity: [classification]
- Distribution: [workspace, app, embedded]

## 8. Next Steps
- [ ] Build/extend semantic model (power-bi-semantic-model skill)
- [ ] Create DAX measures (power-bi-dax-development skill)
- [ ] Generate PBIP report (power-bi-pbip-report skill)
```

## Anti-Patterns to Avoid

- **Starting with visuals** before understanding the business question
- **Measuring everything** instead of focusing on actionable KPIs
- **Vanity metrics** that look impressive but don't drive decisions
- **One-size-fits-all** reports that serve no audience well
- **Missing the "so what"** — data without insight or recommended action
- **Scope creep** — trying to answer every question in one report
