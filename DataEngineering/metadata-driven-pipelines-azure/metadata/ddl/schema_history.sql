/*
    Metadata table: schema_history
    Purpose: Stores captured snapshots of source schemas per run.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].schema_history', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].schema_history;
GO

CREATE TABLE [$(SchemaName)].schema_history (
    schema_history_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_object_id    INT NOT NULL REFERENCES [$(SchemaName)].source_objects(source_object_id),
    run_id              NVARCHAR(100) NULL,
    column_name         NVARCHAR(128) NOT NULL,
    data_type           NVARCHAR(128) NOT NULL,
    nullable_flag       BIT NOT NULL,
    captured_time        DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME())
);
GO
