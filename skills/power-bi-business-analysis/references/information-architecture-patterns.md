# Information Architecture Patterns

Standard page-flow patterns for Power BI reports, organized by report archetype.
Use these after the stakeholder interview to propose a concrete page structure.

---

## Universal Page Progression

Every report follows this layered structure, regardless of domain:

```
Layer 1 — OVERVIEW          "How are we doing?"       1 page
Layer 2 — ANALYSIS          "Why is it happening?"    1-3 pages
Layer 3 — DETAIL            "Show me the rows"        1 drillthrough page (hidden)
Layer 4 — CONTEXT           "More info on hover"      0-2 tooltip pages (hidden)
```

Minimum viable report = Layer 1 + Layer 3.
Full analytical report = all four layers.

## Archetype-Specific Patterns

### Executive Dashboard (3-5 pages)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Overview    │───▶│  Exception   │───▶│  Drillthrough│
│  (KPI cards, │    │  (what needs │    │  (hidden,    │
│   trend,     │    │   attention?)│    │   detail     │
│   status)    │    │              │    │   table)     │
└──────────────┘    └──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐
│  Period      │  (optional — monthly/quarterly executive pack)
│  Comparison  │
└──────────────┘
```

**Characteristics:** ≤ 4 visuals per page, Big-Idea titles, high whitespace,
minimal slicers (date range only), top button-bar navigation.

### Analytical Report (5-8 pages)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Overview    │───▶│  Dimension A │───▶│  Dimension B │───▶│  Dimension C │
│  (KPI row +  │    │  (e.g.       │    │  (e.g.       │    │  (e.g.       │
│   hero chart)│    │   Product)   │    │   Region)    │    │   Customer)  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                                                          │
       ▼                                                          ▼
┌──────────────┐                                          ┌──────────────┐
│  Trend /     │                                          │  Drillthrough│
│  Comparison  │                                          │  (hidden)    │
└──────────────┘                                          └──────────────┘
```

**Characteristics:** 5-8 visuals per page, KPI row + hero + 3-column grid,
direct labels, sync slicers across analysis pages, tab or button-bar navigation.

### Operational Report (6-12 pages)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Status      │───▶│  Detail A    │───▶│  Detail B    │
│  Board       │    │  (work queue │    │  (shift /    │
│  (traffic-   │    │   or list)   │    │   line view) │
│   light)     │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  Alert /     │───▶│  Drillthrough│
│  Exception   │    │  (hidden)    │
└──────────────┘    └──────────────┘
```

**Characteristics:** 8-12 visuals per page, large fonts, traffic-light indicators,
heavy use of conditional formatting, mobile layout mandatory, bookmark-based
filter presets, page navigator or hub-and-spoke navigation.

## Navigation Patterns

| Pattern | Best For | Pages |
|---|---|---|
| Top button bar | 2-5 pages, equal importance | All archetypes |
| Left rail / sidebar | 5+ pages, hierarchical grouping | Analytical, Operational |
| Bookmark tabs | Same data, different views (e.g. chart vs. table) | Analytical |
| Hub-and-spoke | 1 hub + many drillthrough targets | Executive, Operational |
| Page navigator (built-in) | 5+ pages, simple flat list | Any |
| Breadcrumb trail | Deep drill paths (3+ levels) | Analytical |

## Page Sizing Rules

| Canvas | Use When |
|---|---|
| 1664 × 936 (default) | Standard desktop consumption |
| 1280 × 720 | Presentation / projector mode |
| 1920 × 1080 | Full HD monitors, wall displays |
| 320 × 240 | Tooltip pages |
| Custom (letter / A4) | Paginated / print-optimized reports |

## Composing the Page Plan

For each page, fill this row in the Requirements Document §3:

```
| Page slug | Purpose (1 sentence) | Audience | Hero Visual | Supporting | Measures | Slicers |
```

**Rules:**
1. Every page answers exactly **one question** in its purpose column
2. The hero visual is the largest chart — it dominates the page and answers the question
3. Supporting visuals provide context, not redundancy (no two charts showing the same thing)
4. Slicers are listed per-page; global slicers go in a shared slicer panel
5. If a page needs > 8 visuals, split into two pages
