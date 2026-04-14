# Domain-Specific Report Structures

Recommended page sets, KPI definitions, and visual compositions by industry domain.

---

## Sales / Revenue Analytics
| Page | Type | Key Visuals |
|---|---|---|
| Overview | Standard | KPI cards (Revenue, Growth, Target%), trend line, top-N bar |
| Regional Breakdown | Standard | Map, clustered bar by region, matrix by region×product |
| Product Analysis | Standard | Treemap by category, combo chart (revenue + margin), table |
| Customer Analysis | Standard | Scatter (value vs. frequency), top-10 table, cohort trend |
| Sales Rep Performance | Standard | Bar chart ranked, KPI cards per rep, target gauge |
| Order Detail | Drillthrough | Entity cards, transaction table, trend line |
| Product Tooltip | Tooltip | Card (sales), card (margin%), mini bar chart |

### Sales KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| Revenue | SUM of sales amount | Currency | vs. budget or PY |
| Growth Rate (YoY) | (Current - PY) / PY | Percentage | > 0% = green |
| Average Order Value | Revenue / # Orders | Currency | vs. PY |
| Customer Acquisition Cost | Marketing spend / # New Customers | Currency | lower is better |
| Conversion Rate | # Won opportunities / # Total opportunities | Percentage | industry benchmark |
| Gross Margin % | (Revenue - COGS) / Revenue | Percentage | > target threshold |

### Sales Layout Guidance
- **Overview**: Z-pattern — KPI cards top row → hero trend line middle → top-N bar bottom-left → map bottom-right
- **Rep Performance**: Rank chart sorted descending; use conditional formatting (green/red) on KPI vs. target

## Manufacturing / Operations
| Page | Type | Key Visuals |
|---|---|---|
| Production Overview | Standard | KPI cards (OEE, yield, downtime), line chart (daily output) |
| Quality Control | Standard | Control chart (defect rate), Pareto bar, trend |
| Equipment Status | Standard | Card matrix per machine, gauge (utilization), timeline |
| Inventory | Standard | Stacked bar (stock levels), line (consumption rate), alerts |
| Shift Analysis | Detail | Matrix (shift×metric), combo chart, filter by line/shift |
| Machine Drillthrough | Drillthrough | Machine details, downtime history, maintenance log |

### Manufacturing KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| OEE (Overall Equipment Effectiveness) | Availability × Performance × Quality | Percentage | World-class ≥ 85% |
| Yield Rate | Good units / Total units produced | Percentage | > 95% |
| Downtime Hours | SUM of unplanned stop duration | Hours | < threshold per line |
| Defect Rate | Defective units / Total units | Percentage | < 1% |
| MTBF (Mean Time Between Failures) | Total operating time / # Failures | Hours | higher is better |
| Cycle Time | Avg time per unit from start to finish | Minutes | ≤ standard cycle |

### Manufacturing Layout Guidance
- **Production Overview**: KPI cards use traffic-light colors (OEE: green ≥85%, amber ≥65%, red <65%)
- **Quality Control**: Pareto chart (80/20 rule) highlights top defect causes; use reference line at 80%

## Financial / P&L
| Page | Type | Key Visuals |
|---|---|---|
| Executive Summary | Standard | KPI cards (Revenue, EBITDA, Net Income), waterfall chart |
| Income Statement | Standard | Matrix (account hierarchy), variance bar chart |
| Balance Sheet | Standard | Clustered bar (assets vs liabilities), trend |
| Cash Flow | Standard | Waterfall (operating→investing→financing), line trend |
| Budget vs Actual | Detail | Combo chart (bars=actual, line=budget), variance table |
| Account Drillthrough | Drillthrough | Account transactions, monthly trend, annotations |

### Financial KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| Revenue | SUM of revenue accounts | Currency | vs. budget |
| EBITDA | Operating profit + Depreciation + Amortization | Currency | margin % > 15% |
| Net Income | Revenue - all expenses - taxes | Currency | vs. budget, PY |
| Gross Margin % | (Revenue - COGS) / Revenue | Percentage | industry benchmark |
| Operating Expense Ratio | OpEx / Revenue | Percentage | lower is better |
| Budget Variance % | (Actual - Budget) / Budget | Percentage | ±5% = amber, > ±10% = red |

### Financial Layout Guidance
- **Waterfall chart** is the hero visual for P&L — shows flow from Revenue down to Net Income
- **Variance bars**: positive variance = blue, negative = orange (avoid red/green for accessibility)
- **Matrix**: use indentation or row headers to show account hierarchy (Revenue → COGS → Gross Profit → …)

## Supply Chain / Logistics
| Page | Type | Key Visuals |
|---|---|---|
| Overview | Standard | KPI cards (fill rate, on-time%, lead time), trend lines |
| Inventory Levels | Standard | Stacked bar (by warehouse), line (days of supply), alerts |
| Supplier Performance | Standard | Scatter (quality vs delivery), ranked bar chart |
| Logistics Tracking | Standard | Map (shipment routes), table (order status), funnel |
| Demand Planning | Detail | Line (forecast vs actual), variance chart, accuracy KPI |
| Shipment Drillthrough | Drillthrough | Shipment milestones, carrier detail, timeline |

### Supply Chain KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| On-Time Delivery % | # On-time shipments / # Total shipments | Percentage | ≥ 95% |
| Fill Rate % | # Items fulfilled / # Items ordered | Percentage | ≥ 98% |
| Lead Time (Avg) | Avg days from order to delivery | Days | lower is better |
| Days of Supply | Current inventory / Avg daily consumption | Days | 15-45 (varies) |
| Supplier Defect Rate | Defective items / Total items received | Percentage | < 1% |
| Perfect Order % | Orders with no errors, on time, complete | Percentage | ≥ 90% |

### Supply Chain Layout Guidance
- **Scatter chart**: X = delivery performance, Y = quality score; quadrant lines divide "star" / "at risk" suppliers
- **Map**: Use route lines for logistics tracking; bubble size = shipment volume

## Retail / FMCG
| Page | Type | Key Visuals |
|---|---|---|
| Store Performance | Standard | Map, ranked bar (revenue by store), KPI cards |
| Category Analysis | Standard | Treemap, combo chart (sales + margin), matrix |
| Basket Analysis | Standard | Scatter (basket size vs frequency), top combos table |
| Promotion Effectiveness | Standard | Before/after bar chart, ROI card, trend |
| Store Drillthrough | Drillthrough | Store details, daily trend, product mix pie/bar |

### Retail KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| Revenue per Store | Total revenue / # Active stores | Currency | vs. PY |
| Same-Store Sales Growth | (Current - PY) / PY for same stores | Percentage | > 0% |
| Basket Size (Avg) | Revenue / # Transactions | Currency | growing trend |
| Items per Transaction | # Items sold / # Transactions | Number | growing trend |
| Shrinkage Rate | (Expected inventory - Actual) / Expected | Percentage | < 2% |
| Promotion ROI | (Incremental revenue - Promo cost) / Promo cost | Percentage | > 100% |

### Retail Layout Guidance
- **Store map**: Bubble size = revenue; color = same-store growth (diverging: blue = growth, orange = decline)
- **Promotion page**: Before/after grouped bar chart; use a clear time separator line

## Healthcare / Pharma
| Page | Type | Key Visuals |
|---|---|---|
| Executive Dashboard | Standard | KPI cards (patient volume, readmission, avg LOS), trend lines |
| Patient Volume | Standard | Line chart (admissions over time), bar by department, map by facility |
| Quality Metrics | Standard | Control chart (infection rate), target gauge (readmission), matrix by unit |
| Financial Performance | Standard | Revenue vs cost combo chart, payor mix donut, margin trend |
| Staff Utilization | Detail | Heatmap (staff:patient ratio by shift), overtime bar, vacancy KPI |
| Patient Drillthrough | Drillthrough | Patient demographics, visit history timeline, diagnosis summary |

### Healthcare KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| Patient Volume | COUNT of admissions or visits | Whole number | vs. capacity |
| Average Length of Stay (ALOS) | Total patient days / # Discharges | Days | varies by department |
| Readmission Rate (30-day) | # Readmissions / # Discharges | Percentage | < 10% |
| Bed Occupancy Rate | Occupied beds / Available beds | Percentage | 75-85% optimal |
| Mortality Rate | # Deaths / # Admissions | Percentage | benchmarked by case mix |
| Revenue per Patient | Total revenue / # Patients | Currency | vs. PY |
| Operating Margin | (Revenue - Expenses) / Revenue | Percentage | > 3-5% |
| Staff-to-Patient Ratio | # Staff on shift / # Patients | Ratio | varies by unit type |

### Healthcare Layout Guidance
- **Quality metrics**: Use control charts with UCL/LCL reference lines for infection and readmission rates
- **Patient volume**: Time series with weekday/weekend patterns; use day-of-week heatmap for staffing insights
- **Color guidance**: Avoid red/green for clinical data (colorblind concern); use blue/orange diverging scales

## Technology / IT Operations
| Page | Type | Key Visuals |
|---|---|---|
| IT Service Overview | Standard | KPI cards (uptime, tickets, MTTR), trend lines |
| Incident Management | Standard | Ticket volume trend, priority bar chart, SLA compliance gauge |
| Infrastructure Monitoring | Standard | Server status card matrix, CPU/memory line charts, alerts table |
| Project Portfolio | Standard | Gantt-style timeline, budget vs actual bar, status funnel |
| Cost Management | Detail | Cloud spend by service treemap, trend line, budget variance bar |
| Incident Drillthrough | Drillthrough | Incident timeline, resolution steps, related alerts table |

### Technology KPI Definitions
| KPI | Formula / Logic | Format | Target Guidance |
|---|---|---|---|
| System Uptime % | (Total time - Downtime) / Total time | Percentage | ≥ 99.9% (SLA) |
| Mean Time to Resolve (MTTR) | AVG(Resolution time) | Hours | varies by priority |
| Open Ticket Count | COUNT of active incidents | Whole number | trending down |
| SLA Compliance % | # Met SLA / # Total tickets | Percentage | ≥ 95% |
| Change Success Rate | # Successful changes / # Total changes | Percentage | ≥ 90% |
| Cloud Spend | SUM of cloud resource costs | Currency | ≤ budget |
| Cost per Transaction | Infrastructure cost / # Transactions | Currency | trending down |
| Project On-Time % | # On-time projects / # Total projects | Percentage | ≥ 80% |

### Technology Layout Guidance
- **Infrastructure page**: Card matrix per server/service — green/amber/red status; auto-refresh every 15 min
- **Incident management**: Priority-based stacked bar; highlight P1/P2 incidents with conditional formatting
- **Cost management**: Treemap by service/resource type; line trend with budget reference line
