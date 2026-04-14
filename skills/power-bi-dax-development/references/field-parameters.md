# Field Parameters

Field parameters enable dynamic switching of measures, columns, or tables on
report visuals via slicer selection. They are essential for "let the user
choose what to display" scenarios.

---

## Overview

Field parameters create a **disconnected calculation table** with metadata
that Power BI uses to swap fields on visuals. The user selects a field
from a slicer, and visuals bound to that parameter update dynamically.

### Common Use Cases

| Scenario | Example |
|---|---|
| Dynamic measure switching | User picks Revenue, Margin, or Units on a chart |
| Dynamic axis switching | User picks Month, Quarter, or Year for X-axis |
| Dynamic column switching | User picks which dimension to group by (Region, Product, Category) |
| Calculation group pairing | Combine with time intelligence calculation groups |

---

## Creating Field Parameters

### In Power BI Desktop

1. **Modeling** tab → **New parameter** → **Fields**
2. Add fields (measures or columns) to the parameter
3. Optionally reorder fields (this sets the `Ordinal` column)
4. Check **"Add slicer to this page"** if desired
5. Click **Create**

### Generated DAX Pattern

Power BI generates a calculated table with three columns:

```dax
// Auto-generated — Metric Selection parameter
Metric Selection = {
    ("Revenue",   NAMEOF('Sales'[Revenue]),   0),
    ("Margin %",  NAMEOF('Sales'[Margin %]),  1),
    ("Units",     NAMEOF('Sales'[Units Sold]),2)
}
```

| Column | Purpose |
|---|---|
| Column 1 (Name) | Display text shown in slicer |
| Column 2 (Field) | Reference to the actual measure/column via `NAMEOF()` |
| Column 3 (Ordinal) | Sort order for slicer display |

### TMDL Representation

```tmdl
table 'Metric Selection'
    isParameterTable

    column 'Metric Selection'
        dataType: string
        isNameInferredFromColumn
        sourceColumn: Metric Selection.[Value1]
        sortByColumn: 'Metric Selection Ordinal'

    column 'Metric Selection Fields'
        dataType: string
        isHidden
        isNameInferredFromColumn
        sourceColumn: Metric Selection.[Value2]

    column 'Metric Selection Ordinal'
        dataType: int64
        isHidden
        isNameInferredFromColumn
        sourceColumn: Metric Selection.[Value3]

    partition 'Metric Selection' = calculated
        expression = ```
            {
                ("Revenue",   NAMEOF('Sales'[Revenue]),   0),
                ("Margin %",  NAMEOF('Sales'[Margin %]),  1),
                ("Units",     NAMEOF('Sales'[Units Sold]),2)
            }
            ```
```

---

## Binding to Visuals (PBIR JSON)

When a visual uses a field parameter, the visual.json references the
parameter's Fields column:

```jsonc
// In visual.json → prototypeQuery → Select
{
    "Column": {
        "Expression": {
            "SourceRef": { "Entity": "Metric Selection" }
        },
        "Property": "Metric Selection"   // The display column
    }
}
```

### Slicer Configuration for Field Parameter

```jsonc
// Slicer visual.json using field parameter
{
    "visual": {
        "visualType": "slicer",
        "objects": {
            "data": [{
                "properties": {
                    "mode": { "expr": { "Literal": { "Value": "'Dropdown'" } } }
                }
            }]
        },
        "prototypeQuery": {
            "Select": [{
                "Column": {
                    "Expression": {
                        "SourceRef": { "Entity": "Metric Selection" }
                    },
                    "Property": "Metric Selection"
                },
                "Name": "Metric Selection.Metric Selection"
            }]
        }
    }
}
```

---

## Advanced Patterns

### Dynamic Measure Switching with Calculation Groups

Combine field parameters with calculation groups for maximum flexibility:

```dax
// Field parameter for time intelligence
Time Comparison = {
    ("Current Period",  NAMEOF('Time Intelligence'[Current]),  0),
    ("YoY Change",      NAMEOF('Time Intelligence'[YoY]),      1),
    ("YoY %",           NAMEOF('Time Intelligence'[YoY %]),    2),
    ("YTD",             NAMEOF('Time Intelligence'[YTD]),       3)
}

// Calculation group measures (separate calculation group table)
// Current  :=  SELECTEDMEASURE()
// YoY      :=  SELECTEDMEASURE() - CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
// YoY %    :=  DIVIDE([YoY], CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date])))
// YTD      :=  CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
```

### Multiple Field Parameters on One Visual

Use separate parameters for axis and values:

```dax
// Axis parameter — user picks dimension
Dimension Selection = {
    ("Region",   NAMEOF('Geography'[Region]),   0),
    ("Category", NAMEOF('Product'[Category]),    1),
    ("Channel",  NAMEOF('Sales'[Channel]),       2)
}

// Metric parameter — user picks measure
Metric Selection = {
    ("Revenue", NAMEOF('Sales'[Revenue]), 0),
    ("Units",   NAMEOF('Sales'[Units]),   1)
}
```

### Conditional Formatting with Field Parameters

Since the active field changes dynamically, use `SELECTEDVALUE` on the
parameter to apply conditional logic:

```dax
Dynamic Format String =
VAR _selected = SELECTEDVALUE('Metric Selection'[Metric Selection])
RETURN
    SWITCH(
        _selected,
        "Revenue",  "$#,##0",
        "Margin %", "0.0%",
        "Units",    "#,##0",
        "#,##0"
    )
```

---

## Limitations & Gotchas

| Limitation | Workaround |
|---|---|
| Cannot mix measures and columns in same parameter | Create separate parameters |
| No implicit filtering by parameter selection | Use `SELECTEDVALUE()` in DAX for conditional logic |
| Display names must be unique | Use descriptive names ("Revenue $" vs "Revenue %") |
| Sort order is by Ordinal column | Always include Ordinal and set Sort By Column |
| Not supported in DirectQuery live connections | Works in Import, DirectQuery (standalone), DirectLake |
| Cannot reference field parameters in DAX measures | Use `SELECTEDVALUE()` on the name column instead |
| Slicer shows all options regardless of context | Expected — parameter is a disconnected table |

---

## Quick Reference

| Task | Approach |
|---|---|
| Create field parameter | Modeling → New Parameter → Fields |
| Dynamic metric slicer | Field parameter with measures + slicer visual |
| Dynamic axis | Field parameter with columns + bind to axis |
| Time intelligence switching | Pair with calculation group |
| Format string per metric | `SWITCH(SELECTEDVALUE(...))` pattern |
| Verify in TMDL | Look for `isParameterTable` annotation |
