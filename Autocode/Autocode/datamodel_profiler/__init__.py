"""
DataModel Profiler - A production-ready Python package for data profiling and schema inference.

This package provides comprehensive data profiling capabilities including:
- Multi-format data reading (CSV, Parquet, JSON, YAML, Excel, ORC)
- Fast data profiling with statistical metrics
- Schema inference for multiple output formats
- Primary key detection
- Data quality constraint suggestions
- HTML and Markdown reporting
"""

__version__ = "1.0.0"
__author__ = "Data Model Profiler Team"
__email__ = "team@datamodelprofiler.com"

from .core.profiler import DataProfiler
from .core.schema_inference import SchemaInferencer
from .core.key_detection import KeyDetector
from .core.constraint_suggestion import ConstraintSuggester
from .io.data_loader import DataLoader
from .utils.types import DataType, SemanticType

__all__ = [
    "DataProfiler",
    "SchemaInferencer", 
    "KeyDetector",
    "ConstraintSuggester",
    "DataLoader",
    "DataType",
    "SemanticType",
]
