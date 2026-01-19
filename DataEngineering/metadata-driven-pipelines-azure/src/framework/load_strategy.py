""
"Load strategy implementations (full, incremental, hybrid)."
""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from .models import SourceObjectConfig


class LoadStrategyExecutor:
    """Supports full, incremental, and hybrid load behaviours."""

    def __init__(self, spark: SparkSession, source_cfg: SourceObjectConfig):
        self.spark = spark
        self.cfg = source_cfg

    def execute(self, df: DataFrame, target_table: str) -> DataFrame:
        if self.cfg.load_type == "FULL":
            return self._full_load(df, target_table)
        if self.cfg.load_type == "INCREMENTAL":
            return self._incremental_load(df, target_table)
        return self._hybrid_load(df, target_table)

    def _full_load(self, df: DataFrame, table: str) -> DataFrame:
        df.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(table)
        return df

    def _incremental_load(self, df: DataFrame, table: str) -> DataFrame:
        if self.cfg.hash_strategy == "ROW_HASH":
            df = df.withColumn("_md5_hash", F.md5(F.concat_ws("||", *df.columns)))
        elif self.cfg.hash_strategy == "KEY_HASH":
            cols = [F.col(col) for col in self.cfg.business_keys]
            df = df.withColumn("_md5_hash", F.md5(F.concat_ws("||", *cols)))

        if not self.spark.catalog.tableExists(table):
            df.write.format("delta").mode("append").saveAsTable(table)
            return df

        temp_view = f"source_{table.replace('.', '_')}"
        df.createOrReplaceTempView(temp_view)
        merge_condition = " AND ".join([f"target.{c} = source.{c}" for c in self.cfg.business_keys])
        merge_sql = f"""
        MERGE INTO {table} AS target
        USING {temp_view} AS source
            ON {merge_condition}
        WHEN MATCHED AND target._md5_hash <> source._md5_hash THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
        """
        self.spark.sql(merge_sql)
        return self.spark.table(table)

    def _hybrid_load(self, df: DataFrame, table: str) -> DataFrame:
        df.write.format("delta").mode("append").saveAsTable(table)
        return df








