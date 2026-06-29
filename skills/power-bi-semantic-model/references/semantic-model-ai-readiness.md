# Semantic Model AI Readiness Guidelines

This document describes the guidelines that should be applied when preparing a Power BI semantic model for conversational BI experiences in Microsoft Fabric (Copilot for Power BI, Data Agents, and other natural-language consumers).

## Consumption Mode Decides the Investment

Ask the user which consumption methods are planned before scoping the readiness review.

| Consumption                         | Required Model Investment                                                                                             |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Reports or Ad-hoc model exploration | Standard star schema, explicit measures (see [modeling-guidelines.md](./modeling-guidelines.md)).                     |
| Conversational BI / Copilot         | All of the above PLUS: business-friendly naming, synonyms, descriptions optimized for AI, AI instructions, AI schema. |
| Both                                | Full investment in both report design and Copilot readiness.                                                          |

## Core Principles

- **Foundation first** - A weak model cannot be rescued by AI instructions. Star schema, explicit measures, and correct data types are prerequisites, not optional polish.
- **Literal interpretation** - Copilot reads names and descriptions literally. `AMT` is not the same as `Sales Amount` to a language model.
- **Explicit over implicit** - Implicit measures, extension measures defined in reports, and hidden business logic are invisible to AI. If it must be reachable by natural language, it must live in the model as an explicit measure with metadata.
- **Iterate from observation** - Write descriptions and AI instructions based on real user prompts and Copilot answers. Do not guess.

## Editing Capability

The agent's ability to *apply* a Copilot readiness item depends on (a) whether the item lives in TOM model metadata or in PBIP-only artifacts, and (b) where the model lives. 

| Semantic Model Objects                                                                                   | Editing path                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TOM metadata** - names, descriptions, relationships, measures, hidden flags, data types, summarization | **Prioritize MCP** (any source).                                                                                                                                                                                       |
| **Everything else** - synonyms, AI instructions, AI Data Schema selection, Verified Answers              | **Edit PBIP files** under `<Name>.SemanticModel/Copilot/`. Edit directly on a PBIP project, or via Fabric workspace `getDefinition`/`updateDefinition` round-trip. Not via MCP. PBIX files cannot be edited by Agents. Load [pbip.md](pbip.md) to understand the file structure. |

When presenting findings to the user, tag each item with its routing so the user knows which fixes the agent can apply and which require Desktop work.

**Important:** When incapable of editing any metadata, refer the user to [copilot-prepare-data-ai](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai) documentation.

## Readiness Checklist

Use this checklist as the structure for any Copilot readiness review. Each section is ordered: do not skip ahead - if section 1 fails, fixing section 4 will not help.

## 0. Gathering Business Context

Before writing descriptions or AI instructions, gather context. Do not assume.

1. Interview the user about the business process, key metrics, common questions, and known areas of ambiguity.
2. Review existing reports built on the model - the questions they answer reveal the questions Copilot will be asked.
3. Inspect existing measure names for patterns that imply business logic (`YTD`, `MTD`, `vs Plan`, `vs LY`).
4. Identify contentious metrics. Margins, budgets, and forecasts often have multiple competing definitions across teams - these are the highest-value targets for AI instructions.
5. Capture organizational vocabulary. Different departments may use different terms for the same concept; these become synonyms.

### 1. Model Architecture (Foundation)

Without this, Copilot will produce poor results regardless of any other configuration. Load [modeling-guidelines.md](./modeling-guidelines.md) for full rules; this section flags the items that matter most for Copilot.

**DO:**
- Apply a star schema with clear fact and dimension tables. Avoid flat, denormalized, or pivoted structures.
- Define correct `dataType` on all columns. Copilot derives summarization and filter behavior from the data type.
- Create explicit DAX measures for every key metric. Implicit aggregations are not reliably accessible to Copilot.
- Anticipate common questions: include predefined measures users are most likely to request (e.g., `YTD Sales`, `MoM Growth`, `ROI`, `CAC`, `LTV`). Copilot answers more reliably when the metric already exists as an explicit measure.
- Consolidate or clearly differentiate duplicate or overlapping measures.
- Define logical hierarchies on dimension tables to support drill-down (e.g., `Year > Quarter > Month > Day` on a date dimension; `Country > State > City` on a geography dimension).

**DON'T:**
- Leave unused columns or tables in the model - they pollute the schema Copilot sees and increase the chance of wrong field selection.

### 2. Model Naming

Business-friendly naming is one of the highest-impact changes for Copilot readiness. Load [naming-conventions.md](./naming-conventions.md) for the full rules.

**DO:**
- Use human-readable names on every visible table, column, and measure (e.g., `Transaction Amount`, not `TR_AMT` or `tr_amt`).
- Use the language Copilot will be queried in (typically English) for visible names, even if the source system uses another language.
- Set `summarizeBy` correctly on numeric columns - especially `None` for IDs, year, month number, postal codes, etc., to prevent accidental sums.
- Set the `isDefaultLabel` (or equivalent default field) on dimension tables so Copilot can identify the natural "name" column.

**DON'T:**
- Ship CamelCase, snake_case, UPPER_CASE, or technical abbreviations on visible objects.
- Rely on a single name when users naturally use several terms - add synonyms.

### 3. Descriptions

Descriptions provide context that names alone cannot convey. Descriptions written for AI consumers are different from descriptions written for human users.

**DO:**
- Add a `description` to every visible table, column, and measure.
- **Keep descriptions concise: only the first 200 characters are read by Copilot.** Front-load the most important information (preferred usage, disambiguation, units) at the start of the description.
- Make implicit knowledge explicit. Do not restate the field name.
- For Copilot-focused descriptions, prefer: preferred-usage guidance, disambiguation against similar fields, expected grain, and units.
- For Calculation Groups: calculation *items* are not surfaced as model metadata, so use the description of the calculation group **column** to enumerate items and how to use them (e.g., "Use with measures and date table for: Current, MTD, QTD, YTD, PY, YOY, YOY%"). Same 200-character limit applies.
- Where both audiences need guidance, put human-oriented detail in the `description` and Copilot-specific routing rules in [AI instructions](#4-ai-instructions).

**DON'T:**
- Generate descriptions purely from AI without business context. AI-only descriptions tend to restate what the model structure already shows. Always validate with the user or a domain expert.
- Contradict descriptions across related fields (the column description and the measure description should agree).

### 4. AI Instructions

AI instructions are freeform text that Copilot reads automatically. They are one of the most impactful controls for conversational BI quality.

> **Editing path:** PBIP-level artifact. See [Editing Capability](#editing-capability).

**DO:**
- Metric routing for ambiguous terms ("when users ask about margin, use `[Standard Margin]`").
- Business terminology and abbreviations tied to specific model objects (e.g., "TMS = Total Media Spend, use measure `[Total Media Spend]`").
- Time-period definitions (fiscal year start, busy season, reporting cadence).
- Disambiguation of date fields ("`Order Date` is the primary date; `Ship Date` is only for logistics analysis").
- Default groupings or analysis preferences ("always analyze sales on a quarterly basis").
- Prioritized tables for a question type ("for retail insights, prioritize the `CustomerSegmentation` and `SalesChannel` tables").
- Clarification-asking rules ("when a user asks about product sales, always ask for clarification on location").
- Polarity / direction-of-good ("a lower attrition % is positive").
- Guidance for Calculation Groups, DAX UDFs, or Field Parameters when present.
- Visualization preferences (which chart types to prefer or avoid).
- Keep instructions concise and non-contradictory with descriptions and with each other.
- Refer to fields by their proper, fully qualified names.

**DON'T:**
- Duplicate large blocks of business logic that already live in descriptions.
- Encode information that should instead be a measure, a synonym, or a relationship.
- Rely on instructions to enforce hard rules - the LLM may still ignore them. For non-negotiable behaviour, fix the model itself.
- Exceed 10.000 characters

### 5. AI Data Schema

The AI data schema controls which tables, columns, and measures are exposed to Copilot. It also defines synonyms for tables/columns/measures. Scoping this correctly prevents Copilot from getting confused by helper objects.

> **Editing path:** PBIP-level artifact. See [Editing Capability](#editing-capability).

**DO:**
- Include only tables, columns, and measures that a business user would meaningfully ask about.
- Include all dependent objects for selected measures (any column or measure referenced by a selected measure must also be visible to Copilot).
- Exclude helper measures, intermediate calculations, and technical bridge tables.
- Exclude duplicate or overlapping measures.
- Keep the AI schema selection consistent across "Prep for AI" and any Data Agent configuration that points to this model.
- Configure `synonyms` on tables, columns, and measures for alternative terms users employ (e.g., `Revenue`, `Sales`, `Turnover` for the same measure).
  
**DON'T:**
- Default to "expose everything" - it dilutes the signal Copilot uses to pick the right field.

### 6. Verified Answers

Verified Answers are pre-built report visuals that Copilot can return for specific questions. Detailed authoring of Verified Answers is out of scope for this skill (it requires report-layer work and live testing in Power BI), and the underlying TMDL/MCP surface does not expose Verified Answer content for editing.

> **Editing path:** Don't edit verified answers automatically. Instead suggest good candidates for verified answers and ask the user to configure manually in the tool. See [copilot-prepare-data-ai](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai-verified-answers) documentation.

**DO:**
- When reviewing a PBIP, check whether a Verified Answers definition exists in the project. Note its presence in the readiness summary.
- If absent and the user is interested, point them to the Power BI Desktop authoring experience - do not attempt to author Verified Answers from this skill.
- Inspect the model measures, based on the measure names, descriptions recommend the top five questions worth setting as verified answers

