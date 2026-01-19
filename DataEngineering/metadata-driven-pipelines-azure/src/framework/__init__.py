"""
Framework modules used by metadata-driven ingestion jobs.
This file exposes the public API so jobs can import everything from one place.
"""

from .config_loader import ComputeResolver, ConfigLoader, PathBuilder
from .dq_engine import DataQualityEngine
from .load_strategy import LoadStrategyExecutor
from .metadata_repository import MetadataRepository
from .models import ColumnMetadata, IngestionResult, SourceObjectConfig
from .notifications import EmailNotifier
from .observability import ObservabilityRecorder
from .schema_manager import SchemaManager
from .source_reader import SourceReader

__all__ = [
    "ColumnMetadata",
    "ComputeResolver",
    "ConfigLoader",
    "DataQualityEngine",
    "EmailNotifier",
    "IngestionResult",
    "LoadStrategyExecutor",
    "MetadataRepository",
    "ObservabilityRecorder",
    "PathBuilder",
    "SchemaManager",
    "SourceObjectConfig",
    "SourceReader",
]

