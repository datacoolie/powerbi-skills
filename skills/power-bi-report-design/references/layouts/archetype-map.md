# Official Archetype → Library Layout Map

Bridges the official `design` mode (5 archetypes × variants A/B/C, `../design/archetypes/*.md`) to this
library's recipes (`layouts-index.json`). Use it in Strategist Step 3: route the page to an
archetype + variant first, then pick the closest recipe below (or record a gap).

> All recipes are FHD (1920 × 1080). The official archetype diagrams are drawn schematically (zone
> heights in the file are relative); take **coordinates from the recipe** and the grid rules from
> `../design/layout.md` (12-column grid, 24 px gutters, 32 px margins, 72 px header → content area
> 1856 × 944).

| Archetype | Variant | Closest library recipe(s) | Notes |
|---|---|---|---|
| Executive Summary | A. Hero-Right (3–4 KPIs + one hero) | `exec-overview-16x9` | Default exec page |
| | B. KPI-Strip (5–6 comparable KPIs) | `scorecard-kpi-grid`, `kpi-donut-row`, `advanced-kpi-card-grid` | Consolidate related KPIs into one multi-value `cardVisual` where styling allows |
| | C. Headline-Hero (1–2 KPIs + narrative chart) | `finance-pnl-waterfall`, `esg-carbon-scorecard` | Hero = waterfall / decomposition |
| | (domain exec scorecards) | `hr-dei-scorecard`, `it-service-catalog`, `hc-clinical-quality` | Variant B-like, domain-specific |
| | (navigation hubs — not an archetype) | `landing-navigation`, `dimension-nav-hub` | Landing/hub pages |
| Analytical Canvas | A. Filter-Rail (4+ slicers) | `left-rail-filter-analytical`, `customer-360`, `chiclet-nav-strip` | Rail ≈ 310 px on FHD (2 grid columns) |
| | B. Inline-Slicers (1–3 slicers) | `sales-performance`, `marketing-funnel`, `budget-actual-grid`, `sales-pipeline-forecast`, `hr-headcount-attrition` | Slicers inline with the title row (~230 px each, h 64) |
| | C. Small-Multiples-Grid | **gap** (nearest: `cohort-retention-grid`, `aging-bucket-page`) | Listed in `layouts-index.json` `gaps` |
| | (specialised analytical) | `variance-dual-waterfall`, `geo-territory-map`, `full-page-map`, `what-if-parameter-page`, `drillthrough-detail`, `qna-explore-page`, `supply-inventory-abc`, `sales-rep-leaderboard`, `hc-readmission-analysis`, `it-finops-cost-governance`, `it-release-train`, `it-incident-postmortem`, `hr-*` | Pick by domain/task |
| Operational Monitor | A. 4-Up Status | `ops-single-screen`, `tachometer-gauge-row`, `mfg-line-status` | Large status tiles |
| | B. Wallboard | `ops-single-screen-tv`, `mfg-line-status-tv`, `it-sla-heatmap-tv`, `hc-patient-flow-tv`, `it-service-catalog-tv` | TV wall variants |
| | C. Incident-First | `ops-activity-log`, `it-sla-heatmap`, `hc-patient-flow` | Alert/incident banner first |
| Narrative Story | A. 7/5 Split | `narrative-story-page` | Argument + annotation split |
| | B. Single-Column-Scroll | **gap** | Listed in `gaps` |
| | C. Annotated-Hero | **gap** | Listed in `gaps` |
| Comparative Benchmark | A. Side-by-Side | `comparison-side-by-side` | Small multiples + headline |
| | B. Stacked-Pairs | `variance-dual-waterfall`, `budget-actual-grid` | Actual-vs-reference pairs |
| | C. Slope-Graph-First | **gap** | Listed in `gaps` |

## Using the extra FHD room (official rules)

FHD gives ≈ 2.7× the area of the original 1280 × 720 canvas. Spend it with the official Space-Allocation
and density rules (`../design/layout.md`, archetype files) — not by inflating existing visuals:

- ≤ 15% empty content cells on analytical/operational/comparative pages (≤ 20% executive/narrative); every region must be used.
- Supporting charts ≥ 3 columns × 3 rows of the 12×12 grid; dense labels/legends/small multiples ≥ 4×3 or 3×4; tables ≥ 4 rows unless a top-N spotlight; KPI strips use 2 grid rows.
- One region ≤ 45% of content cells on pages with 4+ data visuals; never make a bare single-value card the hero.
- 7 ± 2 visual groups per page; whitespace tiers 16 (within group) / 24 (between groups) / 32 (sections).
- Budgets on FHD: Executive ≤ 6 visuals, Analytical ≤ 12, Operational ≤ 14 (excluding slicers/buttons/shapes). Executive KPI count stays 3–6.
- Every recipe lists optional **FHD headroom** slots in its *Customization allowed* section — add them only when the data supports a distinct analytical question, never a duplicate absolute-measure card.
