# Metadata-Driven Pipelines — Azure / Microsoft Fabric

The idea behind this is simple: pipeline behavior should live in data, not in code.

Most data pipeline projects I've worked on had the same problem — every source table had its own notebook or script, and the business logic (what keys to use, how to load it, what quality checks to run) was buried in that code. Changing a load strategy meant touching code. Adding a source meant writing a new script. A schema change upstream would silently break things.

This framework flips that model. You register your source in a metadata catalog — load type, keys, watermark columns, column-level DQ rules — and the framework reads that at runtime and handles everything else.

---

## How it works

The metadata catalog is a set of SQL tables that describe your sources:

- `source_systems` — your source connections (DB2, Salesforce, any JDBC system)
- `source_objects` — per-table configuration: load type, business keys, watermark column
- `source_object_columns` — column types, DQ rules, severity levels
- `schema_history` — a log of every schema change detected
- `data_quality_results` — DQ results stored per load, not just logged to console

When you run the orchestration wrapper, it reads those tables, figures out what needs to run, and executes. Adding a new source is adding rows to the catalog — nothing else.

---

## The ingestion flow

```
Metadata Catalog
      │
      ▼
Orchestration Wrapper (discovers all active sources)
      │
      ├── source_reader.py      reads from DB2, SFDC, JDBC
      ├── schema_manager.py     compares live schema vs stored, logs drift
      ├── load_strategy.py      FULL / INCREMENTAL / HYBRID
      ├── dq_engine.py          runs column-level rules, stores results
      ├── observability.py      records run metrics
      └── notifications.py      Teams or email on failure
            │
            ▼
      Landing (Parquet) → Bronze (Delta) → Silver (Delta)
```

Landing is a raw Parquet snapshot before any transformations. This makes reruns safe — you can reprocess from landing without hitting the source system again.

---

## Load strategies

Three modes, set per source object in the catalog:

- **FULL** — overwrites the target table each run. Good for small reference tables.
- **INCREMENTAL** — hash-based merge using business keys. For large transactional tables.
- **HYBRID** — append with configurable watermark. For event or log tables.

Switching a table from FULL to INCREMENTAL is a metadata change, not a code change.

---

## Schema drift detection

This is the part that saves the most headaches. On every Bronze load, `schema_manager.py` reads the live schema from the source and compares it to what's stored in the catalog. New columns, dropped columns, type changes — all logged to `schema_history`. Breaking changes surface early, before Silver or reporting layers are affected.

---

## Onboarding a new source

```sql
-- Register the source system
INSERT INTO source_systems (system_name, connection_profile, active)
VALUES ('ORDERS_DB', 'JDBC_PROFILE', 1);

-- Register the table
INSERT INTO source_objects (system_name, object_name, load_type, business_key_columns, watermark_column, active)
VALUES ('ORDERS_DB', 'ORDERS', 'INCREMENTAL', 'ORDER_ID', 'MODIFIED_DATE', 1);

-- Define column rules
INSERT INTO source_object_columns (system_name, object_name, column_name, data_type, dq_rule, severity)
VALUES ('ORDERS_DB', 'ORDERS', 'ORDER_ID', 'STRING', 'NOT_NULL', 'ERROR');
```

Next pipeline run picks it up automatically.

---

## Configuration

Connection details, workspace names, and storage paths live in `pipeline_config.yaml`. A sanitized example is included — copy it and fill in your environment.

```bash
cp config/pipeline_config.yaml.example config/pipeline_config.yaml
```

The real config is in `.gitignore`. Never commit actual credentials or storage account names.

---

## Running it

```bash
pip install -r requirements.txt

# Full Bronze run across all active sources
python src/jobs/hy_brnz_load_wrapper_fabric.py

# Single source run
python src/jobs/ingest_source.py --source ORDERS_DB --object ORDERS
```

---

## What's in the repo

```
metadata-driven-pipelines-azure/
├── src/
│   ├── framework/    # The core engine — metadata, schema, DQ, load strategies
│   ├── jobs/         # Entry points — full run and single-source
│   └── utilities/    # SSIS migration helpers, KQL queries for ADF monitoring
├── config/           # pipeline_config.yaml.example
├── metadata/         # DDL to create the catalog, seed data, data model docs
├── docs/             # Architecture walkthrough
└── tests/
```
