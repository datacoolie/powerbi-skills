# Formal UAT Workflow

For production reports or reports with regulatory/compliance needs, run formal User Acceptance Testing before release.

## When UAT is required

- Report goes to external audiences (customers, regulators, board)
- Report drives financial decisions (revenue recognition, compensation)
- Report is subject to regulatory scrutiny (SOX, HIPAA, GDPR)
- Report replaces an existing production report (parallel-run validation)
- Report is a major version (new pages, model restructure)

## When UAT can be skipped

- Internal analytics / exploration reports
- Hotfix for a Critical-severity issue (do abbreviated UAT post-hoc)
- Cosmetic-only changes

## Four-stage UAT

### Stage 1 — Preparation

```
□ Deploy report to a UAT workspace (NOT production)
□ Use production-equivalent data (sanitized copy if PII)
□ Document expected values for key KPIs (source them from the system of record)
□ Prepare test cases covering: all pages, all slicers, all drillthroughs, RLS roles, mobile views
□ Identify UAT testers: business owner, 2-3 power users, 1 accessibility reviewer
□ Set UAT window (typically 3-5 business days)
□ Distribute UAT plan document
```

### Stage 2 — Test Execution

Testers exercise the report against structured test cases:

```
Functional tests
□ Each visual shows correct data for known inputs
□ KPI numbers match system of record within tolerance
□ Totals reconcile (page totals = sum of drillthrough details)
□ Empty / null / edge cases handled gracefully

Filter tests
□ Slicers filter the intended visuals only
□ Cross-filtering between visuals produces expected highlights
□ Drillthrough passes the correct filter context
□ Bookmarks restore the correct filter state
□ Sync slicers propagate across pages

Edge case tests
□ Empty data (filter that returns no rows)
□ Single row / single category
□ Max date range (full history)
□ Null / blank values displayed sensibly

Performance tests
□ Page load ≤ 10 seconds
□ Visual interaction ≤ 3 seconds
□ Refresh time within SLA

Security tests
□ RLS returns correct data for each test role
□ No user sees data outside their role's scope
□ Sensitive measures hidden from unauthorized roles

Mobile tests (if applicable)
□ Key pages render on tablet (1024×768)
□ Key pages render on phone (portrait)
□ Touch targets are large enough

Accessibility tests
□ Contrast ratio ≥ 4.5 on all text
□ Alt text on every visual
□ Tab order sensible
□ Screen reader can announce titles and values
```

### Stage 3 — Issue Tracking

For each defect found:

```markdown
## UAT Issue #<id>
- **Page / visual:** ________________
- **Tester:** ______________________
- **Found:** <date>
- **Steps to reproduce:** ___________
- **Expected:** ____________________
- **Actual:** ______________________
- **Screenshot:** __________________
- **Classification:** <blocker | major | minor | cosmetic>
- **Status:** <open | in-fix | retest | closed>
```

**Severity definitions for UAT:**
| Severity | Definition | Release impact |
|---|---|---|
| Blocker | Wrong number, security breach, page crash | Must fix before release |
| Major | Functional but incorrect behavior in common case | Must fix before release |
| Minor | Functional but annoying; uncommon case | Fix in next patch |
| Cosmetic | Labels, wording, minor alignment | Fix in next polish sweep |

**Rule: All Blockers and Majors must be fixed before sign-off.**

### Stage 4 — Sign-off

Collect structured sign-off from each role:

```markdown
## UAT Sign-off — [Report Name] v<version> — <date>

### Business Owner
- Name: ______________________
- Date: ______________________
- Signature: __________________
- Scope: Confirms data accuracy, KPI definitions, and business logic

### Data Team Lead
- Name: ______________________
- Date: ______________________
- Signature: __________________
- Scope: Confirms data lineage, refresh, and model correctness

### Report Consumer (Power User)
- Name: ______________________
- Date: ______________________
- Signature: __________________
- Scope: Confirms usability, navigation, and daily-use workflows

### IT / Admin
- Name: ______________________
- Date: ______________________
- Signature: __________________
- Scope: Confirms workspace access, performance, and security

### Open issues accepted for release
- Issue #___ (Minor): ___________
- Issue #___ (Cosmetic): _______

### Open issues blocking release
- None (all resolved)
```

## UAT → Production deployment

Only after all four sign-offs:

1. Tag the release in Git (`v1.0.0`, `v1.1.0`, etc.)
2. Promote to production workspace
3. Update changelog (see `changelog-template.md`)
4. Notify report consumers
5. Monitor for 1-2 days; be ready to roll back

## Anti-patterns

- ❌ Don't skip UAT because "the team already reviewed it" — testers must be the actual users
- ❌ Don't accept sign-off without the test evidence attached
- ❌ Don't release with Blockers open — compounds debt
- ❌ Don't compress the UAT window below 2 business days — testers need time
- ✅ Do run parallel-production for at least one reporting cycle when replacing an old report
