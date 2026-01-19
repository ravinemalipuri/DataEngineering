/*
    Metadata table: schema_change_log
    Purpose: Records compatible/incompatible schema changes detected by the framework.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].schema_change_log', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].schema_change_log;
GO

CREATE TABLE [$(SchemaName)].schema_change_log (
    schema_change_id    BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_object_id    INT NOT NULL REFERENCES [$(SchemaName)].source_objects(source_object_id),
    run_id              NVARCHAR(100) NULL,
    change_type         NVARCHAR(50) NULL,
    change_detail       NVARCHAR(MAX) NOT NULL,
    compatibility_flag  NVARCHAR(20) NOT NULL CHECK (compatibility_flag IN ('COMPATIBLE','INCOMPATIBLE')),
    action_taken        NVARCHAR(200) NOT NULL,
    logged_utc          DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME())
);
GO
