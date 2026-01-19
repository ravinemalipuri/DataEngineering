"""
Fabric-friendly incremental bronze load configured via metadata.

Default arguments mirror the expected environment so the notebook can be
reused without explicitly passing parameters.
"""

from __future__ import annotations

import argparse
from datetime import datetime

from . import move_src_to_bronze


def build_parser() -> argparse.ArgumentParser:
    default_run_id = datetime.utcnow().strftime("fabric-%Y%m%dT%H%M%SZ")
    parser = argparse.ArgumentParser(description="Fabric bronze load runner")
    parser.add_argument("--config-file", default="config/pipeline_config.yaml")
    parser.add_argument("--run-id", default=default_run_id)
    parser.add_argument("--source-system", default="DB2_CORE")
    parser.add_argument("--source-object", default="DB2.CUSTOMER")
    parser.add_argument("--compute", default="FABRIC_LAKEHOUSE")
    parser.add_argument("--catalog", default="lakehouse")
    parser.add_argument("--database", default="bronze")
    parser.add_argument("--lakehouse-home-path", default="/hyonelake/lh_aftersales/home/files")
    return parser


def main():
    args = build_parser().parse_args()
    move_src_to_bronze.run_pipeline(args)


if __name__ == "__main__":
    main()

