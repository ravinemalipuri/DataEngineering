# Azure Data Platform Health Dashboard

> **End-to-end Azure data platform monitoring solution showcasing pipeline performance, cost analysis, and regression detection**

[![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=Power%20BI&logoColor=black)](https://powerbi.microsoft.com/)
[![Bicep](https://img.shields.io/badge/Bicep-005EFF?style=flat&logo=azure-devops&logoColor=white)](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)

## 📋 Overview

The **Azure Data Platform Health Dashboard** is a complete, production-ready portfolio project that demonstrates end-to-end data engineering capabilities. This solution provides comprehensive monitoring, cost analysis, and performance regression detection for Azure Data Factory (ADF) and Microsoft Fabric pipelines.

### Key Features

- ✅ **Cost Visibility**: Identify top 10 costliest pipelines and compute resources
- ✅ **Performance Monitoring**: Track pipeline run times, token usage, and throughput
- ✅ **Regression Detection**: Automatically detect performance degradation vs 7-day baseline
- ✅ **IR Usage Analytics**: Analyze Integration Runtime usage patterns and trends
- ✅ **Star Schema Data Warehouse**: Production-grade dimensional model
- ✅ **Infrastructure as Code**: Fully automated deployment with Bicep
- ✅ **Power BI Dashboards**: Interactive visualizations with DAX measures

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   ADF    │  │  Fabric  │  │Databricks│  │   DQ     │   │
│  │  Logs    │  │  Logs    │  │  Usage   │  │  Events  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │      Staging Layer (stg schema)      │
        └──────────────────┬──────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │    ETL Process (Upsert Scripts)      │
        └──────────────────┬──────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │   Data Warehouse (dw schema)          │
        │  ┌────────────┐      ┌────────────┐  │
        │  │ Dimensions │      │    Facts   │  │
        │  │  DimDate   │      │PipelineRun │  │
        │  │  DimPipe   │      │ActivityRun │  │
        │  │    DimIR   │      │ComputeUsage│  │
        │  │ DimSource  │      │  DQEvents  │  │
        │  └────────────┘      └─────┬──────┘  │
        └───────────────────────────┼──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │     Power BI Dashboard         │
                    │  • Cost Analysis               │
                    │  • Regression Detection        │
                    │  • IR Usage Trends             │
                    └───────────────────────────────┘
```

## 📁 Repository Structure

```
azure-data-platform-health-dashboard/
│
├── README.md                          # This file
│
├── docs/                              # Documentation
│   ├── design-document.md            # Architecture and design details
│   ├── setup-guide.md                # Step-by-step setup instructions
│   ├── metrics-matrix.md             # Complete metrics catalog
│   └── data-model.md                 # Data model documentation
│
├── sql/                               # SQL scripts
│   ├── config/
│   │   └── schema_config.sql         # Schema configuration
│   ├── ddl/                           # Data Definition Language
│   │   ├── 00_create_schema.sql      # Create dw and stg schemas
│   │   ├── 01_dim_date.sql           # Date dimension
│   │   ├── 02_dim_pipeline.sql       # Pipeline dimension
│   │   ├── 03_dim_integration_runtime.sql
│   │   ├── 04_dim_sourcesystem.sql
│   │   ├── 05_fact_pipelinerun.sql
│   │   ├── 06_fact_activityrun.sql
│   │   ├── 07_fact_computeusage.sql
│   │   ├── 08_fact_dqevents.sql
│   │   └── 09_foreign_keys_and_indexes.sql
│   ├── staging/                       # Staging table DDL
│   │   ├── stg_pipelinerun_adf.sql
│   │   ├── stg_activityrun_adf.sql
│   │   ├── stg_pipelinerun_fabric.sql
│   │   ├── stg_computeusage.sql
│   │   └── stg_dqevents.sql
│   └── dml/                           # Data Manipulation Language
│       ├── load_dim_date_sample.sql   # Load 10+ days of dates
│       ├── insert_sample_dims.sql     # Load sample dimensions
│       ├── insert_sample_staging.sql  # Load sample staging data
│       └── upsert_from_staging_to_dw_sample.sql  # ETL logic
│
├── infra/                             # Infrastructure as Code
│   ├── bicep/
│   │   ├── main.bicep                 # Main Bicep template
│   │   └── parameters.json            # Parameter file (update before deployment)
│   └── automation/
│       └── deploy.ps1                 # PowerShell deployment script
│
├── pipelines/                         # Data pipeline definitions
│   ├── adf/
│   │   ├── pl_ingest_adf_pipelineruns.json
│   │   └── pipeline.json
│   └── fabric/
│       └── pl_ingest_fabric_pipelineruns.json
│
├── powerbi/                           # Power BI assets
│   ├── dax/
│   │   ├── pipeline_metrics.dax       # Pipeline performance measures
│   │   ├── cost_metrics.dax           # Cost analysis measures
│   │   ├── regression_metrics.dax     # Regression detection measures
│   │   └── ir_usage.dax               # IR usage measures
│   └── report/
│       └── report-description.md      # Report page specifications
│
└── samples/                           # Sample data files
    ├── adf_pipeline_run_sample.json
    ├── adf_activity_run_sample.json
    ├── fabric_pipeline_run_sample.json
    ├── compute_usage_sample.csv
    └── dq_events_sample.json
```

## 🚀 Quick Start

### Prerequisites

- [Azure Subscription](https://azure.microsoft.com/free/) (free tier eligible)
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- [Azure PowerShell Module](https://docs.microsoft.com/powershell/azure/install-az-ps)
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (optional, for dashboard)
- SQL tools: `sqlcmd` or `Az.Sql` PowerShell module

### 1. Clone the Repository

```bash
git clone <repository-url>
cd azure-data-platform-health-dashboard
```

### 2. Update Configuration

Edit `infra/bicep/parameters.json` and update:
- `sqlServerName`: Must be globally unique
- `storageAccountName`: Must be globally unique (lowercase, no hyphens)
- `sqlAdministratorLogin`: SQL admin username
- `sqlAdministratorLoginPassword`: Strong password

### 3. Deploy Infrastructure

```powershell
# Navigate to automation directory
cd infra\automation

# Run deployment script
.\deploy.ps1 -ResourceGroupName "rg-dphealth-demo" -Location "eastus"
```

This will:
- Create resource group
- Deploy Azure SQL Server and Database
- Create staging and warehouse tables
- Load sample data

### 4. Connect Power BI

1. Open Power BI Desktop
2. Get Data → Azure → Azure SQL Database
3. Enter server and database details
4. Import `dw` schema tables
5. Create relationships (see `docs/setup-guide.md`)
6. Import DAX measures from `powerbi/dax/`
7. Build visualizations (see `powerbi/report/report-description.md`)

### 5. View Results

Open the Power BI dashboard to see:
- **Page 1**: Top 10 costliest pipelines (last 24 hours)
- **Page 2**: Performance regression analysis
- **Page 3**: Cost & token/DBU trends by Integration Runtime

## 📊 Dashboard Pages

### Page 1: Top 10 Costliest Pipelines (Last 24 Hours)

**Purpose**: Identify pipelines consuming the most resources

**Metrics**:
- Total Cost (Last 24H)
- Total Tokens (Last 24H)
- Total DBUs (Last 24H)
- Average Cost Per Run

**Visualizations**:
- Table: Top 10 pipelines by cost
- Bar Chart: Cost breakdown by pipeline
- Cards: Key aggregate metrics

### Page 2: Performance Regression vs Last Week

**Purpose**: Detect pipelines with degraded performance

**Metrics**:
- Token Regression % (vs 7-day baseline)
- Duration Regression % (vs 7-day baseline)
- Pipeline-level regression indicators
- Performance Regression Score

**Visualizations**:
- Table: Pipelines with regression (>10% threshold)
- Scatter Chart: Token regression analysis
- Line Chart: Token trend comparison

### Page 3: Cost & Token/DBU Trends by IR

**Purpose**: Analyze Integration Runtime usage patterns

**Metrics**:
- Daily Cost by IR
- Daily Tokens by IR
- Daily DBU Usage
- IR-level aggregates

**Visualizations**:
- Line Charts: Daily trends by IR
- Stacked Bar Chart: Cost distribution
- Donut Chart: Cost share by IR
- Table: IR usage summary

## 🗄️ Data Model

### Star Schema Design

**Dimensions**:
- `DimDate`: Date dimension for time-based analysis
- `DimPipeline`: Pipeline metadata
- `DimIntegrationRuntime`: IR metadata
- `DimSourceSystem`: Source system metadata

**Facts**:
- `FactPipelineRun`: Pipeline run events (status, duration, tokens, cost)
- `FactActivityRun`: Activity-level execution details
- `FactComputeUsage`: Compute resource usage (DBUs, tokens)
- `FactDQEvents`: Data quality check results

See `docs/data-model.md` for detailed schema documentation.

## 📈 Key Metrics

### Cost Metrics
- Total Billing Cost (Last 24H, 7D, 30D)
- Cost by Integration Runtime
- Average Cost Per Run
- Cost Per Token / Cost Per Row

### Performance Metrics
- Total Pipeline Runs
- Success Rate
- Average Duration
- Average Throughput (rows/second)
- Total Tokens Used

### Regression Metrics
- Token Regression % (vs 7-day baseline)
- Duration Regression % (vs 7-day baseline)
- Performance Regression Score (0-100)
- Pipeline-level regression indicators

### IR Usage Metrics
- Daily Tokens by IR
- Daily Cost by IR
- Daily DBU Usage
- Average Tokens/Cost Per Run by IR

See `docs/metrics-matrix.md` for complete metrics catalog.

## 🔧 Configuration

### Schema Names

Schema names (`dw` and `stg`) are configurable. See `sql/config/schema_config.sql` for details.

**Default**:
- Data Warehouse Schema: `dw`
- Staging Schema: `stg`

### Compute Usage Source

By default, the solution uses a simple synthetic `stg.ComputeUsage` table. To integrate with real sources:

- **Databricks**: Query `system.billing.usage` table
- **Azure Cost Management**: Use Cost Management API
- **Fabric**: Query Fabric billing logs

Update `sql/staging/stg_computeusage.sql` and `sql/dml/upsert_from_staging_to_dw_sample.sql` accordingly.

## 📚 Documentation

- **[Design Document](docs/design-document.md)**: Architecture, components, and design decisions
- **[Setup Guide](docs/setup-guide.md)**: Step-by-step setup instructions
- **[Metrics Matrix](docs/metrics-matrix.md)**: Complete metrics catalog with DAX measures
- **[Data Model](docs/data-model.md)**: Detailed schema documentation

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Data Storage** | Azure SQL Database (S0+) |
| **Infrastructure as Code** | Bicep |
| **Orchestration** | Azure Data Factory (optional) / Fabric Data Factory |
| **BI & Visualization** | Power BI Desktop / Power BI Service |
| **ETL** | T-SQL (MERGE statements) |
| **Deployment** | PowerShell + Azure CLI |

## 🎯 Use Cases

This project is ideal for:

1. **Portfolio Projects**: Showcase data engineering skills
2. **Proof of Concept**: Demonstrate Azure + Fabric + Power BI integration
3. **Learning**: Understand dimensional modeling, ETL, and BI best practices
4. **Small Production Environments**: Deploy for actual monitoring needs

## 📝 Sample Data

The repository includes sample data files in `samples/`:

- ADF pipeline run logs (JSON)
- ADF activity run logs (JSON)
- Fabric pipeline run logs (JSON)
- Compute usage data (CSV)
- Data quality events (JSON)

These can be used for testing and demonstrations.

## 🔒 Security Considerations

- **SQL Authentication**: Use SQL authentication for demo. In production, use Azure AD integration.
- **Password Management**: Store passwords in Azure Key Vault (production).
- **Network Security**: Configure firewall rules appropriately.
- **Access Control**: Use Azure RBAC and SQL roles for access control.

## 💰 Cost Estimation

**Development/Testing** (Approximate monthly cost):
- Azure SQL Database (S0): ~$15/month
- Storage Account (Standard LRS): ~$0.02/GB/month
- Azure Data Factory (Basic): ~$1/month
- **Total**: ~$20-30/month

**Production** (Scale as needed):
- Azure SQL Database (P1+): $200+/month
- Additional compute resources as required

See [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) for accurate estimates.

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

## 📄 License

This project is provided as-is for portfolio and educational purposes.

## 🙏 Acknowledgments

- Microsoft Azure documentation
- Power BI community
- Data engineering best practices from industry leaders

## 📞 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review error messages and troubleshooting sections
3. Verify prerequisites and configuration

## 🔗 Related Resources

- [Azure Data Factory Documentation](https://docs.microsoft.com/azure/data-factory/)
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Power BI Documentation](https://learn.microsoft.com/power-bi/)
- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/sql-database/)
- [Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- [DAX Reference](https://learn.microsoft.com/dax/)

---

**Built with ❤️ for the data engineering community**

*Last Updated: January 2025*
