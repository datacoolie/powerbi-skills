# Recipe: Ribbon Chart (Rank-over-Time)

- **id:** `ribbon-chart`
- **Visual type:** `ribbonChart` (Power BI built-in)
- **Typical size:** 640 × 400

---

## Composition

```
       Q1      Q2      Q3      Q4      Q5
  #1  ───╮   ╭───╮        ╭───────────
         ╰───╯   ╰───╮ ╭──╯
  #2  ───╮   ╭───────╯─╯────────╮
         ╰───╯                  ╰──────
  #3  ─────────────╮ ╭──────────────
                   ╰─╯
```

Ribbons re-order between periods so you can see **rank changes** and
**who overtook whom**, which a stacked-column hides.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Axis | Time / ordered period | `DimDate[QuarterName]` |
| Legend | Category whose rank is tracked | `DimProduct[Product]` |
| Values | Single additive measure | `[Revenue]` |

---

## Formatting (theme-aware)

- **Ribbon palette:** categorical `data0..data4`; top rank in period 1 gets `data0`
- **Ribbon transitions:** keep the default curved transitions (rank story)
- **Labels:** category label on first + last period only (reduce clutter)
- **Hide** categories that never enter the top 5 (TopN visual filter)

---

## Do-NOT list

- ❌ > 6 categories in legend (becomes visual noise)
- ❌ Non-additive measures (ribbons imply summable share)
- ❌ Use it for share (%) story — use `stacked-bar-100` instead
- ❌ Use when rank doesn't change (flat ribbons = wasted visual) — use `trend-line`

---

## Narrative frame by style

| Style | Treatment |
|---|---|
| Executive | 3-4 top categories only; highlight the winner ribbon in accent. |
| Analytical | Up to 6 categories; tooltip shows rank + absolute value + delta. |
| Operational | Rarely appropriate (operational is usually current-state only). |

---

## Checklist

- [ ] TopN filter ≤ 6 categories
- [ ] Axis is *ordered* (time or rank-worthy period)
- [ ] At least two categories swap rank somewhere — or swap to `trend-line`
- [ ] Title frames the story ("how Product X overtook Y")
