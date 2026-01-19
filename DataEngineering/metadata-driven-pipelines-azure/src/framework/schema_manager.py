"""
Schema comparison utilities.
"""

from __future__ import annotations

from typing import Dict, Iterable, List

from pyspark.sql import DataFrame, SparkSession

from .models import ColumnMetadata


class SchemaManager:
    """Compares schemas and applies compatible changes."""

    def __init__(self, metadata_repo):
        self.meta = metadata_repo
        self.spark = SparkSession.getActiveSession()

    @staticmethod
    def cleanse_source_schema(df: DataFrame) -> DataFrame:
        for col in df.columns:
            clean = col.replace("#", "").replace(" ", "_")
            if clean != col:
                df = df.withColumnRenamed(col, clean)
        return df

    @staticmethod
    def _is_widen(new_type: str, old_type: str) -> bool:
        widening_rules = {
            ("int", "bigint"),
            ("smallint", "int"),
            ("float", "double"),
            ("decimal(18,2)", "decimal(38,4)"),
        }
        return new_type.lower() == old_type.lower() or (old_type.lower(), new_type.lower()) in widening_rules

    def compare(self, stored: Iterable[ColumnMetadata], current_df: DataFrame, compat_profile: Dict) -> Dict:
        stored_map = {col.clean_column_name.lower(): col for col in stored}
        current_fields = {field.name.lower(): (field.dataType.simpleString(), field.nullable) for field in current_df.schema.fields}

        diff = {"additions": [], "widenings": [], "incompatible": [], "dropped": []}

        for col_name, (dtype, nullable) in current_fields.items():
            if col_name not in stored_map:
                if compat_profile.get("auto_add_columns", True):
                    diff["additions"].append((col_name, dtype, nullable))
                else:
                    diff["incompatible"].append(f"Column {col_name} missing in metadata (auto-add disabled).")
                continue

            stored_meta = stored_map[col_name]
            if dtype.lower() != stored_meta.data_type.lower():
                if compat_profile.get("allow_type_widen", True) and self._is_widen(dtype, stored_meta.data_type):
                    diff["widenings"].append((col_name, stored_meta.data_type, dtype))
                else:
                    diff["incompatible"].append(f"Type change {stored_meta.data_type}->{dtype} for {col_name}")

            if stored_meta.nullable_flag is False and nullable and not compat_profile.get("allow_nullable_change", True):
                diff["incompatible"].append(f"Nullable change detected for {col_name}")

        for col_name in stored_map:
            if col_name not in current_fields:
                if compat_profile.get("allow_column_drop", False):
                    diff["dropped"].append(col_name)
                else:
                    diff["incompatible"].append(f"Column {col_name} dropped in source")

        return diff

    def apply_compatible_changes(self, table: str, diff: Dict) -> None:
        if not self.spark:
            return
        for col_name, dtype, _ in diff["additions"]:
            stmt = f"ALTER TABLE {table} ADD COLUMNS ({col_name} {dtype})"
            self.spark.sql(stmt)
        for col_name, _, new_type in diff["widenings"]:
            stmt = f"ALTER TABLE {table} ALTER COLUMN {col_name} {new_type}"
            self.spark.sql(stmt)








