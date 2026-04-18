# Changelog / Release Notes Template

Maintain a changelog for every production report to track iteration history and communicate changes to consumers.

## File location

`<Project>.Report/CHANGELOG.md` (co-located with the report)

## Format — Keep a Changelog + SemVer

Follow [Keep a Changelog](https://keepachangelog.com/) conventions + [Semantic Versioning](https://semver.org/).

### Versioning for Power BI reports

| Change type | Bump |
|---|---|
| Breaking (remove page / measure / column users depend on) | Major (1.0 → 2.0) |
| New page / new measure / theme overhaul | Minor (1.0 → 1.1) |
| Bug fix / cosmetic / performance | Patch (1.0 → 1.0.1) |

## Template

```markdown
# Changelog — <Report Name>

All notable changes to this report will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning follows [SemVer](https://semver.org/).

## [Unreleased]
### Added
- (items staged for next release)

### Changed
-

### Fixed
-

---

## [2.1.0] — 2026-07-15
### Added
- Supplier Scorecard drillthrough page (5 visuals, per-supplier view)
- YoY Growth sparklines on Overview page
- Mobile layout for Overview and Supplier Scorecard pages

### Changed
- Sales Trend visual switched from clustered bar to line chart (A/B decision, see docs/design-decisions.md#2026-06)
- Theme updated to 2026 brand colors (navy + accent gold)

### Fixed
- YTD calculation now respects fiscal year (Apr-Mar instead of calendar Jan-Dec)
- Overview page load time reduced from 18s to 6s (removed 2 unused visuals, optimized 3 measures)

### Performance
- FactSales model size reduced by 35% (dropped 12 unused columns)

### Security
- RLS: Regional Manager role now scoped to assigned regions only (was: all regions visible)

### Deprecated
- Legacy "Revenue v1" measure — use "Total Revenue" instead (removal planned for v3.0)

### Sign-off
- Business Owner: Jane Smith — 2026-07-14
- Data Team Lead: Bob Chen — 2026-07-13
- Report Consumer: Lin Wong (VP Sales) — 2026-07-14
- IT Admin: Raj Patel — 2026-07-12

---

## [2.0.0] — 2026-03-01
### Added
- Executive Overview page (replaces v1 landing)
- Drillthrough by Product Category

### Changed
- **BREAKING:** Renamed measure "Sales" to "Total Revenue"
  - Migration: update any external references
- Page order reorganized: Overview → Trend → Geography → Detail

### Removed
- **BREAKING:** "Legacy Dashboard" page (deprecated since v1.5)

---

## [1.2.1] — 2026-01-10
### Fixed
- Tooltip on Product Performance visual no longer shows raw column name

---

## [1.2.0] — 2025-12-15
### Added
- Forecast line on Sales Trend (using LINEST)
- Target vs Actual KPI card

---

## [1.0.0] — 2025-10-01
### Initial release
- Sales Overview page with 5 KPI cards + trend hero + regional breakdown
- Product Performance page with top-10 + bottom-5
- Date range slicer, region slicer, sync across pages
- Light theme, Segoe UI
```

## Release-note checklist

Before publishing a release:

```
□ All Unreleased items moved to the new version section
□ Version number follows SemVer rules
□ Release date accurate
□ Breaking changes clearly marked with **BREAKING:** and migration notes
□ Sign-off section populated (for production releases)
□ Links to related decision docs / UAT results included
□ New Unreleased section opened at top for next cycle
```

## Audiences

Write changelog entries for **three readers**:

1. **Report consumers** — "What changed in my daily experience?" — keep it business-level
2. **Data team** — "What changed in the model / DAX?" — include technical detail
3. **Auditors** — "Who approved it, when?" — keep sign-offs + dates

## Anti-patterns

- ❌ Don't commit "various fixes" — itemize every user-visible change
- ❌ Don't use commit messages as changelog entries — changelog is curated, commits are raw
- ❌ Don't bump major without a migration note
- ❌ Don't skip the Sign-off section for production releases
- ✅ Do link to the PR / commit / decision doc for context
- ✅ Do keep an "Unreleased" section always open for incremental drafting
