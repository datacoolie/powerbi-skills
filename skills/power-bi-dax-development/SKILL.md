---
name: power-bi-dax-development
description: >
  Develop, optimize, and validate DAX measures, calculation groups, visual
  calculations, field parameters, dynamic format strings, time intelligence,
  semi-additive logic, virtual relationships with TREATAS, DAX window
  functions, and user-defined functions for Power BI semantic models. Use for
  requests to write or optimize DAX, create measures, explain CALCULATE or
  evaluation context, build YTD/YoY/WTD logic, use RUNNINGSUM or MOVINGAVERAGE,
  rank with RANK/ROWNUMBER/OFFSET/INDEX/WINDOW, or apply advanced DAX patterns.
  Research Microsoft Learn MCP before recommending patterns.
---

# Power BI DAX Development

You are a DAX development specialist. You create well-structured, performant
DAX measures and calculation groups for Power BI semantic models using the
PowerBI Modeling MCP tools.

## Reference Files

| File | Content | When to Read |
|---|---|---|
| `references/evaluation-contexts.md` | Filter context, row context, context transition, CALCULATE semantics, expanded tables, ALLSELECTED | Before writing any non-trivial measure |
| `references/time-intelligence-patterns.md` | YTD, QTD, MTD, WTD, YoY, rolling averages, fiscal year, semi-additive, calendar-based TI | When building date-based calculations |
| `references/calculation-group-patterns.md` | Calculation groups, items, precedence, format strings, TMDL syntax | When creating reusable calculation modifiers |
| `references/advanced-patterns.md` | ABC analysis, new/returning customers, TREATAS, dynamic segmentation, RANK, ROWNUMBER, WINDOW/INDEX/OFFSET | When building complex analytical patterns |
| `references/field-parameters.md` | Field parameters, dynamic measure switching, axis switching | When users need to switch dimensions or measures dynamically |
| `references/optimization-guide.md` | Query plans, VertiPaq, FE/SE architecture, CALCULATE optimization, iterators, composite models, Direct Lake, debugging workflow | When optimizing slow measures or debugging |
| `references/anti-patterns.md` | 19 common mistakes, performance killers, incorrect patterns, dynamic format strings | Review before finalizing any measure |
| `references/visual-calculations.md` | Visual calculations: RUNNINGSUM, MOVINGAVERAGE, PREVIOUS, NEXT, COLLAPSE, templates | When user needs visual-specific calculations (running sums, moving averages) |
| `references/user-defined-functions.md` | UDF syntax, reusable parameterized DAX logic, TMDL expressions [Preview] | When user needs reusable function definitions or asks about UDFs |

## Core Principles

1. **Research First** — Search Microsoft Learn MCP for latest patterns before writing DAX.
2. **Understand Evaluation Context** — Read `references/evaluation-contexts.md`.
3. **Measures Over Columns** — Calculated columns consume memory, can't be context-aware.
4. **Variables for Readability** — `VAR`/`RETURN` evaluated once, constant once assigned.
5. **Push to Storage Engine** — Avoid row-by-row formula engine iteration.
6. **Test Everything** — Validate with `dax_query_operations`.
7. **Document Intent** — Every measure needs a description.

## Evaluation Contexts

Every DAX expression executes in a filter context + zero or more row contexts.
Misunderstanding contexts is the #1 source of wrong results.
**→ Read `references/evaluation-contexts.md` before writing any non-trivial measure.**

## Workflow

### Step 1 — Understand Requirements

Gather: metric name, business definition, aggregation type, time intelligence needs,
filter context requirements, and formatting.

### Step 2 — Research Best Practices

1. Search Microsoft Learn: `microsoft_docs_search` / `microsoft_code_sample_search`
2. Check existing measures: `measure_operations` — list all current measures
3. Check model context: `table_operations`, `relationship_operations`, `column_operations`

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

**Variable Naming:** Prefix with `_` + camelCase: `_totalSales`, `_previousYear`, `_filteredRows`

### Step 4 — Implement with MCP

Use `measure_operations` to create the measure with: tableName, name, expression,
formatString, description, displayFolder.

### Step 5 — Validate

Test EVERY measure using `dax_query_operations`:

```dax
-- Basic: does it return a value?
EVALUATE { [Total Sales] }

-- Context: aggregates correctly by dimension?
EVALUATE SUMMARIZECOLUMNS(DimProduct[Category], "Sales", [Total Sales])

-- Filter: respects filters correctly?
EVALUATE CALCULATETABLE(
    SUMMARIZECOLUMNS(DimDate[Year], "Sales", [Total Sales]),
    DimProduct[Category] = "Electronics"
)
```

### Step 6 — Optimize if Needed

See `references/optimization-guide.md` for engine architecture, query plan analysis,
CALCULATE optimization, iterator patterns, and debugging workflow.
See `references/anti-patterns.md` for 18+ common mistakes with fixes and benchmarks.

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

### Other Patterns (in reference files)

- **Time Intelligence** → `references/time-intelligence-patterns.md` (YTD, QTD, MTD, WTD, YoY, fiscal, semi-additive, calendar-based)
- **Ranking & Window Functions** → `references/advanced-patterns.md` § WINDOW/INDEX/OFFSET
- **Advanced** → `references/advanced-patterns.md` (New/Returning Customers, ABC/Pareto, TREATAS, ISINSCOPE, PATH, Top N with Others)

---

## Calculation Groups

Modify how existing measures behave — eliminating multiple variants per measure.
See `references/calculation-group-patterns.md` for Time Intelligence, Currency,
Scenario Comparison, Aggregation Type templates, precedence rules, and format strings.

---

## Field Parameters

Enable dynamic switching of measures/columns on visuals.
See `references/field-parameters.md` for creation, TMDL syntax, PBIR bindings,
calculation group pairing, and limitations.

---

## Visual Calculations

DAX calculations defined directly on a visual (not in the model). Simpler for
running sums, moving averages, vs-previous comparisons. Cannot be created via
MCP tools — report-level only. See `references/visual-calculations.md`.

---

## Related Skills

| Skill | When |
|---|---|
| `power-bi-semantic-model` | Model schema defines available tables, columns, relationships |
| `power-bi-report-design` | Measure catalog feeds into Design Spec visual bindings |
| `power-bi-performance-troubleshooting` | DAX optimization, query plan analysis |
| `power-bi-business-analysis` | Measure requirements define what to build |

## Performance & Debugging

See `references/optimization-guide.md` for FE/SE architecture, query plans,
CALCULATE optimization, iterators, Direct Lake, and debugging workflow.
See `references/anti-patterns.md` for 19 common mistakes with benchmarks.

**Quick rules:** Separate CALCULATE filter args (no &&) • Filter dim columns not fact • DIVIDE() for safe division • No context transition on fact tables • No nested iterators on facts • VAR is constant (won't re-evaluate under CALCULATE)

**Debug steps:** Isolate (`EVALUATE { [Measure] }`) → Decompose VARs → Check context (`VALUES`) → Check relationships → Check data
