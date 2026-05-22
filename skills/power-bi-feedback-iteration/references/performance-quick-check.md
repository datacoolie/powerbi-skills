# Performance Quick Check

Short triage checklist for performance feedback. **For deep diagnosis, route to
`power-bi-performance-troubleshooting` skill.**

## Triage Questions (ask before routing)

```
□ Which experience is slow? (page load / slicer / cross-filter / drillthrough / refresh)
□ How slow? (seconds for interaction, minutes for refresh)
□ When? (always / specific pages / specific users / peak hours only)
□ Environment? (Desktop / Service — which SKU / Mobile / Embedded)
□ How many users affected? (single user = RLS/data issue; all users = model/capacity)
```

## Escalation Criteria

Route to `power-bi-performance-troubleshooting` when:

- Any interaction > 3s or page load > 10s
- A quick fix (reduce visuals, enable Apply button) didn't resolve it
- Multiple symptoms appear together (systemic issue)
- Capacity-level saturation suspected (peak hours, multiple reports)
- Refresh exceeds SLA

## What NOT to do here

- ❌ Don't attempt DAX optimization from this skill — route to perf skill
- ❌ Don't "fix" by just removing visuals without understanding why it's slow
- ❌ Don't skip measurement — always capture baseline before changing anything
- ❌ Don't optimize prematurely — measure first with Performance Analyzer
- ✅ Do capture before/after metrics for every perf fix
