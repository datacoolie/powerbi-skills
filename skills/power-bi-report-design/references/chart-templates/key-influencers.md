# Recipe: Key Influencers (AI)

> **Preview:** [![key-influencers preview](../../assets/chart-previews/key-influencers.svg)](../../assets/chart-previews/key-influencers.svg)

- **id:** `key-influencers`
- **Visual type:** `keyDriversVisual`
- **Typical size:** 824 × 480

---

## Composition

```
┌────────────────────────────────────────────────┐
│ What influences  [Churn]  to be  [High] ?       │
│                                                  │
│ ┌─── Key Influencers ───┐  ┌── Top Segments ──┐  │
│ │ Low tenure  ▃▅▇  1.8x │  │ Segment A  42%   │  │
│ │ No upgrade  ▃▅    1.4x│  │ Segment B  31%   │  │
│ │ High cost   ▃     1.2x│  │ Segment C  18%   │  │
│ └───────────────────────┘  └────────────────────┘ │
└────────────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Analyze | Target measure or attribute | `FactChurn[Churned]` (0/1) |
| Explain by | Candidate driver fields | `[Tenure]`, `[Plan Type]`, `[Cost]`, `[Support Calls]` |
| Expand by | Optional grouping dimension | `DimRegion[RegionName]` |

---

## Formatting (theme-aware)

- **Bars:** `data0` for influencer strength
- **Highlight color:** `good` (positive influence) / `bad` (negative) when polar
- **Text:** `foreground` 11pt; target value selector prominent

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Rarely used — prefer single insight card from the visual's output |
| Analytical | Default — full visual with segments pane enabled |
| Operational | Not recommended — visual requires interactive exploration |

---

## Do-NOT list

- ❌ Using with < 100 rows in the fact table (model too thin, conclusions unreliable)
- ❌ Analyzing continuous measures without binning guidance (visual treats as categorical)
- ❌ Mixing categorical and continuous explainers without documenting
- ❌ Leaving "Explain by" fields highly correlated (multicollinearity distorts strength)
- ❌ Exposing personally-identifiable fields as explainers

---

## Data quality gotchas

- Visual computes on the filtered dataset only — report-page filters change
  influencer rankings; document expected filter state
- Binary targets (0/1) work best; for continuous targets, bin first
- Nulls in explainer columns silently exclude rows from the analysis
- Segments pane requires ≥ 20 observations per segment

---

## Checklist

- [ ] Fact table has ≥ 100 rows at the analysis grain
- [ ] Target measure/attribute is clearly defined
- [ ] Explainer fields vetted for correlation / privacy
- [ ] Default page-filter state documented in Design Spec
- [ ] Segments pane enabled / disabled decision recorded
- [ ] AI-generated narrative validated by domain expert before publish
