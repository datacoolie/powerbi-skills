# Recipe: Smart Narrative

> **Preview:** [![smart-narrative preview](../../assets/chart-previews/smart-narrative.svg)](../../assets/chart-previews/smart-narrative.svg)

- **id:** `smart-narrative`
- **Visual type:** `textbox` with narrative visual OR `narrativeVisual`
- **Typical size:** 536 × 240

---

## Composition

```
┌────────────────────────────────────────────┐
│ Revenue Summary                             │
│                                              │
│ Total Revenue was $4.2M, up 12.4% from      │
│ prior year. Growth was driven primarily      │
│ by West region (+24%) and Enterprise         │
│ segment (+18%). Margin improved to 38.4%.   │
│                                              │
│ Last updated: 15 minutes ago                │
└────────────────────────────────────────────┘
```

---

## Slots

| Slot | Purpose | Binding example |
|---|---|---|
| Summary scope | Visuals / measures to summarize | Entire page OR specific visuals |
| Dynamic values | Inline measure tokens | `{Total Revenue}`, `{YoY %}` |

---

## Formatting (theme-aware)

- **Background:** `background2` (subtle contrast from page)
- **Body text:** `foreground` 12pt, line-height 1.5
- **Headline:** `foreground` 14pt Semibold
- **Dynamic values:** `data0` with 1px underline
- **Timestamp:** `foreground` 9pt, muted 50%

---

## Narrative frame by style

| Style | Configuration |
|---|---|
| Executive | Hero placement, 3–4 sentences, manually-authored template + dynamic values |
| Analytical | Auto-generated summary, editable, tied to specific visuals |
| Operational | Short status sentences only, tied to threshold measures |

---

## Do-NOT list

- ❌ Relying solely on auto-generated text without human review (can surface
  misleading claims)
- ❌ Embedding > 6 dynamic values (text becomes cluttered)
- ❌ Writing narrative longer than 5 sentences (readers skim)
- ❌ Missing data-refresh timestamp (readers can't trust the claim)
- ❌ Using as the only visual on a page (needs chart to anchor the claim)

---

## Data quality gotchas

- Auto-narrative uses the current filter state — document which filters are expected
- Dynamic value tokens bind to measures, not columns; measure changes break tokens silently
- Auto-generated claims may hallucinate on sparse / noisy data
- Timestamps reflect dataset refresh, not narrative computation

---

## Checklist

- [ ] Narrative reviewed by domain owner
- [ ] All dynamic value tokens resolve correctly under default filters
- [ ] Length ≤ 5 sentences
- [ ] Data-refresh timestamp visible
- [ ] Paired with at least one chart that substantiates the claim
- [ ] Auto vs manual authoring decision documented in Design Spec
