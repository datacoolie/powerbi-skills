# Worked Example — FMCG Trade Analytics (Executive)

A one-page trace of the four Steps for a realistic brief:

> *"Our brand managers need to see how our trade-promotion spend is paying off
> across modern trade vs. general trade, by brand and by month."*

## Step 1 — Context

- **WHO:** 8 brand managers + 2 commercial directors; data literacy 3; weekly cadence; desktop primary, mobile secondary
- **WHAT:** decide where to reallocate trade budget next quarter; Big-Idea = *"Trade ROI is highest in MT-Premium; shift 15% spend from GT-Mass by Q3"*; success = ≤ 2 hrs to assemble monthly review
- **HOW:** data in gold lakehouse (`gold.FactTradeSpend`, `gold.FactSales`, `gold.DimBrand`); daily grain; 36 months history; RLS by region
- **Archetype:** Analytical (managers + drill-down), leaning Executive at overview page

## Step 2 — Domain

FMCG domain → [domain-kpi-templates.md §FMCG](domain-kpi-templates.md)

- **Must-have KPIs:** Net Revenue, Gross Margin %, Trade Spend ROI, Promotion Uplift, Market Share
- **Nice-to-have:** OOS Rate, Distribution Coverage
- **Dimensions:** Date, Brand, Channel (MT/GT/e-com), Promotion, Geography

## Step 3 — IA + Gaps

- **Page plan:** Overview → Trade ROI by Channel → Brand Deep-dive → Promotion Post-mortem → Detail drillthrough (5 pages)
- **Gap analysis:**
  - Market Share is ❌ (no Nielsen feed) → demote to backlog, keep 4 must-haves
  - Uplift is ⚠️ (baseline calculation needs 12-week pre-period assumption — document in §4)

## Step 4 — Output

- Requirements Document filled; §5 Measure Inventory has 14 measures (4 base + 6 time-intel + 4 ratios)
- Handoff JSON emitted with `from_phase: "phase-1"`; validator passes
- User approves after one round of feedback (requested merging "Brand Deep-dive" + "Promotion Post-mortem" into a single page → updated §3)
- **Exit criteria: all 8 checkboxes satisfied → proceed to Phase 2**
