# Domain KPI Templates

Detailed KPI definitions, analysis patterns, and measure specifications
per business domain. Use these as starting points during Phase 2 (Domain
Analysis) — customize based on actual business requirements.

Cross-reference: Report page structures per domain are in
`../../power-bi-report-design/references/domain-report-structures.md`.

---

## Sales & Revenue

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| Total Revenue | `SUM(Sales[Amount])` | Currency | vs. budget, PY |
| Revenue Growth YoY | `DIVIDE([Rev] - [Rev PY], [Rev PY])` | % | > 0% = positive |
| Average Order Value | `DIVIDE([Revenue], [# Orders])` | Currency | vs. PY benchmark |
| Customer Acquisition Cost | `DIVIDE([Marketing Spend], [# New Customers])` | Currency | declining trend |
| Customer Lifetime Value | `DIVIDE([Total Revenue by Customer], [# Customers])` | Currency | > CAC |
| Conversion Rate | `DIVIDE([# Won], [# Opportunities])` | % | industry benchmark |
| Gross Margin % | `DIVIDE([Revenue] - [COGS], [Revenue])` | % | > threshold |
| Revenue per Rep | `DIVIDE([Revenue], [# Active Reps])` | Currency | above floor |
| Sales Pipeline Value | `SUM(Pipeline[WeightedAmount])` | Currency | ≥ 3x target |
| Win Rate | `DIVIDE([# Won], [# Closed])` | % | > 25% |

### Required Dimensions
- Date (year, quarter, month, week)
- Product (category, subcategory, SKU)
- Geography (region, country, city)
- Customer (segment, industry, size)
- Sales Rep / Team
- Channel (direct, partner, online)

### Key Analyses
- Time series trend (line) with YoY comparison
- Top-N customers/products (horizontal bar)
- Geographic distribution (filled map)
- Pipeline funnel (funnel chart)
- Cohort retention (matrix with conditional formatting)

---

## FMCG (Fast-Moving Consumer Goods)

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| Net Revenue | `SUM(Sales[NetAmount])` | Currency | vs. budget |
| Volume (Units) | `SUM(Sales[Quantity])` | #,##0 | vs. PY |
| Gross Margin % | `DIVIDE([Net Revenue] - [COGS], [Net Revenue])` | % | > category avg |
| Market Share | `DIVIDE([Brand Sales], [Category Sales])` | % | growing |
| Distribution (Weighted) | `SUMX(Store, [StoreRevShare] * [HasProduct])` | % | > 80% |
| Trade Spend ROI | `DIVIDE([Incremental Revenue], [Trade Spend])` | #,##0.0 | > 1.5 |
| Promotion Uplift | `DIVIDE([Promo Sales] - [Baseline], [Baseline])` | % | > 20% |
| Out-of-Stock Rate | `DIVIDE([# OOS Events], [# Store-SKU-Days])` | % | < 3% |
| Days of Inventory | `DIVIDE([Avg Inventory], [Daily Consumption])` | #,##0 | 15-30 days |
| Revenue per Store | `DIVIDE([Net Revenue], [# Active Stores])` | Currency | growing |

### Required Dimensions
- Date, Product (brand, category, SKU), Channel (modern/general trade, e-commerce)
- Customer / Retailer, Geography, Promotion (type, period, mechanic)

### Key Analyses
- Brand/SKU performance waterfall, promotion pre/during/post comparison
- Channel mix (stacked bar), distribution gap analysis, seasonal demand patterns

---

## Manufacturing & Operations

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| OEE | `[Availability] * [Performance] * [Quality]` | % | ≥ 85% world-class |
| Production Volume | `SUM(Production[GoodUnits])` | #,##0 | ≥ plan |
| Yield Rate | `DIVIDE([Good Units], [Total Units])` | % | > 95% |
| Defect Rate | `DIVIDE([Defective Units], [Total Units])` | % | < 1% |
| Downtime Hours | `SUM(Downtime[Duration])` | #,##0.0 | < threshold |
| MTBF | `DIVIDE([Operating Hours], [# Failures])` | #,##0 hrs | higher = better |
| MTTR | `DIVIDE([Total Repair Time], [# Repairs])` | #,##0 hrs | lower = better |
| Cycle Time | `AVERAGE(Production[CycleMinutes])` | #,##0 min | ≤ standard |
| Scrap Rate | `DIVIDE([Scrap Weight], [Total Material])` | % | < 2% |
| Energy per Unit | `DIVIDE([Energy Consumed], [Units Produced])` | #,##0.0 | declining |

### Required Dimensions
- Date, Machine/Equipment, Production Line, Shift
- Product, Material, Defect Type, Downtime Reason

### Key Analyses
- OEE decomposition (availability × performance × quality breakdown)
- Pareto of defect causes, machine utilization heatmap (shift × line)
- Downtime category analysis, production trend by line

---

## Supply Chain & Logistics

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| On-Time Delivery % | `DIVIDE([# On-Time], [# Total Shipments])` | % | ≥ 95% |
| Fill Rate % | `DIVIDE([Fulfilled Qty], [Ordered Qty])` | % | ≥ 98% |
| Avg Lead Time | `AVERAGE(Orders[LeadTimeDays])` | #,##0 days | declining |
| Inventory Turnover | `DIVIDE([COGS], [Avg Inventory])` | #,##0.0x | industry norm |
| Days of Supply | `DIVIDE([Current Inventory], [Avg Daily Consumption])` | #,##0 | 15-45 |
| Perfect Order % | `DIVIDE([# Perfect Orders], [# Total Orders])` | % | ≥ 90% |
| Freight Cost/Unit | `DIVIDE([Total Freight], [Total Units])` | Currency | declining |
| Supplier Defect Rate | `DIVIDE([Defective Items], [Total Received])` | % | < 1% |
| Forecast Accuracy | `1 - ABS([Actual] - [Forecast]) / [Actual]` | % | > 80% |
| Warehouse Utilization | `DIVIDE([Used Capacity], [Total Capacity])` | % | 75-85% |

### Required Dimensions
- Date, Supplier, Warehouse/DC, Product, Carrier/Route
- Order Priority, Shipment Status, Region

### Key Analyses
- Supplier scatter (quality vs delivery), inventory aging stacked bar
- Route cost comparison, demand vs supply gap chart, forecast accuracy trend

---

## Financial / P&L

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| Revenue | `SUM(GL[Amount]) for revenue accounts` | Currency | vs. budget |
| COGS | `SUM(GL[Amount]) for COGS accounts` | Currency | < budget |
| Gross Profit | `[Revenue] - [COGS]` | Currency | vs. budget |
| EBITDA | `[Gross Profit] - [OpEx] + [D&A]` | Currency | margin > 15% |
| Net Income | `[EBITDA] - [Interest] - [Tax]` | Currency | vs. PY |
| Gross Margin % | `DIVIDE([Gross Profit], [Revenue])` | % | > industry avg |
| OpEx Ratio | `DIVIDE([OpEx], [Revenue])` | % | declining |
| Budget Variance % | `DIVIDE([Actual] - [Budget], [Budget])` | % | ±5% amber |
| Working Capital Ratio | `[Current Assets] / [Current Liabilities]` | #,##0.0 | 1.5-2.0 |
| Cash Conversion Cycle | `[DSO] + [DIO] - [DPO]` | #,##0 days | declining |

### Required Dimensions
- Date (fiscal year, period, month), Account (hierarchy: group→subgroup→account)
- Department/Cost Center, Entity/Company, Scenario (Actual, Budget, Forecast)

### Key Analyses
- P&L waterfall (revenue → costs → profit), variance bar chart (actual vs budget)
- Expense trend by category, department comparison matrix, rolling forecast

---

## Retail

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| Net Sales | `[Gross Sales] - [Returns] - [Discounts]` | Currency | vs. PY |
| Same-Store Growth | YoY for stores open > 12 months | % | > 0% |
| Basket Size | `DIVIDE([# Items], [# Transactions])` | #,##0.0 | growing |
| Avg Transaction Value | `DIVIDE([Net Sales], [# Transactions])` | Currency | growing |
| Footfall | `SUM(Traffic[Visits])` | #,##0 | vs. PY |
| Conversion Rate | `DIVIDE([# Transactions], [Footfall])` | % | improving |
| Shrinkage Rate | `DIVIDE([Expected] - [Actual], [Expected])` | % | < 2% |
| Sell-Through Rate | `DIVIDE([Sold], [Sold] + [Remaining])` | % | > 70% |
| Promotion ROI | `DIVIDE([Incremental Rev] - [Promo Cost], [Promo Cost])` | % | > 100% |
| Sales per Sq Ft | `DIVIDE([Net Sales], [Store Sq Ft])` | Currency | vs. benchmark |

### Required Dimensions
- Date, Store (format, region, size), Product (category, brand, SKU)
- Customer (loyalty tier, segment), Promotion (type, period)

### Key Analyses
- Store ranking bar chart, category treemap, hourly sales heatmap
- Promotion before/after comparison, customer segmentation scatter

---

## Procurement

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| Total Spend | `SUM(PO[Amount])` | Currency | ≤ budget |
| # Purchase Orders | `DISTINCTCOUNT(PO[POID])` | #,##0 | trend |
| Avg PO Value | `DIVIDE([Total Spend], [# POs])` | Currency | stable |
| Savings % | `DIVIDE([Budget] - [Actual], [Budget])` | % | > target |
| Contract Compliance | `DIVIDE([Compliant POs], [Total POs])` | % | > 90% |
| PO Cycle Time | `AVERAGE(PO[RequestToApprovalDays])` | #,##0 days | declining |
| Maverick Spend % | `DIVIDE([Off-Contract Spend], [Total Spend])` | % | < 10% |
| Supplier Count | `DISTINCTCOUNT(PO[SupplierID])` | #,##0 | consolidating |
| Spend Under Mgmt | `DIVIDE([Managed Spend], [Total Spend])` | % | > 80% |
| Invoice Accuracy | `DIVIDE([Correct Invoices], [Total Invoices])` | % | > 95% |

### Required Dimensions
- Date, Supplier, Category (UNSPSC or custom), Department, Contract

### Key Analyses
- Spend treemap by category, supplier ranking bar, savings waterfall
- Contract utilization rate, PO process timeline, maverick spend trend

---

## Healthcare / Pharma

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| Patient Volume | `COUNT(Visits[VisitID])` | #,##0 | vs. capacity |
| Avg Length of Stay | `DIVIDE([Patient Days], [# Discharges])` | #,##0.0 days | by dept benchmark |
| Readmission Rate (30d) | `DIVIDE([# Readmissions], [# Discharges])` | % | < 10% |
| Bed Occupancy | `DIVIDE([Occupied Bed-Days], [Available Bed-Days])` | % | 75-85% |
| Mortality Rate | `DIVIDE([# Deaths], [# Admissions])` | % | case-mix adjusted |
| Revenue per Patient | `DIVIDE([Revenue], [# Patients])` | Currency | vs. PY |
| Operating Margin | `DIVIDE([Revenue] - [Expenses], [Revenue])` | % | > 3% |
| Staff:Patient Ratio | `DIVIDE([# Staff], [# Patients])` | #,##0.0 | by unit type |
| Wait Time (Avg) | `AVERAGE(Visits[WaitMinutes])` | #,##0 min | declining |
| Patient Satisfaction | `AVERAGE(Surveys[Score])` | #,##0.0 | > 4.0/5 |

### Required Dimensions
- Date, Department/Unit, Facility, Diagnosis (ICD code), Payor (insurance type)
- Provider, Patient Demographics (age group, gender — anonymized)

### Key Analyses
- Patient volume trend (line) with weekday/weekend patterns
- Quality metrics control charts (readmission, infection rates)
- Payor mix (donut), department comparison matrix, staffing heatmap

---

## Technology / IT Operations

### KPI Definitions

| KPI | DAX Pattern | Format | Target Logic |
|---|---|---|---|
| System Uptime % | `DIVIDE([Total Time] - [Downtime], [Total Time])` | % | ≥ 99.9% |
| MTTR | `AVERAGE(Incidents[ResolutionHours])` | #,##0.0 hrs | by priority |
| Open Tickets | `CALCULATE(COUNT(Tickets[ID]), Tickets[Status] = "Open")` | #,##0 | trending down |
| SLA Compliance % | `DIVIDE([# Met SLA], [# Total Tickets])` | % | ≥ 95% |
| Change Success Rate | `DIVIDE([# Successful Changes], [# Total Changes])` | % | ≥ 90% |
| Cloud Spend | `SUM(CloudCosts[Amount])` | Currency | ≤ budget |
| Cost per Transaction | `DIVIDE([Infra Cost], [# Transactions])` | Currency | declining |
| Project On-Time % | `DIVIDE([# On-Time], [# Total Projects])` | % | ≥ 80% |
| Deployment Frequency | `COUNT(Deployments[ID]) per period` | #,##0 | increasing (DevOps) |
| Security Incidents | `COUNT(SecurityEvents[ID])` | #,##0 | declining |

### Required Dimensions
- Date, Service/Application, Severity/Priority, Team/Owner
- Infrastructure (server, region, cloud provider), Project, Ticket Category

### Key Analyses
- Incident trend by priority (stacked area), SLA compliance gauge
- Infrastructure health card matrix (green/amber/red), cloud cost treemap
- Project portfolio timeline, deployment frequency trend
