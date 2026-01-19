"""
Generate a pipeline Spark configuration YAML from the Fabric Spark settings spreadsheet.

This script reads `data/Fabric_Spark_Settings_Variable_Library.xlsx`, extracts the
environment-specific recommendations (dev/test/prod), and merges the resulting
settings into a base `pipeline_config.yaml` so the resulting file can be used by
the ingestion framework while keeping metadata around compute/spark governance
stored in the spreadsheet.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml


ENV_COLUMN_MAP = {
    "dev": "Dev (Recommended)",
    "test": "Test (Recommended)",
    "prod": "Prod (Recommended)",
}


def _cast_value(raw_value: Any, data_type: str) -> Any:
    if pd.isna(raw_value):
        return None
    normalized = str(raw_value).strip() if isinstance(raw_value, str) else raw_value
    dtype = (data_type or "").strip().lower()
    if dtype == "bool":
        lowered = str(normalized).strip().lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        return bool(normalized)
    if dtype == "int":
        try:
            return int(normalized)
        except (ValueError, TypeError):
            try:
                return int(float(normalized))
            except (ValueError, TypeError):
                return normalized
    return normalized


def _assign_nested(dest: Dict[str, Any], keys: list[str], value: Any) -> None:
    for key in keys[:-1]:
        dest = dest.setdefault(key, {})
    dest[keys[-1]] = value


def _build_config(df: pd.DataFrame, env_column: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for _, row in df.iterrows():
        key_path = row.get("KeyPath (Alt)") or row.get("VariableName (Std)")
        if not key_path or not isinstance(key_path, str):
            continue
        normalized_path = key_path.strip()
        if normalized_path.startswith("cfg."):
            normalized_path = normalized_path[len("cfg.") :]
        keys = [part.strip() for part in normalized_path.split(".") if part.strip()]
        if not keys:
            continue
        value = row.get(env_column)
        if pd.isna(value):
            continue
        data_type = row.get("DataType", "")
        casted = _cast_value(value, data_type)
        if casted is None:
            continue
        _assign_nested(result, keys, casted)
    return result


def _merge_dict(target: Dict[str, Any], source: Dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _merge_dict(target[key], value)
        else:
            target[key] = value


def _safe_load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate pipeline Spark config from Fabric settings")
    parser.add_argument(
        "--excel",
        type=Path,
        default=Path("data/Fabric_Spark_Settings_Variable_Library.xlsx"),
        help="Path to the Fabric Spark settings spreadsheet",
    )
    parser.add_argument(
        "--environment",
        choices=sorted(ENV_COLUMN_MAP),
        default="prod",
        help="Which recommended column to use for the generated config",
    )
    parser.add_argument(
        "--base-config",
        type=Path,
        default=Path("config/pipeline_config.yaml"),
        help="Base pipeline config whose sections should be preserved",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("config/pipeline_spark_config.yaml"),
        help="Where to write the merged configuration",
    )
    args = parser.parse_args()

    df = pd.read_excel(args.excel)
    env_column = ENV_COLUMN_MAP[args.environment]
    updates = _build_config(df, env_column)

    base_cfg = _safe_load_yaml(args.base_config)
    _merge_dict(base_cfg, updates)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(base_cfg, handle, sort_keys=False)


if __name__ == "__main__":
    main()

