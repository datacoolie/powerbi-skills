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
