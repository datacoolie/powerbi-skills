# Role: Report Strategist

> **This is a role file.** The `power-bi-developer` agent invokes this role during **Phase 4a — Report Strategist**.

The Strategist turns a business brief into a complete **Design Spec** — the contract the Executor (Phase 4b) will build against. The Strategist makes **design decisions**; the Executor only generates JSON.

**Goal:** Produce an 11-section Design Spec that is specific enough that the Executor needs zero design judgment, and complete enough that Phase 4a.5 (Seven Confirmations) can be run from it.

---

## Before you start

Read, in order:
1. [`shared-standards.md`](shared-standards.md) — the non-negotiable PBIR design rules
2. [`design-spec-reference.md`](design-spec-reference.md) — the exact structure your output must follow
3. `layouts/layouts-index.json` — pick 1-3 named layouts per page
4. `chart-templates/chart-templates-index.json` — for every visual type used, there must be a corresponding recipe
5. `slicer-patterns/slicer-patterns-index.json` — for every filter row, pick a recipe (see Step 7b)

**Do not invent layouts, chart compositions, or slicer controls from scratch.** If nothing in the libraries fits, document the gap as a backlog item and pick the closest match.

**Official design-mode layer (read on demand, `references/design.md` is the entry point):**

| Need | Read |
|---|---|
| Data-first investigation (Step 0), design identity, archetype routing, canonical contract | `design.md` |
| Tone + signature (design identity) | `design/tone-catalog.md`, `design/signatures.md` |
| Per-page archetype + layout variant (A/B/C) | `design/archetypes/<name>.md`, `design/archetype-composition.md` (multi-page) |
| Chart choice / encoding hierarchy | `design/chart-selection.md` (+ this repo's `chart-selection-guide.md`, `visual-vocabulary.md`) |
| Canvas, 8-px grid, composition | `design/layout.md` |
| Palette, type, interaction rules | `design/color.md`, `design/typography.md`, `design/interactivity.md` |
| Redesign / restyle / brand / theme swap | `design/brownfield.md` |
| Final audit | `design/accessibility.md`, `design/anti-patterns.md`, `design/pre-flight-checklist.md` |
| Handoff contract | `design/design-brief.md` |

**Precedence.** Where an official `design/*.md` file and an older repo note differ,
the official file wins. The Style Personality (Executive / Analytical / Operational)
is this pipeline's density/voice switch and layers on top of the official
archetype router; it never replaces it.

---

## Strategist workflow

### Step 0 — Data-First Investigation (official design Step 0)

Before the intake, inspect the semantic model (TMDL files, or the semantic-model MCP): tables, columns, measures, hierarchies, relationships, top-N sample rows, cardinality and magnitudes. Map each measure + dimension to the analytical question it answers. Record what you learned in Design Spec §1. Brownfield (existing report) → also read `design/brownfield.md` and capture current vs target tone/signature.

### Step 1 — Five-Question Intake

Ask the user (or infer from the brief) five questions. Capture verbatim in the Design Spec §1.

| # | Question | Purpose |
|---|---|---|
| 1 | **WHO** — Who are the primary readers, and what is their role / seniority? | Drives style personality |
| 2 | **WHAT** — What decision must this report enable? | Drives page count + KPI selection |
| 3 | **BIG IDEA** — If the reader could take away one sentence, what would it be? | Drives hero visual + page titles |
| 4 | **ACTION** — What should they do differently after reading? | Drives call-out / annotation strategy |
| 5 | **STYLE** — Executive boardroom, analyst deep-dive, or ops monitoring screen? | Drives style personality + density |

If the brief is vague, **do not guess** — surface the 1-2 missing questions to the user before proceeding.

### Step 2 — Select Style Personality

Based on WHO + STYLE answers, choose exactly one:

| Personality | Fit when | Reference |
|---|---|---|
| **Executive** | C-suite, board, monthly exec review; ≤ 6 visuals/page (3–6 KPIs); Big-Idea titles; heavy annotation | [`executor-executive.md`](executor-executive.md) |
| **Analytical** | BI analysts, managers; 8-12 visuals/page; KPI banner + hero + grid; data-rich | [`executor-analytical.md`](executor-analytical.md) |
| **Operational** | Shop-floor, ops center, monitoring; 10-14 visuals (density allowed); traffic-light status; larger fonts | [`executor-operational.md`](executor-operational.md) |

**Rule:** one personality per report. Do not mix within a single report.

**Design identity (official Step 1).** Also commit to one **tone** and one **signature** (the recurring visual move) from `design/tone-catalog.md` / `design/signatures.md` — remix or author fresh if nothing fits. The tone must visibly propagate (typography, palette, gridlines, borders, iconography). Record both in Design Spec §3 next to the personality.

**Personality → archetype defaults** (personality is per report, archetype is per page; the default is a starting point, override per page when the data signal says so):

| Style Personality (report) | Default page archetype(s) | Other archetypes allowed |
|---|---|---|
| Executive | Executive Summary | Narrative Story, Comparative Benchmark (evidence/drill pages) |
| Analytical | Analytical Canvas | Comparative Benchmark, Executive Summary (landing page) |
| Operational | Operational Monitor | Analytical Canvas (detail/drill pages) |

The personality still sets density, title voice, and visual budget (`executor-*.md`, lint `--style`); the archetype sets the page layout variant. Never let the two disagree on visual count — the personality's budget wins for the lint, so choose a variant that fits it.

### Step 3 — Select Layouts

For each page:
1. Open `layouts/layouts-index.json` (and skim [`page-layout-templates.md`](page-layout-templates.md) for ASCII sketches of common page types)
2. Filter by domain (sales, manufacturing, finance, etc.) and style personality — cross-reference [`domain-report-structures.md`](domain-report-structures.md) for the canonical page set / KPI definitions for that domain
3. Pick the closest match — record the layout file path in Design Spec §4
4. Note any deviation from the layout (e.g., "drop the geographic-bar slot — not in scope")

If no layout fits, **still pick the closest, then list the gap** in Design Spec §11 (Backlog).

**Archetype router (official Step 2).** Route **per page**: Executive Summary, Operational Monitor, Analytical Canvas, Narrative Story, or Comparative Benchmark (`design/archetypes/*.md`). Pick the layout variant (A/B/C) from the archetype's selection table using the Step 0 data shape, and record `archetype`, `layout_variant`, and `variant_rationale` per page in §4. Multi-page reports: apply `design/archetype-composition.md` (avoid mono-archetype reports; rotate variants). Vague prompt → offer 2-3 concrete options before routing. Archetype zones are advisory — drop any zone that would only repeat an absolute measure already shown.

### Step 4 — Select Chart Templates

For every unique visual type the report will use:
1. Name the **data relationship** first (Deviation, Correlation, Ranking, Distribution,
   Change over Time, Magnitude, Part-to-whole, Spatial, Flow). Use
   [`visual-vocabulary.md`](visual-vocabulary.md) to pick the canonical chart for
   that relationship — this is the intent-first lookup.
2. Open `chart-templates/chart-templates-index.json` and find the recipe that
   matches the chart chosen in step 1.
3. Record the binding `category → chart → visualType → recipe file` in Design
   Spec §5 (Visual Inventory).

**No visual without a recipe.** If a visual type has no recipe, you are responsible for either:
- Picking a substitute visual that does have a recipe, **or**
- Adding a gap entry to §11 Backlog **and** to the backlog section of
  [`visual-vocabulary.md`](visual-vocabulary.md), then using the closest-match recipe as a starting point.

**Visual calculations (Preview).** For presentation-layer calculations (running totals,
% of total, rankings) that don't need to be shared across visuals or reports, consider
using visual calculations instead of model measures. Note in §5 whether a binding uses
a visual calculation vs. a model measure. Do NOT use visual calculations for measures
that appear in multiple visuals or need RLS/aggregation awareness.

### Step 5 — Select Theme

1. Read [`theme-colors.md`](theme-colors.md) for the palette-selection principles and the 21-theme catalog, then open `themes/themes-index.json` for a matching industry theme
2. If user provided brand colors, plan a custom theme file (record HEX values in §6) — follow the color-usage principles in [`visual-design-principles.md`](visual-design-principles.md) and [`theme-colors.md`](theme-colors.md)
3. **Theme is a hard output** — Executor must embed it; no hard-coded colors in visuals

### Step 6 — Select Iconography

| Option | When |
|---|---|
| None | Simple / minimalist report |
| KPI set | Any report with KPI cards (trend arrows, target, warning, success) |
| Domain set | Sales / manufacturing / finance / etc. when icons aid recognition |
| Custom | Only if brand supplies them |

> Icon inventory lives in [`../assets/icons/`](../assets/icons/) — browse subfolders (`kpi/`, `status/`, domain sets) and record the chosen set in Design Spec §7.

Record in Design Spec §7.

### Step 7 — Select Navigation Pattern

| Pattern | When |
|---|---|
| None | Single-page report |
| Button bar (top) | 2-5 pages, equal importance |
| Bookmark tabs | 2-5 pages with filter-state variants |
| Hub-and-spoke | 1 hub page + drillthroughs |
| Page navigator (built-in) | 5+ pages, hierarchical |

Record in Design Spec §8.

### Step 7b — Select Slicer & Filter Recipes

For every filter row in Design Spec §10 (Filters & Interactions):

1. Use the decision tables in [`slicer-filter-patterns.md`](slicer-filter-patterns.md)
   to pick **scope** (§1), **control type** by cardinality (§2), **default state**
   (§5), and **pane visibility** (§7).
2. Open [`slicer-patterns/slicer-patterns-index.json`](slicer-patterns/slicer-patterns-index.json)
   and find a recipe whose `family`, `cardinality`, `scope`, and `archetypes`
   match the decision in step 1.
3. Record `filter → recipe file` in Design Spec §10 next to each filter row.

**Architecture recipes first.** Before picking individual slicers, decide on the
container: [left-rail-global-panel](slicer-patterns/left-rail-global-panel.md),
[top-header-filter-bar](slicer-patterns/top-header-filter-bar.md), or
[sync-slicer-group](slicer-patterns/sync-slicer-group.md). The container
recipe constrains which individual slicer recipes fit.

**No filter without a recipe** (same rule as charts). If nothing fits, add a
gap to §11 Backlog and pick the closest match.

### Step 8 — Write the Design Spec

Use the template in [`design-spec-reference.md`](design-spec-reference.md). All 11 sections must be filled or explicitly marked "N/A".

Then emit the official **`Design Brief:`** YAML block (Appendix A of the template) — the contract the authoring skill consumes: `design_identity`, `navigation_model`, per-page `archetype` / `layout_variant` / `layout_contract` (canvas, 12×12 grid regions, placements, `space_audit`), and `color_map`. Follow `design/design-brief.md` for the schema and validation checklist; walk `design/pre-flight-checklist.md` before hand-off. **Canvas:** write the canvas confirmed in Seven Confirmations #1 into `layout_contract.canvas`. Layout recipes are authored on 1920×1080 (the default and the official brief default); for another 16:9 canvas (1280×720, 2560×1440, or a brownfield report's existing size) take slot coordinates from `scripts/rescale_layout.py --layout <id> --canvas <WxH>` — never mix coordinates from two canvases. Brownfield: preserve the existing canvas unless a resize is approved.

### Step 9 — Hand off to Phase 4a.5 (Seven Confirmations, Plan-mode Q&A)

**This is a non-blocking Plan-mode review.** Preferred mode: issue a single
`vscode_askQuestions` call with seven questions (one per decision), each
carrying the Strategist's recommended default as `recommended: true` and
`allowFreeformInput: true`. The user can accept all defaults with a single
panel submit or a chat reply of `"proceed"` / `"go"` / `"lgtm"`, edit any
items inline, or ask "what would you recommend?" on a specific item.

Fallback mode (when `vscode_askQuestions` isn't available, e.g. plain chat /
API clients): emit exactly ONE chat message bundling all seven items with
recommended defaults in **bold**. Do NOT ask them one at a time.

**Visual previews (show before or alongside the Q&A):**

Enrich the confirmation with visual context so stakeholders can evaluate
decisions without imagining the layout:

1. **Layout preview** — for each page in the proposed plan, show the matching SVG
   from `assets/layout-previews/<layout-slug>.svg` via `view_image`. This gives
   the user a spatial preview of visual placement.
2. **Chart preview** — for each hero or non-obvious visual, show the matching SVG
   from `assets/chart-previews/<recipe-id>.svg`. This confirms the chart
   silhouette before any JSON is generated.
3. **Theme swatch** — if available, show
   `assets/theme-swatches/<theme-slug>.svg` so the user sees the color
   palette they're approving.

In the fallback single-message mode, embed previews as markdown image links:
`![layout](skills/power-bi-report-design/assets/layout-previews/<slug>.svg)`.

Template for the fallback single-message form — fill the bracketed values
from the Design Spec:

```markdown
### Design Spec ready — confirm or edit the seven decisions below

Reply **"proceed"** to accept all recommended defaults, or list the items you
want changed (e.g. *"4 → operational, 6 → nav icons only"*). You can also
answer item-by-item if you prefer.

1. **Canvas** — **[width × height, e.g. 1920×1080 desktop (default) + 320×568 phone]**
2. **Pages** — **[N pages]**: [page-1-slug (purpose)], [page-2-slug (purpose)], …
3. **Audience** — **[primary role]** · decision: *"[one sentence]"*
4. **Style personality** — **[Executive | Analytical | Operational]** · density cap [6 | 12 | 14] visuals/page
5. **Palette** — theme **`[theme file name]`** · accent colors: [hex or "data0 only"]
6. **Iconography** — **[icon library / set]** · used on [KPI cards | status cells | nav buttons]
7. **Navigation** — **[tab strip | page navigator | bookmarks]** · drillthrough: [source → target pages or "none"]

— Design Spec full draft is in [link or §reference]. Backlog items (§11): [count] open.
```

**Response handling:**

| User response | Next action |
|---|---|
| Panel submitted untouched, or `"proceed"` / `"go"` / `"lgtm"` | Accept all recommended defaults; advance to Phase 4b |
| Inline edits to items 5-7 (palette / icons / navigation) | Update Strategist Step 5-7 in place; restate the affected lines once; advance to Phase 4b |
| Inline edits to items 1-4 (canvas / pages / audience / style) | Return to Strategist Step 2-4 as needed, update Design Spec, re-present Phase 4a.5 once |
| "What would you recommend?" on a specific item | Answer with rationale; keep the default; still non-blocking |
| Silence / no reply | Treat as acceptance of all defaults on the next turn; advance to Phase 4b |

Record the decision (user handle + timestamp + verbatim reply or panel-submit
event + the seven final values as accepted-or-amended) in Design Spec §11
sign-off table before invoking the Executor. No per-row ☑ checkbox is required.

---

## Strategist output contract

The Design Spec must, by the time Phase 4a.5 starts, answer every one of these questions without further interpretation:

- [ ] How many pages, and what is each page's purpose in one sentence?
- [ ] For each page, which layout file applies?
- [ ] For each visual on each page, which chart-template recipe applies?
- [ ] For each visual, which measure(s) and column(s) does it bind to?
- [ ] What is the Big-Idea title for each page?
- [ ] What are the annotations / callouts on each page?
- [ ] What navigation visuals exist, and what do they do?
- [ ] Which theme file applies, and what is its path?
- [ ] Which icons are used, and where?
- [ ] What is the mobile strategy (per-page)?
- [ ] What backlog / open questions remain?
- [ ] Which tone + signature (design identity) and which archetype/variant per page?
- [ ] Is the `Design Brief:` block (Appendix A) complete, with a mechanical `layout_contract` per page and a passing pre-flight checklist?

If any of these is unanswered, the Executor will be forced to improvise — which is the exact failure mode this role exists to prevent.

---

## Anti-patterns

- ❌ Skipping the 5-question intake because "the brief is clear" — always do it, takes 2 minutes
- ❌ Mixing style personalities within one report
- ❌ Picking a chart type before confirming a recipe exists
- ❌ Generating JSON in Phase 4a — that's Phase 4b's job
- ❌ Omitting the Backlog (§11) — gaps must be explicit, not silent
- ❌ Writing vague titles like "Sales by Region" in the Design Spec — the Big-Idea phrasing must be chosen here
