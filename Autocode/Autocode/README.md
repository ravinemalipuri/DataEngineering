# DataModel Profiler

A production-ready Python package for comprehensive data profiling and schema inference. DataModel Profiler provides fast, scalable data analysis with support for multiple file formats and output schemas.

## Features

### 🔍 **Multi-Format Data Reading**
- **CSV, Parquet, JSON, YAML, Excel (.xlsx), ORC** support
- **Auto-detection** of file formats
- **Streaming/chunked processing** for large files (1-5GB+)
- **Directory processing** for batch analysis

### 📊 **Fast Data Profiling**
- **Row count, column statistics, missingness analysis**
- **Distinct counts, min/max, percentiles**
- **Inferred semantic types** (email, UUID, date, currency, etc.)
- **Basic outlier detection** using IQR method
- **Data quality scoring**

### 🏗️ **Schema Inference**
- **JSON Schema (Draft 2020-12)**
- **Avro schema**
- **SQL DDL** (PostgreSQL, Snowflake, ANSI SQL)
- **Parquet/Arrow schema**
- **Pydantic models**
- **Python dataclasses**

### 🔑 **Primary Key Detection**
- **Single and composite key candidates**
- **Scoring based on uniqueness, nullability, stability**
- **Name-based heuristics** (ID, key, code patterns)
- **Detailed rationale** for each candidate

### ✅ **Data Quality Constraints**
- **Great Expectations integration**
- **Type, range, pattern, allowed values constraints**
- **Foreign key relationship detection**
- **Cross-column constraint suggestions**
- **Confidence scoring** for each constraint

### 📈 **Reporting**
- **HTML reports** (with ydata-profiling integration)
- **Markdown summaries**
- **Machine-readable JSON outputs**
- **Column statistics CSV exports**

## Installation

### Basic Installation
```bash
pip install datamodel-profiler
```

### With Optional Dependencies
```bash
# For HTML reports
pip install datamodel-profiler[html]

# For Polars backend
pip install datamodel-profiler[polars]

# For ORC support
pip install datamodel-profiler[orc]

# For development
pip install datamodel-profiler[dev]
```

**Note**: Great Expectations is included as a core dependency for data quality constraint suggestions.

**Windows Users**: If you encounter installation issues with Great Expectations due to long path limitations, you can still use the package for profiling and schema inference. Constraint suggestions will be limited without Great Expectations.

## Quick Start

### Command Line Interface

#### Profile a Dataset
```bash
# Basic profiling
datamodel-profiler profile data.csv

# With custom options
datamodel-profiler profile data.parquet \
  --format parquet \
  --engine polars \
  --sample-rows 10000 \
  --html-report report.html \
  --output-dir results/
```

#### Infer Schema
```bash
# Generate multiple schema formats
datamodel-profiler infer-schema data.csv \
  --table-name users \
  --sql-dialect postgres \
  --output-dir schemas/
```

#### Detect Primary Keys
```bash
# Find key candidates
datamodel-profiler detect-keys data.csv \
  --max-composite-size 3 \
  --output-dir keys/
```

#### Suggest Constraints
```bash
# Generate data quality constraints
datamodel-profiler suggest-constraints data.csv \
  --lookup-dir lookup_tables/ \
  --max-domain-size 50 \
  --output-dir constraints/
```

### Python API

```python
from datamodel_profiler import DataProfiler, SchemaInferencer, KeyDetector, ConstraintSuggester
from datamodel_profiler.io import DataFormat

# Initialize profiler
profiler = DataProfiler()

# Profile a dataset
profile = profiler.profile("data.csv", DataFormat.CSV)
print(f"Rows: {profile.row_count}, Quality Score: {profile.quality_score}")

# Infer schema
inferencer = SchemaInferencer()
schema = inferencer.infer_schema("data.csv", "users", DataFormat.CSV)

# Export in multiple formats
inferencer.export_schema(schema, "output/", "postgres")

# Detect primary keys
detector = KeyDetector()
candidates = detector.detect_keys("data.csv", DataFormat.CSV)
print(f"Top candidate: {candidates[0].columns}")

# Suggest constraints
suggester = ConstraintSuggester()
constraints = suggester.suggest_constraints("data.csv", DataFormat.CSV)
print(f"Generated {len(constraints)} constraints")
```

## Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| CSV | `.csv` | Configurable delimiter, encoding |
| Parquet | `.parquet` | Fast, columnar format |
| JSON | `.json`, `.jsonl`, `.ndjson` | Records or newline-delimited |
| YAML | `.yaml`, `.yml` | Records format |
| Excel | `.xlsx`, `.xls` | Multiple sheets supported |
| ORC | `.orc` | Optional, requires pyarrow>=10.0.0 |

## Output Formats

### Schema Formats
- **JSON Schema**: `schema.json` - Draft 2020-12 compliant
- **Avro**: `schema.avsc` - Apache Avro schema
- **SQL DDL**: `schema.sql` - Database table definitions
- **Arrow**: `schema_arrow.txt` - Apache Arrow schema
- **Pydantic**: `schema_pydantic.py` - Python model classes
- **Dataclass**: `schema_dataclass.py` - Python dataclasses

### Profiling Outputs
- **Profile**: `profile.json` - Complete profiling results
- **Column Stats**: `column_stats.csv` - Statistical summary
- **HTML Report**: `report.html` - Interactive visualization
- **Markdown**: `report.md` - Human-readable summary

### Key Detection
- **Key Candidates**: `key_candidates.json` - Ranked primary key suggestions

### Constraints
- **Great Expectations**: `constraints.json` - Data quality rules
- **Markdown Report**: `constraints.md` - Constraint documentation

## Configuration

### ProfilingConfig Options

```python
from datamodel_profiler.utils.types import ProfilingConfig

config = ProfilingConfig(
    engine="pandas",              # pandas or polars
    sample_rows=10000,            # Limit rows for analysis
    chunksize=10000,              # Chunk size for processing
    nullable_threshold=0.01,      # NOT NULL threshold
    decimal_precision=38,         # Decimal precision
    decimal_scale=9,              # Decimal scale
    max_domain_size=100,          # Max enum size
    regex_level="basic",          # basic or strict
    enable_html_report=False,     # HTML report generation
    enable_md_report=True         # Markdown report generation
)
```

## Advanced Usage

### Custom Data Processing

```python
from datamodel_profiler.io import DataLoader, DataFormat

# Initialize data loader
loader = DataLoader(engine="polars")

# Load data with custom options
for chunk in loader.load_data(
    "large_file.parquet",
    DataFormat.PARQUET,
    chunksize=50000,
    columns=["id", "name", "email"]
):
    # Process chunk
    print(f"Processing {len(chunk)} rows")
```

### Semantic Type Detection

```python
from datamodel_profiler.utils.validators import SemanticTypeDetector

detector = SemanticTypeDetector()
semantic_type = detector.detect_semantic_type(
    ["user@example.com", "admin@domain.org"],
    threshold=0.8
)
print(semantic_type)  # SemanticType.EMAIL
```

### Custom Constraint Suggestions

```python
from datamodel_profiler.core.constraint_suggestion import ConstraintSuggester

suggester = ConstraintSuggester()
constraints = suggester.suggest_constraints(
    "data.csv",
    lookup_dir="dimension_tables/",
    max_domain_size=50
)

# Export to Great Expectations format
suggester.export_constraints(constraints, "ge_expectations.json")
```

## Performance

### Scalability
- **Streaming processing** for files up to 5GB+
- **Chunked analysis** with configurable chunk sizes
- **Memory-efficient** operations using iterators
- **Optional Polars backend** for faster processing

### Optimization Tips
1. **Use Polars engine** for large datasets: `--engine polars`
2. **Sample data** for quick analysis: `--sample-rows 10000`
3. **Adjust chunk size** based on memory: `--chunksize 50000`
4. **Use Parquet format** for better performance

## Examples

### E-commerce Data Analysis
```bash
# Profile customer data
datamodel-profiler profile customers.csv \
  --html-report customer_report.html \
  --output-dir analysis/

# Infer schema for database
datamodel-profiler infer-schema customers.csv \
  --table-name customers \
  --sql-dialect postgres \
  --output-dir database/

# Detect primary keys
datamodel-profiler detect-keys customers.csv \
  --output-dir keys/

# Suggest constraints with lookup tables
datamodel-profiler suggest-constraints orders.csv \
  --lookup-dir dimension_tables/ \
  --output-dir constraints/
```

### Data Pipeline Integration
```python
import pandas as pd
from datamodel_profiler import DataProfiler

def validate_data_quality(file_path):
    """Validate data quality in pipeline."""
    profiler = DataProfiler()
    profile = profiler.profile(file_path)
    
    # Check quality score
    if profile.quality_score < 0.8:
        raise ValueError(f"Data quality too low: {profile.quality_score}")
    
    # Check for missing primary key
    if not profile.primary_key_candidates:
        raise ValueError("No primary key candidates found")
    
    return profile
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/your-org/datamodel_profiler.git
cd datamodel_profiler
pip install -e ".[dev]"
pytest
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://datamodelprofiler.readthedocs.io](https://datamodelprofiler.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/your-org/datamodel_profiler/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/datamodel_profiler/discussions)

## Changelog

### v1.0.0
- Initial release
- Multi-format data reading (CSV, Parquet, JSON, YAML, Excel, ORC)
- Comprehensive data profiling
- Schema inference for multiple output formats
- Primary key detection with scoring
- Data quality constraint suggestions
- Great Expectations integration
- HTML and Markdown reporting
- Command-line interface
- Python API
