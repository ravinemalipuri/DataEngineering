"""
Metadata repository access layer.
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional, Tuple

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from .models import ColumnMetadata, SourceObjectConfig


class MetadataRepository:
    """Thin JDBC-based access layer for metadata_db."""

    def __init__(self, spark: SparkSession, config: Dict):
        self.spark = spark
        self.jdbc = config["jdbc"]
        self.tables = config["tables"]

    def _jdbc_reader(self, table: str):
        return (
            self.spark.read.format("jdbc")
            .option("url", self.jdbc["url"])
            .option("user", self.jdbc["user"])
            .option("password", self.jdbc["password"])
            .option("driver", self.jdbc.get("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver"))
            .option("dbtable", table)
        )

    def _write_df(self, df: DataFrame, table: str, mode: str = "append") -> None:
        (
            df.write.format("jdbc")
            .mode(mode)
            .option("url", self.jdbc["url"])
            .option("user", self.jdbc["user"])
            .option("password", self.jdbc["password"])
            .option("driver", self.jdbc.get("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver"))
            .option("dbtable", table)
            .save()
        )

    def load_source_object(self, source_system: str, source_object: str) -> SourceObjectConfig:
        table = self.tables["source_objects_view"]
        df = (
            self._jdbc_reader(table)
            .filter(F.col("source_system_name") == source_system)
            .filter(F.col("source_object_name") == source_object)
        )
        rows = df.limit(1).collect()
        if not rows:
            raise ValueError(f"Source object metadata not found for {source_system}.{source_object}")
        row = rows[0]
        return SourceObjectConfig(
            source_object_id=row.source_object_id,
            source_system=row.source_system_name,
            source_object_name=row.source_object_name,
            target_layer=row.target_layer,
            target_path=row.target_path,
            load_type=row.load_type,
            hash_strategy=row.hash_strategy,
            business_keys=json.loads(row.business_keys or "[]"),
            watermark_column=row.watermark_column,
            dq_enabled=bool(row.dq_enabled),
            profiling_enabled=bool(row.profiling_enabled),
            dq_fail_behavior=row.dq_fail_behavior,
            schema_compat_profile=row.schema_compat_profile,
            quarantine_path=row.quarantine_path,
            load_frequency=getattr(row, "load_frequency", "DAILY"),
        )

    def load_columns(self, source_object_id: int) -> List[ColumnMetadata]:
        table = self.tables["source_object_columns"]
        df = self._jdbc_reader(table).filter(F.col("source_object_id") == source_object_id)
        return [
            ColumnMetadata(
                clean_column_name=row.clean_column_name,
                raw_column_name=row.raw_column_name,
                data_type=row.data_type.lower(),
                nullable_flag=bool(row.nullable_flag),
                dq_rules=json.loads(row.dq_rule_set or "{}"),
                dq_severity=row.dq_severity,
            )
            for row in df.collect()
        ]

    def list_active_source_objects(
        self,
        target_layer: Optional[str] = "BRONZE",
        load_types: Optional[List[str]] = None,
        only_active: bool = True,
    ) -> List[Tuple[str, str]]:
        table = self.tables["source_objects_view"]
        reader = self._jdbc_reader(table)
        if target_layer:
            reader = reader.filter(F.col("target_layer") == target_layer)
        if load_types:
            reader = reader.filter(F.col("load_type").isin(load_types))
        if only_active:
            reader = reader.filter(F.col("is_active") == 1)
        rows = reader.select("source_system_name", "source_object_name").collect()
        return [(row.source_system_name, row.source_object_name) for row in rows]

    def persist_schema_snapshot(self, source_object_id: int, run_id: str, schema_json: Dict) -> None:
        table = self.tables["schema_history"]
        rows = []
        for field in schema_json.get("fields", []):
            rows.append(
                (
                    source_object_id,
                    run_id,
                    field["name"],
                    field["type"],
                    bool(field.get("nullable", True)),
                )
            )
        if rows:
            snapshot_df = self.spark.createDataFrame(
                rows, ["source_object_id", "run_id", "column_name", "data_type", "nullable_flag"]
            ).withColumn("captured_time", F.current_timestamp())
            self._write_df(snapshot_df, table)

    def log_schema_change(
        self,
        source_object_id: int,
        run_id: str,
        detail: str,
        compatibility_flag: str,
        action: str,
    ) -> None:
        table = self.tables["schema_change_log"]
        payload = self.spark.createDataFrame(
            [(source_object_id, run_id, detail, compatibility_flag, action)],
            schema="""
                source_object_id INT,
                run_id STRING,
                change_detail STRING,
                compatibility_flag STRING,
                action_taken STRING
            """,
        ).withColumn("logged_time", F.current_timestamp())
        self._write_df(payload, table)

    def write_dq_results(self, df: DataFrame) -> None:
        self._write_df(df, self.tables["data_quality_results"])

    def write_profiling_results(self, df: DataFrame) -> None:
        self._write_df(df, self.tables["data_profiling_results"])

    def write_observability_metrics(self, df: DataFrame) -> None:
        table = self.tables.get("observability_metrics")
        if table:
            self._write_df(df, table)








