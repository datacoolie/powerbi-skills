# Chart template recipes

Composition recipes for every chart visual supported by this skill. Each recipe
documents the visual's slots, formatting, narrative rules, anti-patterns, data
requirements, and a pre-flight checklist.

**Use this folder together with**
[`../visual-vocabulary.md`](../visual-vocabulary.md) (intent-first chart picker)
and [`../chart-selection-guide.md`](../chart-selection-guide.md) (editorial
decision tree).

| Artifact | Role |
|---|---|
| [`../visual-vocabulary.md`](../visual-vocabulary.md) | **Taxonomy** — map data relationship (Deviation, Correlation, Ranking, …) to chart |
| [`../chart-selection-guide.md`](../chart-selection-guide.md) | **Decision guide** — pick the right chart for the audience and intent |
| [`chart-templates-index.json`](chart-templates-index.json) | **Catalog** — machine-readable list of 62 recipes |
| [`chart-templates-index.schema.json`](chart-templates-index.schema.json) | JSON Schema for the catalog |
| `*.md` recipe files | **Cookbook** — 7-section template per recipe |
| [`../../assets/chart-previews/`](../../assets/chart-previews/) | **Visual previews** — 320×180 monochrome SVG silhouettes (one per recipe) |

---

## Recipe template (7 sections)

Every recipe file follows the same order so the Executor and Strategist can
navigate any file by memory:

1. **Composition** — ASCII sketch of the chart
2. **Slots** — table of roles → column/measure bindings
3. **Formatting** — theme tokens, axis, data labels, legend
4. **Narrative** — title/subtitle phrasing per style personality
5. **Do-NOT** — anti-patterns (3D, rainbow palette, dual axis, …)
6. **Data quality / gotchas** — cardinality, NULL handling, model dependencies
7. **Checklist** — pre-ship verification items

---

## Finding a recipe

- **By data relationship** → start in
  [`../visual-vocabulary.md`](../visual-vocabulary.md) §Category reference.
- **By visualType (PBIR)** → grep `chart-templates-index.json` for
  `"visualType"`.
- **By silhouette** → browse
  [`../../assets/chart-previews/`](../../assets/chart-previews/).

Uncharted recipes are tracked in `chart-templates-index.json`'s `gaps[]` array
— add a new file when closing one of those gaps.
