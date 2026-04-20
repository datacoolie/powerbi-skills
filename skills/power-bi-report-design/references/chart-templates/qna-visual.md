# Recipe: Q&A Visual

> **Preview:** [![qna-visual preview](../../assets/chart-previews/qna-visual.svg)](../../assets/chart-previews/qna-visual.svg)

- **id:** `qna-visual`
- **Visual type:** `qnaVisual`
- **Typical size:** 536 × 320

---

## Composition

```
┌───────────────────────────────────────────┐
│ Ask a question about your data:            │
│ ┌───────────────────────────────────────┐  │
│ │ > total revenue by region             │  │
│ └───────────────────────────────────────┘  │
│                                             │
│ Suggested:                                  │
│   • top customers this quarter              │
│   • revenue vs plan by segment              │
│   • churn rate by month                     │
└───────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Suggested questions | 3–5 starter prompts | Authored in Design Spec §9 |
| Synonyms | Alternate field names for Q&A engine | Defined in semantic model's linguistic schema |

---

## Formatting (theme-aware)

- **Question box:** `background` fill, 1px `secondary` border, 12pt
- **Suggested prompts:** `data0` link-style, 11pt
- **Result visual:** auto-rendered by Q&A engine (styled by active theme)
- **Placeholder text:** `foreground` 40% muted

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Landing-page hero with 3 curated prompts |
| Analytical | Larger visual, 5 prompts, synonyms extensively tuned |
| Operational | Not recommended — interactive exploration ≠ monitor use case |

---

## Do-NOT list

- ❌ Publishing without curated suggested questions (blank Q&A is intimidating)
- ❌ Skipping linguistic schema tuning (accuracy stays poor)
- ❌ Allowing questions that expose sensitive fields (Q&A respects RLS but not
  column-level hiding — verify)
- ❌ Relying on Q&A as the sole answer for a critical decision without
  validation against an authored visual

---

## Data quality gotchas

- Q&A depends on well-named tables and columns — `Tbl1`, `Col_X` cause failures
- Synonyms must be curated; without them, "sales" won't match `Revenue`
- Measure descriptions appear in Q&A results — keep them business-friendly
- Date hierarchy must be active for "by month / quarter / year" to work

---

## Checklist

- [ ] 3–5 suggested prompts curated
- [ ] Linguistic schema synonyms reviewed
- [ ] Key measures have business-friendly descriptions
- [ ] Sensitive fields hidden or RLS-scoped
- [ ] Tested against 10 realistic user prompts before publish
- [ ] Fallback visual provided (Q&A is supplementary)
