# Star Schema Design Checklist

Use this checklist to validate a star schema design before building in Power BI.

## Pre-Design Validation

```
□ Business requirements are defined (KPIs, audiences, decisions)
□ Data sources are identified and accessible
□ Grain of fact table(s) is determined (what does one row represent?)
□ Date range and refresh requirements are clear
```

## 1. Fact Table Validation

For each fact table, verify:

```
□ Table name clearly indicates it's a fact (e.g., FactSales, FactOrders, FactProduction)
□ Each row represents a single business event at the defined grain
□ Grain is consistent — no mixed granularity in one table
□ Contains foreign key columns linking to each relevant dimension
□ Contains numeric measure columns suitable for aggregation (SUM, AVG, COUNT)
□ Contains date/time key(s) linking to the Date dimension
□ No descriptive/text columns that belong in a dimension
□ No duplicate rows (for the defined grain)
□ No pre-aggregated totals or subtotals (unless aggregation table)
□ Row count is known and capacity is sufficient
```

## 2. Dimension Table Validation

For each dimension table, verify:

```
□ Contains a unique key column (surrogate integer key preferred)
□ Contains descriptive attributes used for filtering and grouping
□ Supports required hierarchies (e.g., Category → Subcategory → Product)
□ Sort-by columns exist for display columns (MonthName sorted by MonthNumber)
□ No measure-like columns (use fact table or DAX measures instead)
□ No foreign keys to other dimensions (avoid snowflaking)
□ Relatively small row count compared to fact tables
□ Complete — no missing members that would cause orphaned fact records
```

## 3. Date Dimension Validation

The Date table is REQUIRED for time intelligence — and has 5 non-negotiable requirements:

```
5 Requirements (time intelligence fails without all 5):
□ Contains one row per calendar date (no gaps — contiguous)
□ Date column is DATE type — no time component (must be stripped)
□ DateKey column is INT (YYYYMMDD format) — use as the relationship key
□ Marked as the Date Table key (using calendar_operations)
□ Covers the full range of dates in all fact tables (plus buffer)

Additional columns:
□ Year, Quarter, Month, Week, Day columns present
□ MonthName has SortByColumn = MonthNumber
□ QuarterLabel has SortByColumn = QuarterNumber
□ Fiscal calendar columns present if business uses fiscal year
□ Helper columns: IsCurrentMonth, IsCurrentYear, IsWeekend
□ Auto Date/Time is DISABLED at model level
□ Auto-generated LocalDateTable_* tables are removed
```

## 4. Relationship Validation

```
□ Every fact table has at least one relationship to a dimension
□ Every dimension connects directly to fact tables (no chains Dim→Dim→Fact)
□ All relationships are One-to-Many (dimension 1 → fact M)
□ Cross-filter direction is Single (dimension → fact) by default
□ No circular relationship paths
□ No redundant relationships (two paths to same tables)
□ Foreign key columns in fact tables are hidden from report view
□ Inactive relationships are documented (for USERELATIONSHIP usage)
□ Many-to-Many relationships use proper bridge tables (not native M:M)
□ Referential integrity is enabled for Import mode tables
```

## 5. Model Organization

```
□ Measure table(s) exist for organizing measures (e.g., _Measures, _Sales KPI)
□ All measures are in measure tables (not scattered across fact/dim tables)
□ Display folders organize columns within tables
□ Key columns are hidden from report view
□ Table and column names are business-friendly (not technical source names)
□ Descriptions are set for measures and important columns
□ Perspectives defined if model serves multiple audiences (optional)
```

## 6. Performance Validation

VertiPaq compression is driven by column cardinality. Prioritize checks in this order:

```
Priority 1 — Reduce cardinality (biggest compression impact):
□ Remove unused columns entirely (not just hidden — hidden still consume memory)
□ Split DateTime columns into Date + Time (DateTime has high cardinality as a key)
□ Round decimal measures to business-needed precision (fewer distinct values)
□ Group rare categories into an "Other" bucket where possible
□ Bin continuous numeric values (e.g., price ranges) for dimension use

Priority 2 — Use optimal types:
□ Int64 keys, not Text (value encoding vs. hash encoding — directly affects speed)
□ DATE type for date columns, not DATETIME (strips time component)
□ No calculated columns on large fact tables (blocks RLE compression)
□ Prefer Power Query transformations over calculated columns

Priority 3 — Model-level checks:
□ Model size is within capacity limits (< 1GB shared, < 10GB Premium)
□ Aggregation tables present for very large models (>100M rows)
□ Incremental refresh configured for growing fact tables
□ Storage modes are appropriate per table (see storage-mode-decision.md)
□ See references/veritpaq-optimization.md for deep-dive guidance
```

## 7. Security Validation

```
□ RLS roles defined for required access patterns
□ RLS filters use efficient DAX expressions
□ Dynamic RLS uses USERPRINCIPALNAME() where appropriate
□ RLS tested with DAX queries (powerbi-modeling-mcp/dax_query_operations)
□ No data leakage through unfiltered tables
□ Security mapping table exists for dynamic RLS (if needed)
```

## Post-Validation Summary

```
Model Summary:
├── Fact Tables: [count] ([total rows])
├── Dimension Tables: [count]
├── Bridge Tables: [count]
├── Measure Tables: [count] ([total measures])
├── Relationships: [count] (active) + [count] (inactive)
├── Storage Mode: [Import / DirectQuery / DirectLake / Composite]
├── RLS Roles: [count]
├── Estimated Model Size: [size]
└── Status: [✅ PASS / ⚠️ WARNINGS / ❌ ISSUES]
```
