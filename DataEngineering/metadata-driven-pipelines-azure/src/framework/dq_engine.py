"""
Metadata-driven Data Quality engine.
"""

from __future__ import annotations

import json
from typing import Dict, List

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from .models import ColumnMetadata, SourceObjectConfig


class DataQualityEngine:
    """Executes metadata-driven DQ rules and writes results."""

    def __init__(self, spark: SparkSession, metadata_repo):
        self.spark = spark
        self.meta = metadata_repo
        self.last_failure_count = 0

    def run_checks(
        self,
        df: DataFrame,
        source_cfg: SourceObjectConfig,
        columns: List[ColumnMetadata],
        run_id: str,
        layer: str,
    ) -> None:
        if not source_cfg.dq_enabled:
            return

        dq_records = []
        row_count = df.count()
        for col_meta in columns:
            for rule_name, params in (col_meta.dq_rules or {}).items():
                status, metrics, failures = self._execute_rule(df, col_meta.clean_column_name, rule_name, params)
                dq_records.append(
                    (
                        run_id,
                        source_cfg.source_object_id,
                        layer,
                        col_meta.clean_column_name,
                        rule_name,
                        json.dumps(params or {}),
                        status,
                        json.dumps(metrics),
                        failures,
                        row_count,
                        col_meta.dq_severity,
                    )
                )
                self.last_failure_count += failures
                if status == "FAIL" and (col_meta.dq_severity == "FAIL" or source_cfg.dq_fail_behavior == "FAIL"):
                    raise RuntimeError(f"DQ failure: {col_meta.clean_column_name} - {rule_name}")

        if dq_records:
            dq_df = self.spark.createDataFrame(
                dq_records,
                schema="""
                    run_id STRING,
                    source_object_id INT,
                    layer STRING,
                    column_name STRING,
                    check_type STRING,
                    check_params STRING,
                    status STRING,
                    metric_value STRING,
                    failure_count BIGINT,
                    row_count BIGINT,
                    dq_severity STRING
                """,
            ).withColumn("run_time", F.current_timestamp())
            self.meta.write_dq_results(dq_df)

    def _execute_rule(self, df: DataFrame, column: str, rule: str, params: Dict):
        if rule == "NOT_NULL":
            failure_count = df.filter(F.col(column).isNull()).count()
            status = "PASS" if failure_count == 0 else "FAIL"
            return status, {"null_count": failure_count}, failure_count
        if rule == "VALID_VALUES":
            allowed = params.get("values", [])
            failure_count = df.filter(~F.col(column).isin(allowed)).count()
            status = "PASS" if failure_count == 0 else "FAIL"
            return status, {"invalid_count": failure_count}, failure_count
        if rule == "RANGE_CHECK":
            min_value = params.get("min")
            max_value = params.get("max")
            expr = F.lit(True)
            if min_value is not None:
                expr = expr & (F.col(column) >= F.lit(min_value))
            if max_value is not None:
                expr = expr & (F.col(column) <= F.lit(max_value))
            failure_count = df.filter(~expr).count()
            status = "PASS" if failure_count == 0 else "FAIL"
            return status, {"out_of_range": failure_count}, failure_count
        return "PASS", {}, 0

