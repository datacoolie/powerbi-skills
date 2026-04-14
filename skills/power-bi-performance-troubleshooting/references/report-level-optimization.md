# Report-Level Optimization

Performance optimizations at the report/visual layer — the cheapest and fastest
fixes that don't require changing DAX or the data model.

---

## Visual Count Per Page

Every visual on a page generates at least one DAX query. More visuals = more
concurrent queries = longer page load.

| Visual Count | Expected Load | Recommendation |
|---|---|---|
| 1-4 | Fast (< 3s) | Ideal for executive dashboards |
| 5-8 | Acceptable (3-8s) | Standard report pages |
| 9-12 | Slow (8-15s) | Reduce, split, or use bookmarks |
| 13+ | Very slow (15s+) | Must restructure the page |

### Strategies to Reduce Visual Count

1. **Combine related visuals** — Use a combo chart (line + column) instead of separate charts
2. **Use bookmarks** — Show different view states of the same page instead of all-at-once
3. **Drillthrough pages** — Move detail visuals to on-demand drillthrough pages
4. **Tooltip pages** — Move contextual details to tooltip overlays
5. **Progressive disclosure** — Landing page has KPIs only; detail pages load on demand
6. **Remove decorative visuals** — Background shapes, logos, and text boxes with no data
   still generate events (though they don't query the model)

---

## Cross-Filtering Optimization

By default, all visuals on a page cross-filter each other. When Visual A is
clicked, every other visual re-queries with the new filter context.

### Problem: Chain Reactions

If Visual A cross-filters B, C, D, E, F, G, and H — clicking A triggers
7 re-queries simultaneously. If each takes 500ms, the total perceived delay
is the longest query, but the engine must process all of them.

### Fixes

1. **Disable cross-filtering on non-interactive visuals**:
   - Select a visual → Format → Edit interactions
   - Set non-interactive visuals to "None" (no filter / no highlight)
   - KPI cards rarely need to respond to other visual clicks

2. **Change from cross-filter to cross-highlight**:
   - Cross-highlight is cheaper than cross-filter (no re-query; just re-render)
   - Choose "Highlight" instead of "Filter" in Edit Interactions

3. **Break cross-filter chains**:
   - If visuals A→B→C→D all cross-filter, clicking A triggers 3 re-queries
   - Remove unnecessary links: maybe D doesn't need to respond to A

### Visual Interaction Settings

```
Edit Interactions → for each source visual, set targets to:
  ● Filter  — full re-query (most expensive)
  ● Highlight — re-render only (cheaper)
  ● None   — no response (cheapest)
```

---

## Slicer Optimization

Slicers are among the most expensive visuals because they:
- Generate DAX queries on page load to populate values
- Trigger re-queries on ALL cross-filtered visuals when changed
- Can have very high cardinality (thousands of items)

### High-Cardinality Slicer Fixes

| Situation | Fix |
|---|---|
| Slicer shows 10,000+ items | Switch to **Dropdown** mode |
| Date slicer shows individual days | Use **Relative date** or **Between** mode |
| Text slicer with long list | Add **Search** box (Slicer settings → Search) |
| Product slicer with all SKUs | Add a hierarchy (Category → SubCategory → SKU) |
| Multiple slicers on every page | Use a **Sync slicers** group (slicer queries once, syncs to all pages) |

### Apply Button (Query Reduction)

For reports with multiple slicers, enable the Apply button so all slicer
changes are batched into a single re-query:

**Power BI Desktop:** File → Options → Query reduction →
- ✅ Add an apply button to each slicer to apply changes when ready
- ✅ Add an apply button to filter pane to apply changes in one go

**Effect:** Users adjust all slicers first, then click Apply — one batch
re-query instead of N separate re-queries per slicer change.

---

## Custom Visual Performance

Custom visuals (from AppSource or organizational store) can have significantly
different performance characteristics than standard visuals.

### Common Custom Visual Issues

| Issue | Impact | Fix |
|---|---|---|
| Heavy JavaScript rendering | High Visual Display time | Replace with standard visual |
| Excessive data requests | High DAX Query time | Check if visual requests all rows |
| No data reduction | Downloads full dataset to client | Use a visual that supports Top N |
| Memory leaks | Page gets slower over time | Refresh page, replace visual |
| Old/unmaintained visual | Compatibility issues | Update or switch to newer alternative |

### Diagnosis

1. In Performance Analyzer, compare the custom visual's timing vs. a standard
   visual showing the same data
2. If custom visual is 3x+ slower, it's the visual implementation, not your DAX
3. Check if the custom visual has configuration options to limit data (e.g.,
   "Max data points" setting)

---

## Render vs. Query Bottleneck

Use Performance Analyzer to determine which layer is the bottleneck:

### Query Bottleneck (DAX Query >> Visual Display)

```
DAX Query:      5200 ms  ← Bottleneck
Visual Display:  150 ms
Other:            50 ms
```

**Root cause:** Slow measure, expensive model scan, or complex filter context.
**Next step:** Copy DAX query → DAX Studio → Server Timings analysis.

### Render Bottleneck (Visual Display >> DAX Query)

```
DAX Query:       200 ms
Visual Display: 3500 ms  ← Bottleneck
Other:            50 ms
```

**Root cause:** Too many data points, complex SVG rendering, or heavy custom visual.
**Fixes:**
- Add a Top N filter to the visual (e.g., show top 50 products, not all 10,000)
- Reduce scatter chart points (sample or aggregate)
- Replace complex custom visual with standard alternative
- For tables/matrices: reduce visible columns, paginate rows

### Concurrency Bottleneck (Other >> DAX Query + Visual Display)

```
DAX Query:       200 ms
Visual Display:  100 ms
Other:          4000 ms  ← Bottleneck
```

**Root cause:** Visual waiting for other visuals to finish querying first.
**Fixes:**
- Reduce total visual count on the page
- Disable cross-filtering on non-interactive visuals
- Split page into multiple pages with fewer visuals each

---

## Page Load Optimization Checklist

Run through this checklist for any page loading in > 5 seconds:

```
□ Visual count ≤ 8?
□ No unnecessary visuals (decorative shapes generating events)?
□ Cross-filtering disabled on KPI cards and non-interactive visuals?
□ Slicers in dropdown mode (not list mode with 1000+ items)?
□ Apply button enabled for multi-slicer pages?
□ Custom visuals replaced with standard alternatives where possible?
□ Visual-level filters limiting rows (Top N instead of "all")?
□ Default page filters applied to reduce initial data volume?
□ No auto-play animations or auto-refreshing visuals?
□ Tooltips are simple (not tooltip pages with heavy charts)?
```

---

## Quick Reference

| Optimization | Impact | Effort |
|---|---|---|
| Reduce visuals to ≤ 8 | High | Low |
| Disable unnecessary cross-filtering | High | Low |
| Enable Apply button on slicers | Medium | Low |
| Switch slicers to dropdown mode | Medium | Low |
| Add Top N filters to visuals | Medium | Low |
| Replace heavy custom visuals | High | Medium |
| Split dense pages with bookmarks | Medium | Medium |
| Add default page filters | Medium | Low |
