# Recipe: Funnel / Conversion

- **id:** `funnel-conversion`
- **Visual type:** `funnel`
- **Typical size:** 480 × 360

---

## Composition

```
Stage 1 ████████████████████████████████████   10,000   (100%)
Stage 2 ██████████████████████████                7,200   (72%)
Stage 3 ████████████████                          3,900   (39%)
Stage 4 ████████                                  1,850   (18.5%)
Stage 5 ██                                          420   (4.2%)
                                                ▲ overall conversion 4.2%
```

---

## Slots

| Slot | Content | Binding example |
|---|---|---|
| Category | Ordered stage list | `Stage.StageName` (sorted by `Stage.StageOrder`) |
| Value | Count or value at stage | `[Leads in Stage]` or `[Pipeline Value]` |
| Conversion label | Stage-to-stage % | Computed — Power BI shows automatic conversion rate |

Stages must be **strictly ordered and monotonically non-increasing**. If a downstream stage
has MORE entries than an upstream one, your data model is wrong — fix before visualizing.

---

## Formatting (theme-aware)

- **Bar color:** `data0` (flat across stages) — do NOT rainbow one color per stage
- **Data labels:** show both absolute value and percentage-of-previous
- **Category sort:** by stage order column, ascending
- **Gap:** default (do NOT collapse to zero — readability suffers)

---

## Narrative frame

- **Executive:** headline card showing **overall conversion %** above the funnel
- **Analytical:** add a prior-period funnel side-by-side OR a small-multiples variant by segment
- **Operational:** highlight stage with largest absolute drop; threshold-color the drop bar in `bad`

---

## Do NOT

- Use funnel for non-sequential categories (use bar-comparison instead)
- Apply funnel when stage counts aren't monotonically non-increasing (broken funnel signal)
- Use more than **7 stages** — cognitive overload; split into two funnels
- Use 3D funnel — flat only
- Use funnel for a single point-in-time conversion rate (use card with delta)

---

## Data quality gotchas

- **Stage order:** never rely on alphabetical; use an explicit `StageOrder` integer column
- **Time alignment:** a lead in Stage 2 today may not have been in Stage 1 today — decide
  whether the funnel is cohort-based (entered at same time) or snapshot-based (state now).
  Document in Design Spec §5 notes.
- **De-duplication:** count distinct leads, not events, or the funnel inflates
- **Leakage:** leads that skip stages still must appear in prior stages — if they don't,
  the funnel will read higher conversion than reality

---

## Checklist

- [ ] Stages in strict order via explicit ordering column
- [ ] Values monotonically non-increasing (or flagged if not)
- [ ] Overall conversion shown separately (card above funnel)
- [ ] Labels show value + conversion % — both readable at canvas size
- [ ] Flat single-color bars (no rainbow)
- [ ] Alt text: "Funnel showing <N> stages from <first> to <last>, overall conversion <X>%"
