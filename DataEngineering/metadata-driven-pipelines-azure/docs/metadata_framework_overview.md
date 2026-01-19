# Metadata-driven ingestion framework

This project is built around a metadata catalog that drives ingestion behavior end-to-end. The following sections describe the recommended flow for onboarding a new source and how the Fabric scripts tie into each stage.

## 1. Capture metadata

- Load the source/system definitions into the metadata tables (`source_systems`, `source_objects`, `source_object_columns`, etc.). The schema and relationships are documented in `metadata/datamodel/metadata_model.md`.  
- Store load characteristics (load type, hash strategy, business keys, watermark column) in `source_objects`.  
- Store column-level data types, DQ rules, and severities in `source_object_columns`.
- Additional tables such as `schema_compatibility_rules`, `schema_history`, `data_quality_results`, and `data_profiling_results` track governance and runtime results.

## 2. Fabric master pipeline per source

- Each source object references a Fabric compute profile, lakehouse/catalog/database targets, and storage path templates defined in `config/pipeline_config.yaml` or the Fabric-oriented `config/pipeline_spark_config.yaml`.  
- The wrapper entry point `src/jobs/hy_brnz_load_wrapper_fabric.py` discovers all active bronze source objects from metadata and orchestrates parallel runs for each source. It injects shared parameters (lakehouse home path, catalog/database, compute profile, etc.).
- For ad-hoc single-source runs, use `src/jobs/hy_lh_db2_brnz_Incr_Load_fabric.py`, which provides default values and calls the metadata-driven pipeline directly.

## 3. Landing/source load via Fabric data copy

- Sources are read using `src/framework/source_reader.py`, which uses connection profiles defined under `config/pipeline_config.yaml`'s `sources` section (e.g., `DB2_CORE`, `SFDC`).  
- Ingestion writes the raw data to the landing paths (`storage_paths.landing_template`) as Parquet files, ensuring a clean snapshot before Bronze processing (`src/jobs/move_src_to_bronze.py` handles this end-to-end).

## 4. Bronze attachment and delta layer

- `src/jobs/move_src_to_bronze.py` orchestrates the Bronze load:
  - Loads metadata (`SourceObjectConfig`, `ColumnMetadata`) via `src/framework/metadata_repository.py`.  
  - Cleanses schema (`src/framework/schema_manager.py`), compares against stored metadata, and logs schema history/drift.  
  - Executes the load strategy (`src/framework/load_strategy.py`): `FULL` overwrites, `INCREMENTAL` merges via hash key, `HYBRID` appends.  
  - Writes DQ results via `src/framework/dq_engine.py` and records metrics/notifications through `framework/observability.py` and `framework/notifications.py`.
  - Bronze tables are written as Delta tables in the configured catalog/database using dynamically constructed names (`source_system_source_object_bronze`).

## 5. Silver transformation

- Silver loads run a merge-based operation using business keys or hash keys derived from metadata. The existing `LoadStrategyExecutor` can also be extended or replaced with custom Silver logic, but the same metadata catalog drives key selection and compatibility profiles.

## Scripts and helpers

- Generator that translates the Fabric Spark settings workbook into `config/pipeline_spark_config.yaml`: `scripts/generate_pipeline_spark_config.py`.  
- Helper that writes the generated YAML back into the Excel workbook for audit: `scripts/export_pipeline_config_to_xlsx.py`.  
- Bronze wrapper (parallel orchestration): `src/jobs/hy_brnz_load_wrapper_fabric.py`.  
- Single-source launcher (default DB2 customer example): `src/jobs/hy_lh_db2_brnz_Incr_Load_fabric.py`.  
- Metadata-driven Bronze ingestion: `src/jobs/move_src_to_bronze.py`.  
- Core framework components: `src/framework/source_reader.py`, `src/framework/schema_manager.py`, `src/framework/load_strategy.py`, `src/framework/metadata_repository.py`, `src/framework/dq_engine.py`, `src/framework/observability.py`, `src/framework/notifications.py`.

## Governance and configuration flow

- Start by updating the metadata tables, then use the Fabric wrappers to trigger bronze/silver loads.  
- Any gating logic (compute profiles, security settings, pool naming) is centralized in the Excel workbook and captured via the generator into `pipeline_spark_config.yaml`.  
- Notifications, observability metrics, and schema governance tables keep track of each run, while the `PathBuilder` and storage templates ensure all layers write to the correct OneLake paths.

