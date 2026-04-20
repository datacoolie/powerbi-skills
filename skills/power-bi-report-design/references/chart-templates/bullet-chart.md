# Recipe: Bullet Chart (IBCS Actual vs Target)

> **Preview:** [![bullet-chart preview](../../assets/chart-previews/bullet-chart.svg)](../../assets/chart-previews/bullet-chart.svg)

- **id:** `bullet-chart`
- **Visual type:** Custom visual (`BulletChart` / IBCS) OR composed `clusteredBar`
  with reference lines
- **Typical size:** 536 × 320 (stack 4-6 bullets vertically)

---

## Composition

```
Revenue    │█████████████████████▌        │●
Margin     │████████████                  │●
NPS        │██████████████████████████████│●
Quality    │███████                       │●
           └──────── bad ── ok ── good ───┘
                                   ▲
                                target (line)
```

Each row: a neutral **range band** (bad → ok → good), an **actual** bar, and a
**target** tick. Reviewer instantly sees (a) is the metric in the green range
and (b) did it meet its target — two independent questions in one glance.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Category | KPI name | `DimKPI[KPI]` |
| Actual | Current measure | `[Actual]` |
| Target | Target measure | `[Target]` |
| Thresholds | Bad / Ok / Good bounds | `[Bad Threshold]`, `[Ok Threshold]`, `[Max]` |

---

## Formatting (theme-aware)

- **Range band:** three shades of `neutral` (lightest for "good" max, darker
  for "bad" floor) — all monochrome; colour is reserved for deviation
- **Actual bar:** `foreground` thin bar (~40% of row height)
- **Target tick:** `accent` solid vertical line, full row height
- **Labels:** right-aligned absolute value + target delta

---

## Do-NOT list

- ❌ More than 6 bullets in one visual (use several grouped visuals)
- ❌ Colour the range bands with traffic-light colours — deviations are
  carried by the target tick, not the background
- ❌ Use when there's no target (use `bar-comparison` instead)

---

## Checklist

- [ ] Each row has: actual + target + 2-3 threshold bounds
- [ ] Range bands are monochrome shades (no red/amber/green backgrounds)
- [ ] Target tick is a crisp full-height line (not a diamond marker)
- [ ] Sort rows by strategic order, not by value
