// ====================================================================
// Azure Data Platform Health Dashboard - Infrastructure as Code (Bicep)
// ====================================================================
// This Bicep template provisions the Azure infrastructure required for
// the Data Platform Health Dashboard solution:
//   - Resource Group (created outside, passed as parameter)
//   - Azure SQL Server and Database
//   - Azure Data Factory (optional, for pipeline orchestration)
//   - Storage Account (for staging data if needed)
//   - Log Analytics Workspace (optional, for monitoring)
// ====================================================================

@description('Location for all resources. Defaults to resource group location.')
param location string = resourceGroup().location

@description('Name of the Azure SQL Server (must be globally unique)')
param sqlServerName string

@description('Name of the Azure SQL Database')
@allowed(['Basic', 'S0', 'S1', 'S2', 'S3', 'P1', 'P2', 'P4', 'P6', 'P11', 'P15'])
param sqlDatabaseSku string = 'S0'

@description('Name of the storage account (must be globally unique, lowercase)')
param storageAccountName string

@description('Name of the Azure Data Factory (optional, leave empty to skip)')
param dataFactoryName string = ''

@description('Name of the Log Analytics Workspace (optional, leave empty to skip)')
param logAnalyticsWorkspaceName string = ''

@description('SQL Server Administrator Login')
@secure()
param sqlAdministratorLogin string = 'sqladmin'

@description('SQL Server Administrator Password')
@secure()
param sqlAdministratorLoginPassword string

@description('Enable public network access for SQL Server')
param enableSqlPublicNetworkAccess bool = true

@description('Tags to apply to all resources')
param tags object = {}

// Variables
var sqlDatabaseName = 'DataPlatformHealthDW'
var storageAccountKind = 'StorageV2'
var storageAccountSku = 'Standard_LRS'

// ====================================================================
// Azure SQL Server
// ====================================================================
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: sqlServerName
  location: location
  tags: tags
  properties: {
    administratorLogin: sqlAdministratorLogin
    administratorLoginPassword: sqlAdministratorLoginPassword
    version: '12.0'
    minimalTlsVersion: '1.2'
    publicNetworkAccess: enableSqlPublicNetworkAccess ? 'Enabled' : 'Disabled'
  }
}

// SQL Server Firewall Rule - Allow Azure Services
resource sqlServerFirewallRuleAzure 'Microsoft.Sql/servers/firewallRules@2023-05-01-preview' = {
  parent: sqlServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// SQL Server Firewall Rule - Allow current client IP (optional)
// Note: In production, you would add specific IP ranges instead
resource sqlServerFirewallRuleClient 'Microsoft.Sql/servers/firewallRules@2023-05-01-preview' = {
  parent: sqlServer
  name: 'AllowClientIP'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '255.255.255.255'
  }
}

// ====================================================================
// Azure SQL Database
// ====================================================================
resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-05-01-preview' = {
  parent: sqlServer
  name: sqlDatabaseName
  location: location
  tags: tags
  sku: {
    name: sqlDatabaseSku
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    maxSizeBytes: 2147483648 // 2 GB (adjust based on SKU)
    catalogCollation: 'SQL_Latin1_General_CP1_CI_AS'
    zoneRedundant: false
    requestedBackupStorageRedundancy: 'Local'
  }
}

// ====================================================================
// Storage Account (for staging or file-based data if needed)
// ====================================================================
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: tags
  kind: storageAccountKind
  sku: {
    name: storageAccountSku
  }
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    defaultToOAuthAuthentication: false
  }
}

// Storage Account Blob Container for staging data
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: storageAccount::default
  name: 'staging-data'
  properties: {
    publicAccess: 'None'
  }
}

// ====================================================================
// Azure Data Factory (optional)
// ====================================================================
resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' = if dataFactoryName != '' {
  name: dataFactoryName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    repoConfiguration: {}
  }
}

// ====================================================================
// Log Analytics Workspace (optional, for monitoring)
// ====================================================================
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = if logAnalyticsWorkspaceName != '' {
  name: logAnalyticsWorkspaceName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// ====================================================================
// Outputs
// ====================================================================
output sqlServerName string = sqlServer.name
output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
output sqlDatabaseName string = sqlDatabase.name
output sqlConnectionString string = 'Server=tcp:${sqlServer.properties.fullyQualifiedDomainName},1433;Initial Catalog=${sqlDatabaseName};Persist Security Info=False;User ID=${sqlAdministratorLogin};Password=${sqlAdministratorLoginPassword};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
output storageAccountName string = storageAccount.name
output storageAccountPrimaryEndpoint string = storageAccount.properties.primaryEndpoints.blob
output dataFactoryName string = dataFactoryName != '' ? dataFactory.name : ''
output logAnalyticsWorkspaceId string = logAnalyticsWorkspaceName != '' ? logAnalyticsWorkspace.id : ''
