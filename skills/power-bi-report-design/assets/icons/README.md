# Icons

SVG icon library. Grouped into sets so Strategist can bind an **icon family**
(Seven Confirmations item #6 "Iconography") rather than picking icons one at a
time.

## Sets

| Folder | Style | License | Source |
|---|---|---|---|
| `tabler-outline/` | 24×24, 2 px stroke, rounded caps | MIT | [tabler/tabler-icons](https://github.com/tabler/tabler-icons) |
| `tabler-filled/` | 24×24, solid fills | MIT | [tabler/tabler-icons](https://github.com/tabler/tabler-icons) |
| `lucide/` | 24×24, 2 px stroke, square caps | ISC | [lucide-icons/lucide](https://github.com/lucide-icons/lucide) |
| `duotone/` | 24×24, filled backplate + outline glyph | MIT | Custom — two-tone for KPI tile leading marks |
| `custom/` | Project-specific marks | See per-file header | — |

**Theme color:** every SVG must use `stroke="currentColor"` / `fill="currentColor"`.
Power BI injects the theme accent via the format pane, so the same SVG works on
light and dark backgrounds.

## Usage in PBIR

1. Upload selected icon as an Image visual or embed inline in a Shape / Advance
   Card via base64 in `visual.json`.
2. Reference the icon's `id` in Design Spec §5 (Visual Inventory) as
   `icon: <set>/<id>`, e.g. `icon: tabler-outline/trending-up`.
3. Accessibility — the alt text for any icon-only visual must describe the
   *meaning*, not the shape (W10 lint rule).

## Provenance

Four sets, totalling 204 icons across 10 categories:

| Set | Count | Style | License |
|---|---|---|---|
| `tabler-outline/` | 74 | outline, 2 px stroke, rounded caps | MIT |
| `tabler-filled/`  | 46 | solid fills | MIT |
| `lucide/`         | 64 | outline, 2 px stroke, rounded joins | ISC |
| `duotone/`        | 20 | backplate + glyph, two-tone | MIT |

Categories: `kpi-delta`, `chart`, `finance`, `status`, `navigation`, `action`,
`domain`, `geo`, `data`, `comms`. The first three sets overlap on common
meanings (e.g. `trending-up`, `target`, `users`) so a Strategist can pin **one**
set per report. `duotone/` is meant as leading marks on KPI tiles and section
headers — use it alongside an outline/filled set rather than instead of one.
To add more icons, drop the SVG into the set folder and append an entry to
`icons-index.json`.

## Index

[`icons-index.json`](icons-index.json) is the authoritative manifest. It validates
against [`icons-index.schema.json`](icons-index.schema.json). CI (and the
`pbir_gate.py` wrapper's upcoming asset check) will flag drift between the files
on disk and the index.

## Categories at a glance

| Category | Typical icons | Use |
|---|---|---|
| `kpi-delta` | `trending-up`, `trending-down`, `arrow-up`, `arrow-down`, `target` | KPI variance chips |
| `chart` | `chart-bar`, `chart-line`, `chart-pie`, `chart-donut`, `chart-funnel`, `sparkline`, `gauge` | Section / visual titles |
| `finance` | `coin`, `currency-dollar`, `euro`, `credit-card`, `receipt`, `percent` | Finance & FP&A pages |
| `status` | `check`, `circle-check`, `alert-triangle`, `info-circle`, `bell`, `clock`, `shield-check` | Status pills, alerts, SLA markers |
| `navigation` | `home`, `menu`, `arrow-left/right`, `external-link`, `list` | App-bar / sidebar / breadcrumbs |
| `action` | `edit`, `copy`, `trash`, `plus`, `minus`, `download`, `share`, `refresh`, `settings`, `search`, `filter`, `eye` | Toolbars & quick-actions |
| `domain` | `building`, `briefcase`, `truck`, `package`, `users`, `user` | Domain / entity headers |
| `geo` | `map`, `map-pin`, `globe` | Territory / geography pages |
| `data` | `database`, `cloud`, `folder` | Data-source chips, lineage notes |
| `comms` | `mail`, `phone`, `message` | Contact / comms panels |

## Adding icons

1. Drop a 24×24 SVG into the right set folder. Use `currentColor` for all
   strokes/fills; no hard-coded colors.
2. Append an entry to `icons-index.json` with `id`, `file`, `keywords`, and
   `category` (one of the 10 above). Schema-validate the index.
3. Keep IDs consistent across sets where possible so a Strategist can swap sets
   without remapping ids (e.g. `trending-up` exists in outline, filled, lucide,
   and duotone).
