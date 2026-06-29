# Power BI Semantic Model Discovery Queries

Read-only DAX queries for metadata exploration using `INFO.VIEW.*` and `INFO.*` rowsets.

## Scope Estimation Queries

```dax
-- Probe object counts to estimate metadata scope before deep discovery
EVALUATE
ROW(
    "TableCount", COUNTROWS(INFO.VIEW.TABLES()),
    "ColumnCount", COUNTROWS(INFO.VIEW.COLUMNS()),
    "MeasureCount", COUNTROWS(INFO.VIEW.MEASURES()),
    "RelationshipCount", COUNTROWS(INFO.VIEW.RELATIONSHIPS())
)
```

## INFO Output Columns

### INFO.VIEW.* (preferred first-pass metadata)

| Function | High-value columns | What to use them for |
|---|---|---|
| `INFO.VIEW.TABLES()` | `Name`, `DataCategory`, `StorageMode`, `IsHidden`, `Expression`, `CalculationGroupPrecedence`, `LineageTag` | Table inventory, calculated-table detection, storage-mode audits, lineage tracking. |
| `INFO.VIEW.COLUMNS()` | `Table`, `Name`, `DataType`, `DataCategory`, `IsHidden`, `SummarizeBy`, `Expression`, `SortByColumn`, `FormatString`, `LineageTag` | Column dictionary, semantic typing, sort/summarization checks, calculated column review. |
| `INFO.VIEW.MEASURES()` | `Table`, `Name`, `Expression`, `FormatString`, `State`, `DisplayFolder`, `KPIID`, `LineageTag` | Measure inventory, formula review, formatting/state validation, KPI linkage. |
| `INFO.VIEW.RELATIONSHIPS()` | `Relationship`, `IsActive`, `FromTable`, `FromColumn`, `ToTable`, `ToColumn`, `FromCardinality`, `ToCardinality`, `CrossFilteringBehavior`, `SecurityFilteringBehavior` | Join topology, cardinality validation, filter-direction and RLS behavior checks. |

### Critical INFO.* (deep metadata / diagnostics)

| Function | High-value columns | What to use them for |
|---|---|---|
| `INFO.MODEL()` | `Name`, `DefaultMode`, `Culture`, `Collation`, `ModifiedTime`, `Version`, `DirectLakeBehavior`, `ValueFilterBehavior`, `SelectionExpressionBehavior` | Model policy/config audits and environment baseline. |
| `INFO.DEPENDENCIES()` | Commonly exposed dependency fields such as `OBJECT_TYPE`, `TABLE`, `OBJECT`, `REFERENCED_OBJECT_TYPE`, `REFERENCED_TABLE`, `REFERENCED_OBJECT` (engine-dependent) | Dependency graph for a DAX query and impact analysis for a target measure. |
| `INFO.EXPRESSIONS()` | Expression metadata including partition-bound query definitions | Inspect underlying queries bound to partition objects. |

```dax
-- Probe output schema of an INFO function (returns column names and types with zero data rows)
EVALUATE
TOPN(0, INFO.VIEW.COLUMNS())
```

## Narrowing Results (Projection + Filtering)

```dax
-- Pull only needed columns for a single table to reduce output volume
EVALUATE
SELECTCOLUMNS(
    FILTER(INFO.VIEW.COLUMNS(), [Table] = "YourTableName"),
    "Column", [Name],
    "DataType", [DataType]
)
ORDER BY [Column] ASC
```

## Deep Metadata Queries

```dax
-- Detailed model metadata
EVALUATE
INFO.MODEL()
```

```dax
-- Partition of a table
EVALUATE
FILTER(INFO.PARTITIONS(), [TableID] == 123)
```

```dax
-- Underlying queries bound to partition objects
EVALUATE
INFO.EXPRESSIONS()
ORDER BY [Name]
```

```dax
-- Cultures metadata objects
EVALUATE
INFO.CULTURES()
ORDER BY [Name]
```

```dax
-- Object translations metadata
EVALUATE
INFO.OBJECTTRANSLATIONS()
ORDER BY [CultureID], [ObjectID], [Property]
```

## Dependency Discovery

### Dependency rowset for a DAX query

```dax
-- Returns dependency graph for the query payload
DEFINE
VAR _Query = "EVALUATE SUMMARIZECOLUMNS('Date'[Year], 'Product'[Color], ""Sales"", [Sales])"
EVALUATE
INFO.DEPENDENCIES("QUERY", _Query)
```

### Dependency rows scoped to a measure

```dax
-- Adjust values to your model object names
EVALUATE
FILTER(
    INFO.DEPENDENCIES(),
    [OBJECT_TYPE] = "MEASURE"
        && [TABLE] = "Sales"
        && [OBJECT] = "Total Sales"
)
```

### Reverse dependencies (what references a measure)

```dax
-- Use when dependency columns are exposed in your engine rowset
EVALUATE
FILTER(
    INFO.DEPENDENCIES(),
    [REFERENCED_OBJECT_TYPE] = "MEASURE"
        && [REFERENCED_TABLE] = "Sales"
        && [REFERENCED_OBJECT] = "Total Sales"
)
```

> Dependency rowset column names may vary by engine/version; validate available fields with an unfiltered probe query first.

## Complete INFO Function Catalog (Dynamic)

> **Warning:** Only run this query if the required metadata object is not returned by any of the frequently used functions.

Use this query to enumerate all currently exposed `INFO.*` functions in the active engine/version.

```dax
EVALUATE
SELECTCOLUMNS(
    FILTER(
        INFO.FUNCTIONS(),
        LEFT([FUNCTION_NAME], 5) = "INFO."
    ),
    [FUNCTION_NAME]
)
```