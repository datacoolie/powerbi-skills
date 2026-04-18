# A/B Variant Testing (Git-Branch Workflow)

When stakeholders are unsure between two design approaches, build both and compare side-by-side.

## When to use A/B variants

- Chart type choice is contested (e.g., stacked bar vs grouped bar vs small multiples)
- Layout direction is unclear (hero-metric top vs KPI-banner top)
- Color / theme preference (conservative vs brand-forward)
- Navigation pattern (button bar vs page navigator)

**Do NOT use A/B for:**
- Data accuracy issues — there's a correct answer
- Measure correctness — there's a correct formula
- Security — there's a correct rule

## Workflow

### 1. Create variant branches

```bash
# Start from the baseline
git checkout dev
git pull

# Variant A
git checkout -b design/variant-a-bar-layout
# Implement approach A (e.g., bar chart layout)
# Commit all files
git add .
git commit -m "feat(report): variant A — bar chart layout"
git push -u origin design/variant-a-bar-layout

# Variant B
git checkout dev
git checkout -b design/variant-b-matrix-layout
# Implement approach B (e.g., matrix layout)
git add .
git commit -m "feat(report): variant B — matrix layout"
git push -u origin design/variant-b-matrix-layout
```

### 2. Present side-by-side

- Open the `.pbip` from each branch in separate Power BI Desktop instances (or two VS Code windows for the JSON diff)
- Use **the same dataset and the same filter state** for both
- Walk stakeholders through the same analytical questions on each variant
- Capture screenshots of both for the decision record

### 3. Collect structured feedback

Use this evaluation grid:

| Criterion | Weight | Variant A score (1-5) | Variant B score (1-5) |
|---|---|---|---|
| Readability at a glance | 3× | | |
| Data density (appropriate) | 2× | | |
| Interaction speed | 2× | | |
| Mobile compatibility | 1× | | |
| Stakeholder preference | 3× | | |
| Maintainability | 1× | | |
| Accessibility (contrast, alt text) | 2× | | |

Compute weighted totals; declare winner.

### 4. Select winner and merge

```bash
# Merge winner into dev
git checkout dev
git merge design/variant-a-bar-layout

# Delete loser branch (after saving decision doc)
git branch -d design/variant-b-matrix-layout
git push origin --delete design/variant-b-matrix-layout
```

### 5. Document the decision

Add to `docs/design-decisions.md` (or commit message on the merge):

```markdown
## Decision: Bar chart vs matrix layout for Sales Overview — 2026-04-17

- **Chose:** Variant A (bar chart layout)
- **Score:** A 34 vs B 27
- **Key reasons:**
  - Faster to scan at a glance (stakeholders noted 2-3s faster to identify top region)
  - Matrix required > 8 visible rows — exceeded screen height
- **Trade-off accepted:** Lost some per-region detail; compensated by drillthrough page
- **Stakeholders:** Sales VP, Analytics Director
- **Branch retained:** design/variant-a-bar-layout (merged); design/variant-b-matrix-layout (deleted after archive)
```

## Three-way and beyond

For more than two variants:
- Name branches `design/variant-{a|b|c}-<description>`
- Eliminate weakest first (narrowing round)
- Run final head-to-head between top 2

Avoid 4+ variants — stakeholder fatigue degrades decision quality.

## Anti-patterns

- ❌ Don't compare variants with different data / filter state — confounds the evaluation
- ❌ Don't let "novelty bias" win — the newer variant often feels fresher regardless of merit
- ❌ Don't merge both and let users toggle — doubles maintenance; pick one
- ❌ Don't skip the decision document — loses the reasoning for the next project
