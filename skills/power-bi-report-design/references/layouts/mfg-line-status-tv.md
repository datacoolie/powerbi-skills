# Manufacturing Line Status (OEE) (TV Wall 1080p)

> **Derived layout** — TV-wall variant of [`mfg-line-status`](./mfg-line-status.md).

- Canvas: `1920×1080` (tv-wall-1080p)
- Visuals: 12
- Zones: `tv-headline, title-bar, oee-kpis-4, hourly-output, downtime-pareto, sparkline-row-3, work-orders-table, tv-alert-ticker`
- Use when: Always-on wall-mounted variant of `mfg-line-status`. Read-only, 1080p TV.
- Avoid when: Handheld / desktop use — TV variants use oversized type that looks wrong up close.

See the base recipe [`mfg-line-status.md`](./mfg-line-status.md) for the full narrative. This variant inherits intent and data requirements; it differs only in canvas, zone stacking, and visual density. Recommended themes, interaction model, and data requirements are documented in `layouts-index.json` under `id: mfg-line-status-tv`.
