"""
Dataclasses shared across the ingestion framework modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class SourceObjectConfig:
    source_object_id: int
    source_system: str
    source_object_name: str
    target_layer: str
    target_path: str
    load_type: str
    hash_strategy: str
    business_keys: List[str]
    watermark_column: Optional[str]
    dq_enabled: bool
    profiling_enabled: bool
    dq_fail_behavior: str
    schema_compat_profile: str
    quarantine_path: Optional[str]
    load_frequency: str


@dataclass
class ColumnMetadata:
    clean_column_name: str
    raw_column_name: str
    data_type: str
    nullable_flag: bool
    dq_rules: Dict
    dq_severity: str


@dataclass
class IngestionResult:
    success: bool
    rows_read: int
    rows_written: int
    dq_failures: int
    landing_path: str
    bronze_table: str
    duration_seconds: float
    schema_actions: Dict








