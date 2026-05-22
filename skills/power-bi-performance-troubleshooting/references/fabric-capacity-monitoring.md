# Fabric Capacity Monitoring & Optimization

Diagnose performance issues at the capacity/infrastructure level — when the
problem isn't DAX, model, or report design, but resource contention.

---

## When to Suspect Capacity Issues

| Signal | Indicates |
|---|---|
| All reports on a workspace are slow simultaneously | Capacity saturation |
| Reports slow during peak business hours, fast off-hours | Concurrency pressure |
| Reports slow after refresh schedule window | Background operations competing |
| Specific users slow, others fine (same report) | RLS per-user cache, or multi-geo |
| Throttling notifications from admin | CU overcommit |
| Service "busy" errors or query rejections | Hard throttling threshold hit |

## Fabric Capacity Metrics App

### Installation
- Requires capacity admin role
- Install from AppSource: "Microsoft Fabric Capacity Metrics"
- Connects to all capacities you administer

### Key Pages

| Page | Use For |
|---|---|
| Health | High-level overview: which capacities are stressed |
| Compute | 14-day CU utilization trend; identify peak patterns |
| Storage | 30-day storage usage; billable vs soft-deleted |
| Timepoint | Drill into a specific 30-second window to find culprit items |
| Timepoint Summary | Aggregate by operation type at a point in time |
| Timepoint Item Detail | Root-cause: which specific item consumed CUs |

### Diagnosis Workflow

1. Open Health page → identify capacity with issues (red/amber)
2. Switch to Compute page → find peak CU period
3. Note: is peak from interactive (user queries) or background (refreshes)?
4. Drill to Timepoint at peak → identify top-consuming items
5. For each top item:
   - Semantic model refresh → optimize partition strategy / schedule off-peak
   - Interactive queries → optimize DAX / model (route to other perf references)
   - Spark / pipeline → route to data engineering team
6. Evaluate: scale up, scale out, or optimize

### Key Metrics to Monitor

| Metric | Target | Action When Exceeded |
|---|---|---|
| Peak CU utilization | < 80% sustained | Scale up or redistribute workloads |
| Throttling events / week | 0 | Immediate: offload or scale |
| Background / interactive ratio | Background < 40% during business hours | Reschedule refreshes to off-peak |
| Query rejection count | 0 | Scale up; too many concurrent requests |
| Overutilization duration | < 5 min / day | Tolerable; > 30 min needs action |

---

## Evaluation Configuration (Desktop-side)

When Power BI Desktop itself is slow during development:

| Setting | Default | Tune When |
|---|---|---|
| Max simultaneous evaluations | Auto | Import too slow → increase; machine overloaded → decrease |
| Available memory per evaluation | Auto | Large model refresh OOM → increase |
| Max concurrent jobs | Auto | Visual interactions slow → increase |
| Max active connections per source | Auto | DQ timeouts (source-limited) → decrease |

Access: File → Options → Evaluation configuration.

**Caution:** These settings affect Desktop authoring performance only, not Service
performance. Service capacity is governed by the SKU and Fabric CU allocation.

---

## Optimize Ribbon (Desktop)

Quick-access presets for report performance optimization:

| Preset | Effect | Best For |
|---|---|---|
| Query Reduction | Disables cross-highlighting, adds Apply button to slicers/filters | DirectQuery reports |
| Interactivity | Default: cross-highlight, instant slicer response | Import mode, small models |
| Customize | Opens Options dialog for granular control | Mixed scenarios |

Access: Optimize tab in ribbon (Power BI Desktop).

---

## Capacity Optimization Actions

### Immediate (< 1 day)
- Reschedule large refreshes to off-peak hours
- Pause unused refresh schedules
- Enable autoscale (if available on SKU)

### Short-term (1-7 days)
- Optimize top-consuming semantic models (model size, DAX, aggregations)
- Move ad-hoc/exploration workloads to separate capacity
- Implement query reduction settings on DirectQuery reports

### Long-term (weeks)
- Scale up capacity SKU
- Isolate workloads by tier (production vs. dev vs. self-service)
- Implement aggregation tables for heavy dashboards
- Migrate large Import models to Direct Lake (reduces refresh CU)

---

## Workspace Monitoring (Advanced)

For deeper telemetry beyond the Capacity Metrics App:
- **Workspace Monitoring** (Fabric) — item-level logs and metrics
- **Fabric Toolbox** (open-source) — extended monitoring tools
- **Log Analytics** (Azure Monitor) — long-term retention + alerting
- **On-premises data gateway logs** — gateway-specific performance data

---

## Anti-Patterns

- ❌ Blaming DAX when the real problem is capacity contention — check metrics first
- ❌ Ignoring throttling notifications — they indicate user-facing degradation
- ❌ Running all refreshes at midnight (everyone does this → peak contention)
- ❌ Sharing a single capacity across dev/test/production without workload separation
- ❌ Scaling up before optimizing — often 2-3x improvement available through tuning
- ✅ Do monitor capacity weekly using the Metrics App
- ✅ Do establish a CU budget per workload/team (chargeback model)
