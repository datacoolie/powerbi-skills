# Time Intelligence DAX Patterns

Ready-to-use DAX patterns for common time intelligence calculations.
All patterns assume a proper Date dimension (`DimDate`) with a `Date` column
marked as the date table key.

## Prerequisites

- Date table marked with `calendar_operations` (Mark as Date Table)
- Date column is of Date/DateTime data type
- Date table has no gaps in the date range
- Auto Date/Time is DISABLED

---

## Year-to-Date (YTD)

```dax
YTD Sales =
TOTALYTD([Total Sales], DimDate[Date])

-- With fiscal year ending March 31
YTD Sales (Fiscal) =
TOTALYTD([Total Sales], DimDate[Date], "3/31")
```

## Quarter-to-Date (QTD)

```dax
QTD Sales =
TOTALQTD([Total Sales], DimDate[Date])
```

## Month-to-Date (MTD)

```dax
MTD Sales =
TOTALMTD([Total Sales], DimDate[Date])
```

---

## Previous Period Comparisons

### Previous Year (PY)

```dax
PY Sales =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)
```

### Previous Month

```dax
PM Sales =
CALCULATE(
    [Total Sales],
    DATEADD(DimDate[Date], -1, MONTH)
)
```

### Previous Quarter

```dax
PQ Sales =
CALCULATE(
    [Total Sales],
    DATEADD(DimDate[Date], -1, QUARTER)
)
```

### Previous Day (for daily reports)

```dax
Yesterday Sales =
CALCULATE(
    [Total Sales],
    DATEADD(DimDate[Date], -1, DAY)
)
```

---

## Year-over-Year (YoY)

```dax
YoY Sales =
[Total Sales] - [PY Sales]

YoY Sales % =
VAR _current = [Total Sales]
VAR _previous = [PY Sales]
RETURN
    DIVIDE(_current - _previous, _previous)
```

## Month-over-Month (MoM)

```dax
MoM Sales =
[Total Sales] - [PM Sales]

MoM Sales % =
VAR _current = [Total Sales]
VAR _previous = [PM Sales]
RETURN
    DIVIDE(_current - _previous, _previous)
```

---

## Rolling / Moving Averages

### Rolling 3-Month Average

```dax
Rolling 3M Avg Sales =
AVERAGEX(
    DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -3, MONTH),
    [Total Sales]
)
```

### Rolling 12-Month Total

```dax
Rolling 12M Sales =
CALCULATE(
    [Total Sales],
    DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -12, MONTH)
)
```

### Rolling 7-Day Average (for daily data)

```dax
Rolling 7D Avg Sales =
AVERAGEX(
    DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -7, DAY),
    [Total Sales]
)
```

---

## Running Total

```dax
-- Running total within selected date range
RT Sales =
CALCULATE(
    [Total Sales],
    FILTER(
        ALLSELECTED(DimDate[Date]),
        DimDate[Date] <= MAX(DimDate[Date])
    )
)
```

---

## Period Parallel (Year-over-Year with Period to Date)

```dax
-- YTD of Previous Year (for YTD YoY comparison)
PY YTD Sales =
CALCULATE(
    [YTD Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

-- YTD YoY %
YTD YoY Sales % =
VAR _current = [YTD Sales]
VAR _previous = [PY YTD Sales]
RETURN
    DIVIDE(_current - _previous, _previous)
```

---

## Last N Periods

### Last Completed Month

```dax
Last Month Sales =
VAR _maxDate = MAX(DimDate[Date])
VAR _lastMonthEnd = EOMONTH(_maxDate, -1)
VAR _lastMonthStart = DATE(YEAR(_lastMonthEnd), MONTH(_lastMonthEnd), 1)
RETURN
    CALCULATE(
        [Total Sales],
        DimDate[Date] >= _lastMonthStart && DimDate[Date] <= _lastMonthEnd
    )
```

### Same Month Last Year

```dax
SMLY Sales =
CALCULATE(
    [Total Sales],
    PARALLELPERIOD(DimDate[Date], -12, MONTH)
)
```

---

## Opening and Closing Balances (for inventory/balance data)

```dax
Opening Balance =
OPENINGBALANCEMONTH([Inventory Level], DimDate[Date])

Closing Balance =
CLOSINGBALANCEMONTH([Inventory Level], DimDate[Date])

Opening Balance Year =
OPENINGBALANCEYEAR([Inventory Level], DimDate[Date])

Closing Balance Year =
CLOSINGBALANCEYEAR([Inventory Level], DimDate[Date])
```

---

## Days in Period / Working Days

```dax
# Days in Month =
VAR _date = MAX(DimDate[Date])
RETURN
    DAY(EOMONTH(_date, 0))

# Elapsed Days =
VAR _startOfMonth = DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])), 1)
VAR _today = MAX(DimDate[Date])
RETURN
    INT(_today - _startOfMonth) + 1

-- Daily run rate extrapolation
Projected Monthly Sales =
VAR _mtdSales = [MTD Sales]
VAR _elapsed = [# Elapsed Days]
VAR _totalDays = [# Days in Month]
RETURN
    DIVIDE(_mtdSales, _elapsed) * _totalDays
```

---

## Handling Incomplete Periods

```dax
-- Only compare if current period has data
YoY Sales % (Safe) =
VAR _current = [Total Sales]
VAR _previous = [PY Sales]
VAR _hasData = NOT(ISBLANK(_current))
RETURN
    IF(_hasData, DIVIDE(_current - _previous, _previous))
```

---

## Using with Calculation Groups

When calculation groups handle time intelligence, base measures don't need
time variants. See `calculation-group-patterns.md` for the Time Intelligence
calculation group template that applies these patterns dynamically.

---

## Fiscal Year Support

Built-in time intelligence functions support a fiscal year end date:

```dax
-- Fiscal year ending March 31
YTD Sales (Fiscal) =
TOTALYTD([Total Sales], DimDate[Date], "3/31")

-- Fiscal year ending June 30
YTD Sales (J-June) =
TOTALYTD([Total Sales], DimDate[Date], "6/30")
```

For more complex fiscal calendars (4-4-5, 4-5-4, ISO weeks), the built-in
functions won't work. Use custom date table columns:

```dax
-- Custom fiscal YTD using date table columns
Fiscal YTD Sales =
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(DimDate),
        DimDate[FiscalYear] = MAX(DimDate[FiscalYear])
            && DimDate[FiscalDayOfYear] <= MAX(DimDate[FiscalDayOfYear])
    )
)

-- Custom fiscal PY
Fiscal PY Sales =
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(DimDate),
        DimDate[FiscalYear] = MAX(DimDate[FiscalYear]) - 1
            && DimDate[FiscalDayOfYear] <= MAX(DimDate[FiscalDayOfYear])
    )
)
```

---

## Semi-Additive Measures

Semi-additive measures (balances, inventory, headcount) must NOT be summed
across time. Use point-in-time snapshots instead.

### Last Non-Blank Balance

The most common pattern — returns the value at the last date that has data:

```dax
Last Balance =
CALCULATE(
    SUM(FactBalance[Amount]),
    LASTNONBLANK(
        DimDate[Date],
        CALCULATE(SUM(FactBalance[Amount]))
    )
)
```

**Why LASTNONBLANK needs the inner CALCULATE**: LASTNONBLANK iterates dates
and evaluates the second argument to determine which dates have data. The
CALCULATE triggers context transition from the row context inside the iterator.

### End-of-Period Snapshots

```dax
-- Inventory at end of selected period
End Inventory =
CALCULATE(
    SUM(FactInventory[Quantity]),
    LASTDATE(DimDate[Date])
)

-- Average daily balance over selected period
Avg Daily Balance =
AVERAGEX(
    VALUES(DimDate[Date]),
    CALCULATE(SUM(FactBalance[Amount]))
)
```

### Semi-Additive with Time Intelligence

Combining semi-additive measures with time intelligence requires care:

```dax
-- Balance YoY comparison
PY Balance =
CALCULATE(
    [Last Balance],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

-- Balance at end of each month (for monthly trend visual)
Monthly End Balance =
CALCULATE(
    SUM(FactBalance[Amount]),
    LASTNONBLANK(
        DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -1, MONTH),
        CALCULATE(SUM(FactBalance[Amount]))
    )
)
```

---

## Multiple Date Relationships

When a fact table has multiple date columns (OrderDate, ShipDate, DueDate):

### Strategy 1: Single Date Table + USERELATIONSHIP (Recommended)

Only one relationship can be active. Use USERELATIONSHIP to switch:

```dax
-- Active relationship: FactSales[OrderDate] → DimDate[Date]

Sales by Ship Date =
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(FactSales[ShipDate], DimDate[Date])
)

Sales by Due Date =
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(FactSales[DueDate], DimDate[Date])
)
```

This is preferred because it uses one date table and Calculation Groups can
apply time intelligence variants to all measures using any date relationship.

### Strategy 2: Multiple Date Tables (Role-Playing)

Create separate date tables for each date role. This lets users slice by
multiple dates in the same visual, at the cost of model complexity.

---

## Date Table Requirements (for built-in time intelligence)

All built-in time intelligence functions (TOTALYTD, SAMEPERIODLASTYEAR,
DATEADD, etc.) require:

1. **Contiguous dates** — No gaps in the date column
2. **Full years** — The table must cover complete calendar years
3. **Unique dates** — One row per day, Date/DateTime data type
4. **Marked as Date Table** — Use `calendar_operations` to mark it
5. **Auto Date/Time DISABLED** — The hidden auto date tables conflict
