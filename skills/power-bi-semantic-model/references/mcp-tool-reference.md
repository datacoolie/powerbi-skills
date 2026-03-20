# PowerBI Modeling MCP — Tool Reference

Quick reference mapping modeling tasks to the correct `powerbi-modeling-mcp` tool.

## Model Exploration

| Task | Tool | Typical Action |
|---|---|---|
| Get model overview | `model_operations` | List tables, relationships, model properties |
| List all tables | `table_operations` | Get table names, row counts, storage modes |
| Inspect columns | `column_operations` | Get column details, data types, properties |
| View relationships | `relationship_operations` | List all relationships with cardinality |
| Check measures | `measure_operations` | List existing measures and their expressions |
| View partitions | `partition_operations` | Check data sources and refresh config |
| Check connections | `connection_operations` | View data source connection strings |

## Model Building

| Task | Tool | Key Parameters |
|---|---|---|
| Create table | `table_operations` | Table name, columns, source expression |
| Add column | `column_operations` | Table, column name, data type, properties |
| Create relationship | `relationship_operations` | From/to table+column, cardinality, cross-filter |
| Set storage mode | `partition_operations` | Table, mode (import/directQuery/dual) |
| Configure date table | `calendar_operations` | Mark table as date table, set date column |
| Create named expression | `named_expression_operations` | Shared M expressions / parameters |

## Measure Development

| Task | Tool | Notes |
|---|---|---|
| Create measure | `measure_operations` | Table, name, DAX expression, format string |
| Edit measure | `measure_operations` | Update expression, description, format |
| Delete measure | `measure_operations` | Remove unused measures |
| Test measure (DAX query) | `dax_query_operations` | Run EVALUATE queries to validate |
| Create calculation group | `calculation_group_operations` | Define group + calculation items |
| Run DAX query | `dax_query_operations` | EVALUATE, SUMMARIZE, CALCULATETABLE |

## Security & Governance

| Task | Tool | Notes |
|---|---|---|
| Create RLS role | `security_role_operations` | Role name, table filters (DAX) |
| Edit RLS filter | `security_role_operations` | Update DAX filter expression |
| Test RLS | `dax_query_operations` | Run queries with role context |
| Add perspective | `perspective_operations` | Define table/column visibility per perspective |
| Add translations | `object_translation_operations` | Localize display names |
| Set culture | `culture_operations` | Configure locale settings |

## Advanced Operations

| Task | Tool | Notes |
|---|---|---|
| Create hierarchy | `user_hierarchy_operations` | Define drill-down paths |
| Configure function | `function_operations` | Table-valued functions |
| Query groups | `query_group_operations` | Organize queries in folders |
| Manage transactions | `transaction_operations` | Batch operations atomically |
| Trace operations | `trace_operations` | Monitor query execution |
| Database settings | `database_operations` | Compatibility level, options |

## Fabric & Data Source Tools

| Task | Tool (non-modeling) | Notes |
|---|---|---|
| Browse lakehouse tables | `fabric-notebook-mcp/list_artifacts` | Find available data |
| Preview table data | `fabric-notebook-mcp/preview_lakehouse_table` | Inspect rows |
| Get column statistics | `fabric-notebook-mcp/get_table_column_stats` | Cardinality, nulls |
| Query SQL source | `ms-mssql.mssql/mssql_run_query` | Explore gold layer |
| List SQL tables | `ms-mssql.mssql/mssql_list_tables` | Find available tables |
| Browse OneLake files | `fabric-mcp/onelake_file_list` | Delta tables, files |
| Get Fabric best practices | `fabric-mcp/publicapis_bestpractices_get` | Official patterns |

## Microsoft Learn Research

| Task | Tool | Query Examples |
|---|---|---|
| Search docs | `microsoft-learn-mcp/microsoft_docs_search` | "Power BI star schema", "DirectLake mode" |
| Get code samples | `microsoft-learn-mcp/microsoft_code_sample_search` | "Power BI composite model" |
| Fetch full article | `microsoft-learn-mcp/microsoft_docs_fetch` | Specific URL from search results |
