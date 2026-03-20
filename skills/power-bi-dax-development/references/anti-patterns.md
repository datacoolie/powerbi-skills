# DAX Anti-Patterns

Common DAX mistakes with explanations and corrections. Reference this when
writing or reviewing DAX to avoid performance and correctness issues.

---

## 1. Division Without DIVIDE

**Bad:**
```dax
Margin % = [Gross Profit] / [Total Sales]
```
Fails with divide-by-zero error when Total Sales is 0.

**Good:**
```dax
Margin % = DIVIDE([Gross Profit], [Total Sales])
```
Returns BLANK() when denominator is 0. Use the optional third argument for
a custom alternate result: `DIVIDE([Gross Profit], [Total Sales], 0)`.

---

## 2. Calculated Columns Instead of Measures

**Bad:**
```dax
-- Calculated column on FactSales
FactSales[ProfitMargin] = FactSales[Profit] / FactSales[Revenue]
```
Stored row-by-row, increases model size, not context-aware.

**Good:**
```dax
-- Measure
Profit Margin = DIVIDE(SUM(FactSales[Profit]), SUM(FactSales[Revenue]))
```
Calculated at query time, context-aware, no additional storage.

**When calculated columns ARE appropriate:**
- Sort-by columns (MonthNumber for MonthName)
- Columns needed in relationships
- Row-level categorization used in slicers (rarely)

---

## 3. FILTER on Large Tables in CALCULATE

**Bad:**
```dax
Sales Electronics =
CALCULATE(
    [Total Sales],
    FILTER(ALL(FactSales), FactSales[CategoryID] = 1)
)
```
Iterates every row of the entire fact table.

**Good:**
```dax
Sales Electronics =
CALCULATE(
    [Total Sales],
    DimProduct[Category] = "Electronics"
)
```
Uses the relationship and only filters the small dimension table.

**Rule:** CALCULATE filter arguments should reference dimension columns,
not fact table columns, whenever possible.

---

## 4. Nested Iterators on Large Tables

**Bad:**
```dax
Weighted Avg Price =
SUMX(
    FactSales,
    FactSales[Quantity] *
    AVERAGEX(
        FILTER(FactSales, FactSales[ProductID] = EARLIER(FactSales[ProductID])),
        FactSales[UnitPrice]
    )
)
```
O(n²) complexity. EARLIER is also a code smell.

**Good:**
```dax
Weighted Avg Price =
VAR _avgByProduct =
    ADDCOLUMNS(
        VALUES(FactSales[ProductID]),
        "@AvgPrice", CALCULATE(AVERAGE(FactSales[UnitPrice]))
    )
RETURN
    SUMX(
        _avgByProduct,
        CALCULATE(SUM(FactSales[Quantity])) * [@AvgPrice]
    )
```

---

## 5. Using EARLIER Instead of VAR

**Bad:**
```dax
Rank =
COUNTROWS(
    FILTER(
        DimProduct,
        DimProduct[Sales] > EARLIER(DimProduct[Sales])
    )
) + 1
```

**Good:**
```dax
Rank =
VAR _currentSales = DimProduct[Sales]
RETURN
    COUNTROWS(
        FILTER(
            DimProduct,
            DimProduct[Sales] > _currentSales
        )
    ) + 1
```
`VAR` is always clearer than `EARLIER` and performs identically or better.

---

## 6. IF Instead of SWITCH for Multiple Conditions

**Bad:**
```dax
Status =
IF([Score] >= 90, "A",
    IF([Score] >= 80, "B",
        IF([Score] >= 70, "C",
            IF([Score] >= 60, "D", "F")
        )
    )
)
```

**Good:**
```dax
Status =
SWITCH(
    TRUE(),
    [Score] >= 90, "A",
    [Score] >= 80, "B",
    [Score] >= 70, "C",
    [Score] >= 60, "D",
    "F"
)
```
Cleaner, easier to maintain, same performance.

---

## 7. Ignoring Blank Handling

**Bad:**
```dax
YoY Growth =
VAR _current = [Total Sales]
VAR _previous = [PY Sales]
RETURN
    DIVIDE(_current - _previous, _previous)
```
Shows growth rate even when current period has no data (returns negative
of previous period).

**Good:**
```dax
YoY Growth =
VAR _current = [Total Sales]
VAR _previous = [PY Sales]
RETURN
    IF(
        NOT(ISBLANK(_current)),
        DIVIDE(_current - _previous, _previous)
    )
```

---

## 8. DISTINCTCOUNT on High-Cardinality Text Columns

**Bad:**
```dax
# Unique Descriptions = DISTINCTCOUNT(FactSales[Description])
```
Text columns with high cardinality are extremely slow for DISTINCTCOUNT.

**Good:**
- Use an integer surrogate key for counting
- Or hash the text column to a numeric column in the data source
- If you must count text, consider a calculated column with a hash during data load

---

## 9. ALL vs ALLSELECTED Confusion

**Bad:**
```dax
-- Intended: % of visible total (respects slicers)
% of Total =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(DimProduct))
)
```
Ignores ALL slicer selections — shows % of grand total always.

**Good:**
```dax
-- Respects slicer selections
% of Visible Total =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALLSELECTED(DimProduct))
)
```

| Function | Behavior |
|---|---|
| `ALL` | Removes all filters (ignores slicers) |
| `ALLSELECTED` | Removes local visual filters but respects slicers |
| `ALLEXCEPT` | Removes all filters except specified columns |
| `REMOVEFILTERS` | Same as ALL (preferred syntax in new code) |

---

## 10. Bi-Directional Cross-Filter in DAX

**Bad:**
```dax
-- Setting relationship to bi-directional to make a measure work
```
Bi-directional relationships cause ambiguity and performance issues.

**Good:**
```dax
-- Use CROSSFILTER in DAX instead
Sales with Product Reviews =
CALCULATE(
    [Total Sales],
    CROSSFILTER(FactSales[ProductID], DimProduct[ProductID], BOTH)
)
```
Apply bi-directional only where needed, only in the specific measure.

---

## 11. Not Using FORMAT Strings

**Bad:**
```dax
Sales Display = FORMAT([Total Sales], "#,##0.00") & " USD"
```
Converts to text — cannot be used in charts, conditional formatting, or
sorting. Kills visual performance.

**Good:**
Set format string on the measure itself:
```
Format String: $#,##0.00
```
Use `measure_operations` to set the format string property.

---

## 12. SUMMARIZE for Adding Columns

**Bad:**
```dax
SUMMARIZE(
    FactSales,
    DimProduct[Category],
    "Total", SUM(FactSales[Amount])
)
```
SUMMARIZE with extensions (added columns) can produce unexpected results.

**Good:**
```dax
ADDCOLUMNS(
    SUMMARIZE(FactSales, DimProduct[Category]),
    "Total", CALCULATE(SUM(FactSales[Amount]))
)
```
Or in queries (not measures), use SUMMARIZECOLUMNS:
```dax
SUMMARIZECOLUMNS(
    DimProduct[Category],
    "Total", SUM(FactSales[Amount])
)
```

---

## Quick Reference

| Anti-Pattern | Fix |
|---|---|
| `A / B` | `DIVIDE(A, B)` |
| Calculated column for aggregation | Measure |
| `FILTER(FactTable, ...)` in CALCULATE | Dimension filter argument |
| Nested SUMX on fact table | VAR + ADDCOLUMNS approach |
| `EARLIER(...)` | `VAR` |
| Nested `IF` chains | `SWITCH(TRUE(), ...)` |
| No BLANK check on YoY | Wrap in `IF(NOT(ISBLANK(...)))` |
| DISTINCTCOUNT on text | Use integer key |
| `ALL` when meaning `ALLSELECTED` | `ALLSELECTED` |
| Bi-directional relationship | `CROSSFILTER(..., BOTH)` in DAX |
| `FORMAT()` for display | Format string property |
| `SUMMARIZE` with extensions | `ADDCOLUMNS + SUMMARIZE` |
| Combined && in CALCULATE filter | Separate filter arguments |
| IF inside SUMX | FILTER + CALCULATE |
| Context transition on fact tables | Column references in iterators |
| ALLEXCEPT on cross-filtered cols | ALL + VALUES |
| VAR reused across CALCULATE | Use measure instead |
| Unqualified column references | Always use `Table[Column]` |

---

## 13. Combined Filter Conditions in CALCULATE

**Bad:**
```dax
Sales Filtered =
CALCULATE(
    [Total Sales],
    Customer[Country] IN {"Italy", "France"}
        && Customer[Gender] = "Male"
        && MONTH(Customer[Birthday]) = 10
)
```
Combining conditions with && creates a complex multi-column filter that the
storage engine cannot optimize efficiently. In benchmarks from Russo & Ferrari,
this was 12x slower than the alternative.

**Good:**
```dax
Sales Filtered =
CALCULATE(
    [Total Sales],
    Customer[Country] IN {"Italy", "France"},
    Customer[Gender] = "Male",
    MONTH(Customer[Birthday]) = 10
)
```
Separate arguments become independent single-column filters that the storage
engine processes much more efficiently.

---

## 14. IF / Conditional Logic Inside Iterators

**Bad:**
```dax
Sales Gt 200 =
SUMX(
    FactSales,
    IF(
        FactSales[Quantity] * FactSales[NetPrice] >= 200,
        FactSales[Quantity] * FactSales[NetPrice]
    )
)
```
The storage engine cannot execute IF — it requires a callback to the formula
engine for every row, destroying parallelism. On large tables this causes
massive materialization.

**Good:**
```dax
Sales Gt 200 =
CALCULATE(
    [Sales Amount],
    FactSales[Quantity] * FactSales[NetPrice] >= 200
)
```
Pushing the condition to CALCULATE lets the storage engine filter data before
aggregation. In benchmarks: 200ms vs 1.5 seconds (7.5x improvement).

---

## 15. Context Transition on Fact Tables

**Bad:**
```dax
Custom Total =
SUMX(
    FactSales,
    [Sales Amount]    -- Measure reference = context transition per row
)
```
Each row in the fact table triggers a context transition. Fact tables have no
primary key, so DAX must filter on ALL columns to identify the row — extremely
expensive. Materializes the entire table.

**Good:**
```dax
Custom Total =
SUMX(
    FactSales,
    FactSales[Quantity] * FactSales[NetPrice]    -- Direct column references
)
```
No context transition, evaluates in the existing row context. For dimension
tables, context transition is acceptable (they have primary keys).

---

## 16. ALLEXCEPT with Cross-Filtered Columns

**Bad:**
```dax
% of Type =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALLEXCEPT(Customer, Customer[Type]))
)
```
ALLEXCEPT only preserves **directly** filtered columns. If Customer[Type] is
only cross-filtered via a relationship (e.g., through a slicer on another
table), ALLEXCEPT treats it as unfiltered and removes ALL filters — silently
returning the grand total.

**Good:**
```dax
% of Type =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(Customer), VALUES(Customer[Type]))
)
```
ALL + VALUES pattern: removes all filters, then re-applies the visible values
of the column. This respects both direct and cross-filters.

---

## 17. VAR Reused Inside Different CALCULATE Contexts

**Bad:**
```dax
% of Total =
VAR _total = [Total Sales]    -- Evaluated once in current filter context
RETURN
    DIVIDE(
        [Total Sales],
        CALCULATE(_total, ALL(DimProduct))    -- _total does NOT re-evaluate!
    )
```
Variables are constants — once evaluated, they hold that value regardless of
any subsequent CALCULATE. The CALCULATE wrapping _total has no effect.

**Good:**
```dax
% of Total =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(DimProduct))    -- Measure re-evaluates
)
```
Use the measure expression directly when the value must respond to a changed
filter context.

---

## 18. Unqualified Column References

**Bad:**
```dax
Total = SUM([Amount])
```
Without the table name, it's ambiguous which table [Amount] belongs to, and
it makes context transition behavior harder to reason about.

**Good:**
```dax
Total = SUM(FactSales[Amount])
```
Always qualify columns with `TableName[ColumnName]`. Measures are referenced
without a table prefix: `[Total Sales]`.
