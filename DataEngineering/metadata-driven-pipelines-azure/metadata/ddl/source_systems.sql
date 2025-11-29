/*
    Metadata table: source_systems
    Purpose: Stores connection and classification details for each upstream system.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].source_systems', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].source_systems;
GO

CREATE TABLE [$(SchemaName)].source_systems (
    source_system_id        INT IDENTITY(1,1) PRIMARY KEY,
    source_system_name      NVARCHAR(100) NOT NULL UNIQUE,
    system_type             NVARCHAR(50)  NOT NULL,       -- e.g., DB2, SAP, Salesforce
    connection_secret_name  NVARCHAR(200) NOT NULL,       -- Key Vault / Fabric credential
    default_database        NVARCHAR(128) NULL,
    is_active               BIT NOT NULL DEFAULT (1),
    business_owner_name     NVARCHAR(200) NULL,
    business_owner_email    NVARCHAR(320) NULL,
    technical_owner_name    NVARCHAR(200) NULL,
    technical_owner_email   NVARCHAR(320) NULL,
    escalation_emails       NVARCHAR(MAX) NULL, 
    created_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME()),
    updated_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME())
);
GO

