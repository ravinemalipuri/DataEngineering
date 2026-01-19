"""
Fabric-specific wrapper that orchestrates bronze runs via metadata.

Defaults are chosen so the module can be triggered with minimal configuration.
"""

from __future__ import annotations

import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Tuple

from pyspark.sql import SparkSession

from framework.config_loader import ConfigLoader
from framework.metadata_repository import MetadataRepository
from . import move_src_to_bronze

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger("fabric_bronze_wrapper")


def _default_run_id() -> str:
    return datetime.utcnow().strftime("fabric-wrapper-%Y%m%dT%H%M%SZ")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fabric bronze load wrapper")
    parser.add_argument("--config-file", default="config/pipeline_config.yaml")
    parser.add_argument("--run-id", default=_default_run_id())
    parser.add_argument("--compute", default="FABRIC_LAKEHOUSE")
    parser.add_argument("--catalog", default="lakehouse")
    parser.add_argument("--database", default="bronze")
    parser.add_argument("--lakehouse-home-path", default="/hyonelake/lh_aftersales/home/files")
    parser.add_argument("--parallel-jobs", type=int, default=3)
    parser.add_argument("--target-layer", default="BRONZE")
    parser.add_argument("--load-types", default="FULL,INCREMENTAL,HYBRID")
    return parser


def _build_child_run_id(base_run_id: str, source_system: str, source_object: str) -> str:
    clean_system = source_system.replace(".", "_")
    clean_object = source_object.replace(".", "_")
    return f"{base_run_id}-{clean_system}-{clean_object}"


def _prepare_namespace(
    args: argparse.Namespace, source_system: str, source_object: str
) -> argparse.Namespace:
    return argparse.Namespace(
        config_file=args.config_file,
        run_id=_build_child_run_id(args.run_id, source_system, source_object),
        source_system=source_system,
        source_object=source_object,
        compute=args.compute,
        catalog=args.catalog,
        database=args.database,
        lakehouse_home_path=args.lakehouse_home_path,
    )


def _run_for_source(
    args: argparse.Namespace, source_system: str, source_object: str
) -> Tuple[str, str, bool, str]:
    ns = _prepare_namespace(args, source_system, source_object)
    try:
        move_src_to_bronze.run_pipeline(ns)
        return source_system, source_object, True, ""
    except Exception as exc:  # pragma: no cover - logging wrapper
        LOGGER.exception("Run failed for %s.%s", source_system, source_object)
        return source_system, source_object, False, str(exc)


def _discover_sources(
    metadata_repo: MetadataRepository, target_layer: str, load_types: List[str]
) -> List[Tuple[str, str]]:
    return metadata_repo.list_active_source_objects(target_layer=target_layer, load_types=load_types)


def main():
    args = build_parser().parse_args()
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    cfg = ConfigLoader(args.config_file)
    metadata_repo = MetadataRepository(spark, cfg.metadata_store())
    load_types = [l.strip().upper() for l in args.load_types.split(",") if l.strip()]
    target_layer = args.target_layer.upper()
    sources = _discover_sources(metadata_repo, target_layer, load_types)
    if not sources:
        LOGGER.warning("No source objects found for layer=%s load_types=%s", target_layer, load_types)
        return

    LOGGER.info("Discovered %d source objects to run.", len(sources))
    results: List[Tuple[str, str, bool, str]] = []
    with ThreadPoolExecutor(max_workers=args.parallel_jobs) as executor:
        futures = {
            executor.submit(_run_for_source, args, system, obj): (system, obj)
            for system, obj in sources
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "SUCCESS" if result[2] else "FAILED"
            LOGGER.info("%s.%s -> %s", result[0], result[1], status)

    failed = [res for res in results if not res[2]]
    if failed:
        LOGGER.error("Wrapper run completed with %d failures.", len(failed))
        for system, obj, _, reason in failed:
            LOGGER.error("  %s.%s -> %s", system, obj, reason)
        raise SystemExit(1)
    LOGGER.info("Wrapper run completed without failures.")


if __name__ == "__main__":
    main()

