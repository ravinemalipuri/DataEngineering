"""
Export pipeline_spark_config.yaml values back into the Fabric Spark settings workbook.

This is a one-time helper that appends a new sheet called "pipeline_config" listing
every key path/value pair from the generated YAML so the governance spreadsheet can
capture both the original Fabric settings and the derived config.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import yaml


def _flatten_yaml(data: Any, prefix: str = "") -> List[Tuple[str, Any]]:
    entries: List[Tuple[str, Any]] = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            entries.extend(_flatten_yaml(value, new_prefix))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            new_prefix = f"{prefix}[{idx}]"
            entries.extend(_flatten_yaml(item, new_prefix))
    else:
        entries.append((prefix, data))
    return entries


def main() -> None:
    workbook = Path("data/Fabric_Spark_Settings_Variable_Library.xlsx")
    config_path = Path("config/pipeline_spark_config.yaml")

    if not workbook.exists():
        raise FileNotFoundError(f"Workbook not found at {workbook}")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle) or {}

    flattened = _flatten_yaml(cfg)
    df = pd.DataFrame(flattened, columns=["KeyPath", "Value"])
    df["Source"] = "pipeline_spark_config"

    with pd.ExcelWriter(
        workbook,
        engine="openpyxl",
        mode="a",
        if_sheet_exists="replace",
    ) as writer:
        df.to_excel(writer, sheet_name="pipeline_config", index=False)


if __name__ == "__main__":
    main()

