# Deployment & ALM Guide

Guidance for deploying Power BI solutions across environments, version control
with Git/PBIP, and application lifecycle management (ALM).

---

## Git Integration with PBIP

PBIP (Power BI Project) format stores reports and semantic models as text files
(JSON, TMDL) that can be version-controlled in Git.

### Repository Structure

```
repo/
├── <ProjectName>.pbip                    ← Project entry point
├── <ProjectName>.Report/                 ← Report definition (PBIR JSON)
│   └── definition/
│       ├── report.json
│       ├── pages/
│       └── ...
├── <ProjectName>.SemanticModel/          ← Semantic model (TMDL)
│   └── definition/
│       ├── model.tmdl
│       ├── tables/
│       ├── relationships.tmdl
│       └── ...
└── .gitignore
```

### Recommended .gitignore

```gitignore
# Power BI generated files
*.pbip.local
.pbi/
localSettings.json
diagramLayout.json

# Cache files
*.cache
.cache/

# User-specific settings
*.pbix
```

### Branching Strategy

```
main           ← Production-ready models and reports
├── develop    ← Integration branch
│   ├── feature/add-inventory-page
│   ├── feature/new-margin-measure
│   └── fix/rls-region-filter
```

**Workflow:**
1. Create feature branch from `develop`
2. Make changes in Power BI Desktop (or text editor for TMDL/JSON)
3. Commit and push changes
4. Create pull request → code review by team
5. Merge to `develop` → deploy to Test workspace
6. Merge to `main` → deploy to Production workspace

### Git Best Practices for PBIP

| Practice | Reason |
|---|---|
| Commit semantic model + report together | Keep them in sync |
| Use meaningful commit messages | "Add YoY growth measure" not "update" |
| Review TMDL diffs in PRs | Catch unintended model changes |
| Never commit .pbix files | Binary format, not diff-able |
| Store themes in repo | Track visual identity changes |

---

## Fabric Deployment Pipelines

Fabric deployment pipelines promote content across workspaces automatically.

### Pipeline Setup

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Development  │────►│    Test      │────►│ Production   │
│  Workspace   │     │  Workspace   │     │  Workspace   │
└─────────────┘     └─────────────┘     └─────────────┘
     Stage 1              Stage 2              Stage 3
```

### Configuration Steps

1. **Create pipeline** in Fabric portal → Deployment Pipelines
2. **Assign workspaces** to each stage (Dev, Test, Prod)
3. **Configure rules** — parameter and connection string overrides per stage:

| Rule Type | Use Case |
|---|---|
| Data source rules | Different DB server per environment |
| Parameter rules | Change RangeStart/RangeEnd for incremental refresh |
| Connection rules | Different credentials per environment |

### Deployment Best Practices

| Practice | Detail |
|---|---|
| Deploy semantic model first | Reports depend on the model |
| Use deployment rules for connections | Never hardcode prod credentials in dev |
| Test after each deployment | Validate data refresh + report rendering |
| Keep stage parity | Same capacity SKU for Test and Prod |
| Document deployment steps | Runbook for deployment sequence |

---

## CI/CD with PBIP and Azure DevOps / GitHub Actions

### Automated Validation Pipeline

```yaml
# Example: GitHub Actions workflow for PBIP validation
name: Validate PBIP
on:
  pull_request:
    paths:
      - '**.Report/**'
      - '**.SemanticModel/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate report JSON schemas
        run: |
          # Run JSON schema validation against Microsoft schemas
          npx ajv-cli validate -s schemas/report.schema.json -d "*.Report/definition/report.json"

      - name: Check TMDL syntax
        run: |
          # Use Tabular Editor CLI for TMDL validation
          dotnet tool install -g TabularEditor.TOM
          # Validate model definition
```

### Automated Deployment

```yaml
# Deploy to Fabric workspace via REST API
- name: Deploy to Fabric
  env:
    FABRIC_TOKEN: ${{ secrets.FABRIC_TOKEN }}
    WORKSPACE_ID: ${{ secrets.PROD_WORKSPACE_ID }}
  run: |
    # Use Fabric REST API to update semantic model
    # POST /v1/workspaces/{workspaceId}/items/{itemId}/updateDefinition
```

---

## Environment Strategy

### Workspace Naming Convention

```
[Team]-[Project]-[Environment]

Examples:
  BI-Sales-Dev
  BI-Sales-Test
  BI-Sales-Prod
```

### Environment Configuration Matrix

| Setting | Development | Test | Production |
|---|---|---|---|
| Data source | Dev DB / sample data | Test DB / full data | Prod DB |
| Refresh schedule | Manual only | Daily | Every 4 hours |
| RLS | Test with dev accounts | Validate with test users | Full production roles |
| Capacity | Shared / F2 | F8+ | F32+ (production SLA) |
| Access | Developers only | QA + stakeholders | All business users |
| Gateway | Dev gateway cluster | Test gateway | Prod gateway cluster |

---

## Tabular Editor Integration

Tabular Editor (free or paid) is the primary external tool for TMDL editing
and model deployment.

### Common Operations

| Operation | Command |
|---|---|
| Open model | File → Open → Model from Folder (TMDL) |
| Deploy to workspace | Model → Deploy → Select workspace |
| Script changes | C# scripts for bulk operations (rename, add descriptions) |
| Best Practice Analyzer | Run BPA rules to catch model issues before deploy |

### Best Practice Analyzer (BPA) Rules

Configure BPA to run as a pre-deployment gate:

```
Critical rules (block deployment):
□ No calculated columns on fact tables > 1M rows
□ All relationships have referential integrity enabled (Import)
□ No bidirectional cross-filtering without explicit justification
□ All measures have descriptions
□ No unused columns (not referenced by any measure or relationship)

Warning rules (review before deployment):
□ Table names follow naming convention
□ Display folders are configured
□ Date table is marked
□ All key columns are hidden
```

---

## MCP Tools for Deployment

| Tool | Use For |
|---|---|
| `database_operations` (Get) | Export current model state |
| `database_operations` (Deploy) | Deploy model changes to workspace |
| `model_operations` | Inspect model metadata before/after deploy |
| `partition_operations` | Verify partition state post-deployment |
| `fabric-mcp/publicapis_get` | Query deployment pipeline status |
| `fabric-mcp/onelake_item_list` | List workspace items for verification |

---

## Quick Reference

| Task | Approach |
|---|---|
| Version control PBIP | Git with branching strategy |
| Promote across environments | Fabric deployment pipelines |
| Automate validation | CI/CD pipeline with schema checks |
| Bulk model changes | Tabular Editor + C# scripts |
| Pre-deploy quality gate | Best Practice Analyzer rules |
| Parameter per environment | Deployment pipeline rules |
| Monitor deployments | Fabric REST API + deployment history |
