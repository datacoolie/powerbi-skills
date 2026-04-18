# Source Material & Attribution

Reference books and official documentation that inform the skill content.
The ebooks themselves live in `references-ebook/` (gitignored, not distributed).

## Book → Skill Mapping

| Source | Skills Informed | Key Concepts Used |
|---|---|---|
| **The Definitive Guide to DAX** (2nd ed.) — Ferrari & Russo | `power-bi-dax-development` | Evaluation contexts, CALCULATE semantics, context transition, filter propagation, row context |
| **Optimizing DAX** — Russo & Ferrari | `power-bi-dax-development`, `power-bi-performance-troubleshooting` | Storage engine vs formula engine, query plans, VertiPaq internals, CALCULATE optimization, iterator optimization |
| **Data Visualization** (2nd ed.) — Andy Kirk | `power-bi-report-design` | 5-layer design process, chart taxonomy, pre-attentive attributes, color theory, annotation |
| **Storytelling with Data** — Cole Nussbaumer Knaflic | `power-bi-report-design`, `power-bi-business-analysis` | WHO/WHAT/HOW framework, Big Idea, SCQA narrative, chart selection (SWD decision tree), declutter |
| **Storytelling with Data: Let's Practice!** — Knaflic & Madsen | `power-bi-report-design` | Applied exercises for chart makeovers, narrative construction, audience-driven design |
| **Power BI Create Reports** — Microsoft | `power-bi-pbip-report`, `power-bi-report-design` | PBIR format, visual JSON structure, theme schema, report definition patterns |

## Official Documentation

All skills are expected to cross-check against current Microsoft Learn docs
via the `microsoft-learn-mcp` tools (`microsoft_docs_search`,
`microsoft_docs_fetch`) before recommending patterns. This ensures guidance
stays current even if the reference books predate the latest Power BI release.

## Legacy Files

The `references-md/` folder (gitignored) previously contained 8 generic
agent/skill drafts that were superseded when the skill-based architecture was
adopted. Their content has been integrated into the current 7 skills:

| Legacy File | Superseded By |
|---|---|
| `agent.power-bi-data-modeling-expert.md` | `power-bi-semantic-model` skill |
| `agent.power-bi-dax-expert.md` | `power-bi-dax-development` skill |
| `agent.power-bi-performance-expert.md` | `power-bi-performance-troubleshooting` skill |
| `agent.power-bi-visualization-expert.md` | `power-bi-report-design` skill |
| `skill.power-bi-dax-optimization.md` | `power-bi-dax-development/references/optimization-guide.md` |
| `skill.power-bi-model-design-review.md` | `power-bi-semantic-model/references/star-schema-checklist.md` |
| `skill.power-bi-performance-troubleshooting.md` | `power-bi-performance-troubleshooting` skill (full rewrite) |
| `skill.power-bi-report-design-consultation.md` | `power-bi-report-design` skill (full rewrite) |
