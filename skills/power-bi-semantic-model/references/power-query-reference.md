# Power Query / M Language Reference

Power Query (M language) handles data extraction, transformation, and loading (ETL)
in the semantic model. Every partition's `source` expression is M code.

---

## M Language Fundamentals

### Expression Structure

Every M expression follows the `let...in` pattern:

```powerquery-m
let
    // Step 1: Connect to source
    Source = Sql.Database("server.database.windows.net", "SalesDB"),

    // Step 2: Navigate to table
    dbo_Sales = Source{[Schema="dbo", Item="FactSales"]}[Data],

    // Step 3: Transform
    RenamedColumns = Table.RenameColumns(dbo_Sales, {
        {"sale_amount", "SalesAmount"},
        {"order_dt", "OrderDate"}
    }),

    // Step 4: Set types
    TypedColumns = Table.TransformColumnTypes(RenamedColumns, {
        {"SalesAmount", type number},
        {"OrderDate", type date},
        {"CustomerID", Int64.Type}
    })
in
    TypedColumns    // Final step name = output
```

### Key Syntax Rules

| Rule | Example |
|---|---|
| Steps are `Name = Expression` | `Filtered = Table.SelectRows(...)` |
| Steps are comma-separated | Each step ends with `,` except the last |
| `in` returns the final value | `in TypedColumns` |
| Case-sensitive | `Table.SelectRows` not `table.selectrows` |
| String literals use `"..."` | `"Hello"` |
| Comments: `//` or `/* */` | `// This is a comment` |
| Field access: `[ColumnName]` | `each [SalesAmount] > 0` |
| Record field: `{[Key=Value]}` | `Source{[Schema="dbo"]}` |

---

## Common Data Source Connections

### SQL Server / Azure SQL

```powerquery-m
Source = Sql.Database("server.database.windows.net", "DatabaseName", [
    Query = "SELECT * FROM dbo.FactSales WHERE IsDeleted = 0",
    CommandTimeout = #duration(0, 0, 10, 0)
])
```

### Azure Data Lake / Lakehouse (Parquet)

```powerquery-m
Source = AzureStorage.DataLake("https://account.dfs.core.windows.net/container"),
Filtered = Source{[Name="sales/2024/"]}[Content],
Imported = Parquet.Document(Filtered)
```

### SharePoint Online List

```powerquery-m
Source = SharePoint.Tables("https://tenant.sharepoint.com/sites/SiteName", [
    ApiVersion = 15
]),
SalesList = Source{[Title="SalesData"]}[Items]
```

### Excel File

```powerquery-m
Source = Excel.Workbook(File.Contents("C:\Data\Sales.xlsx"), null, true),
Sheet1 = Source{[Item="Sheet1", Kind="Sheet"]}[Data],
PromotedHeaders = Table.PromoteHeaders(Sheet1, [PromoteAllScalars=true])
```

### Web API (REST/JSON)

```powerquery-m
Source = Json.Document(Web.Contents("https://api.example.com/sales", [
    Headers = [#"Authorization" = "Bearer " & Token, #"Content-Type" = "application/json"],
    Query = [startDate = "2024-01-01", pageSize = "1000"]
]))
```

### Dataverse

```powerquery-m
Source = CommonDataService.Database("https://org.crm.dynamics.com"),
Accounts = Source{[Schema="dbo", Item="account"]}[Data]
```

---

## Essential Transformations

### Filter Rows

```powerquery-m
// Simple filter
Filtered = Table.SelectRows(Source, each [Status] = "Active")

// Multiple conditions
Filtered = Table.SelectRows(Source, each
    [OrderDate] >= #date(2024, 1, 1)
    and [Amount] > 0
    and [Region] <> null
)

// Filter nulls
NoNulls = Table.SelectRows(Source, each [CustomerID] <> null)
```

### Select / Remove Columns

```powerquery-m
// Keep only needed columns (removes all others)
Selected = Table.SelectColumns(Source, {
    "OrderID", "OrderDate", "CustomerID", "Amount", "ProductID"
})

// Remove specific columns
Removed = Table.RemoveColumns(Source, {"TempCol", "InternalID", "ETL_Timestamp"})
```

### Rename Columns

```powerquery-m
Renamed = Table.RenameColumns(Source, {
    {"order_id", "OrderID"},
    {"cust_id", "CustomerID"},
    {"amt", "Amount"}
})
```

### Change Data Types

```powerquery-m
Typed = Table.TransformColumnTypes(Source, {
    {"OrderDate", type date},
    {"Amount", Currency.Type},
    {"Quantity", Int64.Type},
    {"ProductName", type text},
    {"IsActive", type logical}
})
```

### Add Calculated Columns

```powerquery-m
// Simple calculation
WithMargin = Table.AddColumn(Source, "Margin", each [Revenue] - [Cost], type number)

// Conditional column
WithCategory = Table.AddColumn(Source, "SizeCategory", each
    if [Amount] >= 10000 then "Large"
    else if [Amount] >= 1000 then "Medium"
    else "Small",
    type text
)

// Date extraction
WithYear = Table.AddColumn(Source, "Year", each Date.Year([OrderDate]), Int64.Type)
WithMonth = Table.AddColumn(WithYear, "MonthName", each Date.MonthName([OrderDate]), type text)
```

### Merge (Join) Tables

```powerquery-m
// Left outer join — keep all rows from Source, match from DimProduct
Merged = Table.NestedJoin(
    Source, {"ProductID"},          // Left table + key column(s)
    DimProduct, {"ProductID"},      // Right table + key column(s)
    "ProductDetails",               // New column name for joined table
    JoinKind.LeftOuter              // Join type
)

// Expand the joined columns you need
Expanded = Table.ExpandTableColumn(Merged, "ProductDetails", {
    "ProductName", "Category", "SubCategory"
})
```

**Join types:** `JoinKind.LeftOuter`, `JoinKind.Inner`, `JoinKind.FullOuter`,
`JoinKind.RightOuter`, `JoinKind.LeftAnti`, `JoinKind.RightAnti`

### Append (Union) Tables

```powerquery-m
// Stack two tables with same columns
Combined = Table.Combine({Sales2023, Sales2024})
```

### Group By (Aggregation)

```powerquery-m
Grouped = Table.Group(Source, {"Region", "ProductCategory"}, {
    {"TotalRevenue", each List.Sum([Amount]), type number},
    {"OrderCount", each Table.RowCount(_), Int64.Type},
    {"AvgOrderValue", each List.Average([Amount]), type number}
})
```

### Pivot / Unpivot

```powerquery-m
// Unpivot month columns into rows
Unpivoted = Table.UnpivotOtherColumns(Source,
    {"ProductID", "ProductName"},   // Columns to keep
    "Month",                         // New attribute column
    "Value"                          // New value column
)

// Pivot rows into columns
Pivoted = Table.Pivot(Source,
    List.Distinct(Source[Region]),    // Unique values become columns
    "Region",                        // Column to pivot
    "Revenue",                       // Values column
    List.Sum                         // Aggregation function
)
```

---

## Query Folding

Query folding is the **single most important performance concept** in Power Query.
When a step "folds," it translates to a native source query (SQL) instead of
being processed in the M engine (slow, memory-bound).

### Checking for Folding

Right-click any step → **View Native Query**:
- If available → step folds ✅
- If grayed out → step does NOT fold ❌ (everything after also won't fold)

### Steps That Fold (Common)

| M Function | SQL Translation |
|---|---|
| `Table.SelectRows` | `WHERE` clause |
| `Table.SelectColumns` / `Table.RemoveColumns` | `SELECT` column list |
| `Table.Sort` | `ORDER BY` |
| `Table.FirstN` / `Table.Range` | `TOP` / `OFFSET FETCH` |
| `Table.Group` | `GROUP BY` |
| `Table.TransformColumnTypes` | `CAST` / `CONVERT` |
| `Table.RenameColumns` | Column alias `AS` |
| `Table.NestedJoin` (database tables) | `JOIN` |
| `Table.Distinct` | `SELECT DISTINCT` |
| `Table.ExpandTableColumn` (from same DB join) | Column list in `SELECT` |

### Steps That Break Folding

| M Function | Why It Breaks |
|---|---|
| `Table.AddColumn` (custom calculation) | No SQL equivalent for arbitrary M logic |
| `Table.Buffer` | Explicitly materializes in memory |
| Referencing other queries | Cross-source → no single SQL target |
| `Table.TransformColumns` (custom function) | Arbitrary M function can't translate |
| `Text.Combine`, `Text.Replace`, etc. | Complex string ops may not fold |
| `List.Generate`, `List.Accumulate` | Imperative loops → no SQL equivalent |

### Best Practices for Folding

1. **Do foldable operations FIRST** — filter, select columns, rename, type changes
2. **Do non-foldable operations LAST** — custom columns, complex transforms
3. **Use native query when needed** — `Value.NativeQuery(Source, "SELECT ...")` for complex SQL
4. **Test every step** — right-click → View Native Query after each step
5. **Avoid `Table.Buffer`** unless deliberately caching for performance

---

## Incremental Refresh Parameters

Required for incremental refresh configuration:

```powerquery-m
// These parameters must exist in the model
// Power BI Service replaces their values at refresh time
RangeStart = #datetime(2024, 1, 1, 0, 0, 0)
    meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]

RangeEnd = #datetime(2024, 12, 31, 0, 0, 0)
    meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
```

**Filter pattern (must fold!):**

```powerquery-m
let
    Source = Sql.Database(ServerName, DatabaseName),
    Sales = Source{[Schema="dbo", Item="FactSales"]}[Data],

    // This filter MUST fold to SQL WHERE for incremental refresh to work
    Filtered = Table.SelectRows(Sales, each
        [OrderDate] >= RangeStart and [OrderDate] < RangeEnd
    )
in
    Filtered
```

---

## Error Handling

```powerquery-m
// Replace errors in a column with null
CleanedColumn = Table.ReplaceErrorValues(Source, {{"Amount", null}})

// Try/otherwise for a single expression
SafeValue = try Number.FromText([PriceText]) otherwise 0

// Remove error rows entirely
NoErrors = Table.RemoveRowsWithErrors(Source, {"Amount", "Quantity"})
```

---

## Custom Functions

```powerquery-m
// Define a reusable function
CleanText = (input as text) as text =>
    let
        Trimmed = Text.Trim(input),
        Cleaned = Text.Clean(Trimmed),
        Upper = Text.Upper(Cleaned)
    in
        Upper

// Use in Table.AddColumn
WithClean = Table.AddColumn(Source, "CleanName", each CleanText([CustomerName]), type text)
```

---

## Performance Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Adding columns before filtering rows | Move `Table.SelectRows` before `Table.AddColumn` |
| Selecting all columns then removing some | Start with `Table.SelectColumns` (keep only needed) |
| Non-folding steps before filter | Restructure query so foldable filters come first |
| Using `Table.Buffer` for every query | Only buffer when intentionally preventing re-evaluation |
| Merging across different data sources | Push join to the source (SQL view) when possible |
| Complex M logic that could be SQL | Use `Value.NativeQuery()` for complex source-side logic |
| Not setting data types | Always set types explicitly — avoids type inference overhead |
| Loading unused queries | Disable load for staging/intermediate queries |

---

## TMDL Integration

In TMDL, the M expression lives in the partition definition:

```tmdl
table Sales
    partition Sales = m
        mode: import
        source =
            let
                Source = Sql.Database(ServerName, DatabaseName),
                dbo_Sales = Source{[Schema="dbo",Item="FactSales"]}[Data],
                Filtered = Table.SelectRows(dbo_Sales, each
                    [OrderDate] >= RangeStart and [OrderDate] < RangeEnd),
                Typed = Table.TransformColumnTypes(Filtered, {
                    {"SalesAmount", Currency.Type},
                    {"OrderDate", type date}
                })
            in
                Typed
```

---

## Quick Reference

| Task | M Function |
|---|---|
| Connect to SQL | `Sql.Database("server", "db")` |
| Filter rows | `Table.SelectRows(tbl, each [Col] = val)` |
| Select columns | `Table.SelectColumns(tbl, {"Col1", "Col2"})` |
| Remove columns | `Table.RemoveColumns(tbl, {"Col1"})` |
| Rename columns | `Table.RenameColumns(tbl, {{"old", "new"}})` |
| Set data types | `Table.TransformColumnTypes(tbl, {{"Col", type}})` |
| Add column | `Table.AddColumn(tbl, "Name", each expr, type)` |
| Merge (join) | `Table.NestedJoin(left, key, right, key, "new", kind)` |
| Append (union) | `Table.Combine({tbl1, tbl2})` |
| Group by | `Table.Group(tbl, {"keys"}, {{"agg", each func}})` |
| Unpivot | `Table.UnpivotOtherColumns(tbl, keep, attr, val)` |
| Pivot | `Table.Pivot(tbl, values, pivotCol, valCol, aggFunc)` |
| Replace errors | `Table.ReplaceErrorValues(tbl, {{"Col", null}})` |
| Native SQL | `Value.NativeQuery(src, "SELECT ...")` |
| Custom function | `(param as type) as type => let ... in result` |
