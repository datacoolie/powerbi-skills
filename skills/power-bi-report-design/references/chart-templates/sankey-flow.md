# Recipe: Sankey Flow (Stage-to-Stage Attribution)

- **id:** `sankey-flow`
- **Visual type:** Custom visual (`Sankey` by Microsoft / `xViz Sankey`)
- **Typical size:** 720 × 400 (wide — flows need horizontal room)

---

## Composition

```
  Source           Stage            Outcome
  ─────            ─────            ───────
  Paid  ███▌╲────────╲
  Organic █▌  ╲─── Lead ▓▓▓▌───── Won  ████
  Refer  █▌  ╱            ╲─── Lost ██▌
  Direct ██▌╱───── MQL ▓▓▌ ───── Open ▌
```

Ribbons whose **thickness** encodes volume flowing between stages. Reader
follows where each source lands and where each outcome came from — two
questions, one visual.

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| From (source node) | Left side of a flow | `DimChannel[Channel]` |
| To (target node) | Right side of a flow | `DimStage[Stage]` |
| Weight | Flow magnitude | `[Opportunity Count]` |
| Order | Optional node ordering key | `DimStage[Stage Order]` |

Many custom Sankey visuals accept multi-stage data — bind Source/Target in
pairs so the visual can chain stages (Channel → Stage → Outcome).

---

## Formatting (theme-aware)

- Node bars: `neutral`, same hue family for all nodes; column-ordered
- Ribbons: `accent` 35-45% opacity; increase opacity for selected path
- Labels: left-align source labels, right-align destination labels
- Tooltips must report both absolute flow and % of source and % of target
- Cap ribbons at ~15 per stage pair — above that, bucket into "Other"

---

## Do-NOT list

- ❌ Use as a primary comparison of magnitudes (bars do that better)
- ❌ Allow loops or back-flows (Sankey is strictly DAG left → right)
- ❌ Colour every ribbon differently — kills the aggregate pattern
- ❌ More than 4 stages (column soup)

---

## Checklist

- [ ] Stages ordered left → right with a clear business meaning
- [ ] "Other" bucket for long-tail ribbons
- [ ] Tooltip includes both source % and destination %
- [ ] No loops / back-flows
