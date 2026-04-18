# Feedback Classification Taxonomy

Classify every piece of user feedback using this taxonomy before routing. The agent consults the routing table in `agents/power-bi-developer.agent.md` to map each category to the correct downstream skill.

## The 12 Categories

| # | Category | Severity | Typical examples |
|---|---|---|---|
| 1 | **Data accuracy** | Critical | "Revenue number is wrong", "Missing orders from last week", "Region filter returns wrong data" |
| 2 | **Security / access** | Critical | "User A sees data they shouldn't", "RLS not filtering correctly", "Workspace permission error" |
| 3 | **Missing insight** | High | "We need to see margin by channel", "How do we track churn here?", "Can't answer the board's question" |
| 4 | **New measure needed** | High | "Add YoY growth", "We need a 3-month rolling average", "Conversion rate not defined" |
| 5 | **Performance** | High | "Page takes 30s to load", "Slicer lags", "Refresh fails / times out" |
| 6 | **Chart type / layout** | Medium | "Pie chart with 12 slices is unreadable", "Should be a line not a bar", "Swap these two visuals" |
| 7 | **New requirement** | Medium | "Add a supplier scorecard page", "Need drillthrough by product", "Support mobile" |
| 8 | **Visual formatting** | Medium | "Font too small", "Axis labels overlap", "Data labels missing", "Title should be bold" |
| 9 | **Filter / slicer** | Medium | "Slicer should sync across pages", "Need a date range instead of single date" |
| 10 | **Navigation** | Low | "Back button missing", "Buttons should be on top not side", "Bookmark jumps wrong" |
| 11 | **Cosmetic / theme** | Low | "Use brand colors", "Too much white space", "Make it look more modern" |
| 12 | **Label / copy** | Low | "Rename 'Sum of Sales' to 'Total Revenue'", "Tooltip wording unclear" |

## How to classify

For each feedback item:

1. **Read the user's exact words** — don't summarize yet
2. **Identify the primary symptom**:
   - Does a number look wrong? → Data accuracy (1)
   - Does a user see data they shouldn't? → Security (2)
   - Is something completely absent from the report? → Missing insight (3) or New requirement (7)
   - Is a calculation missing or wrong? → New measure (4)
   - Is it slow? → Performance (5)
   - Is the visual the wrong shape for the question? → Chart type (6)
   - Is the look / feel wrong? → Visual formatting (8) or Cosmetic (11)
3. **Assign severity** using the table above — don't let the user's emotional intensity override technical severity
4. **One category per item** — if feedback mixes concerns, split it into separate items first

## Severity → response time guidance

| Severity | Fix target | Escalation |
|---|---|---|
| Critical | Same day | Notify report owner + data steward immediately |
| High | Within current sprint | Confirm priority with report owner |
| Medium | Next sprint | Batch with other medium items |
| Low | Next release window | Queue for cosmetic sweep |

## Anti-patterns

- ❌ Don't classify feedback as "everything is broken" — force decomposition into specific items
- ❌ Don't let "critical" severity be assigned by user pressure — use the taxonomy
- ❌ Don't conflate "missing insight" (scope gap) with "new measure" (formula gap) — the first requires Phase 1 revisit
- ❌ Don't skip classification because the fix seems obvious — classification drives routing
