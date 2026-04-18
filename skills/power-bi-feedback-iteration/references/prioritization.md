# Prioritization Matrix

Once feedback is classified, prioritize each item using the impact × effort matrix.

## The 2×2 Matrix

```
                   │ Low Effort (< 1 hour)   │ High Effort (> 1 hour)    │
───────────────────┼─────────────────────────┼───────────────────────────┤
  High Business    │ ★★★★★ DO FIRST        │ ★★★★ PLAN & EXECUTE      │
  Impact           │ (quick + valuable)      │ (batch into sprint)       │
───────────────────┼─────────────────────────┼───────────────────────────┤
  Low Business     │ ★★★ QUICK WIN          │ ★★ DEFER / BACKLOG       │
  Impact           │ (batch when polishing)  │ (challenge whether to do) │
```

## How to score

### Business Impact
| Score | Criteria |
|---|---|
| **High** | Blocks a decision, affects > 5 users, data accuracy issue, security issue, executive-visible |
| **Low** | Cosmetic, single-user preference, edge case, nice-to-have |

### Effort
| Score | Criteria |
|---|---|
| **Low (< 1 hour)** | Label change, visual formatting tweak, color swap, new slicer, existing-pattern measure |
| **High (> 1 hour)** | New page, schema change, new calculation group, performance investigation, RLS redesign |

## Quadrant actions

### ★★★★★ Do First
Same sprint, highest focus. Knock out in the order: data accuracy → security → measure correctness → visual correctness.

### ★★★★ Plan & Execute
Schedule for the current or next sprint. Break into subtasks if > 4 hours. Pair with related items (e.g., multiple new measures in one DAX pass).

### ★★★ Quick Win
Batch together and address at the end of a sprint (polish sweep). Good candidates for a junior developer or AI agent pass.

### ★★ Defer / Backlog
Question whether the item should be done at all. If yes, add to backlog with a review date. Don't block current work.

## Cross-quadrant rules

- **Never skip a Critical severity item** (from classification.md) regardless of quadrant — Critical implicitly becomes "Do First"
- **Bundle related Low-effort items** — doing 5 cosmetic changes at once costs less than 5 individual context switches
- **Reject scope creep disguised as feedback** — if feedback is actually a new requirement, route through Phase 1 (not directly to implementation)

## Sprint planning heuristic

Budget per sprint (1 week):
- 1-2 Do First items (if any) → guaranteed inclusion
- 2-3 Plan & Execute items → main sprint work
- 5-8 Quick Wins → fill remaining capacity
- 0 Defer items → only promote if a sprint has unexpected slack
