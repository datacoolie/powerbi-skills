# Recipe: Field Parameter Measure/Dimension Switch

> **Preview:** [![field-parameter-switch preview](../../assets/slicer-previews/field-parameter-switch.svg)](../../assets/slicer-previews/field-parameter-switch.svg)

- **id:** `field-parameter-switch`
- **Family:** parameter
- **Control type:** field parameter + slicer
- **Cardinality:** low (3–7 options)
- **Scope:** page (or page group via sync)

---

## Composition

```
┌────────────────────────────────────────────────────────┐
│ Show:                                                  │
│ [● Revenue]  [○ Units]  [○ Margin %]   ← tile slicer  │
│                                                        │
│      ▲                                                 │
│      │ bound to field parameter                        │
│      ▼                                                 │
│ ┌────────────────────────────────────────────┐         │
│ │  Bar chart — values = selected measure     │         │
│ └────────────────────────────────────────────┘         │
└────────────────────────────────────────────────────────┘
```

One chart serves 3–5 views by letting users pick which measure (or which dimension) drives it.

---

## Slots & Bindings

| Slot | Purpose | Binding example |
|---|---|---|
| Field parameter table | Calculated table, 1 row per option | `GENERATESERIES("Revenue", "Units", "Margin %")` |
| Slicer | Bound to the parameter | Filter on `[Parameter]` |
| Visual field well | References the parameter column in place of a measure or dimension | `SUMX(VALUES(FactSales[Measure]), …)` |

---

## Two common uses

### A. Measure switch
User toggles between measures displayed on the same axis.

```
DAX:
Measures Parameter = {
    ("Revenue",   NAMEOF([Total Revenue]),   0),
    ("Units",     NAMEOF([Total Units]),     1),
    ("Margin %",  NAMEOF([Margin Pct]),      2)
}
```

### B. Dimension switch
User toggles the axis dimension of the same chart.

```
DAX:
Dim Parameter = {
    ("By Region",  NAMEOF(DimGeo[Region]),        0),
    ("By Channel", NAMEOF(DimChannel[Channel]),   1),
    ("By Brand",   NAMEOF(DimProduct[Brand]),     2)
}
```

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Slicer type | Chiclet tiles | Options always visible, one click to switch |
| Default selection | First option (index 0) | Predictable |
| Axis/value format | Matches the chosen option's format | Avoid mixing $ and % on same axis |
| Sort order | Explicit numeric column in the parameter table | Stable button order |

---

## Anti-patterns

❌ Mixing incompatible formats (Revenue in $ and Margin in %) on the same axis without conditional formatting.
❌ Putting a field parameter slicer on the global filter panel — forcing every page to accept the same axis choice is confusing.
❌ Using a field parameter when the real need is a second chart — if users want to see two measures side-by-side, show two charts.
❌ > 7 parameter options — the chiclet wraps; consider a dropdown or split the visuals.

---

## Pairs well with

- `bar-comparison`, `trend-line`, `small-multiples-trend` recipes (in `chart-templates/`)
- `chiclet-tile-slicer` (the picker)
- Analytical / exploration layouts with limited canvas

---

## Mobile note

Field parameters survive in mobile layouts; the slicer often moves above the chart to save horizontal space. Keep ≤ 4 options on mobile.
