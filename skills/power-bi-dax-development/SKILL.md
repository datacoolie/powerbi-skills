---
name: power-bi-dax-development
description: >
  Develop, optimize, and validate DAX measures and calculations for Power BI
  semantic models. Covers measure creation, evaluation contexts, CALCULATE
  semantics, time intelligence, semi-additive measures, calculation groups,
  field parameters, advanced patterns (ABC analysis, new/returning customers,
  virtual relationships via TREATAS), and performance optimization using
  PowerBI Modeling MCP tools. Based on "The Definitive Guide to DAX" and
  "Optimizing DAX" by Ferrari & Russo. Always research Microsoft Learn MCP
  before recommending patterns.
---

# Power BI DAX Development

You are a DAX development specialist. You create well-structured, performant
DAX measures and calculation groups for Power BI semantic models using the
PowerBI Modeling MCP tools.

## Core Principles

1. **Research First** — Before writing any DAX pattern, search Microsoft Learn
   for the latest recommended approach.
2. **Understand Evaluation Context** — Every DAX expression runs inside a
   filter context and zero or more row contexts. Know which contexts are
   active before writing any formula.
3. **Measures Over Columns** — Use measures instead of calculated columns whenever
   possible. Calculated columns consume memory and cannot be context-aware.
4. **Variables for Readability** — Use `VAR` / `RETURN` to improve readability and
   performance (variables are evaluated once, are constants once assigned).
5. **Push to Storage Engine** — Write DAX that lets the storage engine (VertiPaq
   or DirectQuery) do the heavy lifting. Avoid patterns that force the formula
   engine to iterate row-by-row.
6. **Test Everything** — Validate every measure with `dax_query_operations` before
   considering it complete.
7. **Document Intent** — Every measure needs a clear description explaining what
   it calculates and when to use it.

## Evaluation Contexts (Mental Model)

Every DAX expression executes inside an **evaluation context** that determines
which data is visible. Misunderstanding contexts is the #1 source of wrong
DAX results. See `references/evaluation-contexts.md` for the full reference.

### Filter Context

A set of active filters on model columns. Comes from: slicers, visual axes,
CALCULATE filter arguments, or page/report filters.

### Row Context

Exists inside iterators (SUMX, ADDCOLUMNS, FILTER, etc.). Provides access
to the current row's column values. Multiple row contexts can be nested.

### Context Transition

When a **measure** is referenced inside a row context, DAX automatically wraps
it in CALCULATE, converting the row context to filter context. This is powerful
but expensive — especially on fact tables (no primary key → must filter all columns).

**Rule:** Inside SUMX over a fact table, use column references
(`Sales[Quantity] * Sales[Price]`) not measure references (`[Sales Amount]`)
unless you specifically need context transition.

### CALCULATE Execution Order

CALCULATE modifies context in this exact order:

1. Evaluate filter arguments in the **original** evaluation context
2. Copy the original filter context
3. Perform context transition (if row contexts exist)
4. Apply CALCULATE modifiers (ALL, USERELATIONSHIP, CROSSFILTER, KEEPFILTERS)
5. Apply explicit filter arguments (replace existing column filters)

Understanding this order is critical for ALLEXCEPT, KEEPFILTERS, and
nested CALCULATE correctness.

## Workflow

### Step 1 — Understand Requirements

Gather from the business analysis output or user request:
- What metric is needed (KPI name, business definition)
- Expected aggregation behavior (SUM, AVERAGE, COUNT, custom)
- Time intelligence requirements (YTD, YoY, rolling)
- Filter context requirements (which slicers should affect it)
- Formatting requirements (number, percentage, currency)

### Step 2 — Research Best Practices

Before writing DAX:

1. Search Microsoft Learn for the pattern:
   - `microsoft_docs_search` — "Power BI DAX [pattern name]"
   - `microsoft_code_sample_search` — "DAX [pattern name]"
2. Check if an existing measure already covers this requirement:
   - `measure_operations` — list all current measures
3. Check the model context:
   - `table_operations` — confirm table names and structure
   - `relationship_operations` — understand active/inactive relationships
   - `column_operations` — verify column data types and availability

### Step 3 — Write DAX

Follow these formatting standards:

```dax
-- Standard measure template
[Measure Name] =
VAR _variableName = <expression>
VAR _anotherVariable = <expression>
RETURN
    <result expression>
```

**Naming Conventions:**

| Measure Type | Prefix/Pattern | Example |
|---|---|---|
| Base aggregation | Direct name | `Total Sales` |
| Percentage | `% ` prefix | `% Margin` |
| Year-to-Date | `YTD ` prefix | `YTD Revenue` |
| Year-over-Year | `YoY ` suffix | `Revenue YoY %` |
| Previous period | `PP ` prefix or ` PP` suffix | `PP Revenue` |
| Running total | `RT ` prefix | `RT Sales` |
| Rank | `Rank ` prefix | `Rank Sales` |
| Count | `# ` prefix | `# Customers` |
| Helper (hidden) | `_` prefix | `_MaxDate` |

**Variable Naming:**
- Prefix with `_` (underscore): `_totalSales`, `_previousYear`
- Use camelCase after underscore
- Be descriptive: `_filteredRows` not `_fr`

### Step 4 — Implement with MCP

Create the measure:
```
Tool: measure_operations
Action: Create measure
Parameters:
  - tableName: "_Measures" (or appropriate measure table)
  - name: "Total Sales"
  - expression: "SUM(FactSales[SalesAmount])"
  - formatString: "$#,##0.00"
  - description: "Sum of all sales amounts"
  - displayFolder: "Sales"
```

### Step 5 — Validate

Test EVERY measure using `dax_query_operations`:

```dax
-- Basic validation: does it return a value?
EVALUATE { [Total Sales] }

-- Context validation: does it aggregate correctly by dimension?
EVALUATE
SUMMARIZECOLUMNS(
    DimProduct[Category],
    "Sales", [Total Sales]
)

-- Filter validation: does it respect filters correctly?
EVALUATE
CALCULATETABLE(
    SUMMARIZECOLUMNS(
        DimDate[Year],
        "Sales", [Total Sales]
    ),
    DimProduct[Category] = "Electronics"
)

-- Comparison validation: does it match expected values?
EVALUATE
ROW(
    "Total Sales", [Total Sales],
    "Row Count", COUNTROWS(FactSales),
    "Avg Sale", [Total Sales] / COUNTROWS(FactSales)
)
```

### Step 6 — Optimize if Needed

If a measure is slow, apply the 4-step optimization:

1. **Simplify the expression** — Reduce nested CALCULATE, remove unnecessary filters
2. **Use variables** — Replace repeated sub-expressions with VAR
3. **Reduce context transitions** — Minimize row-by-row evaluation
4. **Check the model** — Add aggregation tables or fix relationships

See `references/anti-patterns.md` for common performance mistakes.

---

## Common DAX Patterns

### Base Measures

```dax
-- Always qualify column references with table name
Total Sales = SUM(FactSales[SalesAmount])
Total Cost = SUM(FactSales[CostAmount])
Gross Profit = [Total Sales] - [Total Cost]
% Margin = DIVIDE([Gross Profit], [Total Sales])
# Orders = DISTINCTCOUNT(FactSales[OrderID])
# Customers = DISTINCTCOUNT(FactSales[CustomerID])
Avg Order Value = DIVIDE([Total Sales], [# Orders])
```

### Time Intelligence

See `references/time-intelligence-patterns.md` for comprehensive patterns
including fiscal year, semi-additive measures, and custom calendars.

```dax
-- Year-to-Date
YTD Sales =
TOTALYTD([Total Sales], DimDate[Date])

-- Previous Year
PY Sales =
CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))

-- Year-over-Year % (with blank protection)
YoY Sales % =
VAR _current = [Total Sales]
VAR _previous = [PY Sales]
RETURN
    IF(
        NOT(ISBLANK(_current)),
        DIVIDE(_current - _previous, _previous)
    )
```

### Semi-Additive Measures (Balances, Inventory)

Semi-additive measures must NOT be summed across time — use
LASTNONBLANK or LASTDATE instead:

```dax
-- Balance at last available date in the period
Last Balance =
CALCULATE(
    SUM(FactBalance[Amount]),
    LASTNONBLANK(DimDate[Date], CALCULATE(SUM(FactBalance[Amount])))
)

-- Inventory at end of period
End Inventory =
CALCULATE(
    SUM(FactInventory[Quantity]),
    LASTDATE(DimDate[Date])
)
```

### Ranking

```dax
Rank Sales =
VAR _currentValue = [Total Sales]
RETURN
    COUNTROWS(
        FILTER(
            ALLSELECTED(DimProduct[ProductName]),
            [Total Sales] >= _currentValue
        )
    ) 
```

### Conditional Formatting Helpers

```dax
-- KPI status: 1 = Good, 0 = Neutral, -1 = Bad
_KPI Margin Status =
VAR _margin = [% Margin]
RETURN
    SWITCH(
        TRUE(),
        _margin >= 0.30, 1,
        _margin >= 0.15, 0,
        -1
    )
```

### Dynamic Measures (with Calculation Groups)

See `references/calculation-group-patterns.md` for templates.

### Selected Value Display

```dax
Selected Category =
IF(
    HASONEVALUE(DimProduct[Category]),
    SELECTEDVALUE(DimProduct[Category]),
    "All Categories"
)
```

### Virtual Relationships (TREATAS)

Use TREATAS when you need to filter a table without a physical relationship,
or to give data lineage to anonymous tables:

```dax
-- Filter using values from an unrelated table
Sales by Segment =
CALCULATE(
    [Total Sales],
    TREATAS(VALUES(SegmentMap[ProductKey]), FactSales[ProductKey])
)

-- Apply a literal filter list with correct lineage
Sales Red Blue =
CALCULATE(
    [Total Sales],
    TREATAS({"Red", "Blue"}, DimProduct[Color])
)
```

### Hierarchy-Aware Measures (ISINSCOPE)

Use ISINSCOPE to write measures that behave differently at each hierarchy level:

```dax
% of Parent =
VAR _sales = [Total Sales]
RETURN
    SWITCH(
        TRUE(),
        ISINSCOPE(DimProduct[ProductName]),
            DIVIDE(_sales, CALCULATE(_sales, ALLSELECTED(DimProduct[ProductName]))),
        ISINSCOPE(DimProduct[SubCategory]),
            DIVIDE(_sales, CALCULATE(_sales, ALLSELECTED(DimProduct[SubCategory]))),
        ISINSCOPE(DimProduct[Category]),
            DIVIDE(_sales, CALCULATE(_sales, ALLSELECTED(DimProduct[Category]))),
        BLANK()
    )
```

### Advanced Patterns

See `references/advanced-patterns.md` for complete implementations of:
- New vs. Returning Customers (EXCEPT pattern)
- ABC / Pareto Analysis (running totals with ADDCOLUMNS)
- Many-to-Many relationships (bridge table patterns)
- Parent-Child Hierarchies (PATH functions)
- Dynamic Segmentation (SWITCH + custom ranges)
- Budget Allocation (weighted distribution)

---

## Calculation Groups

Calculation groups modify how existing measures behave, eliminating the need
to create multiple variants of each measure.

### When to Use Calculation Groups

- Time intelligence variants (YTD, PY, YoY) applied to ALL measures
- Currency conversion across all monetary measures
- Scenario analysis (Actual, Budget, Forecast)
- Percentage-of-total variants

### Implementation

```
Tool: calculation_group_operations
Action: Create calculation group
Parameters:
  - name: "Time Intelligence"
  - items: [
      { name: "Current", expression: "SELECTEDMEASURE()" },
      { name: "YTD", expression: "TOTALYTD(SELECTEDMEASURE(), DimDate[Date])" },
      { name: "PY", expression: "CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(DimDate[Date]))" },
      { name: "YoY %", expression: "VAR _c = SELECTEDMEASURE() VAR _p = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(DimDate[Date])) RETURN DIVIDE(_c - _p, _p)" }
    ]
```

---

## Field Parameters

Field parameters let report users dynamically switch which measure or
dimension appears on a visual.

```dax
-- Example: dynamic measure selector
Sales Metrics =
{
    ("Revenue", NAMEOF([Total Sales]), 0),
    ("Profit", NAMEOF([Gross Profit]), 1),
    ("Margin %", NAMEOF([% Margin]), 2),
    ("# Orders", NAMEOF([# Orders]), 3)
}
```

Create using `measure_operations` or `table_operations` depending on whether
it's a measure-type or column-type field parameter.

---

## Performance Guidelines

See `references/optimization-guide.md` for the full optimization reference
including engine architecture, VertiPaq internals, and DirectQuery/Composite
model guidance.

### Engine Architecture Awareness

The DAX engine has two layers:
- **Formula Engine (FE):** Single-threaded, orchestrates queries, processes
  datacaches. Expensive operations here cannot be parallelized.
- **Storage Engine (SE):** Multi-threaded (VertiPaq) or external (DirectQuery).
  Push as much work here as possible.

**Goal:** Minimize formula engine work. Write DAX that translates to simple
storage engine queries returning small, pre-aggregated datacaches.

### Measure Complexity Tiers

| Tier | Description | Expected Performance |
|---|---|---|
| Simple | Single aggregation (SUM, COUNT) | < 100ms |
| Standard | CALCULATE with 1-2 filters | < 500ms |
| Complex | Nested iterators, FILTER over large tables | < 2s |
| Heavy | Multiple context transitions, large CROSSJOIN | May need optimization |

### Optimization Rules

1. **Separate CALCULATE filter arguments** — Multiple conditions as separate
   arguments can be 12x faster than combining with AND/&&.
   ```dax
   -- SLOW (combined)
   CALCULATE([Sales], Customer[Country] IN {"Italy","France"} && Customer[Gender] = "M")
   -- FAST (separate)
   CALCULATE([Sales], Customer[Country] IN {"Italy","France"}, Customer[Gender] = "M")
   ```
2. **Filter dimension columns, not fact columns** — CALCULATE predicates on
   dimension columns use relationships; fact column filters iterate every row.
3. **DIVIDE > division** — Always use DIVIDE() for safe division (handles zero).
4. **Avoid IF inside iterators** — Push conditions to FILTER + CALCULATE to let
   the storage engine handle them.
   ```dax
   -- SLOW: IF in SUMX iterates every row in FE
   SUMX(Sales, IF(Sales[Qty] * Sales[Price] >= 200, Sales[Qty] * Sales[Price]))
   -- FAST: CALCULATE pushes filter to SE
   CALCULATE([Sales Amount], Sales[Qty] * Sales[Price] >= 200)
   ```
5. **Avoid context transition on fact tables** — Inside SUMX over facts, use
   column references, not measure references.
6. **Avoid EARLIER** — Indicates nested row context issues; restructure with VAR.
7. **Avoid nested iterators on fact tables** — SUMX inside SUMX on millions of
   rows is O(n²). Use ADDCOLUMNS + VALUES to pre-aggregate.
8. **ALLEXCEPT trap** — ALLEXCEPT only preserves *directly* filtered columns.
   Use ALL + VALUES instead for reliable results:
   ```dax
   -- UNRELIABLE: loses cross-filters
   CALCULATE([Sales], ALLEXCEPT(Customer, Customer[Type]))
   -- RELIABLE: ALL + VALUES respects all filters
   CALCULATE([Sales], ALL(Customer), VALUES(Customer[Type]))
   ```
9. **VAR is a constant** — Variables are evaluated once in their original context
   and cannot be re-evaluated. Don't use a VAR where you need a measure that
   reacts to changing filter context inside CALCULATE.
10. **Reduce model cardinality** — Fewer distinct values per column = better
    VertiPaq compression = faster storage engine scans.

---

## Debugging Workflow

When a measure returns unexpected results:

1. **Isolate** — Test the measure alone: `EVALUATE { [Measure] }`
2. **Decompose** — Replace VARs with literals to find the broken part
3. **Check context** — Add `VALUES(DimTable[Column])` to see what filters are active
4. **Check relationships** — Use `relationship_operations` to verify paths
5. **Check data** — Use `dax_query_operations` to inspect raw data
6. **Compare** — Test in a known-good context vs. the failing context

```dax
-- Debug helper: inspect filter context
EVALUATE
ROW(
    "Result", [Problematic Measure],
    "Active Year Filters", CONCATENATEX(VALUES(DimDate[Year]), DimDate[Year], ", "),
    "Active Product Filters", CONCATENATEX(VALUES(DimProduct[Category]), DimProduct[Category], ", "),
    "Row Count", COUNTROWS(FactSales)
)
```

### Performance Debugging

When a measure is slow, use DAX Studio Server Timings to identify bottlenecks:

1. **Check SE vs FE time split** — If FE >> SE, the formula engine is doing
   too much work (context transitions, row-by-row iteration)
2. **Check materialization size** — Large datacaches mean early materialization;
   rewrite to push aggregation to storage engine
3. **Check CallbackDataID** — Presence of callbacks means formula engine is
   interrupting storage engine scans (very expensive)
4. **Check number of SE queries** — Many small queries indicate excessive
   CALCULATE calls; consolidate logic
