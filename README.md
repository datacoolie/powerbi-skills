# Power BI Skills — Install Guide

A VS Code Copilot agent for end-to-end Power BI development.

Unlike single-file agents you copy into `.github/agents/`, this one is **multi-file**: it ships an agent file **plus** eight companion skill folders that the agent loads on demand.

---

## What's in This Repo

```
powerbi-skills/
├── AGENTS.md                            ← the agent file (multi-platform)
└── skills/                              ← 8 skill folders the agent uses
    ├── power-bi-business-analysis/
    ├── power-bi-semantic-model/
    ├── power-bi-dax-development/
    ├── power-bi-report-design/
    ├── power-bi-report-authoring/
    ├── power-bi-management/
    ├── power-bi-performance-troubleshooting/
    └── power-bi-feedback-iteration/
```

Each `skills/<name>/` folder contains a `SKILL.md` plus its own `references/`, `assets/`, or `scripts/`.

---

## Install

You have three options.

### Option A — One-line install (recommended)

Use the `skills` CLI to install directly into your workspace:

```bash
npx skills add datacoolie/powerbi-skills
```

Or use `curl` to fetch just the agent file:

```bash
curl -o AGENTS.md https://raw.githubusercontent.com/datacoolie/powerbi-skills/main/AGENTS.md
```

### Option B — Use this repo as your workspace

Just clone and open. No copying needed.

```bash
git clone https://github.com/datacoolie/powerbi-skills.git powerbi-skills
code powerbi-skills
```

VS Code auto-discovers `agents/*.agent.md` and `skills/*/SKILL.md` from the workspace root.

### Option C — Install into your own workspace

Copy two folders into your project:

| Copy from this repo | Paste into your workspace |
|---|---|
| `AGENTS.md` | `AGENTS.md` (repo root) |
| Each folder under `skills/power-bi-*/` | `.agents/skills/<same-folder-name>/` |

So after copying, your workspace looks like:

```
your-project/
├── AGENTS.md
└── .agents/
    └── skills/
        ├── power-bi-business-analysis/
        ├── power-bi-semantic-model/
        ├── power-bi-dax-development/
        ├── power-bi-report-design/
        ├── power-bi-report-authoring/
        ├── power-bi-management/
        ├── power-bi-performance-troubleshooting/
        └── power-bi-feedback-iteration/
```

> **Important:** Copy the **whole skill folder** (including `references/`, `assets/`, `scripts/`), not just `SKILL.md`. The agent reads files inside those folders.
>
> **Install the skills as a set.** The skills cross-reference each other with relative paths (for example `../../power-bi-management/references/…` from planning, `../power-bi-report-authoring/references/…` from design). Copy every `skills/power-bi-*` folder side by side; a partial install leaves those links dangling.

---

## What VS Code Actually Loads (vs. Reference Files)

Only **two file types** are auto-discovered by VS Code Copilot. Everything else is pulled in on demand by the agent or a skill.

| File | Auto-loaded? | Who reads it |
|---|---|---|
| `AGENTS.md` | Yes | VS Code Copilot, Claude Code, Cursor, Windsurf, and other AI tools |
| `skills/<name>/SKILL.md` | Yes (listed) | Agent reads it when the skill applies |
| `skills/<name>/references/*.md` | No | Agent reads only when `SKILL.md` points to a specific file |
| `skills/<name>/scripts/*.py` | No | Agent runs them via terminal (e.g. Phase 4c QA) |
| `skills/<name>/assets/*` | No | Agent shows them to you (e.g. layout preview SVGs) |

So although VS Code only "sees" `SKILL.md`, that file uses relative paths like `references/strategist.md` and `scripts/pbir_gate.py`. If you copy only `SKILL.md`, those paths break — that's why you copy the **entire folder**.

---

## Verify

1. Open the workspace in VS Code
2. Open Copilot Chat (Ctrl+Shift+I)
3. Switch to **Agent** mode (dropdown at the top of the chat panel)
4. **Power BI Developer** should appear in the agent picker

If it doesn't show up, restart VS Code.

---

## CLIs and MCP Servers — CLI first

**Policy: if a CLI and an MCP tool can both do the job, the agent uses the CLI.** MCP is used only where no CLI exists.

### CLIs (preferred)

| CLI | Install | What the agent uses it for |
|---|---|---|
| `powerbi-report-author` (Node ≥ 20) | `npm install -g @microsoft/powerbi-report-authoring-cli@latest` | Official Microsoft PBIR toolkit: `scaffold`, `catalog`, `formatting`, `expr`, `theme`, `text`, `validate`, `preview --host desktop\|service` (reload + screenshots; bundles the Desktop bridge), `preview-*`, `pack`/`unpack`. Verify with `powerbi-report-author doctor`. |
| `az` (Azure CLI) | [install](https://learn.microsoft.com/cli/azure/install-azure-cli), then `az login` | Fabric REST (`az rest`): report CRUD, definition download/upload, rebind, publish, workspace/item discovery. Calls carry the mandatory `x-ms-fabric-skill: powerbi-report-cli` header (opt out: `POWERBI_SKILLS_TELEMETRY=off`). |
| `fab` (Microsoft Fabric CLI, optional) | `pip install ms-fabric-cli`, then `fab auth login` | OneLake/lakehouse discovery for modeling (`fab find`, `fab dir`, `fab get`, `fab table schema`) and `fab api` (pass `-H "x-ms-fabric-skill=powerbi-report-cli"`). Preferred over `Fabric-MCP-*` / `fabric-notebook-mcp` when installed. |
| `python` ≥ 3.10 | — | Phase 4c QA scripts, `power_bi_management.py` helper |

### MCP servers (only where there is no CLI equivalent)

| Server | What it does | Required? |
|---|---|---|
| `powerbi-modeling-mcp` (also seen as `powerbi-authoring-local` — same tool set: `measure_operations`, `dax_query_operations`, `table_operations`, …) | Live semantic-model authoring + DAX execution (no CLI equivalent) | Required for Phase 2–3 |
| `microsoft-learn-mcp` | Looks up official Microsoft docs (no CLI equivalent) | Strongly recommended |
| `fabric-notebook-mcp` | Lakehouse/notebook inspection — **fallback** when `fab` is not installed | Optional |
| `fabric-mcp` | **Fallback only** — Fabric operations the CLI path doesn't cover; report/item operations use `az rest` instead | Optional |

Example `.vscode/mcp.json`:

```jsonc
{
  "servers": {
    "powerbi-modeling-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "<package-name-for-the-server>"]
    }
  }
}
```

Replace `<package-name-for-the-server>` with the actual MCP server package name from its repository. Without the modeling MCP the agent still runs but falls back to editing TMDL files directly.

### Official Microsoft skill coverage

`power-bi-report-authoring`, `power-bi-report-design`, `power-bi-management`, and the planning flow in `power-bi-business-analysis` mirror the four modes of Microsoft's [`powerbi-report-cli`](https://github.com/microsoft/skills-for-fabric) skill (v1.0.5 / `apm` 0.2.9, MIT; CLI `@microsoft/powerbi-report-authoring-cli` 0.5.0) verbatim — all 86 reference files — with repo-specific pipeline layers on top. On conflict, the official file wins.

| Official mode | This repo | Official files |
|---|---|---|
| `planning` | `power-bi-business-analysis` | `references/planning.md`, `planning-part-02.md` |
| `design` | `power-bi-report-design` | `references/design.md`, `references/design/**` |
| `authoring` | `power-bi-report-authoring` | `references/authoring.md`, `authoring-part-02/03/04.md`, `references/authoring/**` |
| `management` | `power-bi-management` | `references/management.md`, `management-part-02/03/04.md` (+ `fabric-common-cli.md`) |

The semantic-model side mirrors Microsoft's `semantic-model-authoring` skill the same way (`power-bi-semantic-model/references/official-workflows.md` + the official modeling/TMDL/metadata/field-parameter/Direct Lake guidelines).

---

## Use It

In Copilot Chat (Agent mode → Power BI Developer), describe what you want:

```
I need a sales analytics report for our retail division.
We track revenue, units sold, and stock-out rates across 5 stores.
Audience is the Operations Manager who reviews numbers daily.
```

The agent will walk you through 9 phases: Requirements → Model → DAX → Design → Build → Polish → Feedback → Release.

You can also jump in mid-pipeline:

| Say this | Agent starts at |
|---|---|
| *"Help me write DAX measures for this model"* | Phase 3 |
| *"Design a report for this dataset"* | Phase 4a — agent first checks the model has every measure the report needs (Measures Gate); missing ones are created in Phase 3 before design starts |
| *"Validate this PBIP report"* | Phase 4c (runs the QA scripts) |
| *"My report is slow"* | Performance troubleshooting skill |

---

## Optional: QA Scripts

The `power-bi-report-authoring` skill ships Python scripts you can run standalone:

```bash
# QA pass on a .Report folder — read-only by default (lint → validate → layout drift)
python skills/power-bi-report-authoring/scripts/pbir_gate.py \
  --report path/to/MyReport.Report \
  --style analytical
# add --apply to let the polish stage rewrite a report you just generated
# (refused on a dirty git tree unless --force-apply; backed up first outside git)

# Generate a page from a layout recipe + slot spec (FHD slots, roles checked against the CLI catalog)
python skills/power-bi-report-authoring/scripts/build_report_from_layout.py \
  --report path/to/MyReport.Report \
  --spec skills/power-bi-report-authoring/references/layout-spec-example.json

# Is the built report still what was approved?
python skills/power-bi-report-authoring/scripts/check_layout_drift.py --report path/to/MyReport.Report

# Rescale a recipe to another 16:9 canvas / validate a recipe's slot table
python skills/power-bi-report-design/scripts/rescale_layout.py --layout exec-overview-16x9 --canvas 1280x720 --format md
python skills/power-bi-report-design/scripts/rescale_layout.py --canvas 1920x1080 --check skills/power-bi-report-design/references/layouts/exec-overview-16x9.md
```

Requires Python 3.10+. Install `jsonschema` for full schema validation:

```bash
pip install jsonschema
```

## Tests

CI (`.github/workflows/skill-tests.yml`) runs the skill script tests on every push/PR.
Script unit tests live in `skills/**/scripts/tests/` and are tracked in git.

---

## Troubleshooting

**Agent doesn't appear in Copilot Chat.** Make sure you're in **Agent** mode (not Ask or Edit). Check that `AGENTS.md` is at the repo root. Restart VS Code.

**Agent says "skill not found".** You only copied `SKILL.md` and forgot the rest of the folder. Recopy the entire `skills/<name>/` folder including `references/`.

**MCP tool errors.** Check `.vscode/mcp.json` is configured and restart VS Code. The agent will continue with reduced capabilities if a server is missing.

**`powerbi-report-author` not found / preview unavailable.** Run `npm install -g @microsoft/powerbi-report-authoring-cli@latest`, then `powerbi-report-author doctor` and `powerbi-report-author preview --list-hosts`. Desktop preview needs Power BI Desktop with *Enable external tool access to Power BI Desktop through secure local APIs* turned on (Options → Preview features) and the report opened from its `.pbip`.

---

## What Each Skill Does

| Skill | Purpose | Triggers when you say |
|---|---|---|
| `power-bi-business-analysis` | Phase 1: requirements interview, KPI selection, official report planning (`_brief/report-spec.md` + approval gate) | "analyze requirements", "what KPIs", "create a report", "plan then build" |
| `power-bi-semantic-model` | Phase 2: star schema, storage modes, RLS, naming conventions, DAX standards, AI/Copilot readiness, REST API | "build the model", "star schema", "DirectLake", "naming conventions", "prepare for Copilot" |
| `power-bi-dax-development` | Phase 3: DAX measures, time intelligence | "write a measure", "CALCULATE", "YTD" |
| `power-bi-report-design` | Phase 4a: archetypes, tone/signature, layouts, charts, themes, Design Spec + `Design Brief:` | "design a report", "choose chart types", "redesign" |
| `power-bi-report-authoring` | Phase 4b/4c: scaffold/edit PBIR, validate, preview + screenshots (CLI), lint | "build the report", "validate this PBIP", "preview/screenshot" |
| `power-bi-management` | Phase 6: publish/download/list/update/delete/rebind reports in Fabric (CLI-first: `az rest` + `pack`/`unpack`) | "publish to Fabric", "deploy this report", "download report definition" |
| `power-bi-performance-troubleshooting` | Cross-cutting: diagnose slow reports | "report is slow", "query timeout" |
| `power-bi-feedback-iteration` | Phase 5/6: classify feedback, UAT, changelog | "user feedback", "release notes" |
