# Data Model Documentation

## Overview

The Azure Data Platform Health Dashboard uses a **star schema** dimensional data model optimized for analytics and reporting. The model consists of dimension tables (descriptive attributes) and fact tables (measurable events/metrics).

## Schema Structure

### Staging Schema (`stg`)

The staging schema contains raw data from source systems before transformation. Tables mirror the source data structure.

### Data Warehouse Schema (`dw`)

The data warehouse schema contains the dimensional model with optimized structures for Power BI reporting.

---

## Dimension Tables

### DimDate

**Purpose**: Date dimension for time-based analysis and filtering.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| DateKey | INT | Primary key (format: YYYYMMDD, e.g., 20250101) |
| Date | DATE | Actual date value |
| Year | SMALLINT | Year (e.g., 2025) |
| Quarter | TINYINT | Quarter (1-4) |
| Month | TINYINT | Month (1-12) |
| MonthName | VARCHAR(20) | Month name (e.g., "January") |
| Day | TINYINT | Day of month (1-31) |
| DayOfWeek | TINYINT | Day of week (1-7) |
| DayName | VARCHAR(20) | Day name (e.g., "Monday") |
| WeekOfYear | TINYINT | Week number (1-52) |
| IsWeekend | BIT | 1 if weekend, 0 if weekday |

**Sample Data**:
```
DateKey: 20250101
Date: 2025-01-01
Year: 2025
Quarter: 1
Month: 1
MonthName: January
Day: 1
DayOfWeek: 3
DayName: Wednesday
WeekOfYear: 1
IsWeekend: 0
```

**Relationships**:
- One-to-Many with FactPipelineRun (via DateKey)
- One-to-Many with FactActivityRun (via DateKey)
- One-to-Many with FactComputeUsage (via DateKey)
- One-to-Many with FactDQEvents (via DateKey)

---

### DimPipeline

**Purpose**: Dimension for pipeline metadata.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| PipelineKey | INT | Primary key (surrogate key, auto-increment) |
| PipelineId | NVARCHAR(200) | Pipeline identifier from source system |
| PipelineName | NVARCHAR(256) | Human-readable pipeline name |
| Environment | NVARCHAR(50) | Environment (e.g., "Prod", "Dev") |
| SourceSystem | NVARCHAR(100) | Source system (e.g., "Salesforce", "SAP") |
| Domain | NVARCHAR(100) | Business domain (e.g., "Sales", "SupplyChain") |
| OwnerEmail | NVARCHAR(256) | Pipeline owner email |
| IsActive | BIT | 1 if active, 0 if inactive |
| CreatedOn | DATETIME2(3) | Record creation timestamp |
| ModifiedOn | DATETIME2(3) | Record last modification timestamp |

**Unique Index**: `UX_DimPipeline_PipelineId_Env` on (PipelineId, Environment)

**Sample Data**:
```
PipelineKey: 1
PipelineId: adf-pl-sales-ingest
PipelineName: ADF Sales Ingest
Environment: Prod
SourceSystem: Salesforce
Domain: Sales
OwnerEmail: sales.owner@example.com
IsActive: 1
```

**Relationships**:
- One-to-Many with FactPipelineRun (via PipelineKey)
- One-to-Many with FactActivityRun (via PipelineKey)

---

### DimIntegrationRuntime

**Purpose**: Dimension for Integration Runtime (IR) metadata.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| IRKey | INT | Primary key (surrogate key, auto-increment) |
| IRName | NVARCHAR(256) | Integration Runtime name |
| IRType | NVARCHAR(50) | IR type (e.g., "Azure", "SelfHosted") |
| Region | NVARCHAR(100) | Azure region or location |
| Environment | NVARCHAR(50) | Environment (e.g., "Prod", "Dev") |
| IsActive | BIT | 1 if active, 0 if inactive |

**Unique Index**: `UX_DimIR_Name_Env` on (IRName, Environment)

**Sample Data**:
```
IRKey: 1
IRName: AutoResolveIntegrationRuntime
IRType: Azure
Region: East US
Environment: Prod
IsActive: 1
```

**Relationships**:
- One-to-Many with FactPipelineRun (via IRKey)

---

### DimSourceSystem

**Purpose**: Dimension for source system metadata.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| SourceKey | INT | Primary key (surrogate key, auto-increment) |
| SourceName | NVARCHAR(200) | Source system name (e.g., "Salesforce", "SAP") |
| SystemType | NVARCHAR(100) | System type (e.g., "SaaS", "ERP", "Database") |
| Description | NVARCHAR(500) | Description of the source system |
| Environment | NVARCHAR(50) | Environment (e.g., "Prod", "Dev") |
| IsActive | BIT | 1 if active, 0 if inactive |

**Unique Index**: `UX_DimSourceSystem_Name_Env` on (SourceName, Environment)

**Sample Data**:
```
SourceKey: 1
SourceName: Salesforce
SystemType: SaaS
Description: CRM SFDC
Environment: Prod
IsActive: 1
```

**Relationships**:
- One-to-Many with FactPipelineRun (via SourceKey)

---

## Fact Tables

### FactPipelineRun

**Purpose**: Fact table for pipeline run events.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| PipelineRunKey | BIGINT | Primary key (surrogate key, auto-increment) |
| PipelineRunId | NVARCHAR(200) | Pipeline run identifier from source |
| PipelineId | NVARCHAR(200) | Pipeline identifier (denormalized) |
| Environment | NVARCHAR(50) | Environment |
| PipelineKey | INT | Foreign key to DimPipeline |
| DateKey | INT | Foreign key to DimDate |
| IRKey | INT | Foreign key to DimIntegrationRuntime |
| SourceKey | INT | Foreign key to DimSourceSystem |
| StartTime | DATETIME2(3) | Pipeline run start timestamp |
| EndTime | DATETIME2(3) | Pipeline run end timestamp |
| DurationSeconds | INT | Calculated duration in seconds |
| Status | NVARCHAR(50) | Run status (e.g., "Succeeded", "Failed") |
| SlaCutoffTime | DATETIME2(3) | SLA cutoff time (optional) |
| IsSlaBreached | BIT | 1 if SLA breached, 0 otherwise |
| TokensUsed | DECIMAL(18,4) | Tokens consumed by the run |
| BillingCost | DECIMAL(18,6) | Billing cost for the run |
| RowsProcessed | BIGINT | Number of rows processed |
| BytesProcessed | BIGINT | Number of bytes processed |
| InsertedOn | DATETIME2(3) | Record insertion timestamp |
| UpdatedOn | DATETIME2(3) | Record last update timestamp |

**Unique Index**: `UX_FactPipelineRun_RunId_Env` on (PipelineRunId, Environment)

**Performance Indexes**:
- `IX_FactPipelineRun_DateKey_Status` on (DateKey, Status) with INCLUDE columns
- `IX_FactPipelineRun_PipelineKey_StartTime` on (PipelineKey, StartTime DESC) with INCLUDE columns
- `IX_FactPipelineRun_IRKey_DateKey` on (IRKey, DateKey) with INCLUDE columns

**Sample Data**:
```
PipelineRunKey: 1
PipelineRunId: run-001
PipelineId: adf-pl-sales-ingest
Environment: Prod
PipelineKey: 1
DateKey: 20250101
IRKey: 1
SourceKey: 1
StartTime: 2025-01-01 01:00:00.000
EndTime: 2025-01-01 01:10:00.000
DurationSeconds: 600
Status: Succeeded
TokensUsed: 10.5000
BillingCost: 0.750000
RowsProcessed: 100000
BytesProcessed: 104857600
```

**Grain**: One row per pipeline run

---

### FactActivityRun

**Purpose**: Fact table for activity-level execution details.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| ActivityRunKey | BIGINT | Primary key (surrogate key, auto-increment) |
| ActivityRunId | NVARCHAR(200) | Activity run identifier |
| PipelineRunId | NVARCHAR(200) | Parent pipeline run ID |
| ActivityName | NVARCHAR(256) | Activity name |
| ActivityType | NVARCHAR(100) | Activity type (e.g., "Copy", "DataFlow") |
| Environment | NVARCHAR(50) | Environment |
| PipelineRunKey | BIGINT | Foreign key to FactPipelineRun |
| PipelineKey | INT | Foreign key to DimPipeline |
| DateKey | INT | Foreign key to DimDate |
| StartTime | DATETIME2(3) | Activity start timestamp |
| EndTime | DATETIME2(3) | Activity end timestamp |
| DurationSeconds | INT | Calculated duration in seconds |
| Status | NVARCHAR(50) | Activity status |
| RowsRead | BIGINT | Rows read by the activity |
| RowsWritten | BIGINT | Rows written by the activity |
| BytesRead | BIGINT | Bytes read |
| BytesWritten | BIGINT | Bytes written |
| IRName | NVARCHAR(256) | Integration Runtime name (denormalized) |
| InsertedOn | DATETIME2(3) | Record insertion timestamp |
| UpdatedOn | DATETIME2(3) | Record last update timestamp |

**Performance Indexes**:
- `IX_FactActivityRun_PipelineRunKey` on (PipelineRunKey) with INCLUDE columns
- `IX_FactActivityRun_DateKey_Status` on (DateKey, Status) with INCLUDE columns

**Sample Data**:
```
ActivityRunKey: 1
ActivityRunId: act-001
PipelineRunId: run-001
ActivityName: CopyFromSFDC
ActivityType: Copy
Environment: Prod
PipelineRunKey: 1
PipelineKey: 1
DateKey: 20250101
StartTime: 2025-01-01 01:01:00.000
EndTime: 2025-01-01 01:09:00.000
DurationSeconds: 480
Status: Succeeded
RowsRead: 100000
RowsWritten: 100000
BytesRead: 52428800
BytesWritten: 104857600
```

**Grain**: One row per activity run

---

### FactComputeUsage

**Purpose**: Fact table for compute resource usage (DBUs, tokens, etc.).

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| ComputeUsageKey | BIGINT | Primary key (surrogate key, auto-increment) |
| DateKey | INT | Foreign key to DimDate |
| Environment | NVARCHAR(50) | Environment |
| PipelineRunId | NVARCHAR(200) | Related pipeline run ID (optional) |
| PipelineRunKey | BIGINT | Foreign key to FactPipelineRun (optional) |
| JobId | NVARCHAR(200) | Job identifier (e.g., Databricks job ID) |
| JobRunId | NVARCHAR(200) | Job run identifier |
| ClusterId | NVARCHAR(200) | Cluster identifier |
| WarehouseId | NVARCHAR(200) | Warehouse identifier (Fabric) |
| UsageStartTime | DATETIME2(3) | Usage period start |
| UsageEndTime | DATETIME2(3) | Usage period end |
| UsageUnit | NVARCHAR(50) | Usage unit (e.g., "DBU", "Token") |
| UsageQuantity | DECIMAL(18,6) | Usage quantity |
| Cost | DECIMAL(18,6) | Cost for this usage |
| AdfRunTag | NVARCHAR(200) | ADF run tag (optional) |
| CustomTagsJson | NVARCHAR(MAX) | Custom tags as JSON |
| InsertedOn | DATETIME2(3) | Record insertion timestamp |

**Performance Indexes**:
- `IX_FactComputeUsage_DateKey_UsageUnit` on (DateKey, UsageUnit) with INCLUDE columns
- `IX_FactComputeUsage_PipelineRunKey` on (PipelineRunKey) with INCLUDE columns

**Sample Data**:
```
ComputeUsageKey: 1
DateKey: 20250101
Environment: Prod
PipelineRunId: run-001
PipelineRunKey: 1
JobId: job-123
JobRunId: jobrun-123-1
ClusterId: cluster-01
WarehouseId: NULL
UsageStartTime: 2025-01-01 01:00:00.000
UsageEndTime: 2025-01-01 01:15:00.000
UsageUnit: DBU
UsageQuantity: 5.000000
Cost: 0.500000
AdfRunTag: NULL
CustomTagsJson: {"adf_run_id":"run-001"}
```

**Grain**: One row per usage period (typically per hour or per job run)

---

### FactDQEvents

**Purpose**: Fact table for data quality check events.

**Columns**:
| Column Name | Data Type | Description |
|------------|-----------|-------------|
| DQEventKey | BIGINT | Primary key (surrogate key, auto-increment) |
| DateKey | INT | Foreign key to DimDate |
| PipelineRunKey | BIGINT | Foreign key to FactPipelineRun (optional) |
| PipelineRunId | NVARCHAR(200) | Pipeline run ID |
| CheckName | NVARCHAR(200) | Data quality check name |
| CheckType | NVARCHAR(100) | Check type (e.g., "Completeness", "Validity") |
| Status | NVARCHAR(50) | Check status (e.g., "Pass", "Fail") |
| FailedRowCount | BIGINT | Number of rows that failed the check |
| DetailsJson | NVARCHAR(MAX) | Additional check details as JSON |
| InsertedOn | DATETIME2(3) | Record insertion timestamp |

**Performance Indexes**:
- `IX_FactDQEvents_DateKey_Status` on (DateKey, Status) with INCLUDE columns
- `IX_FactDQEvents_PipelineRunKey` on (PipelineRunKey) with INCLUDE columns

**Sample Data**:
```
DQEventKey: 1
DateKey: 20250101
PipelineRunKey: 1
PipelineRunId: run-001
CheckName: NullCheck_CustomerId
CheckType: Completeness
Status: Pass
FailedRowCount: 0
DetailsJson: NULL
```

**Grain**: One row per data quality check execution

---

## Relationships Diagram

```
                    ┌──────────┐
                    │ DimDate  │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌─────▼──────┐  ┌─────▼──────┐
    │FactPipe │    │FactActivity│  │FactCompute │
    │lineRun  │    │   Run      │  │   Usage    │
    └────┬────┘    └─────┬──────┘  └─────┬──────┘
         │               │               │
         │               └───────┬───────┘
         │                       │
         │                  ┌────▼────┐
         │                  │FactDQ   │
         │                  │Events   │
         │                  └─────────┘
         │
    ┌────┴─────────────────────────────────────┐
    │                                          │
┌───▼────┐  ┌──────────────┐  ┌──────────────┐
│DimPipe │  │DimIntegration│  │DimSource     │
│line    │  │Runtime       │  │System        │
└────────┘  └──────────────┘  └──────────────┘
```

---

## Data Loading Strategy

### 1. Staging to Warehouse (ETL Process)

1. **Dimension Loading**:
   - Use `MERGE` statements to upsert dimensions
   - Look up existing records by natural keys (e.g., PipelineId + Environment)
   - Insert new records, update existing records if attributes changed

2. **Fact Loading**:
   - Use `MERGE` statements to upsert facts
   - Join staging data with dimensions to resolve foreign keys
   - Calculate derived columns (e.g., DurationSeconds, DateKey)

3. **Incremental Loading**:
   - Filter staging data by `InsertedOn` timestamp
   - Only process new records since last load
   - Use `MERGE` for idempotent updates

### 2. Sample Data Loading

The sample data scripts demonstrate:
- Populating `DimDate` for a date range (10+ days)
- Inserting sample dimension records
- Inserting sample staging data
- Executing ETL upsert logic

---

## Design Principles

1. **Star Schema**: Simple star schema with denormalized dimensions
2. **Surrogate Keys**: All dimension and fact tables use surrogate keys (INT/BIGINT identity)
3. **Natural Keys**: Dimensions maintain natural keys for lookups (e.g., PipelineId + Environment)
4. **Grain**: Each fact table has a clear grain (one row per event)
5. **Slowly Changing Dimensions (SCD)**: Type 1 (overwrite) for simplicity
6. **Indexing**: Performance indexes on foreign keys and common filter columns
7. **Null Handling**: Foreign keys allow NULL for optional relationships

---

## Performance Considerations

1. **Indexes**: Covering indexes on fact tables for common query patterns
2. **Partitioning**: Consider partitioning large fact tables by DateKey (future enhancement)
3. **Compression**: Use page compression on large fact tables (future enhancement)
4. **Query Optimization**: Power BI uses star schema for optimal query performance

---

## Future Enhancements

- **DimTime**: Separate time dimension for hour/minute-level analysis
- **DimJob**: Dimension for Databricks/Fabric jobs
- **DimCluster**: Dimension for cluster metadata
- **Partitioning**: Partition fact tables by DateKey for improved performance
- **Archival Strategy**: Archive old fact data to separate tables/archives
