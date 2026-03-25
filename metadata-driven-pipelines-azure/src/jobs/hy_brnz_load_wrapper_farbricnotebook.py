"""
Notebook helper that fetches the full-FULL-source list that ran today so the
Fabric wrapper logic can re-use the same metadata-driven filtering.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from pyspark.sql import DataFrame, SparkSession

from framework.config_loader import ConfigLoader


def _resolve_table_name(metadata_tables: Dict[str, str], key: str, default: str) -> str:
    """Return either the configured table name or fall back to the default."""
    return metadata_tables.get(key, default)


def build_todays_full_run_sql(metadata_tables: Dict[str, str]) -> str:
    """
    Return a SQL statement that only brings back today's FULL runs that were not skipped.

    The query joins the source_objects projection (view) with the Fabric pipeline
    run metrics table so we can filter on `is_active`, `load_type = 'FULL'`, and
    `skip_load = 0`. Batch runs are filtered by the date portion of
    `batch_load_datetime` so it matches today's date.
    """
    source_objects_view = _resolve_table_name(
        metadata_tables, "source_objects_view", "[metadata_db].[dbo].[vw_source_objects]"
    )
    pipeline_metrics_table = _resolve_table_name(
        metadata_tables, "pipeline_run_metrics", "[metadata_db].[dbo].[vw_pipeline_run_metrics]"
    )

    return f"""
SELECT
    so.source_system_name,
    so.source_object_name,
    prm.pipeline_start_time,
    prm.batch_load_datetime,
    prm.skip_load
FROM {source_objects_view} AS so
INNER JOIN {pipeline_metrics_table} AS prm
    ON prm.source_system_name = so.source_system_name
    AND prm.source_object_name = so.source_object_name
WHERE CAST(prm.batch_load_datetime AS DATE) = CAST(GETDATE() AS DATE)
  AND so.is_active = 1
  AND so.load_type = 'FULL'
  AND prm.skip_load = 0
"""


def read_todays_full_runs(
    config_file: str = "config/pipeline_config.yaml",
    spark_session: Optional[SparkSession] = None,
) -> DataFrame:
    """
    Execute the query over JDBC so a notebook or Fabric orchestration flow can
    consume the list of (system, object) pairs that ran today.
    """
    spark = spark_session or SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    cfg = ConfigLoader(config_file)
    metadata_store = cfg.metadata_store()

    jdbc_opts = metadata_store["jdbc"]
    sql = build_todays_full_run_sql(metadata_store["tables"])

    return (
        spark.read.format("jdbc")
        .option("url", jdbc_opts["url"])
        .option("user", jdbc_opts["user"])
        .option("password", jdbc_opts["password"])
        .option("driver", jdbc_opts.get("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver"))
        .option("dbtable", f"({sql}) AS todays_full_runs")
        .load()
    )


def list_todays_full_runs(
    config_file: str = "config/pipeline_config.yaml", spark_session: Optional[SparkSession] = None
) -> List[Tuple[str, str]]:
    """
    Return a list of (source_system, source_object) tuples for all today's FULL,
    non-skipped runs that are marked active.
    """
    df = read_todays_full_runs(config_file=config_file, spark_session=spark_session)
    return [(row.source_system_name, row.source_object_name) for row in df.collect()]


DEFAULT_BRONZE_SOURCE_PATH = (
    "abfss://a12345b-e12d-123c-bc1f-123456@onelake.dfs.fabric.microsoft.com/"
    "3abc9de1-811a-4078-9a07-e71380149847/Files/src/db2l/"
)


def resolve_bronze_source_path(variable_library: Optional[Dict[str, str]] = None) -> str:
    """
    Return the path used for testing. Prefer the `bronzeSrcPath` value from the
    Fabric variables library, fallback to a hard-coded default for notebooks.
    """
    if variable_library is None:
        return DEFAULT_BRONZE_SOURCE_PATH
    return variable_library.get("bronzeSrcPath", DEFAULT_BRONZE_SOURCE_PATH)


def read_source_parquet(
    spark_session: Optional[SparkSession] = None,
    source_path: Optional[str] = None,
    variable_library: Optional[Dict[str, str]] = None,
) -> DataFrame:
    """
    Read the parquet data for the notebook proof-of-concept. The path comes
    from the variable library when available, otherwise the default constant.
    """
    spark = spark_session or SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    path = source_path or resolve_bronze_source_path(variable_library)
    return spark.read.format("parquet").load(path)


if __name__ == "__main__":
    df = read_todays_full_runs()
    print("Today's FULL, non-skipped run list:")
    df.show(truncate=False)
