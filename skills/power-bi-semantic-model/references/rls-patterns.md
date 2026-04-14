# RLS & OLS Patterns

Comprehensive Row-Level Security (RLS) and Object-Level Security (OLS)
patterns for Power BI semantic models, including dynamic RLS, DirectLake
considerations, testing procedures, and performance impact.

---

## RLS Fundamentals

Row-Level Security restricts data access at the row level. Users see only
the data their role permits.

### Architecture

```
User opens report
  → Power BI checks role membership
    → DAX filter expression is applied to tables
      → All visuals see only filtered rows
```

### Basic Patterns

**Static filter — hardcoded value:**
```dax
// Role: "North Region"
[Region] = "North"
```

**Dynamic — current user's email:**
```dax
// Role: "Dynamic Region"
// Requires a DimUser table with Email and Region columns
'DimUser'[Email] = USERPRINCIPALNAME()
```

**Lookup table pattern — many-to-many security:**
```dax
// SecurityBridge table: Email | Region (one row per user-region pair)
// Role filter on SecurityBridge:
'SecurityBridge'[Email] = USERPRINCIPALNAME()
// Relationship: SecurityBridge[Region] → Geography[Region] (many-to-1)
// This filters Geography → cascades to Fact via star schema
```

---

## Advanced Dynamic RLS Patterns

### Pattern 1: Manager Hierarchy (Parent-Child)

Managers see their own data plus all reports' data.

```dax
// DimEmployee table with EmployeeID, ManagerID, Email columns
// Create a PATH column:
EmployeePath = PATH('DimEmployee'[EmployeeID], 'DimEmployee'[ManagerID])

// RLS filter expression:
VAR _currentUser =
    LOOKUPVALUE(
        'DimEmployee'[EmployeeID],
        'DimEmployee'[Email], USERPRINCIPALNAME()
    )
RETURN
    PATHCONTAINS('DimEmployee'[EmployeePath], _currentUser)
```

### Pattern 2: Multi-Attribute Security

User has access based on multiple dimensions (e.g., Region + Department):

```dax
// SecurityMatrix table: Email | Region | Department
// RLS filter on SecurityMatrix:
'SecurityMatrix'[Email] = USERPRINCIPALNAME()

// Relationships:
//   SecurityMatrix[Region] → Geography[Region]
//   SecurityMatrix[Department] → Department[Department]
// Both relationships filter fact tables via star schema cascade
```

### Pattern 3: Time-Based Access

Users see data only from certain date ranges:

```dax
// SecurityDateRange table: Email | StartDate | EndDate
VAR _userRanges =
    FILTER(
        'SecurityDateRange',
        'SecurityDateRange'[Email] = USERPRINCIPALNAME()
    )
RETURN
    COUNTROWS(
        FILTER(
            _userRanges,
            'Date'[Date] >= 'SecurityDateRange'[StartDate]
                && 'Date'[Date] <= 'SecurityDateRange'[EndDate]
        )
    ) > 0
```

### Pattern 4: All-Access Admin Role

```dax
// Role: "Admin"
// Filter expression (always true):
1 = 1

// Or simply create a role with no filter expressions
// (all tables return all rows)
```

---

## Object-Level Security (OLS)

OLS restricts access to specific **tables or columns** (not rows).
Users without access see a placeholder or error when accessing the object.

### Configuration in TMDL

```tmdl
table Salary
    column EmployeeID
        dataType: int64
    column BaseSalary
        dataType: decimal
    column BonusAmount
        dataType: decimal

role 'HR Only'
    modelPermission: read
    tablePermission Salary = 'SecurityBridge'[Email] = USERPRINCIPALNAME()

    // OLS: restrict column access
    columnPermission Salary.BaseSalary = none
    columnPermission Salary.BonusAmount = none
```

### OLS Behavior

| Scenario | Result |
|---|---|
| User without OLS access queries restricted column | Error message |
| Visual references restricted column | Visual shows error |
| Measure references restricted column | Measure returns error |
| Restricted column in filter pane | Not visible |

### OLS Best Practices

| Practice | Reason |
|---|---|
| Use OLS sparingly | Broad column hiding creates confusing UX |
| Combine with RLS | OLS for column-level, RLS for row-level |
| Test with "View as Role" | Verify error handling in visuals |
| Create fallback measures | Show "Access Restricted" instead of error |

---

## DirectLake RLS

DirectLake mode has specific RLS considerations:

### Fixed Identity

In DirectLake, RLS can use a **fixed identity** — the query runs under
the semantic model's credentials, and RLS is enforced in the engine:

```
DirectLake → Reads parquet from OneLake
  → RLS DAX filter applied in VertiPaq engine (in-memory)
  → Filtered results returned to visual
```

### Limitations

| Limitation | Detail |
|---|---|
| `USERPRINCIPALNAME()` works | Returns the report viewer's UPN |
| `USERNAME()` works | Returns the viewer's identity |
| Complex DAX in RLS | May cause fallback to DirectQuery mode |
| PATH() in RLS | May cause fallback — test carefully |
| LOOKUPVALUE in RLS | Supported but monitor for fallback |

### Avoiding DirectQuery Fallback

```
Keep RLS expressions simple:
✅  [Region] = USERPRINCIPALNAME()   → stays in DirectLake
✅  Table filter with simple equality → stays in DirectLake
⚠️  PATH() hierarchy                  → may fall back
⚠️  Complex CALCULATE in RLS         → may fall back
❌  Dynamic security with nested      → likely falls back
    SUMMARIZE/ADDCOLUMNS
```

---

## Testing RLS

### In Power BI Desktop

1. **Modeling** → **View as** → Select role(s)
2. Optionally check **"Other user"** and enter a UPN
3. All visuals now show data as that role would see it
4. Yellow banner indicates you're in "View as" mode

### Via MCP Tools

```
// Test role membership effect
1. Use security_role_operations → List roles
2. Use security_role_operations → Get role details (see filter expressions)
3. Use dax_query_operations → Run EVALUATE with role context:

EVALUATE
CALCULATETABLE(
    SUMMARIZE('Sales', 'Geography'[Region], "Rows", COUNTROWS('Sales')),
    USERELATIONSHIP(...) // if needed
)
// Compare results with and without role to verify filtering
```

### Testing Checklist

| Test | Verify |
|---|---|
| Role returns correct rows | Run DAX query per role |
| No data leakage | Check cross-filter directions |
| Bi-directional relationships | Ensure RLS filters propagate both ways |
| Default "no role" behavior | Unassigned users see no data (not all data) |
| Performance under RLS | Compare query times with/without RLS |
| Edge cases | Users in multiple roles (union), users with no mapping |

---

## Performance Impact

### RLS Performance Factors

| Factor | Impact |
|---|---|
| Simple column filter | Negligible overhead |
| USERPRINCIPALNAME() lookup | Small overhead per query |
| SecurityBridge join | Moderate — depends on bridge table size |
| PATH() hierarchy | Significant — materializes path per row |
| CALCULATE in RLS | Significant — evaluated per row |
| Many roles per user | Union of all roles — cumulative filter cost |

### Optimization Strategies

1. **Pre-compute security mappings** — materialize the user-to-dimension
   mapping in ETL rather than computing it in DAX
2. **Minimize bridge table rows** — only store active user mappings
3. **Avoid bi-directional on large tables** — use single-direction + CROSSFILTER
4. **Index security columns** — ensure the filtered column has good cardinality
5. **Test with realistic user count** — RLS cache is per-user identity

---

## Bi-Directional Relationship Gotchas

When RLS filters a dimension that has a bi-directional relationship to a
fact table, the filter propagates in **both directions**:

```
SecurityBridge ←→ Geography ←→ Sales (fact)
                                 ↕
                              Products

If Geography is filtered by RLS:
  → Sales is filtered (correct)
  → Products may also be filtered if bi-directional (unexpected)
```

### Fix: Use Single-Direction + Explicit DAX

```dax
// Instead of bi-directional relationship on Products → Sales:
// Use CROSSFILTER in specific measures that need it:
Filtered Product Count =
CALCULATE(
    COUNTROWS('Products'),
    CROSSFILTER('Sales'[ProductID], 'Products'[ProductID], Both)
)
```

---

## Quick Reference

| Pattern | When to Use |
|---|---|
| Static filter | Few fixed roles (regions, departments) |
| USERPRINCIPALNAME() | Dynamic per-user filtering |
| SecurityBridge table | Many-to-many user ↔ dimension mapping |
| Manager hierarchy (PATH) | Org chart–based access |
| OLS | Hide sensitive columns (salary, PII) |
| Fixed identity (DirectLake) | Lakehouse RLS without gateway |
| Admin role (1=1) | Bypass RLS for admins/power users |

| MCP Tool | RLS Use |
|---|---|
| `security_role_operations` | List, create, modify roles |
| `dax_query_operations` | Test RLS filter results |
| `model_operations` | Verify model-level permissions |
| `table_operations` | Check table permissions |
