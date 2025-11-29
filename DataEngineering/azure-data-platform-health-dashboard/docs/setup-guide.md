# Azure Data Platform Health Dashboard - Setup Guide

## Prerequisites

Before starting the setup, ensure you have the following:

1. **Azure Subscription**: Active Azure subscription with permissions to create resources
2. **Azure CLI**: Installed and configured ([Installation Guide](https://docs.microsoft.com/cli/azure/install-azure-cli))
3. **Azure PowerShell Module**: Installed ([Installation Guide](https://docs.microsoft.com/powershell/azure/install-az-ps))
4. **SQL Tools**: One of the following:
   - `sqlcmd` (SQL Server Command Line Tools)
   - Azure PowerShell module (`Az.Sql`)
5. **Power BI Desktop**: For building the dashboard ([Download](https://powerbi.microsoft.com/desktop/))
6. **Git**: For cloning the repository (optional)

## Step-by-Step Setup

### Step 1: Clone or Download the Repository

```powershell
# Clone the repository (if using Git)
git clone <repository-url>
cd azure-data-platform-health-dashboard
```

Or download and extract the ZIP file to your local machine.

### Step 2: Prepare Azure Environment

#### 2.1 Login to Azure

```powershell
# Login to Azure
Connect-AzAccount

# Verify your subscription
Get-AzSubscription

# Set your subscription (if you have multiple)
Select-AzSubscription -SubscriptionId "<your-subscription-id>"
```

#### 2.2 Update Bicep Parameters

Edit `infra/bicep/parameters.json` and update the following:

- `sqlServerName`: Must be globally unique (e.g., `dphealth-sql-YOURNAME`)
- `storageAccountName`: Must be globally unique, lowercase, no hyphens (e.g., `dphealthstgYOURNAME`)
- `dataFactoryName`: Optional, must be globally unique if provided
- `sqlAdministratorLogin`: SQL admin username
- `sqlAdministratorLoginPassword`: Strong password for SQL admin

**Important**: Make a note of the SQL admin username and password - you'll need them later!

### Step 3: Deploy Infrastructure

#### Option A: Using the PowerShell Deployment Script (Recommended)

```powershell
# Navigate to the automation directory
cd infra\automation

# Run the deployment script
.\deploy.ps1 -ResourceGroupName "rg-dphealth-demo" -Location "eastus"

# If you want to skip SQL scripts initially (to review them first)
.\deploy.ps1 -ResourceGroupName "rg-dphealth-demo" -Location "eastus" -SkipSqlScripts
```

#### Option B: Manual Deployment with Azure CLI

```powershell
# Create resource group
az group create --name rg-dphealth-demo --location eastus

# Deploy Bicep template
cd infra\bicep
az deployment group create `
  --resource-group rg-dphealth-demo `
  --template-file main.bicep `
  --parameters @parameters.json

# Note the outputs (SQL server name, database name, etc.)
```

### Step 4: Execute SQL Scripts

If you skipped SQL scripts in Step 3, execute them manually:

#### 4.1 Using sqlcmd

```powershell
# Set variables (replace with your values from deployment)
$SqlServerName = "dphealth-sql-UNIQUE.database.windows.net"
$SqlDatabaseName = "DataPlatformHealthDW"
$SqlAdminLogin = "sqladmin"
$SqlAdminPassword = "YOUR_PASSWORD"

# Execute DDL scripts
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\ddl\00_create_schema.sql"
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\ddl\01_dim_date.sql"
# ... continue for all DDL scripts in order

# Execute staging table scripts
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\staging\stg_pipelinerun_adf.sql"
# ... continue for all staging scripts

# Execute DML scripts (sample data)
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\dml\load_dim_date_sample.sql"
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\dml\insert_sample_dims.sql"
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\dml\insert_sample_staging.sql"
sqlcmd -S $SqlServerName -d $SqlDatabaseName -U $SqlAdminLogin -P $SqlAdminPassword -i "..\sql\dml\upsert_from_staging_to_dw_sample.sql"
```

#### 4.2 Using PowerShell (Az.Sql Module)

```powershell
# Install Az.Sql module if not already installed
Install-Module -Name Az.Sql -Force

# Set variables
$ResourceGroupName = "rg-dphealth-demo"
$SqlServerName = "dphealth-sql-UNIQUE"  # Without .database.windows.net
$SqlDatabaseName = "DataPlatformHealthDW"
$SqlAdminLogin = "sqladmin"
$SecurePassword = ConvertTo-SecureString "YOUR_PASSWORD" -AsPlainText -Force

# Get SQL script content
$ScriptContent = Get-Content "sql\ddl\00_create_schema.sql" -Raw

# Execute script
Invoke-AzSqlDatabaseExecute `
  -ResourceGroupName $ResourceGroupName `
  -ServerName $SqlServerName `
  -DatabaseName $SqlDatabaseName `
  -Query $ScriptContent `
  -QueryTimeout 300

# Repeat for all scripts
```

### Step 5: Verify Data Load

Verify that sample data has been loaded:

```sql
-- Check dimension counts
SELECT 'DimDate' AS TableName, COUNT(*) AS RowCount FROM dw.DimDate
UNION ALL
SELECT 'DimPipeline', COUNT(*) FROM dw.DimPipeline
UNION ALL
SELECT 'DimIntegrationRuntime', COUNT(*) FROM dw.DimIntegrationRuntime
UNION ALL
SELECT 'DimSourceSystem', COUNT(*) FROM dw.DimSourceSystem;

-- Check fact counts
SELECT 'FactPipelineRun' AS TableName, COUNT(*) AS RowCount FROM dw.FactPipelineRun
UNION ALL
SELECT 'FactActivityRun', COUNT(*) FROM dw.FactActivityRun
UNION ALL
SELECT 'FactComputeUsage', COUNT(*) FROM dw.FactComputeUsage
UNION ALL
SELECT 'FactDQEvents', COUNT(*) FROM dw.FactDQEvents;

-- View sample data
SELECT TOP 5 * FROM dw.FactPipelineRun;
```

Expected results:
- DimDate: 10+ rows
- DimPipeline: 2-3 rows
- DimIntegrationRuntime: 2 rows
- DimSourceSystem: 2 rows
- FactPipelineRun: 5+ rows
- FactActivityRun: 3+ rows
- FactComputeUsage: 4+ rows
- FactDQEvents: 5+ rows

### Step 6: Configure Power BI Connection

#### 6.1 Open Power BI Desktop

1. Launch Power BI Desktop

2. **Get Data** → **Azure** → **Azure SQL Database**

3. Enter connection details:
   - **Server**: `dphealth-sql-UNIQUE.database.windows.net` (from deployment output)
   - **Database**: `DataPlatformHealthDW`
   - **Data Connectivity mode**: Import (recommended) or DirectQuery
   - Click **OK**

4. Enter credentials:
   - **Authentication method**: Database
   - **Username**: `sqladmin` (or your SQL admin login)
   - **Password**: Your SQL admin password
   - Click **Connect**

#### 6.2 Import Tables

1. In the **Navigator** window, select the following tables from the `dw` schema:
   - `DimDate`
   - `DimPipeline`
   - `DimIntegrationRuntime`
   - `DimSourceSystem`
   - `FactPipelineRun`
   - `FactActivityRun`
   - `FactComputeUsage`
   - `FactDQEvents`

2. Click **Load** (or **Transform Data** if you need to modify data first)

#### 6.3 Create Relationships

1. Switch to **Model** view (left sidebar)

2. Create relationships between fact and dimension tables:

   - **FactPipelineRun** → **DimPipeline** (PipelineKey)
   - **FactPipelineRun** → **DimDate** (DateKey)
   - **FactPipelineRun** → **DimIntegrationRuntime** (IRKey)
   - **FactPipelineRun** → **DimSourceSystem** (SourceKey)
   - **FactActivityRun** → **FactPipelineRun** (PipelineRunKey)
   - **FactActivityRun** → **DimPipeline** (PipelineKey)
   - **FactActivityRun** → **DimDate** (DateKey)
   - **FactComputeUsage** → **DimDate** (DateKey)
   - **FactComputeUsage** → **FactPipelineRun** (PipelineRunKey)
   - **FactDQEvents** → **DimDate** (DateKey)
   - **FactDQEvents** → **FactPipelineRun** (PipelineRunKey)

3. For each relationship:
   - Drag from foreign key to primary key
   - Set **Cardinality**: Many-to-One
   - Set **Cross filter direction**: Single (or Both if needed)

#### 6.4 Import DAX Measures

1. Open **Report** view

2. For each DAX file in `powerbi\dax\`:
   - Open the file in a text editor
   - Copy the measure definitions
   - In Power BI, go to the **Modeling** tab
   - Click **New Measure**
   - Paste the DAX code (one measure at a time)
   - Adjust table references if needed

**Note**: For bulk import, consider using Tabular Editor or Power BI Desktop's Advanced Editor.

### Step 7: Build Visualizations

Refer to `powerbi/report/report-description.md` for detailed visualization specifications.

#### Quick Start: Top 10 Costliest Pipelines

1. Create a new page: **Page 1: Top 10 Costliest Pipelines**

2. Add a **Table** visual:
   - **Values**: PipelineName (from DimPipeline), TotalBillingCost_Last24H
   - **Filters**: Add filter on FactPipelineRun[StartTime] >= TODAY() - 1
   - **Sort**: By TotalBillingCost_Last24H descending
   - **Top N**: Show Top 10

3. Add **Card** visuals for key metrics:
   - Total Cost (Last 24H)
   - Total Tokens (Last 24H)
   - Total Runs (Last 24H)

4. Add a **Bar Chart**:
   - **X-Axis**: PipelineName
   - **Y-Axis**: TotalBillingCost_Last24H

### Step 8: Publish to Power BI Service (Optional)

1. Click **File** → **Publish** → **Publish to Power BI**

2. Sign in to Power BI Service

3. Select a workspace and click **Select**

4. Once published, schedule data refresh:
   - Go to the dataset in Power BI Service
   - Click **Schedule Refresh**
   - Configure refresh frequency (daily recommended)

## Troubleshooting

### Common Issues

#### 1. SQL Connection Failed

**Error**: "Cannot connect to server"

**Solutions**:
- Verify firewall rules allow your IP address
- Check SQL server name (must include `.database.windows.net`)
- Verify credentials
- Ensure "Allow Azure services" firewall rule is enabled

#### 2. Bicep Deployment Failed

**Error**: "Resource name already exists"

**Solutions**:
- Use unique names for SQL server and storage account
- Update `parameters.json` with unique values

#### 3. SQL Script Execution Failed

**Error**: "Incorrect syntax near 'GO'"

**Solutions**:
- Use `sqlcmd` instead of Azure PowerShell (which doesn't support GO)
- Or split scripts that contain GO statements

#### 4. Power BI Relationships Not Working

**Error**: "Relationship cannot be created"

**Solutions**:
- Verify data types match (DateKey should be Integer in both tables)
- Check for null values in foreign keys
- Ensure primary keys are unique

### Getting Help

- Review error messages in Azure Portal → Resource Group → Deployments
- Check SQL database logs in Azure Portal
- Review Power BI Desktop query diagnostics

## Next Steps

1. **Customize Sample Data**: Modify `sql/dml/insert_sample_staging.sql` to add more realistic data
2. **Add Real Data Sources**: Integrate actual ADF/Fabric pipelines to ingest real logs
3. **Create Alerts**: Set up Power BI data alerts for cost thresholds
4. **Extend Dashboards**: Add more pages for specific use cases

## Additional Resources

- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/sql-database/)
- [Power BI Documentation](https://learn.microsoft.com/power-bi/)
- [DAX Reference](https://learn.microsoft.com/dax/)
- [Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
