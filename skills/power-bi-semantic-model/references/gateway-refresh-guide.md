# Data Gateway & Refresh Guide

Configuration and troubleshooting for on-premises data gateways,
scheduled refresh, and incremental refresh in Power BI.

---

## Gateway Types

| Type | Use Case | Install |
|---|---|---|
| **Standard (Enterprise)** | Shared by multiple users/reports, IT-managed | Dedicated server |
| **Personal** | Single user, development/testing only | Developer machine |
| **VNet gateway** | Fabric/Premium — connects to VNet-secured sources | Fabric portal config |

### When You Need a Gateway

| Data Source | Gateway Required? |
|---|---|
| Azure SQL Database (public endpoint) | No — cloud-to-cloud |
| On-premises SQL Server | Yes — standard gateway |
| On-premises file share | Yes — standard gateway |
| Azure SQL with Private Link | Yes — VNet gateway |
| SharePoint Online | No — cloud-to-cloud |
| Dataverse | No — direct connector |
| OneLake / Lakehouse | No — Fabric native |
| Web API (public) | No — cloud-to-cloud |
| Web API (behind firewall) | Yes — standard gateway |

---

## Gateway Architecture

```
Power BI Service
  │
  ├── Cloud data sources → Direct connection (no gateway)
  │
  └── On-premises / private network sources
        │
        ▼
   ┌─────────────────┐     ┌──────────────────────┐
   │ Gateway Cluster  │     │ On-Premises Network   │
   │                  │────►│                        │
   │ Gateway Node 1   │     │ SQL Server             │
   │ Gateway Node 2   │     │ Oracle                 │
   │ (failover)       │     │ File Shares            │
   └─────────────────┘     └──────────────────────┘
        │
   Outbound HTTPS (443) to Azure Service Bus
   (No inbound ports required)
```

### Gateway Cluster Best Practices

| Practice | Detail |
|---|---|
| Minimum 2 nodes | High availability / failover |
| Dedicated server | Don't share with other applications |
| SSD storage | Gateway caches data during refresh |
| 8+ GB RAM | For large dataset refresh operations |
| Close to data source | Minimize network latency |
| Same region as Power BI tenant | Minimize gateway ↔ service latency |

---

## Scheduled Refresh

### Configuration Steps

1. Publish dataset to Power BI Service
2. Go to Dataset Settings → Gateway and cloud connections
3. Map each data source to the gateway
4. Configure credentials (OAuth, Basic, Key, etc.)
5. Set refresh schedule (times and frequency)

### Refresh Limits

| License / Capacity | Max Refreshes per Day |
|---|---|
| Power BI Pro | 8 |
| Power BI Premium Per User (PPU) | 48 |
| Premium / Fabric F SKU | 48 (configurable higher via XMLA) |
| XMLA endpoint refresh | Unlimited (API-triggered) |

### Refresh Schedule Patterns

| Pattern | When |
|---|---|
| Morning before business hours | Dashboards ready when users arrive |
| After ETL pipeline completes | Chain refresh after data load |
| Every 30 min (Premium) | Near-real-time for operational reports |
| On-demand via REST API | Event-driven refresh triggered by pipeline |

---

## Incremental Refresh

Incremental refresh partitions the dataset by date range, refreshing
only recent partitions instead of the full dataset.

### Configuration

Define two parameters in Power BI Desktop:

| Parameter | Type | Purpose |
|---|---|---|
| `RangeStart` | DateTime | Start of the refresh window |
| `RangeEnd` | DateTime | End of the refresh window |

### Power Query Filter

```powerquery-m
// Apply in Power Query Editor for each table that needs incremental refresh
let
    Source = Sql.Database("server", "database"),
    Sales = Source{[Schema="dbo",Item="FactSales"]}[Data],
    // Filter by range parameters — REQUIRED for incremental refresh
    Filtered = Table.SelectRows(Sales, each
        [OrderDate] >= RangeStart and [OrderDate] < RangeEnd
    )
in
    Filtered
```

### Incremental Refresh Policy

Configure in Power BI Desktop → Table properties → Incremental refresh:

| Setting | Example | Purpose |
|---|---|---|
| Archive data starting | 3 Years ago | Total historical data to keep |
| Incrementally refresh starting | 30 Days ago | Window to re-refresh |
| Detect data changes | `LastModifiedDate` column | Only refresh changed partitions |
| Only refresh complete periods | Checked | Avoid partial-day data |

### How Partitions Work

```
Full dataset: 3 years of data

Partitions:
  [2022-01] [2022-02] ... [2024-10] [2024-11-01..15] [2024-11-16..30]
   ─────── Historical ──────────    ── Incremental ──   ── Current ──
   (never refreshed again)          (re-refreshed)      (always refreshed)
```

### TMDL Partition Pattern

```tmdl
table FactSales
    partition 'FactSales-2024-01' = m
        mode: import
        expression = ```
            let
                Source = ...,
                Filtered = Table.SelectRows(Source, each
                    [OrderDate] >= #datetime(2024, 1, 1, 0, 0, 0)
                    and [OrderDate] < #datetime(2024, 2, 1, 0, 0, 0))
            in Filtered
            ```

    partition 'FactSales-Current' = m
        mode: import
        expression = ```
            let
                Source = ...,
                Filtered = Table.SelectRows(Source, each
                    [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
            in Filtered
            ```
```

---

## Refresh Troubleshooting

### Common Errors

| Error | Cause | Fix |
|---|---|---|
| "Gateway unreachable" | Gateway service stopped or network issue | Restart gateway service, check connectivity |
| "Data source credentials invalid" | Expired OAuth token or changed password | Update credentials in dataset settings |
| "Query timeout" | Source query takes too long | Optimize source query, increase timeout |
| "Memory exceeded" | Dataset too large for gateway RAM | Add RAM, use incremental refresh, or optimize model |
| "Expression.Error: key didn't match" | Source schema changed (renamed column) | Update Power Query to match new schema |
| "Refresh exceeded time limit" | 2-hour limit (Pro) or 5-hour limit (Premium) | Use incremental refresh to reduce refresh scope |

### Refresh Monitoring

| Method | How |
|---|---|
| Power BI Service | Dataset → Refresh history |
| REST API | `GET /groups/{groupId}/datasets/{datasetId}/refreshes` |
| Fabric Monitoring Hub | Real-time refresh status across workspace |
| Email notifications | Configure in dataset settings |
| Azure Log Analytics | Premium — detailed refresh telemetry |

### Gateway Diagnostics

| Tool | Purpose |
|---|---|
| Gateway app → Diagnostics | Run built-in connectivity tests |
| Gateway logs | `C:\Users\<GatewayUser>\AppData\Local\Microsoft\On-premises data gateway\` |
| Performance counters | Monitor CPU, memory, network on gateway server |
| Network trace | Verify outbound 443 to `*.servicebus.windows.net` |

---

## MCP Tools for Refresh Operations

| Tool | Use For |
|---|---|
| `partition_operations` (List) | View partition status and last refresh time |
| `partition_operations` (Refresh) | Trigger partition refresh via XMLA |
| `database_operations` | Check database state after refresh |
| `table_operations` | Verify row counts post-refresh |
| `trace_operations` | Monitor refresh performance metrics |
| `fabric-mcp/publicapis_get` | Query refresh history via REST API |

---

## Quick Reference

| Task | Approach |
|---|---|
| Connect to on-prem source | Install standard gateway, configure data source |
| High availability | Gateway cluster with 2+ nodes |
| Refresh > 8x/day | Premium capacity or XMLA endpoint |
| Large dataset refresh | Incremental refresh with date partitions |
| Chain refresh after ETL | REST API trigger or Fabric pipeline activity |
| Monitor refresh failures | Email alerts + refresh history API |
| Troubleshoot gateway | Check logs + run diagnostics in gateway app |
