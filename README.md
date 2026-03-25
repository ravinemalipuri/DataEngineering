# Data Engineering Toolkit

This repo is where I keep the patterns I keep reaching for on every data project.

Most of it started from a recurring frustration: teams spending weeks building the same ingestion logic from scratch, every project, every time. New source system? Write a new notebook. Schema changed upstream? Find out three hours later when a report broke. Load strategy needs to change? Dig through code.

The stuff in here is my answer to that. Config-driven pipelines, automated quality checks, schema profiling — built to be adapted for a new environment without starting from zero.

---

## What's in here

**[metadata-driven-pipelines-azure](./metadata-driven-pipelines-azure/)**
The core of it. A pipeline framework where behavior — load type, keys, DQ rules, schema — lives in a metadata catalog, not in code. Onboarding a new source means adding rows to a table. The framework handles the rest.

Built for Microsoft Fabric and Databricks, though the design patterns apply anywhere.

**[dataquality](./dataquality/)**
A standalone DQ validation module built on Great Expectations. Works against files (CSV, Parquet, Excel) or live database tables across Snowflake, Databricks, PostgreSQL, Redshift, and BigQuery. Results are persisted — not just logged and forgotten — so you have an audit trail and can track quality trends over time.

**[dataprofiling](./dataprofiling/)**
Automated profiling for when you're onboarding a new source and need to understand it fast. Reads the data, infers schema, scores data quality, detects primary key candidates, and outputs schema definitions in whatever format you need — JSON Schema, Avro, SQL DDL for Snowflake or PostgreSQL, Pydantic models.

---

## How these fit together

The typical flow on a project looks like this:

1. Run the profiler against new source data to understand what you're working with
2. Use the generated DDL and schema docs to set up the metadata catalog
3. Let the pipeline framework take it from there — ingestion, quality checks, schema drift detection, all driven by metadata

None of these modules require the others. Each one is self-contained and can be dropped into an existing stack.

---

## Tech

Python, PySpark, Delta Lake, Microsoft Fabric, Databricks, Azure Data Lake Gen2, Great Expectations, SQLAlchemy, YAML config.

---

## Getting started

```bash
git clone https://github.com/ravinemalipuri/DataEngineering
cd DataEngineering/metadata-driven-pipelines-azure

cp config/pipeline_config.yaml.example config/pipeline_config.yaml
# Fill in your workspace, storage paths, and source connections

pip install -r requirements.txt
python src/jobs/hy_brnz_load_wrapper_fabric.py
```

The metadata DDL to set up the catalog is in `metadata/ddl/`.

---

[LinkedIn](https://linkedin.com/in/ravinemalipuri) · Open to Data Architect and Data Engineering Manager roles
