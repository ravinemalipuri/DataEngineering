/*
    Metadata table: source_objects
    Purpose: Configures ingestion behavior per physical table/file.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].source_objects', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].source_objects;
GO

CREATE TABLE [$(SchemaName)].source_objects (
    source_object_id        INT IDENTITY(1,1) PRIMARY KEY,
    source_system_id        INT NOT NULL REFERENCES [$(SchemaName)].source_systems(source_system_id),
    source_object_name      NVARCHAR(200) NOT NULL,           -- schema.table or file path
    target_layer            NVARCHAR(20) NOT NULL CHECK (target_layer IN ('BRONZE','SILVER','GOLD')),
    target_path             NVARCHAR(500) NOT NULL,
    load_type               NVARCHAR(20) NOT NULL CHECK (load_type IN ('FULL','INCREMENTAL','HYBRID')),
    hash_strategy           NVARCHAR(20) NOT NULL CHECK (hash_strategy IN ('NONE','ROW_HASH','KEY_HASH')),
    business_keys           NVARCHAR(1000) NULL,               -- JSON array of column names
    watermark_column        NVARCHAR(128) NULL,
    dq_enabled              BIT NOT NULL DEFAULT (1),
    profiling_enabled       BIT NOT NULL DEFAULT (0),
    dq_fail_behavior        NVARCHAR(20) NOT NULL DEFAULT ('WARN'),
    schema_compat_profile   NVARCHAR(50) NOT NULL DEFAULT ('DEFAULT'),
    quarantine_path         NVARCHAR(500) NULL,
    load_notes              NVARCHAR(1000) NULL,
    last_success_run        DATETIME2(3) NULL,
    is_active               BIT NOT NULL DEFAULT (1),
    business_owner_name     NVARCHAR(200) NULL,
    business_owner_email    NVARCHAR(320) NULL,
    technical_owner_name    NVARCHAR(200) NULL,
    technical_owner_email   NVARCHAR(320) NULL,
    escalation_emails       NVARCHAR(MAX) NULL,  -- optional JSON array for table-specific alerts
    created_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME()),
    updated_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT UQ_source_object UNIQUE (source_system_id, source_object_name)
);
GO
