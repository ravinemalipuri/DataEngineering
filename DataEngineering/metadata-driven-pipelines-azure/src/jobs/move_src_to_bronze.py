"""
Metadata-driven ingestion entry point (clean orchestration).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
import traceback
from datetime import datetime

from pyspark.sql import SparkSession

from framework import (
    ComputeResolver,
    ConfigLoader,
    DataQualityEngine,
    EmailNotifier,
    IngestionResult,
    LoadStrategyExecutor,
    MetadataRepository,
    ObservabilityRecorder,
    PathBuilder,
    SchemaManager,
    SourceReader,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("metadata_ingestion")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Metadata-driven ingestion runner")
    parser.add_argument("--config-file", default="config/pipeline_config.yaml")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-system", required=True)
    parser.add_argument("--source-object", required=True)
    parser.add_argument("--compute", help="Override compute profile from config", default=None)
    parser.add_argument("--catalog", default="lakehouse")
    parser.add_argument("--database", default="bronze")
    parser.add_argument("--lakehouse-home-path", default=None)
    return parser


def run_pipeline(args):
    run_ctx = {
        "run_id": args.run_id,
        "ingest_dt": datetime.utcnow().strftime("%Y-%m-%d"),
        "catalog": args.catalog,
        "database": args.database,
    }
    start_ts = time.time()

    cfg = ConfigLoader(args.config_file)
    notifier = EmailNotifier(cfg.notifications())
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()

    ComputeResolver(cfg.fabric()).resolve(args.compute)
    metadata_repo = MetadataRepository(spark, cfg.metadata_store())
    storage_paths = dict(cfg.storage_paths())
    if args.lakehouse_home_path:
        storage_paths["root"] = args.lakehouse_home_path
    path_builder = PathBuilder(storage_paths)
    source_cfg = metadata_repo.load_source_object(args.source_system, args.source_object)
    column_meta = metadata_repo.load_columns(source_cfg.source_object_id)

    reader = SourceReader(spark, cfg.sources())
    raw_df = reader.read(source_cfg)
    clean_df = SchemaManager.cleanse_source_schema(raw_df)
    landing_path = path_builder.landing_path(source_cfg, run_ctx)
    clean_df.write.mode("overwrite").format(storage_paths["landing_format"]).save(landing_path)

    compat_profiles = cfg.metadata_store().get("compatibility_profiles", {})
    compat_profile = compat_profiles.get(source_cfg.schema_compat_profile, {"auto_add_columns": True})
    schema_manager = SchemaManager(metadata_repo)
    schema_diff = schema_manager.compare(column_meta, clean_df, compat_profile)
    if schema_diff["incompatible"]:
        metadata_repo.log_schema_change(
            source_cfg.source_object_id,
            run_ctx["run_id"],
            json.dumps(schema_diff["incompatible"]),
            "INCOMPATIBLE",
            "PIPELINE_FAILED",
        )
        clean_df.write.mode("overwrite").parquet(path_builder.quarantine_path(source_cfg, run_ctx))
        raise RuntimeError(f"Incompatible schema change detected: {schema_diff['incompatible']}")

    bronze_table = path_builder.bronze_table(source_cfg, run_ctx)
    schema_manager.apply_compatible_changes(bronze_table, schema_diff)
    metadata_repo.persist_schema_snapshot(
        source_cfg.source_object_id, run_ctx["run_id"], json.loads(clean_df.schema.json())
    )

    loader = LoadStrategyExecutor(spark, source_cfg)
    written_df = loader.execute(clean_df, bronze_table)

    dq_engine = DataQualityEngine(spark, metadata_repo)
    dq_engine.run_checks(written_df, source_cfg, column_meta, run_ctx["run_id"], layer="BRONZE")

    duration = time.time() - start_ts
    result = IngestionResult(
        success=True,
        rows_read=clean_df.count(),
        rows_written=written_df.count(),
        dq_failures=dq_engine.last_failure_count,
        landing_path=landing_path,
        bronze_table=bronze_table,
        duration_seconds=duration,
        schema_actions=schema_diff,
    )

    observability = ObservabilityRecorder(
        spark, metadata_repo, cfg.observability().get("metrics_table")
    )
    observability.record(
        {
            "run_id": run_ctx["run_id"],
            "source_object_id": source_cfg.source_object_id,
            "rows_read": result.rows_read,
            "rows_written": result.rows_written,
            "duration_seconds": result.duration_seconds,
            "schema_actions": result.schema_actions,
            "dq_failures": result.dq_failures,
        }
    )

    notifier.notify(
        success=True,
        subject_suffix=f"{source_cfg.source_system}.{source_cfg.source_object_name}",
        body=(
            f"Run {run_ctx['run_id']} completed.\n"
            f"Compute: {args.compute or cfg.fabric().get('default_compute')}\n"
            f"Rows read: {result.rows_read}\n"
            f"Rows written: {result.rows_written}\n"
            f"DQ failures: {result.dq_failures}\n"
            f"Landing path: {result.landing_path}\n"
            f"Bronze table: {result.bronze_table}\n"
            f"Duration (s): {result.duration_seconds:.2f}"
        ),
    )


def main():
    args = build_argument_parser().parse_args()
    try:
        run_pipeline(args)
    except Exception as exc:  # pylint: disable=broad-except
        cfg = ConfigLoader(args.config_file)
        notifier = EmailNotifier(cfg.notifications())
        error_trace = traceback.format_exc()
        notifier.notify(
            success=False,
            subject_suffix=f"{args.source_system}.{args.source_object}",
            body=f"Run {args.run_id} failed with error: {exc}\n\n{error_trace}",
        )
        raise


if __name__ == "__main__":
    main()








