"""
Utilities to capture run metrics / observability signals.
"""

from __future__ import annotations

import json
from typing import Dict

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


class ObservabilityRecorder:
    def __init__(self, spark: SparkSession, metadata_repo, metrics_table: str | None):
        self.spark = spark
        self.metadata_repo = metadata_repo
        self.metrics_table = metrics_table

    def record(self, payload: Dict) -> None:
        if not self.metrics_table:
            return
        df = self.spark.createDataFrame(
            [
                (
                    payload["run_id"],
                    payload["source_object_id"],
                    payload.get("rows_read"),
                    payload.get("rows_written"),
                    payload.get("duration_seconds"),
                    json.dumps(payload.get("schema_actions", {})),
                    payload.get("dq_failures", 0),
                )
            ],
            schema="""
                run_id STRING,
                source_object_id INT,
                rows_read BIGINT,
                rows_written BIGINT,
                duration_seconds DOUBLE,
                schema_actions STRING,
                dq_failures BIGINT
            """,
        ).withColumn("run_time", F.current_timestamp())
        self.metadata_repo.write_observability_metrics(df)








