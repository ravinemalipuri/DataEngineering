# DataModel Profiler - Codebase Prompt

## Overview
This is a production-ready Python package called `datamodel_profiler` that provides comprehensive data profiling and schema inference capabilities. The package is designed to handle multiple file formats, perform fast data analysis, and generate various output schemas.

## Architecture

### Core Components

1. **Data I/O Layer** (`datamodel_profiler/io/`)
   - `data_loader.py`: Main data loader that handles multiple formats
   - `formats.py`: Format-specific readers (CSV, Parquet, JSON, YAML, Excel, ORC)
   - Supports streaming/chunked processing for large files
   - Auto-detection of file formats

2. **Profiling Engine** (`datamodel_profiler/core/profiler.py`)
   - Fast data profiling with statistical metrics
   - Column statistics (nulls, distinct counts, min/max, percentiles)
   - Semantic type detection (email, UUID, date, currency, etc.)
   - Outlier detection using IQR method
   - Data quality scoring

3. **Schema Inference** (`datamodel_profiler/core/schema_inference.py`)
   - Generates multiple schema formats:
     - JSON Schema (Draft 2020-12)
     - Avro schema
     - SQL DDL (PostgreSQL, Snowflake, ANSI SQL)
     - Parquet/Arrow schema
     - Pydantic models
     - Python dataclasses

4. **Key Detection** (`datamodel_profiler/core/key_detection.py`)
   - Primary key candidate detection
   - Single and composite key analysis
   - Scoring based on uniqueness, nullability, stability
   - Name-based heuristics

5. **Constraint Suggestions** (`datamodel_profiler/core/constraint_suggestion.py`)
   - Great Expectations integration
   - Type, range, pattern, allowed values constraints
   - Foreign key relationship detection
   - Cross-column constraint suggestions

6. **Utilities** (`datamodel_profiler/utils/`)
   - `types.py`: Type definitions and data models
   - `validators.py`: Semantic type validators
   - `formatters.py`: Schema formatters for different output formats

7. **CLI Interface** (`datamodel_profiler/cli.py`)
   - Command-line interface with subcommands:
     - `profile`: Data profiling
     - `infer-schema`: Schema inference
     - `detect-keys`: Primary key detection
     - `suggest-constraints`: Constraint suggestions

## Key Features

### Multi-Format Support
- **CSV**: Configurable delimiter, encoding
- **Parquet**: Fast, columnar format
- **JSON**: Records or newline-delimited
- **YAML**: Records format
- **Excel**: Multiple sheets supported
- **ORC**: Optional, requires pyarrow>=10.0.0

### Data Profiling
- Row count, column statistics, missingness analysis
- Distinct counts, min/max, percentiles
- Inferred semantic types
- Basic outlier detection
- Data quality scoring

### Schema Generation
- Multiple output formats for different use cases
- Type inference with nullability detection
- Constraint generation based on data patterns
- Cross-platform compatibility

### Primary Key Detection
- Algorithmic scoring system
- Uniqueness, nullability, and stability metrics
- Name-based heuristics (ID, key, code patterns)
- Composite key support

### Data Quality Constraints
- Great Expectations integration
- Automated constraint suggestions
- Foreign key relationship detection
- Confidence scoring for each constraint

## Configuration

The package uses a `ProfilingConfig` class for configuration:

```python
@dataclass
class ProfilingConfig:
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
```

## Usage Patterns

### Command Line
```bash
# Profile a dataset
datamodel-profiler profile data.csv --html-report report.html

# Infer schema
datamodel-profiler infer-schema data.csv --table-name users --sql-dialect postgres

# Detect primary keys
datamodel-profiler detect-keys data.csv --max-composite-size 3

# Suggest constraints
datamodel-profiler suggest-constraints data.csv --lookup-dir lookup_tables/
```

### Python API
```python
from datamodel_profiler import DataProfiler, SchemaInferencer, KeyDetector, ConstraintSuggester
from datamodel_profiler.io import DataFormat

# Initialize profiler
profiler = DataProfiler()
profile = profiler.profile("data.csv", DataFormat.CSV)

# Infer schema
inferencer = SchemaInferencer()
schema = inferencer.infer_schema("data.csv", "users", DataFormat.CSV)

# Detect keys
detector = KeyDetector()
candidates = detector.detect_keys("data.csv", DataFormat.CSV)

# Suggest constraints
suggester = ConstraintSuggester()
constraints = suggester.suggest_constraints("data.csv", DataFormat.CSV)
```

## Dependencies

### Core Dependencies
- `pandas>=1.5.0`: Data manipulation
- `pyarrow>=10.0.0`: Parquet/Arrow support
- `numpy>=1.21.0`: Numerical operations
- `click>=8.0.0`: CLI framework
- `pydantic>=2.0.0`: Data validation
- `jsonschema>=4.0.0`: JSON Schema support
- `avro-python3>=1.10.0`: Avro schema support
- `openpyxl>=3.0.0`: Excel support
- `PyYAML>=6.0.0`: YAML support
- `great-expectations>=0.17.0`: Data quality framework (mandatory)

**Note**: Great Expectations may have installation issues on Windows systems without long path support enabled. The package will work without it, but constraint suggestions will be limited.

### Optional Dependencies
- `ydata-profiling>=4.0.0`: HTML reports
- `polars>=0.20.0`: Alternative data engine

## Testing

The package includes comprehensive tests in the `tests/` directory:
- `test_profiler.py`: Profiling engine tests
- `test_schema_inference.py`: Schema inference tests
- `test_key_detection.py`: Key detection tests
- `test_constraint_suggestion.py`: Constraint suggestion tests

## Performance Considerations

- **Streaming processing**: Handles files up to 5GB+ with chunked processing
- **Memory efficiency**: Uses iterators and configurable chunk sizes
- **Engine options**: Supports both pandas and polars backends
- **Optimization**: Parquet format recommended for better performance

## Extension Points

The package is designed for extensibility:

1. **Custom validators**: Add new semantic type validators in `utils/validators.py`
2. **New formats**: Implement format readers in `io/formats.py`
3. **Custom formatters**: Add new schema formatters in `utils/formatters.py`
4. **Additional constraints**: Extend constraint suggestions in `core/constraint_suggestion.py`

## Error Handling

The package includes robust error handling:
- Graceful degradation when optional dependencies are missing
- Clear error messages for unsupported formats
- Validation of input parameters
- Comprehensive logging for debugging

## License

This project is licensed under the Apache License 2.0, making it suitable for both open source and commercial use.

## Contributing

The codebase follows clean architecture principles:
- Separation of concerns
- Dependency injection
- Configurable components
- Comprehensive testing
- Clear documentation

When extending the package, maintain these principles and ensure all new features include appropriate tests and documentation.
