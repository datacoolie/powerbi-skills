# Role: Polisher

> **This is a role file.** The `power-bi-developer` agent invokes this role during **Phase 4c — Polish & Design QA**.

The Polisher runs **after** the Executor finishes Pass 2 and **before** the report is handed to the user. It has two phases:
1. **Mechanical polish** — run `finalize_pbir.py` (deterministic fixes)
2. **Design QA** — run `design_quality_check.py` (lint) + human review against Design Spec

---

## Phase 1 — Mechanical polish

Run `python scripts/finalize_pbir.py --report <path-to-.Report>` with these sub-modules (all on by default):

| Sub-module | What it fixes |
|---|---|
| `snap_grid` | Rounds every x/y/width/height to the 8px grid |
| `align_kpi_row` | Detects card visuals in a horizontal band, equalizes top + height, snaps gutters |
| `apply_theme_tokens` | Replaces any literal `#RRGGBB` hex in visual.json with the matching theme token |
| `normalize_fonts` | Enforces the Segoe UI family + size scale from `shared-standards.md` §4 |
| `ensure_alt_text` | Where alt text is missing, derives it from visual title + role |

**Run order matters** — `snap_grid` must precede `align_kpi_row`. The script enforces this.

**What Polisher does NOT do mechanically:**
- Does not change visual types or bindings
- Does not invent measures
- Does not modify the model or DAX

If a mechanical fix would alter semantics (e.g., a deliberately off-grid visual), the script logs a warning rather than forcing the change.

---

## Phase 2 — Design QA (automated lint)

Run `python scripts/design_quality_check.py --report <path-to-.Report>`. The linter surfaces:

| Level | Examples | Polisher response |
|---|---|---|
| **Error** (blocks sign-off) | Contrast < 4.5:1; missing drillthrough back button; dead bookmark reference; hard-coded hex after theme pass | Fix before continuing |
| **Warning** (must acknowledge) | Page has > 8 visuals in Analytical style; pie > 5 slices; default page name "Page 1"; title contains "Sum of" | Fix OR document exception in Design Spec §11 |
| **Info** | Data label off on a chart with room for labels; tooltip page absent on a dense chart | Discretionary |

The script writes `design_report.md` in the report root — attach this to the handoff to the user.

---

## Phase 3 — Design Spec reconciliation

The linter can't catch everything. Polisher must manually verify:

- [ ] Every page in Design Spec §4 exists with the right slug
- [ ] Every visual in Design Spec §5 exists at the right position with the right binding
- [ ] Theme file (§6) is applied at report level
- [ ] Navigation (§8) is wired — click every button, verify target page exists
- [ ] Mobile layouts (§9) exist for pages flagged "Yes"
- [ ] Backlog (§11) items are captured in the agent's Open Questions handoff

Discrepancies go to Phase 4a for Design Spec revision, not to the user as-is.

---

## Phase 4 — Evidence-building

Polisher prepares the handoff package:

1. **Screenshots** — render each page (via Power BI Desktop or headless render); capture to `evidence/screenshots/`
2. **design_report.md** — from the linter
3. **design_spec_final.md** — copy of Design Spec with ☑ on all Seven Confirmations and §11 updated
4. **open_questions.md** — anything still ambiguous for the user

---

## When to return to an earlier phase

| Condition | Route to |
|---|---|
| Linter flags an **error** that requires re-design (e.g., chart type fundamentally wrong) | Phase 4a (Strategist) |
| Linter flags an error in generation only (e.g., hard-coded hex not removed) | Phase 4b (Executor) — re-run Pass 2 fix |
| User reviewed screenshots and requested a change | Phase 5 (Feedback) |
| All errors resolved, warnings acknowledged | Hand off to user with evidence package |

---

## Anti-patterns

- ❌ Running `finalize_pbir.py` before the Executor's Pass 2 is complete (destroys in-progress narrative)
- ❌ Suppressing linter errors without documenting why
- ❌ Fixing an error by changing the Design Spec to match the generation (makes Spec a rationalization, not a contract)
- ❌ Skipping screenshot evidence — the user needs to see, not just read
- ❌ Handing off with un-triaged warnings — every warning is either fixed or explicitly acknowledged
