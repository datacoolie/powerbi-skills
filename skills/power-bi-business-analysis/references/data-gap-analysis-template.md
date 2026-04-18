# Data Gap Analysis Template

Systematic comparison of **required metrics** (from the KPI list) vs.
**available data sources** to surface gaps before model design begins.
Run this as the final step of Phase 1, after the interview and domain analysis.

---

## Step 1 — Build the Requirements-vs-Data Matrix

For every KPI in §2 of the Requirements Document, list the columns it needs
and whether those columns exist in an available source:

```markdown
| # | KPI | Required Column(s) | Source Table | Available? | Gap Action |
|---|---|---|---|---|---|
| 1 | Total Revenue | Sales[NetAmount] | gold.FactSales | ✅ Yes | — |
| 2 | Revenue YoY % | Sales[NetAmount], Date[Year] | gold.FactSales, gold.DimDate | ✅ Yes | — |
| 3 | Customer Acquisition Cost | Marketing[Spend], Customer[IsNew] | — | ❌ No | Need marketing data source |
| 4 | OEE | Production[GoodUnits], [TotalUnits], Downtime[Duration] | gold.FactProduction | ⚠️ Partial | Downtime table missing |
```

### Availability Legend

| Symbol | Meaning | Impact |
|---|---|---|
| ✅ Yes | Column exists with correct grain and data type | No action needed |
| ⚠️ Partial | Column exists but needs transformation, different grain, or incomplete history | ETL / Power Query work needed |
| ❌ No | Column or table does not exist in any known source | Requires new data source or scope reduction |

## Step 2 — Classify Each Gap

| Gap Type | Description | Resolution Path |
|---|---|---|
| **Missing source** | No table or API provides this data | Ask stakeholder to provide data or defer the KPI to a future iteration |
| **Wrong grain** | Data exists but at a different level (e.g. monthly, need daily) | ETL aggregation/disaggregation; document assumption |
| **Incomplete history** | Source starts too recently for required time comparisons | Backfill or adjust time-intelligence scope |
| **Access restriction** | Data exists but the team lacks permissions | Escalate to data engineering / admin; document blocker |
| **Quality issue** | Column has NULLs, duplicates, or inconsistent values | Add data-cleaning step in Power Query; document risk |
| **Derived metric** | KPI can be calculated from existing columns but doesn't exist as-is | No gap — will be a DAX measure (Phase 3) |

## Step 3 — Gap Resolution Plan

For each ❌ or ⚠️ gap:

```markdown
| # | KPI | Gap Type | Owner | Resolution | ETA | Fallback if Unresolved |
|---|---|---|---|---|---|---|
| 3 | CAC | Missing source | Data Eng | Connect marketing DB | 2 weeks | Remove KPI from v1, add to backlog |
| 4 | OEE | Partial — no downtime | Plant IT | Expose downtime table | 1 week | Show Availability × Quality only |
```

## Step 4 — Update Requirements Document

After the gap analysis:

1. **Remove** KPIs where the gap cannot be resolved in the project timeline
   → move to §9 (Open Questions / Backlog) with a note
2. **Adjust** the page plan if a removed KPI was the hero metric on a page
3. **Add** new data sources to §4 (Data Requirements) for any gaps that will be resolved
4. **Flag** partial-data KPIs with an asterisk in §2 and a footnote explaining the limitation

## Step 5 — Data Readiness Score

Summarize overall readiness:

```
Data Readiness: [X] of [Y] KPIs fully sourced ([Z]%)
  ✅ Fully available:  [count]
  ⚠️ Partial / needs work:  [count]
  ❌ Missing / blocked:  [count]
```

**Decision rule:**
- ≥ 80% fully available → proceed to Phase 2
- 50-79% → proceed but flag partial KPIs; schedule a data-readiness checkpoint
- < 50% → pause and escalate data availability before continuing

## Anti-Patterns

- ❌ Assuming data exists without checking — always verify with `table_operations` or source catalog
- ❌ Designing a page around a KPI that has no data — leads to blank visuals in the final report
- ❌ Silently dropping a KPI — every removal must be documented in the backlog with rationale
- ❌ Over-scoping to fill gaps — don't build an ETL pipeline inside a BI project; surface the gap and let data engineering own it
