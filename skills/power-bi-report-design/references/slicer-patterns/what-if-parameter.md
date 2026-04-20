# Recipe: What-If Parameter Slicer

> **Preview:** [![what-if-parameter preview](../../assets/slicer-previews/what-if-parameter.svg)](../../assets/slicer-previews/what-if-parameter.svg)

- **id:** `what-if-parameter`
- **Family:** parameter
- **Control type:** what-if parameter (numeric)
- **Cardinality:** continuous (bounded)
- **Scope:** page

---

## Composition

```
┌──────────────────────────────────────────────────────────┐
│  Scenario inputs                                         │
│                                                          │
│  Discount %   ●───────●────────    12 %                  │
│  FX rate      ●────────●───────    1.08 USD/EUR          │
│  Volume lift  ●─────●──────────    +5 %                  │
│                                                          │
│  ┌────────────────────────────────────────┐              │
│  │  KPI cards + chart recalculate live    │              │
│  └────────────────────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

Numeric sliders (or input boxes) drive DAX measures that respond to the picked value in real time.

---

## Slots & Bindings

| Slot | Purpose | DAX example |
|---|---|---|
| Parameter table | Generated sequence of values | `GENERATESERIES(0, 0.30, 0.01)` |
| `Value` measure | Exposes selected value | `Discount % Value = SELECTEDVALUE('Discount Parameter'[Discount %], 0.10)` |
| Consumer measure | Uses the value | `Scenario Net Revenue = [Total Revenue] * (1 - [Discount % Value])` |
| Slicer | Single-select, between, or buttons | Bound to `'Discount Parameter'[Discount %]` |

---

## Property Snippet (parameter table)

```dax
Discount Parameter =
GENERATESERIES(0, 0.30, 0.01)

Discount % Value =
SELECTEDVALUE('Discount Parameter'[Discount %], 0.10)
```

Slicer visual: `slicer`, single-select between, min = 0, max = 0.30, step = 0.01.

---

## Defaults

| Setting | Default | Why |
|---|---|---|
| Slider range | Realistic business bounds | 0–30 % discount, not 0–100 % |
| Step | Natural granularity | 1 % (not 0.001 %) |
| Default value | Current baseline | Scenario opens at "as-is" |
| Display format | Match the measure format | %, $, unit |

---

## Anti-patterns

❌ What-if parameter without a "reset to baseline" button — user can't recover.
❌ 6+ independent parameters on one page — cognitive overload; split into a tab or wizard.
❌ Parameter that silently multiplies an already-adjusted measure (double-counting).
❌ Using a what-if for a dimension filter (like "Region") — that's a slicer, not a parameter.

---

## Documentation requirement

Every what-if parameter page **must** show:
1. The baseline value (in text or via a reference line on the chart)
2. A "Reset" button that restores all parameters to baseline
3. A note clarifying the scenario is not saved / doesn't persist

---

## Pairs well with

- `what-if-parameter-page` layout
- `kpi-donut-row` or `kpi-banner` charts showing the scenario output
- `field-parameter-switch` — pair to switch which KPI reacts to the parameter
