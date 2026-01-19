# Data Pipeline Metrics Model (Azure Data Factory & Fabric)

## Purpose
A unified, metadata-driven model to capture operational and performance metrics for Azure Data Factory (ADF) and Fabric pipelines. Designed to support observability, SLA tracking, cost attribution, and quality monitoring across activities, runs, and resources.

## Current Scope (Pipeline-Level Tables)

### Table: pipeline
- `pipeline_id` (PK, bigint) — internal surrogate key  
- `platform` (string) — enum: `adf`, `fabric`  
- `external_id` (string) — ADF pipeline name / Fabric item id  
- `display_name` (string)  
- `description` (string, nullable)  
- `folder_path` (string, nullable)  
- `tags` (JSON/map, nullable)  
- `owner` (string) — email/UPN  
- `source_repo` (string, URI)  # data factory name or workspace repo link  
- `domain` (string, nullable)  # fabric-specific  
- `sub_domain` (string, nullable)  # fabric-specific  
- `is_active` (bool)  
- `created_time` (datetime)  
- `updated_time` (datetime)

### Table: pipeline_run
- `pipeline_run_id` (PK, bigint) — internal surrogate key  
- `pipeline_id` (FK → pipeline.pipeline_id)  
- `run_external_id` (string) — ADF run id / Fabric run id  
- `trigger_type` (string) — `manual`, `schedule`, `event`, `rerun`  
- `trigger_name` (string, nullable)  
- `start_time` (datetime)  
- `end_time` (datetime, nullable)  
- `duration_ms` (bigint, nullable)  
- `status` (string) — `Succeeded`, `Failed`, `Cancelled`, `Queued`, `InProgress`  
- `error_code` (string, nullable)  
- `error_message` (string, nullable)  
- `retry_count` (int, nullable)  
- `sla_breach` (bool, computed/flag)  
- `data_volume_mb` (decimal, nullable; rollup)  
- `activity_count` (int, nullable)  
- `cost_estimate` (decimal, nullable; currency)  
- `run_parameters` (JSON, nullable)  
- `environment` (string) — `dev`, `test`, `prod`, etc.

### Relationships (in-scope)
- pipeline 1→many pipeline_run

## Future State (not in current tables)
- activity, activity_run (per-activity metrics)
- triggers and trigger_run
- linked_service, dataset
- alerts / data quality checks
- extended cost and compute dimensions

## Notes
- Defaults assume append-only pipeline_run; consider partitioning by start_time.  
- Tags and JSON columns allow platform-specific extensions without schema churn.  
- SLA breach is computed from configured SLA vs `start_time`/`end_time`/`duration_ms`.
