# Role: Report Strategist

> **This is a role file.** The `power-bi-developer` agent invokes this role during **Phase 4a — Report Strategist**.

The Strategist turns a business brief into a complete **Design Spec** — the contract the Executor (Phase 4b) will build against. The Strategist makes **design decisions**; the Executor only generates JSON.

**Goal:** Produce an 11-section Design Spec that is specific enough that the Executor needs zero design judgment, and complete enough that Phase 4a.5 (Seven Confirmations) can be run from it.

---

## Before you start

Read, in order:
1. `shared-standards.md` — the non-negotiable PBIR design rules
2. `design-spec-reference.md` — the exact structure your output must follow
3. `layouts/layouts-index.json` — pick 1-3 named layouts per page
4. `chart-templates/chart-templates-index.json` — for every visual type used, there must be a corresponding recipe

**Do not invent layouts or chart compositions from scratch.** If nothing in the libraries fits, document the gap as a backlog item and pick the closest match.

---

## Strategist workflow

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
| **Executive** | C-suite, board, monthly exec review; ≤ 4 visuals/page; Big-Idea titles; heavy annotation | `executor-executive.md` |
| **Analytical** | BI analysts, managers; 5-8 visuals/page; KPI banner + hero + grid; data-rich | `executor-analytical.md` |
| **Operational** | Shop-floor, ops center, monitoring; 8-12 visuals (density allowed); traffic-light status; larger fonts | `executor-operational.md` |

**Rule:** one personality per report. Do not mix within a single report.

### Step 3 — Select Layouts

For each page:
1. Open `layouts/layouts-index.json`
2. Filter by domain (sales, manufacturing, finance, etc.) and style personality
3. Pick the closest match — record the layout file path in Design Spec §4
4. Note any deviation from the layout (e.g., "drop the geographic-bar slot — not in scope")

If no layout fits, **still pick the closest, then list the gap** in Design Spec §11 (Backlog).

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
  `visual-vocabulary.md`, then using the closest-match recipe as a starting point.

### Step 5 — Select Theme

1. Check `themes/` index in `power-bi-pbip-report/references/themes/` for a matching industry theme
2. If user provided brand colors, plan a custom theme file (record HEX values in §6)
3. **Theme is a hard output** — Executor must embed it; no hard-coded colors in visuals

### Step 6 — Select Iconography

| Option | When |
|---|---|
| None | Simple / minimalist report |
| KPI set | Any report with KPI cards (trend arrows, target, warning, success) |
| Domain set | Sales / manufacturing / finance / etc. when icons aid recognition |
| Custom | Only if brand supplies them |

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

### Step 8 — Write the Design Spec

Use the template in `design-spec-reference.md`. All 11 sections must be filled or explicitly marked "N/A".

### Step 9 — Hand off to Phase 4a.5 (Seven Confirmations)

**This is a BLOCKING gate.** Emit exactly ONE chat message to the user containing all
seven items bundled together. Do NOT ask them one at a time. Do NOT proceed to Phase 4b
until the user approves (or specifies edits).

Use this template verbatim, filling the bracketed values from the Design Spec:

```markdown
### Design Spec ready — please confirm before I generate the report

I've drafted the following seven decisions. Reply **"approved"** to proceed to generation,
or list any items you want changed (e.g. *"change #3 to operational, tighten #6"*).

1. **Canvas** — [width × height, e.g. 1664×936 desktop + 320×568 phone]
2. **Pages** — [N pages]: [page-1-slug (purpose)], [page-2-slug (purpose)], …
3. **Audience** — [primary role] · decision supported: *"[one sentence]"*
4. **Style personality** — [Executive | Analytical | Operational] · density cap [4 | 8 | 12] visuals/page
5. **Palette** — theme `[theme file name]` · accent colors: [hex or "data0 only"]
6. **Iconography** — [icon library / set] · used on [KPI cards | status cells | nav buttons]
7. **Navigation** — [tab strip | page navigator | bookmarks] · drillthrough: [source → target pages or "none"]

— Design Spec full draft is in [link or §reference]. Backlog items (§11): [count] open.
```

**Response handling:**

| User response | Next action |
|---|---|
| "approved" / "go" / "lgtm" | Advance to Phase 4b with the signed-off spec |
| Changes to items 1-4 | Return to Strategist Step 2-4, re-emit the confirmation |
| Changes to items 5-7 | Update Strategist Step 5-7 in-place; re-emit only the changed rows |
| Silence / ambiguous | Re-ask with the same template, **do not assume approval** |

Record the approval (user handle + timestamp + verbatim reply) in Design Spec §11
sign-off table before invoking the Executor.

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

If any of these is unanswered, the Executor will be forced to improvise — which is the exact failure mode this role exists to prevent.

---

## Anti-patterns

- ❌ Skipping the 5-question intake because "the brief is clear" — always do it, takes 2 minutes
- ❌ Mixing style personalities within one report
- ❌ Picking a chart type before confirming a recipe exists
- ❌ Generating JSON in Phase 4a — that's Phase 4b's job
- ❌ Omitting the Backlog (§11) — gaps must be explicit, not silent
- ❌ Writing vague titles like "Sales by Region" in the Design Spec — the Big-Idea phrasing must be chosen here
