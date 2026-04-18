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

## Related Skills

| Skill | Relationship | When |
|---|---|---|
| `power-bi-performance-troubleshooting` | Routes to | Performance-related feedback gets deep diagnosis here |
| `power-bi-semantic-model` | Routes to | Data accuracy, missing data, RLS, and relationship issues |
| `power-bi-dax-development` | Routes to | New or broken measures, calculation fixes |
| `power-bi-report-design` | Routes to | Chart type changes, layout redesign, theme updates |
| `power-bi-pbip-report` | Routes to | Visual formatting fixes, JSON corrections, mobile layout |
| `power-bi-business-analysis` | Routes to | New requirements or significant scope expansion |

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

