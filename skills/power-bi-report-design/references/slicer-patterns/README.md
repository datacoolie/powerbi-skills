# Slicer & Filter Pattern Recipes

Composition recipes for slicers, filter architectures, governance filters, and
parameter-driven controls. Each recipe has an ASCII mockup, slot bindings, a
property snippet, sensible defaults, and anti-patterns.

**Use this folder together with** [`../slicer-filter-patterns.md`](../slicer-filter-patterns.md):

| Artifact | Role |
|---|---|
| `../slicer-filter-patterns.md` | **Decision guide** — tells you *which* recipe to pick (scope, cardinality, RLS, pane visibility) |
| `slicer-patterns-index.json` | **Catalog** — machine-readable list of recipes with `family`, `cardinality`, `archetypes` filters |
| `*.md` recipe files | **Cookbook** — composition, bindings, property snippet, defaults, anti-patterns for one recipe |

---

## Recipe index

### Date (continuous)
| Recipe | When to use |
|---|---|
| [date-relative-rolling](date-relative-rolling.md) | Regularly-reviewed reports — auto-advances |
| [date-between-slider](date-between-slider.md) | Retrospective / investigation — absolute range |

### Category
| Recipe | Cardinality | When to use |
|---|---|---|
| [chiclet-tile-slicer](chiclet-tile-slicer.md) | 3–7 | Always-visible primary dimension |
| [dropdown-search-slicer](dropdown-search-slicer.md) | 8–25 | Secondary filter with typeahead |
| [hierarchy-slicer](hierarchy-slicer.md) | Nested | Year→Qtr→Month, Region→Country→City |
| [search-box-high-card](search-box-high-card.md) | > 10 000 | Customer / SKU / Invoice lookup |

### Numeric
| Recipe | When to use |
|---|---|
| [numeric-range-slicer](numeric-range-slicer.md) | Bounding a numeric measure (order value, age, tenure) |

### Architecture (composition of multiple slicers)
| Recipe | When to use |
|---|---|
| [left-rail-global-panel](left-rail-global-panel.md) | 3–5 slicers, wide desktop, analyst audience |
| [top-header-filter-bar](top-header-filter-bar.md) | 2–4 slicers, executive / operational pages |
| [sync-slicer-group](sync-slicer-group.md) | Narrative continuity across Analysis pages |

### Governance
| Recipe | When to use |
|---|---|
| [hidden-applied-filter](hidden-applied-filter.md) | Data hygiene, locked period, pre-scoping |
| [role-based-bookmark](role-based-bookmark.md) | 2–4 canned view switches (My / All) |

### Parameter
| Recipe | When to use |
|---|---|
| [field-parameter-switch](field-parameter-switch.md) | Swap measure or dimension on one chart |
| [what-if-parameter](what-if-parameter.md) | Scenario input (discount %, FX, volume lift) |
| [chart-type-toggle](chart-type-toggle.md) | Swap the visualization type on one visual (Bar/Line/Table) — other visuals unchanged |

---

## Archetype × recipe matrix

Pick recipes that match your report archetype(s):

| Recipe | Executive | Analytical | Operational | Exploration | Mobile | TV-wall |
|---|---|---|---|---|---|---|
| chiclet-tile-slicer           | ● | ● | ● |   | ● | ● |
| dropdown-search-slicer        | ○ | ● |   | ● |   |   |
| hierarchy-slicer              |   | ● |   | ● |   |   |
| date-between-slider           |   | ● |   | ● |   |   |
| date-relative-rolling         | ● | ● | ● |   | ● | ● |
| numeric-range-slicer          |   | ● |   | ● |   |   |
| search-box-high-card          |   | ● | ● | ● |   |   |
| left-rail-global-panel        |   | ● |   | ● |   |   |
| top-header-filter-bar         | ● |   | ● |   | ● | ● |
| sync-slicer-group             | ● | ● |   | ● |   |   |
| hidden-applied-filter         | ● | ● | ● |   |   |   |
| role-based-bookmark           | ● | ● |   |   |   |   |
| field-parameter-switch        |   | ● |   | ● |   |   |
| what-if-parameter             |   | ● |   | ● |   |   |
| chart-type-toggle             |   | ● |   | ● |   |   |

● = strong fit   ○ = acceptable   blank = avoid

---

## Picking a recipe — 4-step drill

1. **Scope** (from `../slicer-filter-patterns.md` §1): report / sync-group / page / visual?
2. **Control type** (§2): date, category (by cardinality), numeric, search?
3. **Composition**: single slicer, or an architecture recipe (`left-rail-global-panel`, `top-header-filter-bar`)?
4. **Governance overlay** (§7, §8): add `hidden-applied-filter`, `role-based-bookmark`, or a parameter recipe as needed.

Then open the matching recipe `.md` file and drop its composition + property snippet into the Design Spec §10.
