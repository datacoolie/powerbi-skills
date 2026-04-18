# Recipe: Decomposition Tree

- **id:** `decomposition-tree`
- **Visual type:** `decompositionTreeVisual`
- **Typical size:** full-page width × 560+ (exploratory)

---

## Composition

```
 ┌──────────┐     ┌──── Region A ── $2.4M ▼ ───┐
 │ Revenue  │────▶│ ── Region B ── $1.9M       ├── [ + add level ]
 │  $5.2M   │     │ ── Region C ── $0.9M       │
 └──────────┘     └────────────────────────────┘
                                ▲
                      click to expand further
                      (Category → Channel → Product)
```

Interactive root-cause tree. User picks a root measure, then drills through dimensions,
optionally using **AI splits** (Power BI suggests the most-impactful dimension at each level).

---

## Slots

| Slot | Content | Binding example |
|---|---|---|
| Analyze | Root measure | `[Revenue]` (single measure only) |
| Explain by | Dimensions available for drill | Multiple: `Region`, `Channel`, `Category`, `Product`, `Customer Segment` |

At runtime the user picks any order — design-time only defines the list of candidates.

---

## Formatting (theme-aware)

- **Bar color:** single `data0` for all bars at all levels (variation comes from length)
- **Absolute / relative:** set to **Absolute** for business comparison; relative for contribution-focused analysis
- **Sort:** DESC by value (largest contributor first)
- **AI split icon:** leave enabled (light bulb) unless the model has RLS that breaks AI splits
- **Level cap:** Power BI allows up to ~50; practical limit is **5 levels** before cognitive overload

---

## Narrative frame

- **Executive:** rarely used — executives want the finding, not the exploration. If used, preset 2 levels and explain in title.
- **Analytical:** primary use case — pair with a trend-line showing the selected path over time
- **Operational:** avoid — decomposition trees invite exploration, ops boards should be read-only

---

## Do NOT

- Include **more than 8 "Explain by" dimensions** — choice paralysis; pick the business-relevant 4-6
- Use decomposition tree for **additive-only metrics** when some dims aren't additive (e.g., distinct counts) — you'll get misleading totals
- Expose a root measure with **RLS / OLS** the user can't fully see — branches will render zero silently
- Use on small canvases — needs breathing room for expanded branches

---

## Data quality gotchas

- **Additivity:** root measure must be additive across all listed dims. `DISTINCTCOUNT` breaks decomposition — use `SUM`-based or pre-aggregated measures
- **Null dimension members:** render as "(Blank)" — make sure blanks are meaningful or filtered out
- **Hierarchy fields:** don't add both parent and child (Region + Subregion) — pick the grain you want users to drill to
- **AI splits + RLS:** AI splits may be disabled for users under row-level security; test both personas

---

## Checklist

- [ ] Single additive root measure
- [ ] 4-6 "Explain by" dimensions (not 15)
- [ ] Sort by value DESC
- [ ] AI splits tested with each security role
- [ ] Title explains the starting measure (e.g., "Drivers of Revenue")
- [ ] Paired with a supporting visual on the same page (trend or ranking)
- [ ] Alt text: "Interactive decomposition tree analyzing <measure> by <N> dimensions"
