# Calculation Group Patterns

Templates for common calculation groups in Power BI. Calculation groups
modify how existing measures behave, avoiding the need to create multiple
variants of each measure.

## Prerequisites

- Power BI Desktop (or Fabric) with calculation groups support
- Enhanced compute engine enabled
- Use `calculation_group_operations` to create/manage calculation groups

---

## 1. Time Intelligence Calculation Group

The most common calculation group. Applies time intelligence to ANY measure.

```
Calculation Group: Time Intelligence
Column Name: Time Calculation

Items:
┌───────────────┬───────────────────────────────────────────────────────────────┐
│ Item Name     │ Expression                                                    │
├───────────────┼───────────────────────────────────────────────────────────────┤
│ Current       │ SELECTEDMEASURE()                                             │
│               │                                                               │
│ YTD           │ TOTALYTD(SELECTEDMEASURE(), DimDate[Date])                    │
│               │                                                               │
│ QTD           │ TOTALQTD(SELECTEDMEASURE(), DimDate[Date])                    │
│               │                                                               │
│ MTD           │ TOTALMTD(SELECTEDMEASURE(), DimDate[Date])                    │
│               │                                                               │
│ PY            │ CALCULATE(                                                    │
│               │     SELECTEDMEASURE(),                                        │
│               │     SAMEPERIODLASTYEAR(DimDate[Date])                         │
│               │ )                                                             │
│               │                                                               │
│ YoY           │ VAR _current = SELECTEDMEASURE()                              │
│               │ VAR _previous = CALCULATE(                                    │
│               │     SELECTEDMEASURE(),                                        │
│               │     SAMEPERIODLASTYEAR(DimDate[Date])                         │
│               │ )                                                             │
│               │ RETURN _current - _previous                                   │
│               │                                                               │
│ YoY %         │ VAR _current = SELECTEDMEASURE()                              │
│               │ VAR _previous = CALCULATE(                                    │
│               │     SELECTEDMEASURE(),                                        │
│               │     SAMEPERIODLASTYEAR(DimDate[Date])                         │
│               │ )                                                             │
│               │ RETURN DIVIDE(_current - _previous, _previous)                │
│               │                                                               │
│ PY YTD        │ CALCULATE(                                                    │
│               │     TOTALYTD(SELECTEDMEASURE(), DimDate[Date]),               │
│               │     SAMEPERIODLASTYEAR(DimDate[Date])                         │
│               │ )                                                             │
│               │                                                               │
│ Rolling 12M   │ CALCULATE(                                                    │
│               │     SELECTEDMEASURE(),                                        │
│               │     DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]),          │
│               │         -12, MONTH)                                           │
│               │ )                                                             │
└───────────────┴───────────────────────────────────────────────────────────────┘

Ordinal: Current=0, YTD=1, QTD=2, MTD=3, PY=4, YoY=5, YoY%=6, PYYTD=7, R12M=8
```

### Usage in Reports

Place "Time Calculation" column in a slicer or matrix column header.
Any measure placed in the matrix values will be dynamically modified.

---

## 2. Currency Conversion Calculation Group

For multi-currency reporting.

```
Calculation Group: Currency
Column Name: Currency Display

Requires: An exchange rate table (DimExchangeRate) with:
  - CurrencyCode, Date, ExchangeRate (to base currency)

Items:
┌──────────────────┬────────────────────────────────────────────────────────────┐
│ Item Name        │ Expression                                                 │
├──────────────────┼────────────────────────────────────────────────────────────┤
│ Local Currency   │ SELECTEDMEASURE()                                          │
│                  │                                                            │
│ USD              │ VAR _rate =                                                │
│                  │     SELECTEDVALUE(DimExchangeRate[RateToUSD], 1)           │
│                  │ RETURN SELECTEDMEASURE() * _rate                           │
│                  │                                                            │
│ EUR              │ VAR _rate =                                                │
│                  │     SELECTEDVALUE(DimExchangeRate[RateToEUR], 1)           │
│                  │ RETURN SELECTEDMEASURE() * _rate                           │
└──────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 3. Scenario Comparison Calculation Group

Compare Actual vs Budget vs Forecast.

```
Calculation Group: Scenario
Column Name: Scenario Type

Requires: Separate fact tables or columns for each scenario
  - FactActual[Amount], FactBudget[Amount], FactForecast[Amount]

Items:
┌──────────────────┬────────────────────────────────────────────────────────────┐
│ Item Name        │ Expression                                                 │
├──────────────────┼────────────────────────────────────────────────────────────┤
│ Actual           │ SELECTEDMEASURE()                                          │
│                  │                                                            │
│ Budget           │ CALCULATE(                                                 │
│                  │     SELECTEDMEASURE(),                                     │
│                  │     USERELATIONSHIP(                                       │
│                  │         FactBudget[DateKey], DimDate[DateKey]              │
│                  │     )                                                      │
│                  │ )                                                          │
│                  │                                                            │
│ Forecast         │ CALCULATE(                                                 │
│                  │     SELECTEDMEASURE(),                                     │
│                  │     USERELATIONSHIP(                                       │
│                  │         FactForecast[DateKey], DimDate[DateKey]            │
│                  │     )                                                      │
│                  │ )                                                          │
│                  │                                                            │
│ Variance         │ VAR _actual = SELECTEDMEASURE()                            │
│                  │ VAR _budget = CALCULATE(                                   │
│                  │     SELECTEDMEASURE(),                                     │
│                  │     USERELATIONSHIP(                                       │
│                  │         FactBudget[DateKey], DimDate[DateKey]              │
│                  │     )                                                      │
│                  │ )                                                          │
│                  │ RETURN _actual - _budget                                   │
│                  │                                                            │
│ Variance %       │ VAR _actual = SELECTEDMEASURE()                            │
│                  │ VAR _budget = CALCULATE(                                   │
│                  │     SELECTEDMEASURE(),                                     │
│                  │     USERELATIONSHIP(                                       │
│                  │         FactBudget[DateKey], DimDate[DateKey]              │
│                  │     )                                                      │
│                  │ )                                                          │
│                  │ RETURN DIVIDE(_actual - _budget, _budget)                  │
└──────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 4. Aggregation Type Calculation Group

Let users choose aggregation method dynamically.

```
Calculation Group: Aggregation
Column Name: Aggregation Type

Items:
┌──────────────────┬────────────────────────────────────────────────────────────┐
│ Item Name        │ Expression                                                 │
├──────────────────┼────────────────────────────────────────────────────────────┤
│ Total            │ SELECTEDMEASURE()                                          │
│ Average          │ AVERAGEX(VALUES(DimDate[MonthKey]), SELECTEDMEASURE())     │
│ Maximum          │ MAXX(VALUES(DimDate[MonthKey]), SELECTEDMEASURE())         │
│ Minimum          │ MINX(VALUES(DimDate[MonthKey]), SELECTEDMEASURE())         │
│ Per Day Avg      │ DIVIDE(SELECTEDMEASURE(), COUNTROWS(VALUES(DimDate[Date])))│
└──────────────────┴────────────────────────────────────────────────────────────┘
```

---

## Calculation Group Precedence

When multiple calculation groups are used together, precedence controls
evaluation order. Higher precedence = evaluated OUTER (applied last).

```
Example with Time Intelligence (precedence=10) + Currency (precedence=20):

Step 1: Time Intelligence modifies the base measure
        YTD Sales = TOTALYTD([Total Sales], DimDate[Date])
Step 2: Currency modifies the result of Step 1
        YTD Sales in USD = YTD Sales * ExchangeRate
```

Set precedence in the calculation group properties. Lower number = inner
(applied first), higher number = outer (applied last).

---

## Implementation Checklist

```
□ Identify which measures benefit from the calculation group
□ Ensure the Date table meets all prerequisites
□ Create using calculation_group_operations
□ Set ordinal values for consistent sort order in slicers
□ Set precedence if using multiple calculation groups
□ Format string expressions (optional) to handle % vs absolute formats
□ Test with dax_query_operations:
    EVALUATE
    SUMMARIZECOLUMNS(
        'Time Intelligence'[Time Calculation],
        "Result", [Total Sales]
    )
□ Verify that visuals respond correctly to slicer selections
```

---

## Format String Expressions

Use format string expressions to dynamically change the format based on
the selected calculation item:

```dax
-- On the "YoY %" item:
Format String Expression: "0.0%;-0.0%;0.0%"

-- On the "Current" item:
Format String Expression: SELECTEDMEASUREFORMATSTRING()
```

This ensures that when "YoY %" is selected, values display as percentages,
while "Current" uses the original measure's format.

---

## Measure Exclusion with ISSELECTEDMEASURE

Some calculation items should not apply to certain measures. For example,
"per day average" should not apply to percentage measures:

```dax
-- In the "Per Day Average" calculation item:
IF(
    ISSELECTEDMEASURE([% Margin]) || ISSELECTEDMEASURE([% Growth]),
    SELECTEDMEASURE(),    -- Return unchanged
    DIVIDE(SELECTEDMEASURE(), COUNTROWS(VALUES(DimDate[Date])))
)
```

For dynamic exclusion by measure name pattern:

```dax
-- Exclude all measures starting with "%" from time division
IF(
    LEFT(SELECTEDMEASURENAME(), 1) = "%",
    SELECTEDMEASURE(),
    DIVIDE(SELECTEDMEASURE(), COUNTROWS(VALUES(DimDate[Date])))
)
```

---

## 5. Moving Average Calculation Group

Complement the Time Intelligence group with moving/rolling calculations:

```
Calculation Group: Moving Calculations
Column Name: Moving Calc

Items:
┌──────────────────┬────────────────────────────────────────────────────────────┐
│ Item Name        │ Expression                                                 │
├──────────────────┼────────────────────────────────────────────────────────────┤
│ Current          │ SELECTEDMEASURE()                                          │
│                  │                                                            │
│ 3M Moving Avg    │ AVERAGEX(                                                  │
│                  │     DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]),       │
│                  │         -3, MONTH),                                        │
│                  │     SELECTEDMEASURE()                                      │
│                  │ )                                                          │
│                  │                                                            │
│ 12M Moving Avg   │ AVERAGEX(                                                  │
│                  │     DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]),       │
│                  │         -12, MONTH),                                       │
│                  │     SELECTEDMEASURE()                                      │
│                  │ )                                                          │
│                  │                                                            │
│ 12M Running Total│ CALCULATE(                                                 │
│                  │     SELECTEDMEASURE(),                                     │
│                  │     DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]),       │
│                  │         -12, MONTH)                                        │
│                  │ )                                                          │
└──────────────────┴────────────────────────────────────────────────────────────┘
```

---

## Key Rules for Calculation Groups

1. **SELECTEDMEASURE() applies to each measure reference independently** —
   If your base measure is `[A] + [B]`, then YTD becomes `YTD([A]) + YTD([B])`,
   not `YTD([A] + [B])`. This gives correct results for additive measures
   but can be wrong for ratios. For ratio measures, wrap in IF:
   ```dax
   -- For a ratio measure like % Margin:
   IF(
       ISSELECTEDMEASURE([% Margin]),
       DIVIDE(
           CALCULATE(SELECTEDMEASURE(), ...[numerator logic]),
           CALCULATE(SELECTEDMEASURE(), ...[denominator logic])
       ),
       -- Default: apply to the whole measure
       TOTALYTD(SELECTEDMEASURE(), DimDate[Date])
   )
   ```

2. **Precedence determines nesting order** — When two calculation groups
   are active simultaneously, the lower precedence number is applied first
   (inner), and the higher precedence number is applied second (outer).
   Example: Time Intelligence (precedence=10) → Currency (precedence=20)
   means "first apply time calc, then convert currency."

3. **One column per calculation group** — Each group contributes exactly one
   column to the model. Users pick items from that column via slicers.

4. **Avoid sideways recursion in user-facing groups** — Calculation items
   can reference other items in the same group, but this creates complex
   dependencies that are hard to debug. Keep this in hidden groups only.

5. **Format string expressions are per-item** — Set them on every item that
   changes the output format (e.g., YoY % needs "0.0%;-0.0%;0.0%").

---

## Advanced Properties (TMDL)

### isAvailableInMDX

Controls whether the calculation group column appears in Excel PivotTable
field lists and XMLA/MDX queries.

```tmdl
table 'Time Intelligence'
    calculationGroup

    column 'Time Calculation'
        dataType: string
        isKey
        sourceColumn: Name
        isAvailableInMDX: false    /// ← hides from Excel PivotTables
```

**When to use:**
- Set to `false` for calculation groups designed only for Power BI reports
  (prevents Excel PivotTable users from seeing confusing calculation items)
- Keep `true` (default) for enterprise models consumed by both Power BI
  and Excel/SSAS PivotTable users

### hideMembers

Controls whether the "Default" (blank) member appears for the calculation
group when no item is selected. Prevents the blank row in PivotTables.

```tmdl
table 'Time Intelligence'
    calculationGroup
        hideMembers: autoOrDefault    /// ← hides blank member
```

Values: `default` (show blank member), `autoOrDefault` (hide blank member
when no explicit selection), `always` (always hide all members from
PivotTable — effectively makes the group invisible to MDX clients).

### Dynamic Format String Expression

For items where the format should depend on the measure being modified,
use a DAX expression (not a static format string):

```tmdl
    calculationItem 'YoY Change' =
        ```
        VAR _current = SELECTEDMEASURE()
        VAR _prior = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
        RETURN _current - _prior
        ```
        ordinal: 1
        formatStringDefinition =
            ```
            SELECTEDMEASUREFORMATSTRING()
            ```
        /// ← inherits format from the base measure ($ for revenue, # for units)

    calculationItem 'YoY %' =
        ```
        VAR _current = SELECTEDMEASURE()
        VAR _prior = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
        RETURN DIVIDE(_current - _prior, _prior)
        ```
        ordinal: 2
        formatStringDefinition = "0.0%;-0.0%;0.0%"
        /// ← forces percentage format regardless of base measure
```

**Rules for format string expressions:**
- `SELECTEDMEASUREFORMATSTRING()` — inherits the base measure's format (use for absolute values like YoY Change)
- Static string (e.g., `"0.0%"`) — forces a specific format (use for ratios/percentages)
- DAX `IF`/`SWITCH` expression — conditionally pick format based on `SELECTEDMEASURENAME()`
