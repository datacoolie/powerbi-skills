# User-Defined Functions (UDF) in DAX

> Preview feature — available in Power BI Desktop since late 2024.
> Check current GA status before relying on this in production.

---

## Overview

User-Defined Functions (UDFs) let you define reusable, parameterized DAX logic
that can be called from measures, calculated columns, or other UDFs. They reduce
code duplication and improve readability for repeated patterns.

---

## Syntax

```dax
DEFINE
    FUNCTION MyFunction(param1, param2[, ...])
        VAR _result = <expression using param1, param2>
        RETURN _result

EVALUATE
    { MyFunction(10, 20) }
```

### In TMDL (Model-Level UDF)

```tmdl
expression MyFunction =
    (param1 as number, param2 as number) =>
    VAR _result = param1 + param2
    RETURN _result
```

---

## Common Use Cases

### Safe Division with Custom Default

```dax
DEFINE
    FUNCTION SafeDivide(numerator, denominator, alt)
        RETURN IF(denominator = 0, alt, numerator / denominator)

EVALUATE { SafeDivide(100, 0, -1) }  -- Returns -1
```

### Percentage Formatting Logic

```dax
DEFINE
    FUNCTION PctChange(current, previous)
        RETURN DIVIDE(current - previous, ABS(previous))
```

### Reusable YoY Calculation

```dax
DEFINE
    FUNCTION YoY(measure_value, py_value)
        VAR _delta = measure_value - py_value
        VAR _pct = DIVIDE(_delta, ABS(py_value))
        RETURN _pct
```

---

## Limitations

| Limitation | Notes |
|---|---|
| Preview feature | May change before GA |
| Not supported in all tools | Check SSMS, Tabular Editor, DAX Studio support |
| Cannot reference model objects directly | Pass values as parameters |
| No recursion | Functions cannot call themselves |
| Query-scoped (DEFINE block) | Unless defined as model expressions (TMDL) |
| No side effects | Pure functions only — cannot modify state |

---

## When to Use vs. Alternatives

| Pattern | Use UDF When | Use Alternative When |
|---|---|---|
| Repeated DIVIDE logic | Same custom default in 10+ measures | Standard DIVIDE() suffices |
| Complex scoring formula | Multiple measures need same formula | Only 1-2 measures use it |
| Parameterized threshold | Threshold varies per caller | Fixed threshold → just hardcode |
| Multi-step normalization | 5+ steps repeated | 2-3 steps → inline VAR chain |

---

## Sources

- https://learn.microsoft.com/power-bi/transform-model/desktop-user-defined-functions
