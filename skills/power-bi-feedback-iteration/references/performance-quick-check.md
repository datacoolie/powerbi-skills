# Performance Quick Check

Short diagnostic checklist for performance feedback. **For deep diagnosis and optimization, use the dedicated `power-bi-performance-troubleshooting` skill** — this file is only a first-pass triage.

## Triage questions

Before routing to the performance skill, establish scope:

```
□ Which specific experience is slow?
  □ Initial page load
  □ Slicer interaction
  □ Cross-filter / cross-highlight
  □ Drillthrough transition
  □ Dataset refresh

□ How slow is it?
  □ Initial load time: _____ seconds (target < 10)
  □ Interaction time: _____ seconds (target < 3)
  □ Refresh time: _____ minutes (target within SLA)

□ When does it happen?
  □ Always
  □ Only on specific pages / visuals
  □ Only for specific users (scale / RLS issue)
  □ Only during peak hours (concurrency)

□ What's the environment?
  □ Power BI Desktop (local)
  □ Fabric / Power BI Service capacity — which SKU?
  □ Mobile app
  □ Embedded
```

## Quick causes & quick fixes

| Symptom | Likely cause | Quick check | Fix direction |
|---|---|---|---|
| Slow initial page load | Too many visuals (>8) | Count visuals on the page | Reduce to 6-8; move detail to drillthrough |
| Slow slicer | High-cardinality field | Count distinct values in slicer field | Add search box; limit displayed items; or convert to hierarchical slicer |
| Slow single visual | Expensive DAX | Run Performance Analyzer; inspect DAX query time | Route to perf skill — likely needs DAX rewrite |
| Slow refresh (Import) | Large table or many columns | Check model size; count columns in biggest table | Remove unused columns; add incremental refresh |
| Slow cross-filter | Bi-directional relationships | Inspect relationships.tmdl for bi-di | Change to single-direction where possible |
| Slow DirectQuery | Source database slow | Run source query directly | Add source indexes; aggregations; or switch to Import for affected tables |
| Slow at peak hours | Capacity saturation | Check Fabric capacity metrics | Scale capacity; add aggregations; schedule intensive refreshes off-peak |
| Slow on mobile only | Mobile layout rendering | Check mobile.json for visual count | Reduce mobile visuals; simplify layout |

## Performance budget targets

| Metric | Good | Acceptable | Bad |
|---|---|---|---|
| Page load | < 5s | 5-10s | > 10s |
| Visual interaction | < 1s | 1-3s | > 3s |
| Slicer response | < 500ms | 500ms-1s | > 1s |
| Model size (Import) | < 100 MB | 100-500 MB | > 500 MB |
| Refresh time | Within SLA | Near SLA | Exceeds SLA |
| Visuals per page | ≤ 6 | 7-8 | > 8 |
| Slicers per page | ≤ 4 | 5-6 | > 6 |

## Escalation to the performance skill

Route the feedback item to `power-bi-performance-troubleshooting` when:

- Any target is in the "Bad" column
- A fix attempt from the "Quick fixes" table didn't resolve the issue
- Multiple symptoms appear together (likely a systemic issue)
- Source-side (database, gateway, capacity) seems involved

The performance skill provides:
- Performance Analyzer workflow
- DAX query optimization patterns (variables, CALCULATE anti-patterns, iterator avoidance)
- Model optimization (aggregations, composite models, partitioning)
- Capacity planning guidance
- Gateway / data source optimization

## Anti-patterns

- ❌ Don't "fix" by just removing visuals without understanding why it's slow
- ❌ Don't add more bi-directional relationships "to make it work" — they compound perf issues
- ❌ Don't optimize prematurely — measure first with Performance Analyzer
- ❌ Don't ignore refresh perf — it degrades quietly until a failed refresh
- ✅ Do capture before/after metrics for every perf fix
