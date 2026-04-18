# Power BI Skills — Install Guide

A VS Code Copilot agent for end-to-end Power BI development.

Unlike single-file agents you copy into `.github/agents/`, this one is **multi-file**: it ships an agent file **plus** seven companion skill folders that the agent loads on demand.

---

## What's in This Repo

```
powerbi-skills/
├── agents/
│   └── power-bi-developer.agent.md     ← the agent file
└── skills/                              ← 7 skill folders the agent uses
    ├── power-bi-business-analysis/
    ├── power-bi-semantic-model/
    ├── power-bi-dax-development/
    ├── power-bi-report-design/
    ├── power-bi-pbip-report/
    ├── power-bi-performance-troubleshooting/
    └── power-bi-feedback-iteration/
```

Each `skills/<name>/` folder contains a `SKILL.md` plus its own `references/`, `assets/`, or `scripts/`.

---

## Install

You have two options.

### Option A — Use this repo as your workspace (easiest)

Just clone and open. No copying needed.

```bash
git clone <this-repo-url> powerbi-skills
code powerbi-skills
```

VS Code auto-discovers `agents/*.agent.md` and `skills/*/SKILL.md` from the workspace root.

### Option B — Install into your own workspace

Copy two folders into your project:

| Copy from this repo | Paste into your workspace |
|---|---|
| `agents/power-bi-developer.agent.md` | `.github/agents/power-bi-developer.agent.md` |
| Each folder under `skills/power-bi-*/` | `.agents/skills/<same-folder-name>/` |

So after copying, your workspace looks like:

```
your-project/
├── .github/
│   └── agents/
│       └── power-bi-developer.agent.md
└── .agents/
    └── skills/
        ├── power-bi-business-analysis/
        ├── power-bi-semantic-model/
        ├── power-bi-dax-development/
        ├── power-bi-report-design/
        ├── power-bi-pbip-report/
        ├── power-bi-performance-troubleshooting/
        └── power-bi-feedback-iteration/
```

> **Important:** Copy the **whole skill folder** (including `references/`, `assets/`, `scripts/`), not just `SKILL.md`. The agent reads files inside those folders.

---

## What VS Code Actually Loads (vs. Reference Files)

Only **two file types** are auto-discovered by VS Code Copilot. Everything else is pulled in on demand by the agent or a skill.

| File | Auto-loaded? | Who reads it |
|---|---|---|
| `agents/*.agent.md` | Yes | VS Code, when you pick the agent in chat |
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

## MCP Servers (Optional but Recommended)

The agent works best with these MCP servers configured in `.vscode/mcp.json`:

| Server | What it does | Required? |
|---|---|---|
| `microsoft-learn-mcp` | Looks up official Microsoft docs | Strongly recommended |
| `powerbi-modeling-mcp` | Creates tables, measures, RLS in semantic models | Required for Phase 2–3 |
| `fabric-mcp` | Publishes to Microsoft Fabric workspaces | Optional |
| `fabric-notebook-mcp` | Fabric notebook operations | Optional |

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

Replace `<package-name-for-the-server>` with the actual MCP server package name from its repository. Without these servers the agent still runs but skips the model-build steps.

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
| *"Design a report for this dataset"* | Phase 4a |
| *"Validate this PBIP report"* | Phase 4c (runs the QA scripts) |
| *"My report is slow"* | Performance troubleshooting skill |

---

## Optional: QA Scripts

The `power-bi-pbip-report` skill ships Python scripts you can run standalone:

```bash
# Full QA pass on a .Report folder (finalize → lint → validate)
python skills/power-bi-pbip-report/scripts/pbir_gate.py \
  --report path/to/MyReport.Report \
  --style analytical
```

Requires Python 3.10+. Install `jsonschema` for full schema validation:

```bash
pip install jsonschema
```

---

## Troubleshooting

**Agent doesn't appear in Copilot Chat.** Make sure you're in **Agent** mode (not Ask or Edit). Check that the agent file is at `.github/agents/power-bi-developer.agent.md` (Option B) or `agents/power-bi-developer.agent.md` (Option A). Restart VS Code.

**Agent says "skill not found".** You only copied `SKILL.md` and forgot the rest of the folder. Recopy the entire `skills/<name>/` folder including `references/`.

**MCP tool errors.** Check `.vscode/mcp.json` is configured and restart VS Code. The agent will continue with reduced capabilities if a server is missing.

---

## What Each Skill Does

| Skill | Purpose | Triggers when you say |
|---|---|---|
| `power-bi-business-analysis` | Phase 1: requirements interview, KPI selection | "analyze requirements", "what KPIs" |
| `power-bi-semantic-model` | Phase 2: star schema, storage modes, RLS | "build the model", "star schema", "DirectLake" |
| `power-bi-dax-development` | Phase 3: DAX measures, time intelligence | "write a measure", "CALCULATE", "YTD" |
| `power-bi-report-design` | Phase 4a: layouts, charts, themes, design spec | "design a report", "choose chart types" |
| `power-bi-pbip-report` | Phase 4b/4c: generate PBIR JSON, lint, validate | "build the report", "validate this PBIP" |
| `power-bi-performance-troubleshooting` | Cross-cutting: diagnose slow reports | "report is slow", "query timeout" |
| `power-bi-feedback-iteration` | Phase 5/6: classify feedback, UAT, changelog | "user feedback", "release notes" |
