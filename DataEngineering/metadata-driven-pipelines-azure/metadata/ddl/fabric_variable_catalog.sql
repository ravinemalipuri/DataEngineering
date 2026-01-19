/*
    Metadata table: fabric_variable_catalog
    Purpose: Central catalog for pipeline variables, their values per environment, and governance hints.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
::setvar DatabaseName metadata_db
::setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].fabric_variable_catalog', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].fabric_variable_catalog;
GO

/*
    Legend for LOV (List of Values) hints:
        variable_category:
            ('governance', 'Naming standards, ownership, tagging')
            ('pathing', 'OneLake, Lakehouse, folder and table paths')
            ('connectivity', 'Source/target endpoints (non-secret)')
            ('security', 'Secret references, auth modes, key vault')
            ('logging', 'Audit logs, metrics, observability')
            ('data_quality', 'DQ rules, thresholds, quarantine')
            ('performance', 'Concurrency, batch size, tuning')
            ('orchestration', 'Triggers, retries, scheduling')
            ('schema', 'Schema drift, evolution, metadata')
            ('devops', 'CI/CD, release, promotion')
            ('cost_control', 'Capacity, throttles, limits')
            ('retention', 'Data & log retention policies')
        scope_level:
            ('factory', 'Fabric Data Factory / tenant-wide variables')
            ('workspace', 'Workspace or environment-specific variables (Dev/Test/Prod)')
            ('pipeline', 'Runtime pipeline parameters (per run / per entity)')
        environment:
            ('global', 'Applies to all environments')
            ('dev', 'Development environment')
            ('test', 'Test / QA environment')
            ('prod', 'Production environment')
*/

CREATE TABLE [$(SchemaName)].fabric_variable_catalog (
    variable_id            BIGINT IDENTITY(1,1) PRIMARY KEY,
    variable_name          VARCHAR(200) NOT NULL,
    scope_level            VARCHAR(50)  NOT NULL,
    category               VARCHAR(50)  NOT NULL,
    purpose                VARCHAR(200) NOT NULL,
    default_value          VARCHAR(MAX) NULL,
    dev_value              VARCHAR(MAX) NULL,
    test_value             VARCHAR(MAX) NULL,
    prod_value             VARCHAR(MAX) NULL,
    is_secret              BIT NOT NULL DEFAULT 0,
    fabric_usage           VARCHAR(200) NULL,
    databricks_usage       VARCHAR(200) NULL,
    owner_team             VARCHAR(100) NULL,
    owner_contact          VARCHAR(200) NULL,
    is_active              BIT NOT NULL DEFAULT 1,
    config_version         VARCHAR(50) NOT NULL DEFAULT 'v1',
    effective_from_ts      DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    effective_to_ts        DATETIME2(3) NULL,
    created_by             VARCHAR(100) NOT NULL DEFAULT SYSTEM_USER,
    created_ts             DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_by             VARCHAR(100) NULL,
    updated_ts             DATETIME2(3) NULL,
    CONSTRAINT uq_variable UNIQUE (variable_name, scope_level, config_version)
);
GO

*** End Patch

