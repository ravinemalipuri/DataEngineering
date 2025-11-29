# ====================================================================
# Azure Data Platform Health Dashboard - Deployment Script
# ====================================================================
# This PowerShell script automates the deployment of the entire
# Data Platform Health Dashboard solution:
#   1. Login to Azure (if not already)
#   2. Deploy Azure infrastructure using Bicep
#   3. Execute SQL DDL scripts to create schema and tables
#   4. Execute SQL DML scripts to load sample data
# ====================================================================
# Prerequisites:
#   - Azure CLI installed and configured
#   - Azure PowerShell module installed (Az.Sql, Az.Resources)
#   - SQL Server tools (sqlcmd) or ability to execute SQL scripts
#   - Permissions to create resources in Azure subscription
# ====================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$false)]
    [string]$BicepParametersFile = ".\bicep\parameters.json",
    
    [Parameter(Mandatory=$false)]
    [string]$BicepTemplateFile = ".\bicep\main.bicep",
    
    [Parameter(Mandatory=$false)]
    [string]$SqlScriptsPath = "..\..\sql",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipInfraDeployment,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipSqlScripts
)

# Set error handling
$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$SqlPath = Join-Path $RepoRoot "sql"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Azure Data Platform Health Dashboard - Deployment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ====================================================================
# Step 1: Login to Azure and verify subscription
# ====================================================================
Write-Host "Step 1: Checking Azure authentication..." -ForegroundColor Yellow

try {
    $context = Get-AzContext
    if (-not $context) {
        Write-Host "Not logged in. Please log in to Azure..." -ForegroundColor Yellow
        Connect-AzAccount
    } else {
        Write-Host "Already logged in as: $($context.Account.Id)" -ForegroundColor Green
        Write-Host "Subscription: $($context.Subscription.Name)" -ForegroundColor Green
    }
} catch {
    Write-Host "Error connecting to Azure: $_" -ForegroundColor Red
    exit 1
}

# ====================================================================
# Step 2: Create Resource Group (if it doesn't exist)
# ====================================================================
Write-Host ""
Write-Host "Step 2: Checking resource group..." -ForegroundColor Yellow

$rg = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (-not $rg) {
    Write-Host "Creating resource group: $ResourceGroupName in $Location..." -ForegroundColor Yellow
    $rg = New-AzResourceGroup -Name $ResourceGroupName -Location $Location
    Write-Host "Resource group created successfully." -ForegroundColor Green
} else {
    Write-Host "Resource group already exists: $ResourceGroupName" -ForegroundColor Green
}

# ====================================================================
# Step 3: Deploy Infrastructure using Bicep
# ====================================================================
if (-not $SkipInfraDeployment) {
    Write-Host ""
    Write-Host "Step 3: Deploying Azure infrastructure using Bicep..." -ForegroundColor Yellow
    
    $bicepParamsPath = Join-Path $ScriptDir $BicepParametersFile
    $bicepTemplatePath = Join-Path $ScriptDir $BicepTemplateFile
    
    if (-not (Test-Path $bicepTemplatePath)) {
        Write-Host "ERROR: Bicep template not found at: $bicepTemplatePath" -ForegroundColor Red
        exit 1
    }
    
    try {
        # Read parameters from file if it exists
        $deploymentParams = @{}
        if (Test-Path $bicepParamsPath) {
            Write-Host "Loading parameters from: $bicepParamsPath" -ForegroundColor Gray
            $paramsContent = Get-Content $bicepParamsPath | ConvertFrom-Json
            $deploymentParams = @{}
            foreach ($param in $paramsContent.parameters.PSObject.Properties) {
                if ($param.Name -eq "sqlAdministratorLoginPassword") {
                    # Prompt for password securely
                    $securePassword = Read-Host "Enter SQL Administrator Password" -AsSecureString
                    $deploymentParams[$param.Name] = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))
                } else {
                    $deploymentParams[$param.Name] = $param.Value.value
                }
            }
        } else {
            Write-Host "Parameters file not found. Using defaults and prompting for required values." -ForegroundColor Yellow
            $deploymentParams["sqlAdministratorLoginPassword"] = Read-Host "Enter SQL Administrator Password" -AsSecureString
            $deploymentParams["sqlAdministratorLoginPassword"] = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($deploymentParams["sqlAdministratorLoginPassword"]))
        }
        
        Write-Host "Deploying Bicep template..." -ForegroundColor Gray
        $deployment = New-AzResourceGroupDeployment `
            -ResourceGroupName $ResourceGroupName `
            -TemplateFile $bicepTemplatePath `
            -TemplateParameterObject $deploymentParams `
            -Mode Incremental `
            -Verbose
        
        Write-Host "Infrastructure deployed successfully!" -ForegroundColor Green
        Write-Host "SQL Server: $($deployment.Outputs.sqlServerName.Value)" -ForegroundColor Green
        Write-Host "SQL Database: $($deployment.Outputs.sqlDatabaseName.Value)" -ForegroundColor Green
        
        # Store outputs for SQL script execution
        $script:SqlServerName = $deployment.Outputs.sqlServerFqdn.Value
        $script:SqlDatabaseName = $deployment.Outputs.sqlDatabaseName.Value
        $script:SqlAdminLogin = $deploymentParams["sqlAdministratorLogin"]
        $script:SqlAdminPassword = $deploymentParams["sqlAdministratorLoginPassword"]
        
    } catch {
        Write-Host "ERROR deploying infrastructure: $_" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Skipping infrastructure deployment (user requested skip)." -ForegroundColor Yellow
    Write-Host "Please provide SQL connection details manually:" -ForegroundColor Yellow
    $script:SqlServerName = Read-Host "SQL Server FQDN"
    $script:SqlDatabaseName = Read-Host "SQL Database Name"
    $script:SqlAdminLogin = Read-Host "SQL Admin Login"
    $securePassword = Read-Host "SQL Admin Password" -AsSecureString
    $script:SqlAdminPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))
}

# ====================================================================
# Step 4: Execute SQL Scripts
# ====================================================================
if (-not $SkipSqlScripts) {
    Write-Host ""
    Write-Host "Step 4: Executing SQL scripts..." -ForegroundColor Yellow
    
    # Check if sqlcmd is available
    $sqlcmdPath = Get-Command sqlcmd -ErrorAction SilentlyContinue
    if (-not $sqlcmdPath) {
        Write-Host "WARNING: sqlcmd not found in PATH. Attempting to use SQL Server PowerShell module..." -ForegroundColor Yellow
        
        # Try using Invoke-Sqlcmd from Az.Sql module
        try {
            Import-Module Az.Sql -ErrorAction Stop
            $UseAzSql = $true
            Write-Host "Using Az.Sql module for SQL execution." -ForegroundColor Green
        } catch {
            Write-Host "ERROR: Neither sqlcmd nor Az.Sql module available. Please install one of them." -ForegroundColor Red
            exit 1
        }
    } else {
        $UseAzSql = $false
        Write-Host "Using sqlcmd for SQL execution." -ForegroundColor Green
    }
    
    # Build connection string
    $connectionString = "Server=$($script:SqlServerName);Database=$($script:SqlDatabaseName);User Id=$($script:SqlAdminLogin);Password=$($script:SqlAdminPassword);Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
    
    # Define script execution order
    $scriptOrder = @(
        "ddl\00_create_schema.sql",
        "ddl\01_dim_date.sql",
        "ddl\02_dim_pipeline.sql",
        "ddl\03_dim_integration_runtime.sql",
        "ddl\04_dim_sourcesystem.sql",
        "ddl\05_fact_pipelinerun.sql",
        "ddl\06_fact_activityrun.sql",
        "ddl\07_fact_computeusage.sql",
        "ddl\08_fact_dqevents.sql",
        "ddl\09_foreign_keys_and_indexes.sql",
        "staging\stg_pipelinerun_adf.sql",
        "staging\stg_activityrun_adf.sql",
        "staging\stg_pipelinerun_fabric.sql",
        "staging\stg_computeusage.sql",
        "staging\stg_dqevents.sql",
        "dml\load_dim_date_sample.sql",
        "dml\insert_sample_dims.sql",
        "dml\insert_sample_staging.sql",
        "dml\upsert_from_staging_to_dw_sample.sql"
    )
    
    foreach ($script in $scriptOrder) {
        $scriptPath = Join-Path $SqlPath $script
        if (Test-Path $scriptPath) {
            Write-Host "Executing: $script" -ForegroundColor Gray
            try {
                if ($UseAzSql) {
                    $scriptContent = Get-Content $scriptPath -Raw
                    $securePassword = ConvertTo-SecureString $script:SqlAdminPassword -AsPlainText -Force
                    $credential = New-Object System.Management.Automation.PSCredential($script:SqlAdminLogin, $securePassword)
                    
                    Invoke-AzSqlDatabaseExecute `
                        -ResourceGroupName $ResourceGroupName `
                        -ServerName $script:SqlServerName.Split('.')[0] `
                        -DatabaseName $script:SqlDatabaseName `
                        -Query $scriptContent `
                        -QueryTimeout 300 `
                        -ErrorAction Stop | Out-Null
                } else {
                    $env:SQLCMDSERVER = $script:SqlServerName
                    $env:SQLCMDUSER = $script:SqlAdminLogin
                    $env:SQLCMDPASSWORD = $script:SqlAdminPassword
                    $env:SQLCMDDB = $script:SqlDatabaseName
                    
                    & sqlcmd -i $scriptPath -b | Out-Null
                    if ($LASTEXITCODE -ne 0) {
                        throw "sqlcmd exited with code $LASTEXITCODE"
                    }
                }
                Write-Host "  ✓ $script completed" -ForegroundColor Green
            } catch {
                Write-Host "  ✗ ERROR executing $script : $_" -ForegroundColor Red
                Write-Host "    Continuing with next script..." -ForegroundColor Yellow
            }
        } else {
            Write-Host "  ⚠ Script not found: $scriptPath" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    Write-Host "SQL scripts execution completed!" -ForegroundColor Green
} else {
    Write-Host "Skipping SQL scripts execution (user requested skip)." -ForegroundColor Yellow
}

# ====================================================================
# Summary
# ====================================================================
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Deployment Summary" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor White
Write-Host "SQL Server: $($script:SqlServerName)" -ForegroundColor White
Write-Host "SQL Database: $($script:SqlDatabaseName)" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open Power BI Desktop" -ForegroundColor White
Write-Host "2. Connect to Azure SQL Database using:" -ForegroundColor White
Write-Host "   Server: $($script:SqlServerName)" -ForegroundColor Gray
Write-Host "   Database: $($script:SqlDatabaseName)" -ForegroundColor Gray
Write-Host "   Username: $($script:SqlAdminLogin)" -ForegroundColor Gray
Write-Host "3. Import the DAX measures from powerbi\dax\" -ForegroundColor White
Write-Host "4. Build your Power BI report using the star schema tables" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see: docs\setup-guide.md" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

