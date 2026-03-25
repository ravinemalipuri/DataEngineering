/*
    Metadata table: source_object_columns
    Purpose: Stores per-column technical metadata and DQ definitions.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].source_object_columns', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].source_object_columns;
GO

CREATE TABLE [$(SchemaName)].source_object_columns (
    source_object_id        INT NOT NULL REFERENCES [$(SchemaName)].source_objects(source_object_id),
    ordinal_position        INT NOT NULL,
    raw_column_name         NVARCHAR(128) NOT NULL,
    clean_column_name       AS REPLACE(REPLACE(raw_column_name, '#', ''), ' ', '_') PERSISTED,
    data_type               NVARCHAR(128) NOT NULL,
    nullable_flag           BIT NOT NULL,
    dq_rule_set             NVARCHAR(MAX) NULL,             -- JSON describing rules
    dq_severity             NVARCHAR(20) NOT NULL DEFAULT ('WARN'),
    is_active               BIT NOT NULL DEFAULT (1),
    created_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME()),
    updated_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT PK_source_object_columns PRIMARY KEY (source_object_id, raw_column_name)
);
GO
