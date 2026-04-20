# Slicer & Filter Patterns

Decision guide for **where** to put a filter, **what type** of control to use,
and **how** it should behave. Populate the "Filters & Interactions" section of
the Design Spec (see [design-spec-reference.md §10](design-spec-reference.md))
using the tables below.

> **Visual preview catalog:** SVG mockups for every slicer recipe live in
> [`../assets/slicer-previews/`](../assets/slicer-previews/) (15 previews, dark-mode aware).

Input: the **filter requirements** captured upstream in
[../../power-bi-business-analysis/references/requirements-document-template.md](../../power-bi-business-analysis/references/requirements-document-template.md)
§6 — the business-analysis skill lists *which dimensions* the audience needs to
filter by; this reference decides *how* each one is implemented.

This reference answers 8 recurring questions:

1. Global vs. page-level vs. visual-level filter
2. Slicer type selection (dropdown / list / slider / hierarchy / date / search)
3. Sync slicer groups (which pages share filter state)
4. Cross-filter vs. highlight (cross-filter interaction behavior)
5. Default state selection
6. Filter vs. drillthrough (when a filter should become a page transition)
7. Filter pane visibility and governance
8. RLS interaction (avoid redundant filters)

**Recipe catalog.** Once a decision is made, pick a concrete composition from
[`slicer-patterns/`](slicer-patterns/README.md) — 14 recipes organised by family
(date, category, numeric, search, architecture, governance, parameter). Each
recipe has an ASCII mockup, slot bindings, a property snippet, defaults, and
anti-patterns. See [`slicer-patterns/slicer-patterns-index.json`](slicer-patterns/slicer-patterns-index.json) for the machine-readable catalog.

---

## 1. Filter Scope — Global vs. Page vs. Visual

Pick the smallest scope that works. Wider scope = less flexibility for the user.

| Scope | Where it applies | Use when | Example | Recipes |
|---|---|---|---|---|
| **Report-level (global)** | Every page, every visual | Dimension is universal to the whole story (Date, Region/BU, Currency) | `Date range`, `Region`, `Currency` | [left-rail-global-panel](slicer-patterns/left-rail-global-panel.md), [top-header-filter-bar](slicer-patterns/top-header-filter-bar.md) |
| **Page-level** | All visuals on one page | Dimension is meaningful only on that page | `Promotion ID` on a Promotion Post-mortem page | Any single-slicer recipe |
| **Visual-level** | One visual only | You need a different grain for one visual on a page that already has a page filter | `Top 10` filter on a single bar chart | (filters pane — no dedicated recipe) |
| **Sync-slicer group** | A defined subset of pages | Multiple pages share a narrative but not all pages | Filter persists across Analysis pages, resets on Detail page | [sync-slicer-group](slicer-patterns/sync-slicer-group.md) |

### Decision rule

```
Ask: "If I change this filter, should every page/visual update?"
├── Yes, everywhere                → Report-level (global slicer panel)
├── Yes, but only on related pages → Sync-slicer group
├── Yes, but only this page         → Page-level slicer
└── Yes, but only this visual       → Visual-level filter (filters pane)
```

**Anti-pattern:** Adding a global slicer for something that only matters on one
page — forces users to keep re-setting it when they leave and return.

---

## 2. Slicer Type Selection

| Data shape | Cardinality | Recommended control | Recipe |
|---|---|---|---|
| **Date range** | Continuous | Between slider OR relative-date (Last N months) | [date-between-slider](slicer-patterns/date-between-slider.md), [date-relative-rolling](slicer-patterns/date-relative-rolling.md) |
| **Single date** | — | Dropdown calendar | [date-between-slider](slicer-patterns/date-between-slider.md) (set equal bounds) |
| **Categorical low-card** (≤ 7) | 2–7 values | Button/tile slicer (horizontal chips) | [chiclet-tile-slicer](slicer-patterns/chiclet-tile-slicer.md) |
| **Categorical medium** (8–25) | 8–25 | Dropdown with search | [dropdown-search-slicer](slicer-patterns/dropdown-search-slicer.md) |
| **Categorical high-card** (> 25) | 26–10 000 | Dropdown with search + multi-select | [dropdown-search-slicer](slicer-patterns/dropdown-search-slicer.md) |
| **Very high cardinality** (> 10 000) | Customer ID, SKU | **Do not use a slicer** — require drill-in or search visual | [search-box-high-card](slicer-patterns/search-box-high-card.md) |
| **Hierarchical** (Year → Quarter → Month; Region → Country → City) | Any | Hierarchy slicer (expand/collapse) | [hierarchy-slicer](slicer-patterns/hierarchy-slicer.md) |
| **Numeric continuous** | Any | Numeric range slider | [numeric-range-slicer](slicer-patterns/numeric-range-slicer.md) |
| **Boolean / On-Off** | 2 | Button slicer with 2 tiles | [chiclet-tile-slicer](slicer-patterns/chiclet-tile-slicer.md) |
| **Unknown / free-text search** | Any | Search box bound to a text column | [search-box-high-card](slicer-patterns/search-box-high-card.md) |

### Multi-select vs. single-select

| Rule | Applies when |
|---|---|
| **Single-select** | Comparisons depend on one category being "current" (e.g. drillthrough target) |
| **Multi-select** | Side-by-side analysis is the point (e.g. compare 3 regions) |
| **Single-select with "All"** | Default view is aggregated, optional filter |
| **Never both Select-All and required** | Contradictory UX |

---

## 3. Sync Slicer Groups

A **sync group** is a named set of pages that share slicer state. When a user
changes the slicer on Page A, Pages B and C (in the same group) update too.

### When to use

| Scenario | Sync group | Notes |
|---|---|---|
| Overview + 2-3 Analysis pages drive the same narrative | ✅ Yes | User tells "the same story" across pages |
| Detail/Drillthrough page | ❌ No | Drillthrough passes its own filter context; syncing overwrites it |
| Tooltip page | ❌ No | Inherits context from the hovered visual |
| Pages serving different audiences (e.g. Executive Overview vs. Analyst Workbench) | ❌ No | Different mental models; keep independent |
| Mobile layouts | ✅ Yes (usually) | Keep parity with desktop unless the mobile story branches |

### How to document

In the Design Spec "Filters & Interactions" section, record the sync group:

```markdown
| Scope | Filter / Slicer | Type | Default | Sync group |
|---|---|---|---|---|
| Group: Analysis | Region | Dropdown | All | `analysis-group` |
| Group: Analysis | Date range | Between | Last 12M | `analysis-group` |
| Page: Detail | (none — receives drillthrough context) | — | — | — |
```

---

## 4. Cross-Filter vs. Highlight (Visual Interactions)

When a user clicks a bar/slice/point on Visual A, what happens to Visual B?

| Behavior | Effect on Visual B | Use when |
|---|---|---|
| **Cross-filter** | Rows/points not matching A are hidden | B is a ranked list or table where irrelevant rows should disappear |
| **Highlight** | All points remain; matching portion is emphasized | B is a KPI card, gauge, or trend — user wants to see the part-of-whole |
| **None** | No change | B is independent reference data (target line, benchmark) |

### Default rule

| Visual type of target (B) | Default behavior |
|---|---|
| Card, KPI, gauge | **Highlight** (preserves context) |
| Line/area chart (trend) | **Highlight** (preserves the whole-period baseline) |
| Bar / column chart | **Cross-filter** (focus on matching categories) |
| Table / matrix | **Cross-filter** (reduce rows to what matters) |
| Map | **Highlight** (keep geography intact) |
| Slicer | **Cross-filter** (narrow the available values) |

Document deviations in the Design Spec under "Cross-filter behavior."

---

## 5. Default State

Defaults set the **first impression** — they must show a meaningful story before
the user touches anything.

| Filter | Good default | Bad default | Why |
|---|---|---|---|
| Date range | Last complete period (e.g. "Last 12 months", "Last complete quarter") | All time | All time often shows noise; latest period is usually the question |
| Region / BU | "All" if user has access to all; otherwise user's own region | Hard-coded single region | RLS should handle scoping; defaults should not embed user identity |
| Product / SKU | "All" | Top 1 by revenue | Forces user to undo to explore |
| Comparison mode | Current vs. Previous Year | "No comparison" | Comparison is usually the point |
| Currency | Reporting currency | User's local | Consistent executive view |

### Relative-date defaults

Use relative-date filters (auto-advancing) for anything that gets viewed weekly+:
- Daily ops dashboard → `Last 7 days` (relative)
- Monthly review → `Last 3 months` or `Current month` (relative)
- Annual planning → `Current year` (relative)

### Lock vs. default

| State | Meaning |
|---|---|
| **Default** | Pre-set value, user can change |
| **Locked** | Pre-set, user cannot change (use when the report's meaning depends on it, e.g. "Q1 Retrospective" page locked to Q1) |
| **Hidden & applied** | Filter is invisible but active (filters pane items with "lock" icon) |

---

## 6. Filter vs. Drillthrough

A filter *narrows what's on the current page*. A drillthrough *takes the user to
a different page with context carried over*. Pick the right one.

| Pattern | Use filter | Use drillthrough |
|---|---|---|
| User wants more detail about one item | ❌ | ✅ — open a Detail page for that item |
| User wants to compare several items | ✅ multi-select | ❌ — drillthrough is single-context |
| User wants to see the same visuals scoped to a subset | ✅ | ❌ |
| User wants to see **different** visuals for that subset | ❌ | ✅ — Detail page has its own layout |
| The filter values are bounded (few options) | ✅ slicer | ❌ |
| The filter values are unbounded (any customer, any SKU) | ❌ — don't populate a slicer | ✅ — right-click → drillthrough |

### Design rule

Drillthrough is for **"zoom in on one thing"**. A slicer is for **"change the
lens"**. If you catch yourself adding a slicer with thousands of options to
support detail exploration, that's a drillthrough pattern misused.

Every drillthrough target page **must have a Back button** (see executor style
references in `power-bi-report-design`).

---

## 7. Filter Pane Visibility & Governance

Power BI has three control surfaces: **slicers** (visible on-canvas), the
**filters pane** (side panel), and **page-level filters** (hidden from viewer
by default).

| Filter location | Who sees/changes | Governance guidance | Recipes |
|---|---|---|---|
| Slicers on canvas | Every user | Primary dimensions only — keep to ≤ 4 per page | [chiclet-tile-slicer](slicer-patterns/chiclet-tile-slicer.md), [dropdown-search-slicer](slicer-patterns/dropdown-search-slicer.md), [date-relative-rolling](slicer-patterns/date-relative-rolling.md) |
| Filters pane — Visual filters | Users with pane open | Power-user controls, secondary refinements | (pane only) |
| Filters pane — Page filters | Users with pane open | Apply per-page scope that shouldn't be visible on canvas | [hidden-applied-filter](slicer-patterns/hidden-applied-filter.md) |
| Filters pane — Report filters | Users with pane open | Report-wide rails (rarely used; prefer global slicers) | [left-rail-global-panel](slicer-patterns/left-rail-global-panel.md) |
| Hidden filters | Never visible | Data-quality filters (`[IsActive] = TRUE`), RLS pre-filter | [hidden-applied-filter](slicer-patterns/hidden-applied-filter.md) |
| Locked filters | Visible, not editable | Page represents a fixed view (e.g. a "Q1" page) | [hidden-applied-filter](slicer-patterns/hidden-applied-filter.md), [role-based-bookmark](slicer-patterns/role-based-bookmark.md) |

### Pane visibility defaults

| Report type | Filters pane default |
|---|---|
| Executive | **Collapsed or hidden** — clutter distracts |
| Analytical | **Collapsed** — available when needed |
| Exploration | **Expanded** — power users live in it |
| Operational | **Hidden** — decisions come from canvas, not pane |

### Hidden vs. locked (decision)

```
Is the filter value part of the page's meaning?
├── Yes, and users must not change it   → Locked + visible (so they see the scope)
├── Yes, but users should not see it     → Hidden + applied
└── No, users should freely change it    → Slicer on canvas
```

---

## 8. RLS Interaction — Avoid Redundant Filters

If the Requirements Document §7
([../../power-bi-business-analysis/references/requirements-document-template.md](../../power-bi-business-analysis/references/requirements-document-template.md))
defines RLS
(e.g. Region Manager sees only their own region), then:

| Filter | Redundant with RLS? | Action |
|---|---|---|
| Region slicer on overview page | Yes — RLS already scopes | **Remove**; or keep for multi-region users only |
| Region dropdown that lists all regions | Yes | **Replace** with a slicer bound to the RLS-scoped table so only accessible regions show |
| "My Team" vs. "All Teams" toggle | Yes | **Remove** — RLS should do this silently |
| Division slicer when role is defined by Division | Yes | **Remove** |
| Product-category slicer when RLS is Region-based | No | **Keep** — orthogonal dimensions |

### Rule

**RLS handles identity; slicers handle choice.** Never build a slicer that
replicates what RLS already enforces — it creates the illusion of control and
can confuse users who see regions they can't actually filter to.

### When to keep an RLS-aligned slicer

- Users with "All-access" roles (e.g. finance controllers) need to scope further
- The column is used as a dimension in visuals, not just for security
- Mobile/export scenarios where the pane isn't available

Document this in the Design Spec (cross-reference Requirements Document §7):

```markdown
RLS-aligned columns: Region, Division
Slicers retained despite RLS: Region (for all-access controllers only; hidden for scoped roles via role-based bookmark)
```

---

## Decision Checklist — per filter

Before adding any filter, answer these 7 questions:

- [ ] **Scope**: Report / Sync-group / Page / Visual? (§1)
- [ ] **Type**: Which control fits the data cardinality? (§2)
- [ ] **Sync**: Which page group shares this? (§3)
- [ ] **Interaction**: Cross-filter or Highlight for each target visual? (§4)
- [ ] **Default**: Relative or absolute? Locked or editable? (§5)
- [ ] **Filter or drillthrough?** If cardinality > 1 000, prefer drillthrough (§6)
- [ ] **RLS check**: Is this column already scoped by a security role? (§8)

Record the answers in the Design Spec "Filters & Interactions" section.

---

## Worked Example — FMCG Trade Analytics

Continuing the SKILL.md worked example (5 pages: Overview → Trade ROI by Channel
→ Brand Deep-dive → Promotion Post-mortem → Detail drillthrough):

```markdown
## §6 Filters and Interactions

| Scope | Filter / Slicer | Type | Default | Sync group | Notes |
|---|---|---|---|---|---|
| Global | Date range | Relative between (Last 12 months) | Last 12M, rolling | analysis-group | |
| Global | Channel | Button tiles (MT / GT / e-com) | All | analysis-group | Low cardinality → buttons |
| Sync: Analysis | Brand | Dropdown with search | All | analysis-group | 15 brands → searchable dropdown |
| Page: Promotion Post-mortem | Promotion type | Button tiles (Price / BOGO / Display / TV) | All | — | Page-specific |
| Page: Detail (drillthrough) | (receives Brand + Date + Channel from source visual) | — | — | — | Back button required |
| Visual: Overview Top-10 chart | Top N = 10 | Visual-level filter | 10 | — | Fixed |

**Cross-filter behavior:**
- KPI cards and trend lines: Highlight (preserve baseline)
- Bar charts and tables: Cross-filter (reduce rows)
- Reference target lines: None (independent)

**Pane visibility:** Collapsed by default (Analytical archetype)

**RLS interaction:** Region-based RLS applied; no Region slicer needed. Channel
and Brand are orthogonal to RLS — slicers retained.
```
