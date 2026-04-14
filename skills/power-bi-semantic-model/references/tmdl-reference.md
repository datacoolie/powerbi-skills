# TMDL Reference

Comprehensive Tabular Model Definition Language (TMDL) syntax reference
for Power BI semantic models stored in PBIP format.

---

## TMDL File Structure

```
<ProjectName>.SemanticModel/
└── definition/
    ├── model.tmdl                ← Model-level properties
    ├── tables/
    │   ├── Sales.tmdl            ← One file per table
    │   ├── Date.tmdl
    │   └── Product.tmdl
    ├── relationships.tmdl        ← All relationships
    ├── roles.tmdl                ← RLS roles (if any)
    ├── cultures/
    │   └── en-US.tmdl            ← Translations
    ├── expressions.tmdl          ← Shared M expressions (parameters)
    └── perspectives.tmdl         ← Perspectives (if any)
```

---

## Model Definition (model.tmdl)

```tmdl
model Model
    culture: en-US
    defaultPowerBIDataSourceVersion: powerBI_V3
    discourageImplicitMeasures

    annotation PBI_QueryOrder = ["Sales", "Date", "Product", "Geography"]
```

| Property | Purpose |
|---|---|
| `culture` | Default locale for formatting |
| `defaultPowerBIDataSourceVersion` | Compatibility level |
| `discourageImplicitMeasures` | Prevent auto-SUM on columns |

---

## Tables

### Import Table

```tmdl
table Sales
    lineageTag: a1b2c3d4-...

    column SalesID
        dataType: int64
        isKey
        formatString: 0
        lineageTag: ...
        summarizeBy: none
        sourceColumn: SalesID

    column OrderDate
        dataType: dateTime
        formatString: Short Date
        lineageTag: ...
        sourceColumn: OrderDate

    column Revenue
        dataType: decimal
        formatString: $#,##0.00
        lineageTag: ...
        sourceColumn: Revenue

    column ProductID
        dataType: int64
        isHidden
        lineageTag: ...
        summarizeBy: none
        sourceColumn: ProductID

    measure 'Total Revenue' =
        SUM(Sales[Revenue])
        formatString: $#,##0
        displayFolder: Revenue Metrics
        lineageTag: ...

    measure 'Revenue YoY %' =
        ```
        VAR _current = [Total Revenue]
        VAR _prior = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))
        RETURN DIVIDE(_current - _prior, _prior)
        ```
        formatString: 0.0%;-0.0%;0.0%
        displayFolder: Revenue Metrics
        lineageTag: ...

    partition Sales = m
        mode: import
        source =
            let
                Source = Sql.Database("server.database.windows.net", "SalesDB"),
                dbo_Sales = Source{[Schema="dbo",Item="FactSales"]}[Data]
            in
                dbo_Sales

    annotation PBI_ResultType = Table
```

### Calculated Table

```tmdl
table 'Date'
    lineageTag: ...
    isHidden

    column Date
        dataType: dateTime
        isKey
        formatString: Short Date
        sourceColumn: [Date]

    column Year
        dataType: int64
        sourceColumn: [Year]
        sortByColumn: 'Date'[Date]

    column MonthName
        dataType: string
        sourceColumn: [MonthName]
        sortByColumn: 'Date'[MonthNumber]

    column MonthNumber
        dataType: int64
        isHidden
        sourceColumn: [MonthNumber]

    partition 'Date' = calculated
        expression =
            ```
            CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31))
            ```

    annotation PBI_ResultType = Table
```

### DirectLake Table

```tmdl
table Sales
    lineageTag: ...

    column Revenue
        dataType: decimal
        sourceColumn: Revenue
        sourceLineageTag: ...

    partition Sales = entity
        mode: directLake
        source
            entityName: Sales
            schemaName: dbo
            expressionSource: DatabaseQuery
```

---

## Column Properties

| Property | Values | Purpose |
|---|---|---|
| `dataType` | `string`, `int64`, `double`, `decimal`, `dateTime`, `boolean` | Column data type |
| `isKey` | (flag) | Marks column as table key |
| `isHidden` | (flag) | Hide from report field list |
| `formatString` | Format string | Number/date display format |
| `summarizeBy` | `none`, `sum`, `count`, `min`, `max`, `average` | Default aggregation |
| `sortByColumn` | `'Table'[Column]` | Sort this column by another column |
| `sourceColumn` | Source column name | Maps to source data column |
| `displayFolder` | Folder path | Organize in field list |
| `lineageTag` | GUID | Unique identifier for lineage tracking |
| `description` | Text | Column description for documentation |
| `dataCategory` | `Address`, `City`, `Country`, `WebUrl`, etc. | Semantic data category |

### Calculated Column

```tmdl
    column 'Profit Margin' =
        DIVIDE(Sales[Profit], Sales[Revenue])
        dataType: double
        formatString: 0.0%
        lineageTag: ...
```

---

## Measures

### Simple Measure

```tmdl
    measure 'Total Revenue' =
        SUM(Sales[Revenue])
        formatString: $#,##0
        displayFolder: Revenue
        lineageTag: ...
        description: "Sum of revenue from all sales transactions"
```

### Multi-Line Measure

```tmdl
    measure 'Revenue vs Target' =
        ```
        VAR _actual = [Total Revenue]
        VAR _target = [Revenue Target]
        VAR _variance = _actual - _target
        RETURN
            _variance
        ```
        formatString: $#,##0
        displayFolder: Variance Analysis
        lineageTag: ...
```

### Dynamic Format String (Measure)

```tmdl
    measure 'Dynamic Metric' =
        ```
        SWITCH(
            SELECTEDVALUE('Metric Selection'[Metric Selection]),
            "Revenue", [Total Revenue],
            "Units", [Total Units],
            [Total Revenue]
        )
        ```
        formatString: #,##0
        lineageTag: ...

        formatStringDefinition =
            ```
            SWITCH(
                SELECTEDVALUE('Metric Selection'[Metric Selection]),
                "Revenue", "$#,##0",
                "Units", "#,##0",
                "$#,##0"
            )
            ```
```

---

## Relationships (relationships.tmdl)

```tmdl
relationship rel_Sales_Date
    fromColumn: Sales.OrderDateKey
    toColumn: 'Date'.DateKey
    crossFilteringBehavior: oneDirection

relationship rel_Sales_Product
    fromColumn: Sales.ProductKey
    toColumn: Product.ProductKey
    crossFilteringBehavior: oneDirection

relationship rel_Sales_Geography
    fromColumn: Sales.GeographyKey
    toColumn: Geography.GeographyKey
    crossFilteringBehavior: oneDirection

/// Inactive relationship for ShipDate
relationship rel_Sales_ShipDate
    isActive: false
    fromColumn: Sales.ShipDateKey
    toColumn: 'Date'.DateKey
    crossFilteringBehavior: oneDirection
```

### Relationship Properties

| Property | Values | Purpose |
|---|---|---|
| `fromColumn` | `Table.Column` | Many-side (fact table) |
| `toColumn` | `Table.Column` | One-side (dimension table) |
| `crossFilteringBehavior` | `oneDirection`, `bothDirections` | Filter propagation |
| `isActive` | `true` (default), `false` | Active or inactive relationship |
| `securityFilteringBehavior` | `oneDirection`, `bothDirections` | RLS filter direction |
| `joinOnDateBehavior` | `datePartOnly` | For date columns |
| `relyOnReferentialIntegrity` | (flag) | Assume referential integrity (Import) |

---

## Roles (roles.tmdl)

```tmdl
role 'Regional Manager'
    modelPermission: read

    tablePermission Geography =
        ```
        VAR _userEmail = USERPRINCIPALNAME()
        VAR _userRegion =
            LOOKUPVALUE(
                SecurityMapping[Region],
                SecurityMapping[Email], _userEmail
            )
        RETURN
            [Region] = _userRegion
        ```

role 'Admin'
    modelPermission: read
    // No tablePermission = sees all data

role 'Sales Rep'
    modelPermission: read

    tablePermission SecurityBridge =
        'SecurityBridge'[Email] = USERPRINCIPALNAME()
```

---

## Shared Expressions (expressions.tmdl)

Parameters and shared M expressions used across tables:

```tmdl
expression ServerName =
    "server.database.windows.net" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
    lineageTag: ...

expression DatabaseName =
    "SalesDB" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
    lineageTag: ...

expression RangeStart =
    #datetime(2024, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
    lineageTag: ...

expression RangeEnd =
    #datetime(2024, 12, 31, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
    lineageTag: ...
```

---

## Calculation Groups

```tmdl
table 'Time Intelligence'
    calculationGroup

    column 'Time Calculation'
        dataType: string
        isKey
        sourceColumn: Name

    column Ordinal
        dataType: int64
        isHidden
        sourceColumn: Ordinal

    calculationItem Current =
        SELECTEDMEASURE()
        ordinal: 0

    calculationItem 'YoY' =
        ```
        VAR _current = SELECTEDMEASURE()
        VAR _prior = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
        RETURN _current - _prior
        ```
        ordinal: 1

    calculationItem 'YoY %' =
        ```
        VAR _current = SELECTEDMEASURE()
        VAR _prior = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
        RETURN DIVIDE(_current - _prior, _prior)
        ```
        ordinal: 2
        formatStringDefinition =
            ```
            "0.0%;-0.0%;0.0%"
            ```

    calculationItem 'YTD' =
        CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
        ordinal: 3
```

---

## Partitions

### Import Partition

```tmdl
    partition Sales = m
        mode: import
        source =
            let
                Source = Sql.Database(ServerName, DatabaseName),
                Data = Source{[Schema="dbo",Item="FactSales"]}[Data]
            in
                Data
```

### Incremental Refresh Partition

```tmdl
    partition 'Sales-2024-01' = m
        mode: import
        source =
            let
                Source = Sql.Database(ServerName, DatabaseName),
                Data = Source{[Schema="dbo",Item="FactSales"]}[Data],
                Filtered = Table.SelectRows(Data, each
                    [OrderDate] >= #datetime(2024, 1, 1, 0, 0, 0) and
                    [OrderDate] < #datetime(2024, 2, 1, 0, 0, 0))
            in
                Filtered
```

### DirectLake Partition

```tmdl
    partition Sales = entity
        mode: directLake
        source
            entityName: Sales
            schemaName: dbo
            expressionSource: DatabaseQuery
```

### Calculated Partition

```tmdl
    partition 'DateTable' = calculated
        expression =
            ```
            CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31))
            ```
```

---

## Composite Models (Mixed Storage Modes)

Composite models combine Import and DirectQuery partitions in the same model. Use Import
for dimensions and aggregated facts (fast); use DirectQuery for large detail tables (real-time).

### Storage Mode Per Partition

```tmdl
/// Import partition — data is cached in the model
table Sales
    partition Sales = m
        mode: import
        source =
            let
                Source = Sql.Database("server.database.windows.net", "SalesDB"),
                dbo_Sales = Source{[Schema="dbo",Item="FactSales"]}[Data]
            in
                dbo_Sales

/// DirectQuery partition — queries go live to the source
table SalesDetail
    partition SalesDetail = m
        mode: directQuery
        source =
            let
                Source = Sql.Database("server.database.windows.net", "SalesDB"),
                dbo_SalesDetail = Source{[Schema="dbo",Item="FactSalesDetail"]}[Data]
            in
                dbo_SalesDetail

/// Dual mode — acts as Import when related to Import tables, DirectQuery otherwise
table Product
    partition Product = m
        mode: dual
        source =
            let
                Source = Sql.Database("server.database.windows.net", "SalesDB"),
                dbo_Product = Source{[Schema="dbo",Item="DimProduct"]}[Data]
            in
                dbo_Product
```

### DirectLake Partition (Fabric Lakehouse / Warehouse)

```tmdl
table Sales
    partition Sales = entity
        mode: directLake
        entityName: FactSales
        schemaName: dbo
        source
            entitySource
                expressionSource: DatabaseQuery
```

### Composite Model Design Rules

- **Dimensions** shared between Import and DirectQuery facts → set to `dual` mode
- **Relationships** crossing storage boundaries require the shared table to be `dual`
- **RLS** filters apply to both Import and DirectQuery tables — test both paths
- **Aggregations**: Import tables can serve as aggregation caches for DirectQuery detail tables
- Avoid user-facing DAX that mixes Import and DirectQuery tables without a `dual` bridge

---

## Common Annotations

```tmdl
    annotation PBI_ResultType = Table
    annotation PBI_NavigationStepName = Navigation
    annotation PBI_QueryOrder = ["Sales", "Date", "Product"]
    annotation __PBI_TimeIntelligenceEnabled = 1
```

---

## Quick Reference

| Element | File | Syntax |
|---|---|---|
| Model properties | `model.tmdl` | `model Model` |
| Table | `tables/<Name>.tmdl` | `table '<Name>'` |
| Column | Inside table file | `column '<Name>'` indented |
| Measure | Inside table file | `measure '<Name>' = <DAX>` indented |
| Calc column | Inside table file | `column '<Name>' = <DAX>` indented |
| Relationship | `relationships.tmdl` | `relationship <name>` |
| Role | `roles.tmdl` | `role '<Name>'` |
| Calc group | `tables/<Name>.tmdl` | `calculationGroup` + `calculationItem` |
| Expression | `expressions.tmdl` | `expression <Name> = <M>` |
| Partition | Inside table file | `partition '<Name>' = m/entity/calculated` |

| Convention | Example |
|---|---|
| Multi-line DAX | Use triple backticks ``` |
| Hidden column | Add `isHidden` flag (no value needed) |
| Key column | Add `isKey` flag |
| Sort by | `sortByColumn: 'Table'[Column]` |
| Display folder | `displayFolder: Folder Name` |
| Format string | `formatString: $#,##0` |
