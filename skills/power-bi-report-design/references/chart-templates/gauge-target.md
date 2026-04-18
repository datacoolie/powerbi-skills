# Recipe: Gauge vs Target

- **id:** `gauge-target`
- **Visual type:** `gauge` (built-in) — preferred only for Operational style
- **Typical size:** 320 × 220

---

## Composition

```
              ╭────────────────╮
            ╱    ╱ ─────── ╲    ╲
          ╱   ╱     value    ╲    ╲
        ╱   ╱      82.3%      ╲    ╲         ← needle at current value
       ╱   │   ╔═══════════╗   │    ╲
      │    │   ║   target  ║   │     │       ← target tick mark
      │    │   ║    80%    ║   │     │
       ╲   ╲                   ╱    ╱
        min                       max
        0                         100
```

Single-metric visual showing actual against a target, min, and max. Built-in `gauge` is acceptable
**only for Operational dashboards** where the target/threshold metaphor is mandatory.

---

## Slots

| Slot | Content | Binding example |
|---|---|---|
| Value | Current actual | `[OEE]` |
| Target | Target threshold | `[OEE Target]` (measure or constant) |
| Minimum | Scale start | `0` or `[OEE Min]` |
| Maximum | Scale end | `100` or `[OEE Max]` |

---

## Formatting (theme-aware)

- **Fill color:** conditional — `good` when value ≥ target, `neutral` when close, `bad` when well below
- **Target marker:** high-contrast line (`foreground`)
- **Arc background:** `background2`
- **Data label:** the value shown in the center, 24-32pt Semibold
- **Units:** always shown (% / $ / count) in the label

---

## Narrative frame

- **Executive:** generally AVOID — gauges consume lots of real estate for one number. Use a card + delta instead.
- **Analytical:** AVOID — gauges hide context (trend, breakdown). Use a trend-line with a target reference line.
- **Operational:** primary use case — shop floor / kiosk boards where the threshold semaphore is the point

---

## Do NOT

- Use multiple gauges in a row — a multi-row card or KPI banner shows the same info more compactly
- Use gauges for **unbounded metrics** (total revenue has no natural max) — use card or bar
- Use **3D gauges** — bans apply (see `shared-standards.md`)
- Use gauge when the audience needs to see **trend** — gauges are point-in-time only
- Use gauge to compare multiple entities — each is an isolated snapshot

---

## Data quality gotchas

- **Min / max stability:** if Min and Max come from measures, they can shift with filters — viewers perceive the same value at different positions. Prefer constants or model parameters.
- **Target semantics:** target above OR below value? A gauge implies "higher is better" — for "lower is better" (defect rate, cost), either invert the color logic or use a different visual
- **Null values:** render as empty gauge with `neutral` text, never as 0 (0 may look catastrophic)
- **Percentage vs absolute:** if the metric is a percentage, set Max = 100; if absolute, use a realistic ceiling (not infinity)

---

## Checklist

- [ ] Value bound to a measure, not a column
- [ ] Target bound (constant or measure) — never missing
- [ ] Min / max stable across filter changes (constants preferred)
- [ ] Conditional fill color using `good` / `neutral` / `bad` tokens
- [ ] Used only in Operational style pages
- [ ] Units displayed alongside value
- [ ] Alt text: "Gauge showing <metric> at <value>, target <target>, status <good/neutral/bad>"
