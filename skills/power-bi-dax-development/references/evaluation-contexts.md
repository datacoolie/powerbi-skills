# Evaluation Contexts Reference

The foundation of DAX correctness. Every bug in a DAX measure can be traced
to a misunderstanding of evaluation context.

Based on "The Definitive Guide to DAX" (Ferrari & Russo, 2nd Edition).

---

## The Two Contexts

### Filter Context

A set of active filters applied to the entire model. Determines which data
is visible to any expression.

**Sources of filter context:**
- Slicer selections
- Visual axes and legend fields
- Page, report, and visual-level filters
- CALCULATE filter arguments
- Row-level security (RLS)
- Context transition from row context

**Key property:** Filter context propagates through relationships from the
"one" side to the "many" side (in single-direction relationships).

### Row Context

A pointer to "the current row" during an iteration. Exists inside:
- Iterator functions: SUMX, AVERAGEX, MINX, MAXX, COUNTX, RANKX, FILTER,
  ADDCOLUMNS, SELECTCOLUMNS, GENERATE
- Calculated columns (iterate the table)
- The condition of IF/SWITCH inside iterators

**Key properties:**
- Row context does NOT propagate through relationships (use RELATED/RELATEDTABLE)
- Multiple row contexts can be nested (e.g., SUMX inside SUMX)
- EARLIER accesses outer row contexts (legacy — use VAR instead)

---

## Context Transition

When a **measure** is evaluated inside a row context, DAX automatically
wraps it in an implicit CALCULATE. This converts the row context into an
equivalent filter context — called **context transition**.

### How It Works

```
Inside SUMX(Products, [Sales Amount]):
  For each row in Products:
    1. Row context provides: Product[Key] = current key
    2. Context transition: CALCULATE([Sales Amount], Product[Key] = current key)
    3. Filter context now filters FactSales via relationship
    4. [Sales Amount] = SUM(FactSales[Amount]) returns product's total sales
```

### When Context Transition Happens

| Expression | Context Transition? |
|---|---|
| `SUMX(Products, [Sales Amount])` | YES — [Sales Amount] is a measure |
| `SUMX(Sales, Sales[Qty] * Sales[Price])` | NO — column references only |
| `SUMX(Sales, [Sales Amount])` | YES — measure reference on fact table! |
| `ADDCOLUMNS(Products, "S", [Sales Amount])` | YES — measure in expression |
| `FILTER(Products, [Sales Amount] > 100)` | YES — measure in condition |

### Cost of Context Transition

**On dimension tables (recommended):** Low cost. Dimension tables have primary
keys, so context transition produces an efficient single-column filter.

**On fact tables (AVOID):** Very expensive. Fact tables typically have no
primary key. DAX must filter on ALL columns to identify the row. Each row in
the iteration produces a separate storage engine query → O(n) queries where
n = number of rows.

### The Rule

```
✅ SUMX(DimProduct, [Sales Amount])        — Context transition on dimension
❌ SUMX(FactSales, [Sales Amount])          — Context transition on fact table
✅ SUMX(FactSales, Sales[Qty] * Sales[Price]) — Column refs, no transition
```

---

## CALCULATE Execution Order

CALCULATE changes the evaluation context. Its execution follows a strict order
that is critical for correctness:

### Step-by-Step

```
CALCULATE(<expression>, <filter1>, <filter2>, ...)

Step 1: Evaluate ALL filter arguments in the ORIGINAL context
        (before any modification)

Step 2: Copy the original filter context as the base for the new context

Step 3: If row contexts exist → perform context transition
        (row context converted to filter context)

Step 4: Apply CALCULATE MODIFIERS to the new context
        - ALL / ALLEXCEPT / ALLSELECTED / REMOVEFILTERS
        - USERELATIONSHIP / CROSSFILTER

Step 5: Apply explicit filter arguments to the new context
        - Each filter REPLACES the existing filter on that column
        - KEEPFILTERS: INTERSECTS instead of replaces
```

### Why Order Matters

**Example: ALLEXCEPT + context transition**

```dax
% of Category =
CALCULATE(
    [Sales Amount],
    ALLEXCEPT(DimProduct, DimProduct[Category])
)
```

Inside a matrix with Category and ProductName:
1. Original context: Category="Bikes", ProductName="Mountain-200"
2. Context transition adds: Category="Bikes", ProductName="Mountain-200"
3. ALLEXCEPT removes all Product filters EXCEPT Category
4. Result: Category="Bikes" only → correct % of category total

Without understanding step order, this measure looks like it would just
return [Sales Amount] unchanged.

---

## KEEPFILTERS vs. Default Behavior

By default, CALCULATE filter arguments **replace** existing filters on the
same column:

```dax
-- Default: REPLACES any existing Year filter
Only 2023 = CALCULATE([Sales], DimDate[Year] = 2023)
-- If user selects 2022 in a slicer → returns 2023 data (slicer ignored!)
```

KEEPFILTERS **intersects** with existing filters instead:

```dax
-- KEEPFILTERS: intersects with existing Year filter
Sales 2023 = CALCULATE([Sales], KEEPFILTERS(DimDate[Year] = 2023))
-- If user selects 2022 → returns BLANK (2022 ∩ 2023 = empty)
-- If user selects 2023 → returns 2023 data
```

### When to Use KEEPFILTERS

- When the filter should respect slicer selections (most common)
- When building conditional measures that shouldn't override user choices
- Inside calculation group items to preserve external filter context

---

## The ALL Family

| Function | Used As | Behavior |
|---|---|---|
| `ALL(table)` | CALCULATE modifier | Removes ALL filters from the table |
| `ALL(col1, col2)` | CALCULATE modifier | Removes filters from specific columns |
| `ALLEXCEPT(table, col)` | CALCULATE modifier | Removes all EXCEPT specified columns |
| `ALLSELECTED()` | CALCULATE modifier | Restores filters from outside current visual |
| `ALLNOBLANKROW(table)` | CALCULATE modifier | Like ALL but excludes blank row |
| `REMOVEFILTERS()` | CALCULATE modifier | Alias for ALL (preferred in new code) |
| `ALL(table)` | Table function | Returns all rows (ignores all filters) |
| `VALUES(col)` | Table function | Returns visible distinct values |
| `DISTINCT(col)` | Table function | Returns distinct values (no blank row) |

### The ALLEXCEPT Trap

ALLEXCEPT only preserves **directly** applied filters. Cross-filters
(filters arriving via relationships) are NOT preserved:

```dax
-- UNRELIABLE with cross-filters:
CALCULATE([Sales], ALLEXCEPT(Customer, Customer[Segment]))
-- If Segment is only cross-filtered (not directly), this = ALL(Customer)!

-- RELIABLE pattern:
CALCULATE([Sales], ALL(Customer), VALUES(Customer[Segment]))
-- ALL removes everything, VALUES re-applies visible values (respects cross-filters)
```

**Rule:** Prefer `ALL + VALUES` over `ALLEXCEPT` unless you are certain
the preserved column is always directly filtered.

---

## Expanded Tables

Every table in DAX has an **expanded version** that contains all columns of the
base table plus all columns reachable by following many-to-one relationships.
This is the theoretical foundation for understanding filter propagation.

Based on "The Definitive Guide to DAX" Ch. 14 (Ferrari & Russo).

### How Expansion Works

Expansion follows **many-to-one relationships** outward from the base table:

```
Model: Sales →* Product →* Product Subcategory →* Product Category
                Sales →* Date

Expanded Sales   = Sales + Product + Product Subcategory + Product Category + Date
Expanded Product = Product + Product Subcategory + Product Category
Expanded Product Subcategory = Product Subcategory + Product Category
Expanded Product Category    = Product Category (no outgoing many-to-one)
Expanded Date                = Date (no outgoing many-to-one)
```

**Rules:**
- Expansion goes toward the **one-side** of a relationship only
- One-to-many (reversed direction) does NOT expand the table
- **Bidirectional cross-filter** does NOT change expansion — it uses a different
  mechanism (filter injection by the engine)
- **Weak relationships (MMR)** where both sides are "many" do NOT expand in
  either direction
- **One-to-one relationships** expand in both directions (both sides are "one")

### Why Expanded Tables Matter

Filter context propagation works on expanded tables:

> When a filter is applied to a column, it filters **every expanded table
> that contains that column**.

```dax
-- When a slicer filters Product[Color] = "Red":
-- → Product is filtered (native column)
-- → Sales is filtered (its expanded version includes Product columns)
-- → Product Subcategory is NOT filtered (its expansion does not include Product)
-- → Date is NOT filtered
```

This explains:
- Why filtering a dimension automatically filters its fact table
- Why filtering a fact table does NOT filter dimensions (unless bidirectional)
- Why ALL(Product) removes filters from Sales too (Sales' expanded table
  includes Product columns)

### Table Filters vs. Column Filters in CALCULATE

A table filter in CALCULATE filters all columns of the **expanded** table — not
just the columns explicitly in the table:

```dax
-- Table filter: filters ALL columns of expanded Product (includes Subcategory, Category)
CALCULATE([Sales Amount], FILTER(ALL(Product), Product[Color] = "Red"))
-- This is equivalent to filtering on ALL columns, then keeping Red rows.
-- The SE must group by ALL Product columns → large datacache → slow!

-- Column filter: filters ONLY the specified column
CALCULATE([Sales Amount], Product[Color] = "Red")
-- The SE applies a simple predicate → fast!

-- This is why "never use table filters in CALCULATE" is a golden rule.
-- A table filter over a fact table (Sales) includes ALL columns of Sales'
-- expanded table = the entire model → catastrophic performance.
```

### Expansion and RELATED / RELATEDTABLE

- **RELATED** navigates from many-side to one-side (follows expansion direction).
  Works because the expanded table already "contains" the related column.
- **RELATEDTABLE** navigates from one-side to many-side (reverse expansion).
  Returns the rows of the related table that match the current row context.

---

## ALLSELECTED and Shadow Filter Contexts

ALLSELECTED is one of the most misunderstood DAX functions because it relies
on an invisible concept: the **shadow filter context**.

Based on "The Definitive Guide to DAX" Ch. 14 (Ferrari & Russo).

### What ALLSELECTED Actually Does

ALLSELECTED does **not** mean "remove filters from the current visual and keep
slicer selections." That is an oversimplification.

Precisely: ALLSELECTED **restores the filter context that was active just before
the outermost SUMMARIZECOLUMNS / iterator that introduced the current
grouping**.

This "just before" context is called the **shadow filter context**.

### Shadow Filter Context

When Power BI generates a query for a visual, the structure is typically:

```dax
-- What Power BI generates:
EVALUATE
SUMMARIZECOLUMNS(
    Product[Category],          -- Group by (creates row contexts → filter contexts)
    TREATAS({2023}, Date[Year]), -- Slicer filter
    "Sales", [Sales Amount]
)
```

The shadow filter context = the context **before** SUMMARIZECOLUMNS starts
iterating. It contains the slicer filters (Year = 2023) but NOT the per-row
Category grouping.

When a measure uses ALLSELECTED:

```dax
% of Visible Total =
DIVIDE(
    [Sales Amount],
    CALCULATE([Sales Amount], ALLSELECTED(Product[Category]))
)
```

ALLSELECTED(Product[Category]) removes the Category filter added by the
visual's grouping, **restoring** the shadow filter context (Year = 2023 only).
The denominator becomes the total across all visible categories.

### ALLSELECTED Without Parameters

`ALLSELECTED()` with no parameters restores the **entire** shadow filter
context — removing all filters introduced by the visual's grouping columns.

```dax
% of Grand Visible Total =
DIVIDE(
    [Sales Amount],
    CALCULATE([Sales Amount], ALLSELECTED())
)
-- Denominator = total across all visual grouping columns, but slicer filters remain
```

### Common ALLSELECTED Pitfalls

**Pitfall 1: Nested CALCULATE changes the shadow**

```dax
-- UNRELIABLE: inner CALCULATE creates a new shadow context
Bad % =
CALCULATE(
    DIVIDE(
        [Sales Amount],
        CALCULATE([Sales Amount], ALLSELECTED(Product[Category]))
    ),
    Product[Color] = "Red"
)
-- The outer CALCULATE modified the filter context.
-- ALLSELECTED now restores a shadow that includes Color = "Red",
-- which may not be the intended behavior.
```

**Pitfall 2: ALLSELECTED with columns not in the visual**

```dax
-- If Product[Brand] is NOT on the visual axes:
CALCULATE([Sales Amount], ALLSELECTED(Product[Brand]))
-- The shadow filter context has no Brand filter to restore → acts like ALL(Product[Brand])
-- This is often the correct behavior, but can surprise when Brand IS on rows
```

**Rule:** Use ALLSELECTED only for "percentage of visual total" patterns.
For explicit denominator control, prefer `ALL + VALUES` combinations.

---

## Table Functions: Context Behavior

| Function | Creates Row Context? | Modifies Filter Context? |
|---|---|---|
| `FILTER(table, condition)` | YES (iterates rows) | NO |
| `ADDCOLUMNS(table, "name", expr)` | YES (new row context) | NO |
| `SELECTCOLUMNS(table, "name", expr)` | YES (new row context) | NO |
| `SUMMARIZE(table, groupCols)` | YES | YES (group context) |
| `CALCULATETABLE(table, filters)` | NO | YES (like CALCULATE) |
| `GENERATE(table1, table2Expr)` | YES (outer rows) | NO |
| `CROSSJOIN(table1, table2)` | NO | NO |
| `TREATAS(table, col1, col2)` | NO | YES (applies lineage) |

### FILTER vs. CALCULATETABLE

- **FILTER**: Iterates rows and applies condition. No filter context change.
  The expression sees the original filter context.
- **CALCULATETABLE**: Changes filter context FIRST, then evaluates the table
  expression in the new context. Equivalent to CALCULATE for tables.

```dax
-- FILTER: rows evaluated in original context, then filtered
FILTER(Product, [Sales Amount] > 1000)  -- [Sales Amount] sees all slicers

-- CALCULATETABLE: changes context first
CALCULATETABLE(Product, [Sales Amount] > 1000)  -- filters added to context
```

---

## Data Lineage and TREATAS

Every column in DAX carries **data lineage** — a link to the column it
originated from. This determines whether a table can filter the model.

- Columns from model tables → have lineage → can filter
- Columns from anonymous tables (ROW, {}, SELECTCOLUMNS with renamed cols) → no lineage → cannot filter

TREATAS assigns lineage to anonymous table columns:

```dax
-- Without TREATAS: no filtering effect
CALCULATE([Sales], {2023})  -- Does nothing!

-- With TREATAS: proper filtering
CALCULATE([Sales], TREATAS({2023}, DimDate[Year]))  -- Filters Year=2023

-- Virtual relationship: filter across tables without physical relationship
Customer Segment Sales =
CALCULATE(
    [Total Sales],
    TREATAS(
        VALUES(SegmentMapping[CustomerKey]),
        FactSales[CustomerKey]
    )
)
```

---

## Common Context Mistakes

### Mistake 1: Expecting row context to propagate

```dax
-- WRONG: Row context doesn't cross relationships
Revenue = SUMX(FactSales, FactSales[Qty] * DimProduct[UnitPrice])
-- DimProduct[UnitPrice] is not accessible in FactSales row context!

-- CORRECT: Use RELATED to cross relationships
Revenue = SUMX(FactSales, FactSales[Qty] * RELATED(DimProduct[UnitPrice]))
```

### Mistake 2: Variables don't re-evaluate

```dax
-- WRONG:
VAR _total = [Sales Amount]
RETURN DIVIDE([Sales Amount], CALCULATE(_total, ALL(DimProduct)))
-- _total was already evaluated — CALCULATE has no effect on it!

-- CORRECT:
DIVIDE(
    [Sales Amount],
    CALCULATE([Sales Amount], ALL(DimProduct))
)
```

### Mistake 3: ALLEXCEPT in cross-filter scenarios

See "The ALLEXCEPT Trap" above.

### Mistake 4: Confusing HASONEVALUE with "user selected one"

```dax
-- HASONEVALUE = exactly one value VISIBLE, not necessarily user-selected
-- In a matrix, each cell has one value for the row dimension → HASONEVALUE = TRUE
-- At total level → HASONEVALUE = FALSE

-- Use SELECTEDVALUE for safe extraction:
Current Year = SELECTEDVALUE(DimDate[Year], "Multiple Years")
```
