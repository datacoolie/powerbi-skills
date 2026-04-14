# Advanced Relationship Patterns

Complex relationship scenarios that go beyond basic star schema. Based on
"The Definitive Guide to DAX" Ch. 15 (Ferrari & Russo).

---

## Physical vs. Virtual Relationships

### Performance Hierarchy

Always prefer physical relationships where possible. Performance ranking:

| Priority | Type | Engine Behavior |
|----------|------|-----------------|
| 1 (best) | **Physical one-to-many** | Optimized by VertiPaq; SE handles joins |
| 2 | **Calculated physical** (via calculated column) | Same query performance as native; computed at refresh |
| 3 | **Bidirectional cross-filter / table expansion / MMR weak** | Good but not optimal; engine has less optimization room |
| 4 (worst) | **Virtual** (TREATAS, FILTER in measures) | FE handles join logic; no pre-built structures |

**Rule:** If a logical relationship is used in many measures, create a
physical relationship (even via calculated/bridge table). Reserve virtual
relationships (TREATAS) for one-off scenarios or when physical relationships
are architecturally impossible.

---

## Many-to-Many Patterns

### Pattern 1: Bridge Table (Classic)

When two tables share a many-to-many relationship, create a bridge table
containing the valid combinations:

```
Customer →* CustomerSegmentBridge *← Segment
```

```dax
-- Bridge table connects Customer to Segment
-- Relationship: Customer[CustomerKey] 1→M Bridge[CustomerKey]
-- Relationship: Segment[SegmentKey]   1→M Bridge[SegmentKey]
-- Both relationships: single direction toward fact table

-- In measures:
Sales by Segment =
CALCULATE(
    [Total Sales],
    RELATEDTABLE(CustomerSegmentBridge)  -- Leverages physical relationship
)
```

**Advantage:** Physical relationships, engine-optimized.
**Disadvantage:** Requires creating and maintaining the bridge table.

### Pattern 2: MMR Weak Relationships

DAX supports **weak relationships** where both columns can contain duplicates
(Many-to-Many Relationship — MMR). Created by linking columns with
duplicates on both sides.

```
Budget[Brand] *←→* Product[Brand]
Budget[CountryRegion] *←→* Customer[CountryRegion]
```

**Advantages:**
- No bridge table needed
- Simpler model diagram
- Single `Budget Amt = SUM(Budget[Budget])` works without custom DAX

**Critical trap — no blank row in weak relationships:**

When a weak relationship is invalid (e.g., Budget has "Italy" but Customer
has no "Italy"), the orphaned rows are **silently hidden** — no blank row is
created. The grand total includes the hidden values, but no row displays them.

```
Expected report:
  France     200
  Germany    300
  Italy      150    ← MISSING! Italy exists in Budget but not in Customer
  Total      650    ← Total includes Italy's 150, but no visible row shows it

Result: Grand total > sum of visible rows → confusing!
```

**When to use MMR vs. bridge table:**

| Criterion | MMR Weak | Bridge Table |
|-----------|----------|--------------|
| Simplicity | Simpler (no extra table) | Requires materialized table |
| Missing values | Hidden (no blank row) | Visible (blank row appears) |
| Filtering direction | Configurable (single or both) | Via relationship chain |
| Performance | Similar to bridge table | Similar to MMR |
| Debugging | Harder (hidden rows) | Easier (orphans visible) |

**Recommendation:** Use MMR when data integrity is guaranteed. Use bridge
tables when you need missing values to be visible in reports.

### Pattern 3: Virtual M:M with TREATAS

```dax
Budget Amt =
CALCULATE(
    SUM(Budget[Budget]),
    TREATAS(VALUES(Product[Brand]), Budget[Brand]),
    TREATAS(VALUES(Customer[CountryRegion]), Budget[CountryRegion])
)
```

Use when physical relationships are not possible (different granularity,
different data sources, composite models).

---

## Granularity Mismatch

When a relationship connects at a **lower granularity** than the primary key,
filtering by higher-detail columns produces misleading results.

### The Problem

```
Product[Brand] *←→* Budget[Brand]   (relationship at Brand level)

When a report filters by Product[Color]:
1. Cross-filter: Product[Color] = "Blue" → some Brands have blue products
2. Budget sees only those Brands → Budget shows budgets for those Brands
3. BUT: the budget amount is the TOTAL for the brand, not just blue products
4. Result: identical budget numbers for every color within a brand
```

### Detection Pattern

Create a measure that checks if the browsing granularity matches the
relationship granularity:

```dax
NumOfProducts_BudgetGrain =
CALCULATE(
    COUNTROWS(Product),
    ALLEXCEPT(Product, Product[Brand])    -- Keep only Brand (the relationship grain)
)

Budget Amt Safe =
VAR _allProducts = [NumOfProducts_BudgetGrain]
VAR _visibleProducts = COUNTROWS(Product)
RETURN
    IF(
        _visibleProducts = _allProducts,
        [Budget Amt],
        BLANK()                           -- Hide meaningless numbers
    )
```

**Rule:** When using lower-granularity relationships, always validate that
the visual's browsing granularity matches the relationship granularity.
Hide values at incompatible grain levels.

---

## Role-Playing Dimensions (Multiple Relationships to Same Table)

Only **one** relationship between two tables can be active. Additional
relationships are inactive (dashed line in the model diagram).

```
Date[Date] 1→M Sales[OrderDate]     (ACTIVE)
Date[Date] 1→M Sales[ShipDate]      (INACTIVE)
Date[Date] 1→M Sales[DeliveryDate]  (INACTIVE)
```

### Activating Inactive Relationships

```dax
Sales by Ship Date =
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(Sales[ShipDate], Date[Date])
)
```

**Alternative — separate Date tables:** Create physical copies of the Date
table (OrderDate, ShipDate, DeliveryDate) with independent relationships.
Better performance but larger model.

| Approach | Pros | Cons |
|----------|------|------|
| USERELATIONSHIP | Single Date table, smaller model | Every measure needs modifier; can cause ambiguity |
| Separate Date tables | Simple measures, no modifiers needed | Larger model; multiple date hierarchies in field list |

---

## Ambiguity in Relationships

Ambiguity occurs when a filter can reach a table through multiple paths.

### Common Causes

1. **Bidirectional cross-filter** + multiple relationship paths
2. **USERELATIONSHIP** enabling a path that overlaps with existing active paths
3. **CROSSFILTER** modifier changing filter direction at query time

### How the Engine Resolves Ambiguity

- The DAX engine picks the **shortest path** to propagate a filter
- If the shortest path is disabled, the engine uses a longer one
- If multiple paths of equal length exist, the model is considered **ambiguous**
  and the engine refuses to create it

### Runtime Ambiguity (The Hidden Danger)

A model can be valid at design time but become ambiguous at query time:

```dax
-- Model: Date → Sales ← Product → Receipts ← Date (bidirectional on Sales-Product)

-- This measure creates runtime ambiguity:
Receipts Without Direct Date =
CALCULATE(
    [Receipts Amount],
    CROSSFILTER(Date[Date], Receipts[Date], NONE)    -- Disable direct path
)
-- Now Date → Sales → Product → Receipts is the only path
-- But another measure may not disable the direct path → different behavior!
```

**Rule:** Avoid models where filters can reach the same table through
multiple paths. If unavoidable, disable bidirectional filters and control
filter direction explicitly in measures.

---

## Relationship Design Checklist

```
□ Every relationship is one-to-many with single-direction filter (default)
□ Bidirectional cross-filter is enabled ONLY when required and documented
□ No ambiguous paths exist (check by enabling all bidirectional filters mentally)
□ Weak (MMR) relationships are used only with guaranteed data integrity
□ Role-playing dimensions use USERELATIONSHIP or separate tables (decided consistently)
□ Granularity mismatches are documented and measures validate browsing grain
□ Inactive relationships have clear naming and documentation
□ Virtual relationships (TREATAS) are used only when physical relationships are impossible
```
