# Recipe: Calendar Heatmap (Daily Pattern)

- **id:** `heatmap-calendar`
- **Visual type:** `matrix` with conditional background colour OR custom
  visual (Calendar by MAQ / OKVIZ)
- **Typical size:** 800 × 240 (full quarter) or 560 × 180 (single month)

---

## Composition

```
       W1  W2  W3  W4  W5  W6  W7  W8  ...
  Mon  ░░ ░░ ▒▒ ██ ██ ██ ▓▓ ▒▒
  Tue  ▒▒ ▒▒ ██ ██ ▓▓ ██ ██ ██
  Wed  ░░ ▒▒ ██ ▓▓ ██ ██ ██ ▒▒
  Thu  ▒▒ ▒▒ ██ ▓▓ ██ ██ ██ ██
  Fri  ░░ ░░ ▒▒ ▓▓ ██ ██ ██ ▓▓
  Sat  ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░
  Sun  ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░
```

Tile per day, one colour channel (sequential). Patterns like weekend-dips,
month-end-spikes, or promotion weeks pop out instantly.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Rows | Day-of-week (Mon → Sun) | `DimDate[DayOfWeek]` |
| Columns | Week / Date | `DimDate[WeekStart]` |
| Values | Metric | `[Transactions]` |
| Cond. formatting | Background by measure | `FORMAT_STRING_DEFINITION` |

---

## Formatting (theme-aware)

- **Scale:** sequential, from `background` (low) to `accent` (high). Monochrome.
  Avoid diverging scales unless the metric is signed (e.g. variance %).
- **Grid:** 1-2 px transparent gaps between cells — reads as separate days
- **Hover tooltip:** date, absolute value, % vs period-average

---

## Do-NOT list

- ❌ Use rainbow / jet colour scale (perceptually nonlinear, destroys the story)
- ❌ Map negative and positive on the same sequential scale — switch to
  diverging if values are signed
- ❌ Show > 6 months on one row (cells become unreadable) — use small multiples
  by month

---

## Checklist

- [ ] Sequential (or diverging) colour scale — no rainbow
- [ ] Rows sorted Mon → Sun, not alphabetical
- [ ] Legend shows min / median / max values
- [ ] Null days rendered as neutral grey (not missing / white)
