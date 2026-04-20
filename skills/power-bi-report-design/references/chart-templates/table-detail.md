# Recipe: Detail Table

> **Preview:** [![table-detail preview](../../assets/chart-previews/table-detail.svg)](../../assets/chart-previews/table-detail.svg)

- **id:** `table-detail`
- **Visual type:** `tableEx`
- **Typical size:** 824 × 400 (full-width on analytical layouts)

---

## Composition

```
┌───────────────────────────────────────────────────┐
│ Customer      Region    Revenue    Margin   Trend │
│ ─────────────────────────────────────────────────  │
│ Acme Corp     West      $1.2M       42%     ▂▃▅   │
│ Globex        East      $980K       38%     ▅▆▇   │
│ Initech       North     $780K       51%     ▇▆▅   │
│ Umbrella      South     $640K       29%     ▃▂▃   │
│ ────────────── Totals:  $3.6M      40%              │
└───────────────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Columns | Entity dimensions + measures | `DimCustomer[Name]`, `DimRegion[RegionName]`, `[Revenue]`, `[Margin %]` |
| Totals row | Sum / weighted average | Default ON for additive measures |

---

## Formatting (theme-aware)

- **Row separator:** 0.5px `secondary`, no vertical grid lines
- **Header:** `foreground` 11pt Semibold, `background2` fill
- **Body text:** `foreground` 10pt Regular
- **Conditional formatting:**
  - Data bars on the primary numeric column using `data0`
  - Background color scale on % columns using `minimum`/`center`/`maximum`
  - Icon set for status column using `good`/`neutral`/`bad`

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Avoid — table density rarely suits executive pages |
| Analytical | Default — up to 10 columns, conditional formatting dense |
| Operational | Status column leading, traffic-light icons, large 12pt body |

---

## Do-NOT list

- ❌ > 10 columns (becomes a spreadsheet; add drillthrough page)
- ❌ Heavy gridlines (visual noise)
- ❌ Centered numeric columns (always right-align numbers)
- ❌ Missing totals row for additive measures
- ❌ Field names as column headers (rename to business labels)
- ❌ Exposing technical keys / surrogate IDs to end users

---

## Data quality gotchas

- Sort order must be explicit (click sort + save) or the table reverts to
  first-column alpha on refresh
- Percent columns must be measures, not computed columns (filter-context sensitivity)
- Totals row for weighted averages needs a dedicated measure (not the column's
  default SUM / AVG)

---

## Checklist

- [ ] ≤ 10 columns
- [ ] Numbers right-aligned, text left-aligned
- [ ] All column headers renamed to business terms
- [ ] Totals row present for additive measures
- [ ] Conditional formatting uses semantic tokens
- [ ] Default sort explicit (by primary measure desc)
- [ ] No technical keys exposed
