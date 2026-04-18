# Post-Change Validation Checklist

Run this checklist after implementing any change before marking the feedback item resolved.

## Core validation (every change)

```
Functional
□ The original issue is resolved (verify with reporter's reproduction steps)
□ No regression in existing functionality
□ Data values match expected (test against known-good values)
□ All related visuals still render without error

Cross-filtering
□ Slicers filter the changed visual correctly
□ Cross-highlighting between visuals still works
□ Drillthrough still passes correct filter context
□ Bookmarks still apply the intended filter state

Structure
□ PBIP file integrity (all cross-references valid)
□ Schema validation passes (scripts/validate_report.py)
□ No orphaned references (deleted measure not still referenced by a visual)
□ Page order and navigation intact

Performance
□ Page load < 10 seconds (target)
□ Visual interaction response < 3 seconds
□ Refresh time not degraded (compare before/after)
□ No new DirectQuery timeouts
```

## Scope-specific validation

### Model changes
```
□ Star schema checklist still passes (no circular relationships, no M:M without bridge)
□ Date table still marked as date table
□ All existing measures still compile (run a test DAX query per changed table)
□ RLS rules still filter correctly for each test role
□ Storage mode compatibility verified (no DirectQuery-incompatible DAX introduced)
```

### DAX changes
```
□ Measure evaluates to expected value for known test cases
□ Measure evaluates correctly when filtered by each relevant dimension
□ Time intelligence works across year boundaries (fiscal + calendar)
□ Edge cases: no data, single row, null, division by zero
□ Format string applied (currency, %, decimals)
□ Description set
□ Display folder correct
```

### Report changes
```
□ Visual renders in Power BI Desktop (actually open the file)
□ Visual renders correctly at different window sizes
□ Mobile layout still valid (if mobile is supported)
□ Alt text present on every visual
□ Tab order sensible
□ Print / PDF export looks acceptable (if required)
```

### Theme changes
```
□ All visuals pick up new theme (no hard-coded color overrides left)
□ Contrast ratio ≥ 4.5 on all text
□ Colorblind-safe palette (test with simulator if stakes are high)
□ Consistent font family across all visuals
```

### Security changes
```
□ Each RLS role returns only the intended rows (test with "View as")
□ No role has unintended access to sensitive measures
□ Audit log entries for role changes captured
```

## Acceptance

```
□ Reporter confirms the issue is fixed (with screenshot / reproduction)
□ Key stakeholders have been notified if the change is user-visible
□ No new issues introduced (regression test passed)
□ Changelog updated (see changelog-template.md)
□ Git commit made with descriptive message (see git-pbip-diff-guide.md)
```

## When validation fails

1. **Do not mark the feedback resolved**
2. Log the failure with reproduction steps
3. Decide: rollback (revert commit) or forward-fix (new commit on same branch)?
4. Re-run the full checklist after the fix
5. If 3 forward-fix attempts fail, escalate — the problem is likely deeper (design issue, not a simple fix)

## Validation evidence

For Critical-severity fixes, capture:
- Before screenshot
- After screenshot
- Test queries executed and their results
- Reporter's sign-off (email / chat quote)

Attach these to the feedback record or Git PR description.
