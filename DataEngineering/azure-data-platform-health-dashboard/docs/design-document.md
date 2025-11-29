# Azure Data Platform Health Dashboard - Design Document

## 1. Overview

The Azure Data Platform Health Dashboard is an end-to-end solution for monitoring, analyzing, and optimizing Azure data platform resources, including Azure Data Factory (ADF), Microsoft Fabric pipelines, and compute usage (Databricks DBUs). The solution provides visibility into pipeline performance, costs, and regression detection through a Power BI dashboard.

### 1.1 Objectives

- **Cost Visibility**: Identify costliest pipelines and compute resources
- **Performance Monitoring**: Track pipeline run times, token usage, and throughput
- **Regression Detection**: Automatically detect performance degradation compared to baseline
- **Resource Optimization**: Analyze Integration Runtime (IR) usage patterns

### 1.2 Target Audience

- Data Engineering Managers
- Data Platform Leads
- Data Architects
- DevOps Engineers

## 2. Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   ADF    │  │  Fabric  │  │Databricks│  │   DQ     │      │
│  │  Logs    │  │  Logs    │  │  Usage   │  │  Events  │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
└───────┼─────────────┼─────────────┼─────────────┼────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │      Staging Layer (stg schema)      │
        │  ┌──────────────┐  ┌──────────────┐  │
        │  │ PipelineRun  │  │ ActivityRun  │  │
        │  │ ComputeUsage │  │  DQEvents    │  │
        │  └──────┬───────┘  └──────┬───────┘  │
        └─────────┼──────────────────┼──────────┘
                  │                  │
        ┌─────────┴──────────────────┴──────────┐
        │    ETL Process (Upsert Scripts)        │
        └─────────┬──────────────────┬───────────┘
                  │                  │
        ┌─────────┴──────────────────┴──────────┐
        │   Data Warehouse (dw schema)           │
        │  ┌────────────┐      ┌──────────────┐  │
        │  │ Dimensions │      │    Facts     │  │
        │  │  DimDate   │      │ PipelineRun  │  │
        │  │  DimPipe   │      │ ActivityRun  │  │
        │  │    DimIR   │      │ ComputeUsage │  │
        │  │ DimSource  │      │   DQEvents   │  │
        │  └────────────┘      └──────┬───────┘  │
        └─────────────────────────────┼──────────┘
                                      │
                      ┌───────────────┴───────────────┐
                      │     Power BI / Fabric          │
                      │   ┌───────────────────────┐   │
                      │   │   Health Dashboard    │   │
                      │   │  - Cost Analysis      │   │
                      │   │  - Regression Alerts  │   │
                      │   │  - IR Usage Trends    │   │
                      │   └───────────────────────┘   │
                      └───────────────────────────────┘
```

### 2.2 Technology Stack

- **Data Storage**: Azure SQL Database (or Microsoft Fabric Warehouse)
- **Infrastructure as Code**: Bicep
- **Orchestration**: Azure Data Factory (optional) / Fabric Data Factory
- **BI & Visualization**: Power BI Desktop / Power BI Service
- **ETL**: T-SQL stored procedures and MERGE statements
- **Deployment**: PowerShell scripts with Azure CLI

### 2.3 Data Flow

1. **Ingestion**:
   - Pipeline run logs from ADF/Fabric are ingested into staging tables (`stg.*`)
   - Compute usage data (Databricks DBUs) is ingested into `stg.ComputeUsage`
   - Data Quality events are ingested into `stg.DQEvents`

2. **Transformation**:
   - Staging data is transformed and loaded into dimensional data warehouse (`dw.*`)
   - Dimensions are upserted (DimPipeline, DimIntegrationRuntime, DimSourceSystem)
   - Facts are merged from staging (FactPipelineRun, FactActivityRun, FactComputeUsage, FactDQEvents)
   - Date keys are resolved from DimDate

3. **Visualization**:
   - Power BI connects to the data warehouse
   - DAX measures calculate metrics (cost, tokens, regression %)
   - Interactive dashboards display insights

## 3. Data Model

### 3.1 Schema Design

- **Staging Schema (`stg`)**: Raw data from source systems
- **Data Warehouse Schema (`dw`)**: Star schema with dimensions and facts

### 3.2 Dimension Tables

- **DimDate**: Date dimension with calendar attributes
- **DimPipeline**: Pipeline metadata (ID, name, environment, owner)
- **DimIntegrationRuntime**: Integration Runtime details (name, type, region)
- **DimSourceSystem**: Source system information (Salesforce, SAP, etc.)

### 3.3 Fact Tables

- **FactPipelineRun**: Pipeline run events (status, duration, tokens, cost)
- **FactActivityRun**: Activity-level execution details (rows read/written)
- **FactComputeUsage**: Compute resource usage (DBUs, tokens, cost)
- **FactDQEvents**: Data quality check results

### 3.4 Relationships

- FactPipelineRun → DimPipeline (Many-to-One)
- FactPipelineRun → DimDate (Many-to-One)
- FactPipelineRun → DimIntegrationRuntime (Many-to-One)
- FactPipelineRun → DimSourceSystem (Many-to-One)
- FactActivityRun → FactPipelineRun (Many-to-One)
- FactComputeUsage → FactPipelineRun (Many-to-One, optional)

## 4. Components

### 4.1 Infrastructure Components

- **Azure SQL Server**: Hosts the data warehouse database
- **Azure SQL Database**: Data warehouse with S0 or higher SKU
- **Azure Storage Account**: Optional, for staging file-based data
- **Azure Data Factory**: Optional, for orchestration
- **Log Analytics Workspace**: Optional, for monitoring

### 4.2 Data Components

- **Staging Tables**: Landing zone for raw data
- **Data Warehouse Tables**: Dimensional model
- **Stored Procedures**: ETL logic for upserting data
- **Views**: Optional, for common queries

### 4.3 BI Components

- **Power BI Model**: Data model with relationships
- **DAX Measures**: Calculated metrics (cost, tokens, regression %)
- **Visualizations**: 3 main report pages
  - Top 10 Costliest Pipelines
  - Performance Regression Analysis
  - IR Usage Trends

## 5. Deployment Architecture

### 5.1 Deployment Steps

1. **Infrastructure Deployment**:
   - Execute Bicep template to create Azure resources
   - Provision Azure SQL Server and Database
   - Configure firewall rules

2. **Database Setup**:
   - Execute DDL scripts to create schemas and tables
   - Execute DML scripts to load sample data
   - Create indexes and foreign keys

3. **BI Setup**:
   - Connect Power BI to Azure SQL Database
   - Import DAX measures
   - Build visualizations

### 5.2 Configuration

- Schema names (`dw`, `stg`) are configurable at project level
- Connection strings stored in deployment parameters
- Environment variables for credentials (use Azure Key Vault in production)

## 6. Scalability & Performance

### 6.1 Database Performance

- Indexes on date keys and foreign keys
- Partitioning consideration for large fact tables (future)
- Query optimization through covering indexes

### 6.2 Cost Optimization

- Use Basic/S0 SKU for development
- Scale up for production workloads
- Archive old data to reduce table size

### 6.3 Monitoring

- Azure Monitor for SQL Database metrics
- Log Analytics for pipeline execution logs
- Power BI usage metrics

## 7. Security

### 7.1 Authentication

- SQL authentication for database access
- Service principal for ADF/Fabric API calls
- Azure AD integration for Power BI (recommended)

### 7.2 Data Protection

- Encrypted connections (TLS 1.2)
- Row-level security in Power BI (optional)
- Sensitive data in Azure Key Vault

### 7.3 Access Control

- Azure RBAC for resource access
- SQL roles for database access
- Power BI workspace permissions

## 8. Maintenance

### 8.1 Data Refresh

- Daily ETL execution (recommended)
- Incremental loads from staging to warehouse
- Retention policy for historical data

### 8.2 Monitoring & Alerts

- Alert on ETL failures
- Cost threshold alerts
- Performance regression alerts (via Power BI)

## 9. Future Enhancements

- Real-time streaming ingestion
- Machine learning for anomaly detection
- Automated cost optimization recommendations
- Integration with Azure Cost Management
- Support for additional compute resources (Synapse, Data Lake)

## 10. References

- [Azure Data Factory Documentation](https://docs.microsoft.com/azure/data-factory/)
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Power BI Documentation](https://learn.microsoft.com/power-bi/)
- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/sql-database/)
