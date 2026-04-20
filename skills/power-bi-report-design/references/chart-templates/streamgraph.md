# Recipe: Streamgraph (Deneb sibling)

> **Preview:** [![streamgraph preview](../../assets/chart-previews/streamgraph.svg)](../../assets/chart-previews/streamgraph.svg)

- **id:** `streamgraph`
- **Visual type:** `Deneb6E97C82C58E5467CA7C3188B3E36ADE7` ★
- **Parent recipe:** [`deneb-custom.md`](deneb-custom.md)
- **Typical size:** 824 × 320

---

## Composition

```
┌────────────────────────────────────────┐
│        ╲╲╲╲                             │
│      ╱╱╱╲╲╲╲╲  ╲╲╲╲                     │
│     ╱╱╱╱╱╲╲╲╲╲╲╲╲╲╲╲╲                   │
│ ═══════════════════════════ (center axis)│
│     ╲╲╲╲╲╲╲╱╱╱╱╱╱╱╱╱╱                   │
│      ╲╲╲╱╱╱╱╱╱╱                         │
│        ╱╱╱╱                             │
│  2020   2021   2022   2023   2024        │
└────────────────────────────────────────┘
```

Stacked area centered on a symmetrical axis. Emphasizes proportional change
over time across categories.

---

## Slots

| Role | Binding example |
|---|---|
| X (time) | `DimDate[Month]` |
| Y (value) | `[Volume]` |
| Color (category) | `DimProduct[Category]` |

---

## Vega-Lite mark

```json
{ "mark": { "type": "area" }, "encoding": { "y": { "stack": "center" } } }
```

Inherits scaffold from [`deneb-custom.md`](deneb-custom.md).

## Do-NOT list

- ❌ Using for precise value comparison (no shared baseline)
- ❌ > 7 categories (becomes noisy)
- ❌ Mixing positive and negative values
