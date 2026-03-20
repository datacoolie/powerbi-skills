---
name: power-bi-feedback-iteration
description: >-
  Process user feedback on Power BI reports and drive iterative improvement cycles.
  Use this skill whenever the user provides feedback on an existing report, wants to improve
  or fix a report, requests changes to visuals or measures, reports performance issues,
  asks for a report review, or wants to add/remove/modify pages, measures, or visuals
  in a Power BI project. Triggers include: "user feedback", "improve report", "fix report",
  "report not working", "add a measure", "add a page", "rebuild report", "performance issue",
  "report review", "change the visual", "users are complaining", "iterate on the report",
  "report needs updates". Do NOT use for brand-new projects (use power-bi-business-analysis)
  or for initial model/report creation from scratch.
---

# Power BI Feedback & Iteration

Process user feedback on existing Power BI reports and drive systematic improvement.
Route changes to the correct downstream skill and validate results.

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`) for
relevant best practices before implementing changes.

## Quick Reference

| Feedback Type | Route To | Action |
|---|---|---|
| "Data is wrong / missing" | Semantic model skill | Fix source, add table/column, adjust relationships |
| "Need a new metric" | DAX development skill | Create measure, add to visuals |
| "Chart is confusing" | PBIP report skill | Redesign visual, change chart type, improve layout |
| "Report is slow" | Performance troubleshooting | Diagnose with Performance Analyzer, optimize |
| "Need a new page" | PBIP report skill | Design and generate new page |
| "Need drill-down" | PBIP report skill | Add drillthrough page, configure interactions |
| "Mobile doesn't work" | PBIP report skill | Generate mobile.json layouts |
| "Access / security issue" | Semantic model skill | Review and fix RLS rules |
| "Complete redesign" | Business analysis skill | Re-run full requirements → model → DAX → report |

## Phase 1: Feedback Intake

### Categorize Feedback

Classify each piece of feedback into one of these categories:

```
Feedback Classification:
┌─────────────────────────────────────────────────────┐
│ Category           │ Severity  │ Skill Route        │
├────────────────────┼───────────┼────────────────────┤
│ Data accuracy      │ Critical  │ semantic-model     │
│ Missing insight    │ High      │ business-analysis  │
│ New measure needed │ High      │ dax-development    │
│ UX / visual issue  │ Medium    │ pbip-report        │
│ Performance        │ High      │ (troubleshooting)  │
│ New requirement    │ Medium    │ business-analysis  │
│ Filter / slicer    │ Medium    │ pbip-report        │
│ Navigation         │ Low       │ pbip-report        │
│ Cosmetic / theme   │ Low       │ pbip-report        │
│ Security / access  │ Critical  │ semantic-model     │
└─────────────────────────────────────────────────────┘
```

### Gather Details

For each feedback item, collect:

```
Feedback Detail Template:
□ What exactly is wrong or missing? (specific visual, page, measure)
□ What is the expected behavior or result?
□ Who reported it? (role, frequency of use)
□ How many users are affected?
□ What is the business impact if not fixed?
□ Can you reproduce it? (steps to reproduce)
□ Screenshots or specific examples?
```

## Phase 2: Gap Analysis

Compare the current report against the original requirements:

### Requirements vs. Reality Check

```
Gap Analysis Matrix:
| Original Requirement | Current State | Gap | Priority |
|---|---|---|---|
| [KPI from requirements] | [Exists? Correct?] | [What's missing] | [H/M/L] |
```

### Performance Assessment

If performance is a concern, follow the diagnostic framework from
`references-md/skill.power-bi-performance-troubleshooting.md`:

```
Performance Quick Check:
□ Page load time (target: < 10 seconds)
□ Visual interaction response (target: < 3 seconds)
□ Number of visuals per page (target: ≤ 8)
□ Model size (check for unnecessary columns/tables)
□ DAX query times (use Performance Analyzer)
□ Cross-filtering overhead (check visual interactions)
```

### Common Performance Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| Slow page load | Too many visuals | Reduce to 6-8, use drillthrough for detail |
| Slow slicer | High-cardinality field | Add search, limit displayed items |
| Slow visual | Expensive DAX | Optimize measure with variables, reduce context transitions |
| Slow refresh | Large import model | Add incremental refresh, remove unused columns |
| Slow cross-filter | Bi-directional relationships | Change to single-direction where possible |

## Phase 3: Impact Assessment & Prioritization

### Prioritization Matrix

```
Priority Assessment:
┌───────────────┬────────────────┬──────────────┐
│               │ High Business  │ Low Business │
│               │ Impact         │ Impact       │
├───────────────┼────────────────┼──────────────┤
│ Easy to Fix   │ DO FIRST       │ Quick Win    │
│ (< 1 hour)    │ ★★★★★       │ ★★★         │
├───────────────┼────────────────┼──────────────┤
│ Hard to Fix   │ Plan & Execute │ Defer/Backlog│
│ (> 1 hour)    │ ★★★★         │ ★★          │
└───────────────┴────────────────┴──────────────┘
```

### Change Impact Assessment

Before implementing, assess what each change touches:

```
Impact Scope:
□ Model only (no report changes needed)
□ DAX only (add/modify measures, no visual changes)
□ Report only (visual/layout changes, no model changes)
□ Model + DAX (new table/column → new measure)
□ Model + Report (new relationship → visual interaction change)
□ Full stack (model + DAX + report changes)
```

## Phase 4: Implementation Routing

### Route to Appropriate Skill

Based on the classification, invoke the correct skill:

**Data / Model Issues → `power-bi-semantic-model` skill**
- Missing tables or columns
- Incorrect relationships
- Storage mode changes
- RLS rule updates
- New data source integration

**New Measures → `power-bi-dax-development` skill**
- New KPI calculations
- Modified existing measures
- New time intelligence requirements
- Calculation group additions
- Field parameter changes

**Visual / UX Issues → `power-bi-pbip-report` skill**
- Chart type changes
- Layout restructuring
- New pages (including drillthrough/tooltip)
- Slicer/filter modifications
- Navigation and bookmark updates
- Theme/color changes
- Mobile layout fixes

**Performance Issues → Troubleshooting workflow**
- Use Performance Analyzer to identify bottleneck
- Classify as model, DAX, report, or infrastructure issue
- Apply targeted fix from the performance troubleshooting reference

**New Requirements → `power-bi-business-analysis` skill**
- Significant scope expansion
- New audience or use case
- Fundamentally different analytical questions
- Major restructuring needed

## Phase 5: Validation

After implementing changes, verify:

### Change Validation Checklist

```
Post-Change Verification:
□ Original issue is resolved
□ No regression in existing functionality
□ Performance is acceptable (page load < 10s, interaction < 3s)
□ Cross-filtering still works correctly
□ Data accuracy confirmed with known test values
□ Slicers and filters behave as expected
□ Drillthrough pages receive correct context
□ Mobile layout still functional (if applicable)
□ PBIP file integrity (all cross-references valid)
```

### User Acceptance

```
Acceptance Criteria:
□ Reporter confirms the issue is fixed
□ Key stakeholders review changes
□ No new issues introduced
□ Documentation updated if requirements changed
```

## Phase 6: Version Control (PBIP-Friendly)

Since reports are in PBIP format (file-based), leverage Git for iteration:

### Recommended Git Workflow

```
Branching Strategy:
main          ← Production-ready reports
├── dev       ← Integration branch for testing
│   ├── fix/slow-overview-page
│   ├── feat/add-supplier-scorecard
│   └── fix/ytd-measure-incorrect
```

### Commit Message Convention

```
Pattern: <type>(<scope>): <description>

Types:
- fix:   Bug fix (data, visual, measure)
- feat:  New feature (page, measure, visual)
- perf:  Performance improvement
- style: Cosmetic change (theme, formatting)
- refactor: Model restructuring

Examples:
- fix(dax): correct YTD calculation for fiscal year
- feat(report): add supplier scorecard drillthrough page
- perf(model): remove unused columns from FactSales
- style(report): update theme to match brand guidelines
```

### What Changed — PBIP Diff Guide

| Change Type | Files Affected |
|---|---|
| New page | `pages/pages.json` + new `pages/<slug>/page.json` + visuals |
| Modified visual | `pages/<page>/visuals/<visual>/visual.json` |
| New measure | `reportExtensions.json` (report-level) or `.tmdl` files (model) |
| Theme change | `StaticResources/RegisteredResources/*.json` + `report.json` |
| Layout change | Multiple `visual.json` files (position properties) |

## Iteration Cycle

```
Feedback → Classify → Prioritize → Route → Implement → Validate → Deploy
    ↑                                                          │
    └──────────────────── Next cycle ──────────────────────────┘
```

Repeat until stakeholders confirm the report meets business needs.
Each iteration should be a focused, testable unit of change.
