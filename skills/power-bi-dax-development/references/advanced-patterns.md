# Advanced DAX Patterns

Real-world DAX patterns for complex business scenarios. Based on patterns
from "The Definitive Guide to DAX" (Ferrari & Russo).

---

## New vs. Returning Customers

Classify customers based on whether they appeared in the prior period.

```dax
-- New customers: purchased in current period but NOT in previous year
# New Customers =
VAR _currentCustomers = VALUES(FactSales[CustomerKey])
VAR _priorYearCustomers =
    CALCULATETABLE(
        VALUES(FactSales[CustomerKey]),
        DATESINPERIOD(DimDate[Date], MIN(DimDate[Date]) - 1, -1, YEAR)
    )
VAR _newCustomers = EXCEPT(_currentCustomers, _priorYearCustomers)
RETURN
    COUNTROWS(_newCustomers)

-- Sales from new customers
Sales New Customers =
VAR _currentCustomers = VALUES(FactSales[CustomerKey])
VAR _priorYearCustomers =
    CALCULATETABLE(
        VALUES(FactSales[CustomerKey]),
        DATESINPERIOD(DimDate[Date], MIN(DimDate[Date]) - 1, -1, YEAR)
    )
VAR _newCustomers = EXCEPT(_currentCustomers, _priorYearCustomers)
RETURN
    CALCULATE([Total Sales], KEEPFILTERS(_newCustomers))

-- Returning customers: purchased in BOTH current and prior period
# Returning Customers =
VAR _currentCustomers = VALUES(FactSales[CustomerKey])
VAR _priorYearCustomers =
    CALCULATETABLE(
        VALUES(FactSales[CustomerKey]),
        DATESINPERIOD(DimDate[Date], MIN(DimDate[Date]) - 1, -1, YEAR)
    )
VAR _returningCustomers = INTERSECT(_currentCustomers, _priorYearCustomers)
RETURN
    COUNTROWS(_returningCustomers)

-- Lost customers: purchased last year but NOT this year
# Lost Customers =
VAR _currentCustomers = VALUES(FactSales[CustomerKey])
VAR _priorYearCustomers =
    CALCULATETABLE(
        VALUES(FactSales[CustomerKey]),
        DATESINPERIOD(DimDate[Date], MIN(DimDate[Date]) - 1, -1, YEAR)
    )
RETURN
    COUNTROWS(EXCEPT(_priorYearCustomers, _currentCustomers))
```

---

## ABC / Pareto Analysis

Classify items (products, customers) into A/B/C categories based on their
cumulative contribution to total.

```dax
-- Step 1: Rank products by sales
Product Rank =
VAR _productSales = [Total Sales]
RETURN
    IF(
        HASONEVALUE(DimProduct[ProductKey]),
        COUNTROWS(
            FILTER(
                ALLSELECTED(DimProduct[ProductKey]),
                [Total Sales] > _productSales
            )
        ) + 1
    )

-- Step 2: Cumulative % (running total as % of visible total)
Cumulative % =
VAR _productSales = [Total Sales]
VAR _cumulativeSales =
    SUMX(
        FILTER(
            ALLSELECTED(DimProduct[ProductKey]),
            [Total Sales] >= _productSales
        ),
        [Total Sales]
    )
VAR _totalSales = CALCULATE([Total Sales], ALLSELECTED(DimProduct))
RETURN
    DIVIDE(_cumulativeSales, _totalSales)

-- Step 3: ABC classification
ABC Class =
VAR _cumPct = [Cumulative %]
RETURN
    SWITCH(
        TRUE(),
        _cumPct <= 0.70, "A",
        _cumPct <= 0.90, "B",
        "C"
    )
```

---

## Dynamic Segmentation

Segment data using a disconnected parameter table (not linked to any model table).

### Setup: Create a disconnected segment table

```dax
-- Calculation table or imported table:
SalesSegment =
DATATABLE(
    "Segment", STRING,
    "MinValue", CURRENCY,
    "MaxValue", CURRENCY,
    {
        {"Low", 0, 100},
        {"Medium", 100, 500},
        {"High", 500, 1000},
        {"Premium", 1000, 99999999}
    }
)
```

### Measures

```dax
-- Count customers in each segment (uses SUMX over disconnected table)
# Customers in Segment =
SUMX(
    SalesSegment,
    VAR _min = SalesSegment[MinValue]
    VAR _max = SalesSegment[MaxValue]
    RETURN
        COUNTROWS(
            FILTER(
                VALUES(DimCustomer[CustomerKey]),
                VAR _custSales = [Total Sales]
                RETURN _custSales > _min && _custSales <= _max
            )
        )
)

-- Sales by segment
Sales by Segment =
SUMX(
    SalesSegment,
    VAR _min = SalesSegment[MinValue]
    VAR _max = SalesSegment[MaxValue]
    RETURN
        CALCULATE(
            [Total Sales],
            FILTER(
                VALUES(DimCustomer[CustomerKey]),
                VAR _custSales = [Total Sales]
                RETURN _custSales > _min && _custSales <= _max
            )
        )
)
```

---

## Many-to-Many Relationships

When a fact table relates to a dimension through a bridge table (one fact
can have multiple dimension values).

### Pattern: Bridge Table

```
FactSales [M]---[1] BridgeProdCat [1]---[M] DimCategory
```

```dax
-- Sales distributed across all matching categories
Sales by Category =
CALCULATE(
    [Total Sales],
    BridgeProdCat
)
-- The bridge table acts as a filter propagator

-- Unique count in many-to-many (avoid double-counting)
# Products in Category =
CALCULATE(
    DISTINCTCOUNT(FactSales[ProductKey]),
    BridgeProdCat
)
```

### Pattern: TREATAS Virtual Relationship

When you cannot create a physical bridge table:

```dax
-- Create virtual relationship using TREATAS
Sales via Mapping =
CALCULATE(
    [Total Sales],
    TREATAS(
        SUMMARIZE(MappingTable, MappingTable[ProductKey]),
        FactSales[ProductKey]
    )
)
```

---

## Parent-Child Hierarchies

For organizational charts, chart of accounts, or bill of materials where
parent-child relationships exist within one table.

### PATH Functions

```dax
-- Calculated column: build the full path
Employee[FullPath] = PATH(Employee[EmployeeKey], Employee[ManagerKey])
-- Result: "1|5|12|48" (root to current)

-- Calculated column: extract level values
Employee[Level1] =
    LOOKUPVALUE(
        Employee[Name],
        Employee[EmployeeKey],
        PATHITEM(Employee[FullPath], 1, INTEGER)
    )

Employee[Level2] =
    LOOKUPVALUE(
        Employee[Name],
        Employee[EmployeeKey],
        PATHITEM(Employee[FullPath], 2, INTEGER)
    )

-- Depth of the node
Employee[Depth] = PATHLENGTH(Employee[FullPath])

-- Is this a leaf node?
Employee[IsLeaf] =
    ISEMPTY(FILTER(ALL(Employee), Employee[ManagerKey] = Employee[EmployeeKey]))
```

### Aggregating Up the Hierarchy

```dax
-- Sum for current node and all descendants
Total Team Sales =
SUMX(
    FILTER(
        ALL(Employee),
        PATHCONTAINS(Employee[FullPath], SELECTEDVALUE(Employee[EmployeeKey]))
    ),
    [Direct Sales]
)
```

---

## Budget Allocation / Weighted Distribution

Distribute budget or target values from a higher granularity (e.g., monthly
budget) down to daily granularity based on a weight factor.

```dax
-- Allocate monthly budget to daily based on historical daily sales weight
Daily Budget Allocation =
VAR _monthlyBudget =
    CALCULATE(
        SUM(FactBudget[BudgetAmount]),
        ALLEXCEPT(DimDate, DimDate[YearMonth])
    )
VAR _monthlyHistorical =
    CALCULATE(
        [Total Sales],
        ALLEXCEPT(DimDate, DimDate[YearMonth])
    )
VAR _todaySales = [Total Sales]
RETURN
    DIVIDE(_todaySales, _monthlyHistorical) * _monthlyBudget
```

---

## Ratio to Parent (Hierarchy-Aware Measure)

Shows each item as a percentage of its parent in a hierarchy:

```dax
% of Parent =
VAR _currentSales = [Total Sales]
RETURN
    SWITCH(
        TRUE(),
        ISINSCOPE(DimProduct[Product]),
            DIVIDE(_currentSales,
                CALCULATE([Total Sales], ALLSELECTED(DimProduct[Product]))),
        ISINSCOPE(DimProduct[SubCategory]),
            DIVIDE(_currentSales,
                CALCULATE([Total Sales], ALLSELECTED(DimProduct[SubCategory]))),
        ISINSCOPE(DimProduct[Category]),
            DIVIDE(_currentSales,
                CALCULATE([Total Sales], ALLSELECTED(DimProduct[Category]))),
        1  -- At grand total level
    )
```

**ISINSCOPE** returns TRUE when the column is used to group data at the
current level in a matrix visual. It allows a single measure to behave
differently at each hierarchy level.

---

## Snapshot / Latest Value Across Dimensions

When you need the "latest known value" for each item across a dimension:

```dax
-- Latest price for each product
Current Price =
CALCULATE(
    SELECTEDVALUE(FactPriceHistory[Price]),
    LASTNONBLANK(
        DimDate[Date],
        CALCULATE(COUNTROWS(FactPriceHistory))
    )
)
```

---

## Top N with "Others" Bucket

Show top N items plus an "Others" row aggregating everything else:

```dax
-- In a calculated table or measure:
Sales Top 5 =
VAR _top5 =
    TOPN(5, ALLSELECTED(DimProduct[ProductName]), [Total Sales], DESC)
VAR _isTop5 =
    CONTAINS(_top5, DimProduct[ProductName], SELECTEDVALUE(DimProduct[ProductName]))
RETURN
    IF(
        HASONEVALUE(DimProduct[ProductName]),
        IF(_isTop5, [Total Sales])
    )

Sales Others =
VAR _top5 =
    TOPN(5, ALLSELECTED(DimProduct[ProductName]), [Total Sales], DESC)
RETURN
    CALCULATE(
        [Total Sales],
        EXCEPT(ALLSELECTED(DimProduct[ProductName]), _top5)
    )
```

---

## WINDOW, INDEX, and OFFSET Functions

These functions (introduced in late 2022/2023) enable row-level calculations
within a window of rows — similar to SQL window functions. They operate
over a **relation** (table expression) and use an **orderBy** clause to
define the sort/partition.

> **Always search Microsoft Learn** before using these functions — syntax and
> behavior may have been updated since this reference was written.

### OFFSET — Access a Row at a Fixed Distance

Returns a single row from a relation, offset from the current row.

```dax
-- Previous month's sales (like LAG in SQL)
Previous Month Sales =
CALCULATE(
    [Total Sales],
    OFFSET(
        -1,
        ALLSELECTED(DimDate[YearMonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[YearMonthNumber], ASC)
    )
)

-- Next month's sales (like LEAD in SQL)
Next Month Sales =
CALCULATE(
    [Total Sales],
    OFFSET(
        1,
        ALLSELECTED(DimDate[YearMonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[YearMonthNumber], ASC)
    )
)

-- Month-over-Month change
MoM Change % =
VAR _current = [Total Sales]
VAR _previous = [Previous Month Sales]
RETURN
    DIVIDE(_current - _previous, _previous)
```

**Syntax:** `OFFSET(delta, relation[, orderBy[, blanks[, partitionBy]]])`

- `delta`: Integer offset (-1 = previous row, +1 = next row)
- `relation`: Table expression defining the set of rows (use ALLSELECTED for visual context)
- `orderBy`: ORDERBY() clause defining sort
- `blanks`: Optional — `KEEP` (default) or `DEFAULT`
- `partitionBy`: Optional — PARTITIONBY() clause to restart offsets per partition

### INDEX — Access a Row by Absolute Position

Returns a single row from a relation at a specific ordinal position.

```dax
-- First month's sales in the visible range
First Month Sales =
CALCULATE(
    [Total Sales],
    INDEX(
        1,
        ALLSELECTED(DimDate[YearMonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[YearMonthNumber], ASC)
    )
)

-- Last row (use -1 for the last position)
Last Month Sales =
CALCULATE(
    [Total Sales],
    INDEX(
        -1,
        ALLSELECTED(DimDate[YearMonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[YearMonthNumber], ASC)
    )
)

-- Growth vs. first month (index to base period)
Growth vs First Month % =
VAR _current = [Total Sales]
VAR _first = [First Month Sales]
RETURN
    DIVIDE(_current - _first, _first)
```

**Syntax:** `INDEX(position, relation[, orderBy[, blanks[, partitionBy]]])`

- `position`: 1-based ordinal position (negative = from end; -1 = last row)

### WINDOW — Access a Range of Rows

Returns a set of rows from a relation between two boundary positions.
Boundaries can be absolute (from start/end) or relative (from current row).

```dax
-- 3-month rolling average
Rolling 3M Avg Sales =
VAR _rollingTable =
    WINDOW(
        -2, REL,
        0, REL,
        ALLSELECTED(DimDate[YearMonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[YearMonthNumber], ASC)
    )
RETURN
    AVERAGEX(_rollingTable, [Total Sales])

-- Year-to-date using WINDOW (alternative to TOTALYTD)
YTD Sales (Window) =
VAR _ytdRows =
    WINDOW(
        1, ABS,
        0, REL,
        ALLSELECTED(DimDate[MonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[MonthNumber], ASC),
        PARTITIONBY(DimDate[Year])
    )
RETURN
    SUMX(_ytdRows, [Total Sales])

-- Running total
Running Total Sales =
VAR _runningRows =
    WINDOW(
        1, ABS,
        0, REL,
        ALLSELECTED(DimDate[YearMonthNumber], DimDate[YearMonth]),
        ORDERBY(DimDate[YearMonthNumber], ASC)
    )
RETURN
    SUMX(_runningRows, [Total Sales])
```

**Syntax:** `WINDOW(from, from_type, to, to_type, relation[, orderBy[, blanks[, partitionBy]]])`

- `from` / `to`: Integer boundary positions
- `from_type` / `to_type`: `REL` (relative to current row) or `ABS` (1-based from start; negative from end)

### PARTITIONBY — Restart Calculations per Group

Used with OFFSET, INDEX, or WINDOW to restart the window per partition.

```dax
-- Previous month sales, restarting for each product category
Previous Month Sales by Category =
CALCULATE(
    [Total Sales],
    OFFSET(
        -1,
        ALLSELECTED(
            DimDate[YearMonthNumber],
            DimDate[YearMonth],
            DimProduct[Category]
        ),
        ORDERBY(DimDate[YearMonthNumber], ASC),
        PARTITIONBY(DimProduct[Category])
    )
)

-- Rank within category (dense rank using INDEX)
Rank in Category =
VAR _currentSales = [Total Sales]
RETURN
    COUNTROWS(
        FILTER(
            ALLSELECTED(DimProduct[ProductName]),
            [Total Sales] >= _currentSales
        )
    )
```

### When to Use WINDOW Functions vs. Traditional Patterns

| Scenario | Traditional (pre-2023) | Window Functions |
|---|---|---|
| Previous period value | CALCULATE + DATEADD / SAMEPERIODLASTYEAR | OFFSET(-1) |
| Running total | CALCULATE + DATESBETWEEN / DATESYTD | WINDOW(1, ABS, 0, REL) |
| Moving average | AVERAGEX + DATESINPERIOD | WINDOW(-N, REL, 0, REL) |
| First/last value | CALCULATE + FIRSTDATE/LASTDATE | INDEX(1) / INDEX(-1) |
| Row-by-row comparison | Nested iterators | OFFSET with PARTITIONBY |

**Guidance**: WINDOW/INDEX/OFFSET produce cleaner, more readable DAX for these
scenarios but require the tabular model to be at compatibility level 1601+
(December 2022+). For maximum backwards compatibility, use the traditional
patterns. For new models, prefer window functions when they simplify the logic.
