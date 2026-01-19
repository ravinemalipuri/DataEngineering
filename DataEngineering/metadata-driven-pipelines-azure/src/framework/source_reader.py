"""
Source reading utilities driven by config profiles.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession

from .models import SourceObjectConfig


class SourceReader:
    """Reads source data using connection info defined in pipeline config."""

    def __init__(self, spark: SparkSession, source_profiles):
        self.spark = spark
        self.profiles = source_profiles

    def read(self, source_cfg: SourceObjectConfig) -> DataFrame:
        profile = self.profiles.get(source_cfg.source_system)
        if not profile:
            raise ValueError(f"No source profile configured for {source_cfg.source_system}")
        fmt = profile["format"]
        options = dict(profile.get("options", {}))
        if fmt == "jdbc":
            options["dbtable"] = options.get("dbtable_template", "{object_name}").format(
                object_name=source_cfg.source_object_name
            )
            return self.spark.read.format("jdbc").options(**options).load()
        if fmt == "rest":
            raise NotImplementedError("REST ingestion is not implemented in this sample.")
        raise ValueError(f"Unsupported source format {fmt}")








