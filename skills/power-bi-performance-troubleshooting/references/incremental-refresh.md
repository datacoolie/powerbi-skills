# Incremental Refresh

Configure Power BI to refresh only new/changed data instead of the entire
dataset. Essential for large fact tables where full refresh takes too long
or exceeds gateway/service limits.

---

## When to Use Incremental Refresh

| Scenario | Benefit |
|---|---|
| Fact table > 5M rows | Refreshes only recent partitions |
| Full refresh > 30 minutes | Dramatically reduces refresh time |
| Source database under heavy load | Fewer rows scanned per refresh |
| Near-real-time requirements | Combine with DirectQuery hybrid |
| Data source has query timeout limits | Smaller queries per partition |

### Prerequisites

- Data source must support **query folding** (SQL databases, most OData sources)
- Source table must have a **reliable date/datetime column** for partitioning
- Power BI Pro or Premium/Fabric capacity

---

## RangeStart / RangeEnd Parameters

Incremental refresh relies on two **reserved Power Query parameters**:

### Step 1: Create Parameters

In Power Query Editor → Manage Parameters → New Parameter:

| Parameter | Type | Default Value | Notes |
|---|---|---|---|
| RangeStart | Date/Time | 1/1/2020 12:00:00 AM | Start of range |
| RangeEnd | Date/Time | 1/1/2025 12:00:00 AM | End of range |

**Critical:** Names must be exactly `RangeStart` and `RangeEnd` (case-sensitive).
Type must be `Date/Time` (not Date, not Text).

### Step 2: Filter the Table

Apply the parameters as filters on the date column:

```m
// In Power Query (M language)
let
    Source = Sql.Database("server", "database"),
    Sales = Source{[Schema="dbo", Item="FactSales"]}[Data],
    #"Filtered Rows" = Table.SelectRows(Sales, each
        [OrderDate] >= RangeStart and [OrderDate] < RangeEnd
    )
in
    #"Filtered Rows"
```

**Important:** Use `>=` for RangeStart and `<` (strict) for RangeEnd.
This ensures no rows are duplicated or missed at partition boundaries.

### Step 3: Verify Query Folding

Right-click the last step → **View Native Query**. If the option is grayed out,
query folding is broken and incremental refresh will not work efficiently.

Expected SQL should include a WHERE clause with the date filter:

```sql
SELECT ... FROM [dbo].[FactSales]
WHERE [OrderDate] >= '2024-01-01' AND [OrderDate] < '2024-02-01'
```

---

## Incremental Refresh Policy

Right-click the table in the model → **Incremental refresh and real-time data**:

### Configuration Settings

| Setting | Recommended Value | Notes |
|---|---|---|
| Archive data starting | 3-5 years | How far back to keep data |
| Incrementally refresh starting | 1-30 days | How far back to re-refresh |
| Detect data changes | Optional | Uses a max-date column to skip unchanged partitions |
| Only refresh complete periods | Recommended ON | Avoids partial-day partitions |

### How Partitions Work

Power BI creates time-based partitions automatically:

```
Table: FactSales (3 years of data, monthly partitions)

Partition: 2022-01  [archived — not refreshed]
Partition: 2022-02  [archived — not refreshed]
...
Partition: 2024-10  [archived — not refreshed]
Partition: 2024-11  [incremental — refreshed each time]
Partition: 2024-12  [incremental — refreshed each time]
Partition: 2025-01  [incremental — refreshed each time]
```

Only the incremental window partitions are refreshed. Archived partitions
are left untouched (huge time savings for large datasets).

---

## DirectQuery Hybrid (Real-Time + Import)

For near-real-time scenarios, combine Import partitions with a DirectQuery
partition for the most recent data:

### Configuration

In the incremental refresh dialog:
- ✅ **Get the latest data in real time with DirectQuery**

### How It Works

```
Historical data (2022-2024):  Import partitions (fast, cached)
Recent data (last 30 days):   Import partitions (refreshed daily)
Current data (today):          DirectQuery partition (live from source)
```

**Trade-offs:**
- ✅ Dashboard shows data up to the latest second
- ⚠️ DirectQuery partition adds latency (each query hits the source)
- ⚠️ Source must handle concurrent live queries
- ⚠️ Requires Premium/Fabric capacity

---

## Partition Strategy Decision

| Data Volume | Refresh Window | Partition Granularity |
|---|---|---|
| < 50M rows | Last 7 days | Monthly |
| 50M-500M rows | Last 3 days | Monthly |
| 500M-1B rows | Last 1 day | Daily (use XMLA to verify) |
| > 1B rows | Last 1 day | Daily + aggregation tables |

### Partition Size Guidelines

- **Target:** 1-10M rows per partition
- **Too small** (< 100K rows/partition): Excessive partition overhead
- **Too large** (> 50M rows/partition): Slow individual partition refresh

---

## Monitoring and Troubleshooting

### Check Partition Status (XMLA Endpoint)

Use SQL Server Management Studio (SSMS) or DAX Studio to query partition metadata:

```xml
<!-- SSMS: Right-click table → Partitions → see list of partitions -->
<!-- Check: Last Processed date, Row Count, State -->
```

### Common Issues

| Problem | Cause | Fix |
|---|---|---|
| Full refresh still runs | Query folding broken | Check View Native Query on date filter step |
| Missing recent data | RangeEnd too far back | Verify parameter values and refresh schedule |
| Duplicate rows at boundaries | Wrong filter operator | Use `>=` start, `<` end (not `<=`) |
| Refresh takes same time | Partition strategy wrong | Verify partitions exist (XMLA endpoint) |
| "Cannot determine partitions" error | Parameters named wrong | Must be exactly `RangeStart` / `RangeEnd` (Date/Time type) |
| Historical data disappears | Archive window too short | Increase "Archive data starting" period |

### Detect Data Changes

For large tables where even the incremental window is slow, enable
**Detect data changes** with a column like `LastModifiedDate`:

```
Power BI checks: MAX(LastModifiedDate) per partition
If unchanged since last refresh → skip partition entirely
```

This further reduces refresh time for partitions where data hasn't changed.

---

## Quick Reference

| Configuration | Recommendation |
|---|---|
| RangeStart / RangeEnd type | Date/Time (case-sensitive names) |
| Filter operators | `>=` RangeStart, `<` RangeEnd |
| Query folding | Required — verify with View Native Query |
| Archive window | 3-5 years (match business requirements) |
| Incremental window | 7-30 days (covers late-arriving data) |
| Detect data changes | Enable if source has LastModified column |
| Only refresh complete periods | Enable (avoids partial data) |
| Real-time DirectQuery | Premium/Fabric only; adds source load |
| Monitoring | XMLA endpoint partition metadata |
