# Recipe: Slope Chart (Two-Point Rank Change)

> **Preview:** [![slope-chart preview](../../assets/chart-previews/slope-chart.svg)](../../assets/chart-previews/slope-chart.svg)

- **id:** `slope-chart`
- **Visual type:** `lineChart` with two category positions OR custom visual
- **Typical size:** 480 × 360

---

## Composition

```
       2024          2025
  A  ●──────────●   (flat)
  B  ●─────╱────●   (up — highlighted)
  C  ●╲────────●    (down)
  D  ●──────────●
```

Two vertical axes (period 1, period 2), one dot per category on each side,
slope line connecting them. The line's angle encodes change — perfect for
talking-point narration in Executive decks.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category | Entity | `DimRegion[Region]` |
| Period 1 | Earlier snapshot value | `[Revenue 2024]` |
| Period 2 | Later snapshot value | `[Revenue 2025]` |

---

## Formatting (theme-aware)

- **Lines:** `neutral` at ~35% opacity for context lines, `accent` at 100% for
  the 1-2 lines the narrative is about
- **End-point labels:** category name + value on both sides; only show for
  highlighted lines if space is tight
- **Axis:** no gridlines, just two thin vertical ticks at the two time points

---

## Do-NOT list

- ❌ > 10 categories (lines overlap and tangle)
- ❌ Use for > 2 time points (use `trend-line` or `ribbon-chart`)
- ❌ Highlight everything (defeats the purpose) — 1-2 lines max in accent
- ❌ Omit the value labels — reader shouldn't eyeball the slope

---

## Narrative frame by style

| Style | Treatment |
|---|---|
| Executive | 1 highlighted line; title carries the finding ("North overtook Central"). |
| Analytical | All lines shown; highlight the 2-3 biggest movers; quadrant annotation. |
| Operational | Rarely a fit — use `bar-comparison` with period chips instead. |

---

## Checklist

- [ ] Exactly 2 time points
- [ ] ≤ 10 categories
- [ ] 1-2 lines in accent, the rest muted
- [ ] End-point labels on the highlighted lines
