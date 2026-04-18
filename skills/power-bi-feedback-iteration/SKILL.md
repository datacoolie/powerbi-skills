---
name: power-bi-feedback-iteration
description: >-
  Reference kit for the feedback and iteration phase of a Power BI project.
  Provides classification taxonomy, prioritization matrix, intake template,
  change-impact scoping, post-change validation checklist, A/B variant testing
  workflow, formal UAT workflow, PBIP Git diff guide, changelog template, and
  a performance quick-check pointer. Use this skill whenever the user provides
  feedback on an existing Power BI report, requests iteration, wants to run UAT,
  or needs to document changes. Routing (feedback → correct downstream skill)
  is owned by the power-bi-developer agent, not by this skill.
  Triggers include: "user feedback", "improve report", "fix report",
  "iterate on the report", "report review", "rebuild report", "UAT",
  "changelog", "release notes", "users are complaining", "performance issue",
  "add/remove/modify a page/measure/visual on an existing report".
  Do NOT use this skill for brand-new projects (use power-bi-business-analysis
  to start from scratch).
---

# Power BI Feedback & Iteration

Reference kit for the feedback and iteration phase. The `power-bi-developer`
agent orchestrates the workflow; this skill provides the supporting reference
material.

**Always search Microsoft Learn** (`microsoft-learn-mcp/microsoft_docs_search`)
for best practices before implementing any change.

## When to use this skill

- You received user feedback on an existing report
- You need to classify, prioritize, or scope a change
- You need to run post-change validation
- You need to compare design variants (A/B)
- You need to run or document formal UAT
- You need a PBIP-aware Git workflow, commit convention, or changelog

## Reference index

| Topic | File |
|---|---|
| Classify feedback (12 categories × severity) | [references/classification.md](references/classification.md) |
| Prioritize changes (impact × effort matrix) | [references/prioritization.md](references/prioritization.md) |
| Intake questions to ask the user | [references/feedback-intake-template.md](references/feedback-intake-template.md) |
| What each change touches (file-level impact) | [references/change-impact-scoping.md](references/change-impact-scoping.md) |
| Post-change validation checklist | [references/validation-checklist.md](references/validation-checklist.md) |
| A/B variant testing with Git branches | [references/ab-variant-testing.md](references/ab-variant-testing.md) |
| Formal UAT workflow | [references/uat.md](references/uat.md) |
| PBIP Git diff guide + commit conventions | [references/git-pbip-diff-guide.md](references/git-pbip-diff-guide.md) |
| Changelog / release-notes template | [references/changelog-template.md](references/changelog-template.md) |
| Performance quick check (points to perf skill) | [references/performance-quick-check.md](references/performance-quick-check.md) |

## Iteration cycle overview

```
Feedback → Intake → Classify → Scope → Prioritize → Route (via agent) → Implement → Validate → Release
    ↑                                                                                            │
    └──────────────────────────── Next cycle ────────────────────────────────────────────────────┘
```

## Skill workflow

1. **Intake** — apply [references/feedback-intake-template.md](references/feedback-intake-template.md) to capture symptom, expected behavior, reproduction, reporter, impact
2. **Classify** — apply [references/classification.md](references/classification.md) to assign one of 12 categories + severity
3. **Scope** — apply [references/change-impact-scoping.md](references/change-impact-scoping.md) to identify affected files, downstream validation, and risk
4. **Prioritize** — apply [references/prioritization.md](references/prioritization.md) (impact × effort)
5. **Route** — the `power-bi-developer` agent consults its routing table and dispatches to the correct downstream skill (see the agent's Phase 5 routing table)
6. **Implement** — done by the routed downstream skill (power-bi-semantic-model, power-bi-dax-development, power-bi-report-design, power-bi-pbip-report, or power-bi-performance-troubleshooting)
7. **Validate** — apply [references/validation-checklist.md](references/validation-checklist.md) before marking the item resolved
8. **Release** (optional, production reports) — run [references/uat.md](references/uat.md), tag in Git per [references/git-pbip-diff-guide.md](references/git-pbip-diff-guide.md), update [references/changelog-template.md](references/changelog-template.md)

## When the user contests between two designs

See [references/ab-variant-testing.md](references/ab-variant-testing.md) — build both as Git branches, compare side-by-side with a weighted evaluation grid, merge the winner, document the decision.

## When performance is the feedback

First-pass triage with [references/performance-quick-check.md](references/performance-quick-check.md). For deep diagnosis and optimization, route to the `power-bi-performance-troubleshooting` skill.

## Anti-patterns

- ❌ Don't skip classification because the fix seems obvious — classification drives correct routing
- ❌ Don't accept aggregated feedback ("users are complaining") — decompose into specific items
- ❌ Don't mark items resolved without running the validation checklist
- ❌ Don't release to production without a changelog entry
- ❌ Don't duplicate routing logic in this skill — the agent is the single source of truth

## Relationship to the agent

This skill is **reference material**. The `power-bi-developer` agent Phase 5
is the **orchestration**:

- Agent decides *which* skill fixes *which* category of feedback
- This skill provides the *templates, taxonomies, and checklists* used within Phase 5

Do not duplicate routing logic here. If a routing rule needs updating, update
the agent's routing table.
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
| "Chart is confusing / wrong type" | Report design skill → PBIP report skill | Re-design visual, change chart type, update layout, then regenerate |
| "Fix formatting / JSON error" | PBIP report skill | Fix visual.json directly |
| "Report is slow" | Performance troubleshooting skill | Diagnose with Performance Analyzer, optimize |
| "Need a new page" | Report design skill → PBIP report skill | Design new page, then generate PBIR files |
| "Need drill-down" | Report design skill → PBIP report skill | Design drillthrough page, then generate |
| "Mobile doesn't work" | PBIP report skill | Generate mobile.json layouts |
| "Access / security issue" | Semantic model skill | Review and fix RLS rules |
| "Change theme / colors" | Report design skill → PBIP report skill | Re-select theme, then regenerate theme file |
| "Complete redesign" | Business analysis skill | Re-run full requirements → model → DAX → design → report |

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
│ Chart type / layout│ Medium    │ report-design→     │
│                    │           │ pbip-report        │
│ Visual formatting  │ Medium    │ pbip-report        │
│ Performance        │ High      │ performance-       │
│                    │           │ troubleshooting    │
│ New requirement    │ Medium    │ business-analysis  │
│ Filter / slicer    │ Medium    │ pbip-report        │
│ Navigation         │ Low       │ report-design→     │
│                    │           │ pbip-report        │
│ Cosmetic / theme   │ Low       │ report-design→     │
│                    │           │ pbip-report        │
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

If performance is a concern, use the **power-bi-performance-troubleshooting** skill
for systematic diagnosis:

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

**Visual / UX Issues → `power-bi-report-design` skill first, then `power-bi-pbip-report` skill**
- Chart type changes (redesign decision → regenerate visual)
- Layout restructuring (design spec update → regenerate page)
- Theme/color changes (theme selection → regenerate theme file)
- Navigation and bookmark redesign

**Visual Formatting / JSON Fixes → `power-bi-pbip-report` skill directly**
- Formatting adjustments (padding, borders, font sizes)
- New pages with known design (drillthrough/tooltip)
- Slicer/filter modifications
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

### A/B Design Testing

When stakeholders are unsure between two design approaches, use variant branches:

```
1. Create Variants
   git checkout -b design/variant-a
   # Implement approach A (e.g., bar chart layout)
   git checkout dev
   git checkout -b design/variant-b
   # Implement approach B (e.g., matrix layout)

2. Present Side-by-Side
   - Open both branches in separate Power BI Desktop instances
   - Walk stakeholders through each variant with the same dataset
   - Collect preference votes and specific reasons

3. Select Winner
   - Merge chosen variant: git merge design/variant-a
   - Delete unused branch: git branch -d design/variant-b
   - Document decision rationale in commit message
```

**Evaluation criteria**: readability, data density, interaction speed, mobile compatibility.

### Formal UAT Workflow

For production reports or reports with regulatory/compliance needs:

```
UAT Steps:
1. PREPARATION
   □ Deploy report to a UAT workspace (not production)
   □ Use production-equivalent data (or sanitized copy)
   □ Prepare test cases covering all pages, filters, drillthroughs

2. TEST EXECUTION
   □ Functional: each visual shows correct data for known inputs
   □ Filters: slicers, cross-filters, drillthrough, bookmarks all work
   □ Edge cases: empty data, single-row, max date range, null values
   □ Performance: page load < 10s, interactions < 3s
   □ Access: RLS returns correct data for each test role
   □ Mobile: key pages render on tablet/phone layout

3. ISSUE TRACKING
   □ Log issues with: page, visual, steps to reproduce, expected vs actual
   □ Classify: blocker / major / minor / cosmetic
   □ All blockers must be fixed before sign-off

4. SIGN-OFF
   □ Business owner signs off on data accuracy
   □ Report consumers confirm usability
   □ IT/admin confirms performance and security
   □ Record sign-off date, names, and version in changelog
```

### Changelog / Release Notes Template

Maintain a changelog for production reports to track iteration history:

```markdown
# Report Changelog — [Report Name]

## [v2.1] — 2024-07-15
### Added
- Supplier scorecard drillthrough page
- YoY growth sparklines on overview

### Changed
- Switched Sales Trend from clustered bar to line chart
- Updated theme colors to match 2024 brand guidelines

### Fixed
- YTD calculation now respects fiscal year (Apr start)
- Overview page load time reduced from 18s to 6s

### Sign-off
- Business Owner: [Name] — 2024-07-14
- Data Team: [Name] — 2024-07-13
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
