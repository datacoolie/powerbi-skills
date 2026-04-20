# Recipe: XY Heatmap

> **Preview:** [![xy-heatmap preview](../../assets/chart-previews/xy-heatmap.svg)](../../assets/chart-previews/xy-heatmap.svg)

- **id:** `xy-heatmap`
- **Visual type:** `matrix` with conditional background color
- **Typical size:** 824 × 480

---

## Composition

```
┌────────────────────────────────────────────┐
│         Mon  Tue  Wed  Thu  Fri  Sat  Sun    │
│  00-06  ░    ░    ░    ░    ░    ▒    ▒      │
│  06-12  ▒    ▓    ▓    ▓    ▓    ▓    ▒      │
│  12-18  ▓    █    █    █    █    ▓    ▒      │
│  18-24  ▓    ▓    ▓    ▓    █    █    ▓      │
│  ░ low  ▒ med  ▓ high  █ peak                  │
└────────────────────────────────────────────┘
```

Cross-tabulation of two discrete dimensions with color intensity encoding a
measure. Good for pattern density, weak for precise deltas.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Rows | First discrete dimension | `DimTime[HourBand]` |
| Columns | Second discrete dimension | `DimDate[DayOfWeek]` |
| Values | Heatmap measure | `[Transaction Count]` |

---

## Formatting (theme-aware)

- **Color scale:** monochrome — `minimum` (light) → `maximum` (dark)
- **Cell labels:** OFF unless ≤ 30 cells total (readability over density)
- **Borders:** 0.5px `background2` between cells
- **Row/column headers:** `foreground` 10pt Semibold
- **Null cells:** shown with striped pattern or `background2` fill

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Top-N rows only, annotated peak cells |
| Analytical | Full grid, cell labels on, tooltip verbose |
| Operational | Threshold palette (green/amber/red) for status heatmap |

---

## Do-NOT list

- ❌ Rainbow or jet color scale (perceptually non-linear)
- ❌ > 15 rows × 15 columns visible (density cap)
- ❌ Cell labels AND color when cell count > 50 (duplicate info)
- ❌ Using a diverging palette for an unsigned measure
- ❌ Missing null-cell treatment (readers confuse "no data" with "zero")

---

## Data quality gotchas

- Nulls vs zeros must be distinguished — use ISBLANK() in the measure
- Color scale auto-ranges on filter changes; lock min/max for comparability
- Ordering of row/column headers must be explicit (not alpha when categorical is ordinal)

---

## Checklist

- [ ] Monochrome palette (not rainbow)
- [ ] Null cells styled distinctly from zeros
- [ ] Row / column ordering explicit (time-of-day, day-of-week, etc.)
- [ ] Color scale locked or documented as auto-ranging
- [ ] Cell density ≤ 225 cells
