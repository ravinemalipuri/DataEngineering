"""
Type definitions and enums for datamodel_profiler.
"""

from enum import Enum
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from pydantic import BaseModel


class DataType(Enum):
    """Basic data types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    BINARY = "binary"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


class SemanticType(Enum):
    """Semantic data types."""
    EMAIL = "email"
    UUID = "uuid"
    URL = "url"
    PHONE = "phone"
    CURRENCY = "currency"
    PERCENTAGE = "percentage"
    POSTAL_CODE = "postal_code"
    CREDIT_CARD = "credit_card"
    IP_ADDRESS = "ip_address"
    MAC_ADDRESS = "mac_address"
    SSN = "ssn"
    GENERIC = "generic"


@dataclass
class ColumnStats:
    """Statistics for a single column."""
    name: str
    data_type: DataType
    semantic_type: SemanticType
    null_count: int
    null_percentage: float
    distinct_count: int
    distinct_percentage: float
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    mean_value: Optional[float] = None
    median_value: Optional[Any] = None
    std_dev: Optional[float] = None
    percentiles: Dict[int, Any] = None
    is_outlier_prone: bool = False
    sample_values: List[Any] = None
    regex_pattern: Optional[str] = None


@dataclass
class DatasetProfile:
    """Complete dataset profiling results."""
    row_count: int
    column_count: int
    file_size_bytes: int
    columns: Dict[str, ColumnStats]
    primary_key_candidates: List[Dict[str, Any]]
    quality_score: float
    profiling_time_seconds: float


@dataclass
class ProfilingConfig:
    """Configuration for data profiling."""
    engine: str = "pandas"  # pandas or polars
    sample_rows: Optional[int] = None
    chunksize: int = 10000
    nullable_threshold: float = 0.01
    decimal_precision: int = 38
    decimal_scale: int = 9
    max_domain_size: int = 100
    regex_level: str = "basic"  # basic or strict
    enable_html_report: bool = False
    enable_md_report: bool = True


class SchemaInfo(BaseModel):
    """Schema information for a column."""
    name: str
    data_type: str
    nullable: bool
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    examples: Optional[List[Any]] = None


class TableSchema(BaseModel):
    """Complete table schema."""
    table_name: str
    columns: List[SchemaInfo]
    primary_key: Optional[List[str]] = None
    foreign_keys: Optional[List[Dict[str, str]]] = None
    indexes: Optional[List[Dict[str, Any]]] = None


class KeyCandidate(BaseModel):
    """Primary key candidate information."""
    columns: List[str]
    uniqueness_score: float
    nullability_score: float
    stability_score: float
    overall_score: float
    rationale: str
    is_composite: bool


class ConstraintSuggestion(BaseModel):
    """Data quality constraint suggestion."""
    column_name: str
    constraint_type: str  # type, range, regex, allowed_values, etc.
    parameters: Dict[str, Any]
    confidence: float
    rationale: str
