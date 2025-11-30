# Metadata Model Overview

This document summarizes the logical relationships across metadata tables that drive the ingestion framework.

## Entities

- `$(SchemaName).source_systems`: Master data for upstream platforms along with credential references.
- `$(SchemaName).source_objects`: Per-table/file ingestion configuration, linked to `source_systems`.
- `$(SchemaName).source_object_columns`: Column-level metadata and DQ configuration for each `source_object`.
- `$(SchemaName).schema_history`: Time-series snapshots of source schemas captured at runtime.
- `$(SchemaName).schema_change_log`: Audit log for detected schema drifts and framework decisions.
- `$(SchemaName).schema_compatibility_rules`: Named policies that classify schema differences as compatible vs. incompatible.
- `$(SchemaName).data_quality_results`: Persisted outcomes for rule-based DQ checks.
- `$(SchemaName).data_profiling_results`: Stores profiling metrics (min/max, distinct counts, etc.) captured at configurable cadences.

## Relationships

```text
source_systems (1) ────< source_objects (1) ────< source_object_columns
                             │                         │
                             │                         └── DQ & profiling rules drive runtime checks
                             │
                             ├───< schema_history (per run schema snapshots)
                             ├───< schema_change_log (drift events)
                             ├───< data_quality_results (per run DQ outcomes)
                             └───< data_profiling_results (profiling metrics)

schema_compatibility_rules (1) ────< source_objects (via schema_compat_profile)
```

## Usage Notes

1. **Schema governance**  
   - Store the last approved schema in `source_object_columns`.  
   - Each run captures the live schema in `schema_history` within the chosen schema and compares against stored metadata using the compatibility profile referenced by the source object.

2. **Load strategy metadata**  
   - `source_objects` holds `load_type`, `hash_strategy`, `business_keys`, and `watermark_column` to drive incremental vs. full behavior.

3. **Data quality & profiling orchestration**  
   - DQ rules are stored per column as JSON in `source_object_columns.dq_rule_set`.  
   - Execution outcomes are appended to `data_quality_results`, honoring severities defined at the column level (`dq_severity`) and the source-level fail policy (`dq_fail_behavior`).  
   - Profiling metrics land in `data_profiling_results`, often on a lower frequency than DQ.

4. **Extensibility**  
   - Add more helper tables (e.g., `dq_rule_catalog`, `run_audit`) as needed; the core relationships above remain consistent irrespective of database/schema supplied at deployment time.  
   - Sample seed data for each table lives under `metadata/dml/` to accelerate environment bootstrap.

