/*
    Metadata table: data_profiling_results
    Purpose: Stores column-level profiling metrics (min/max, distinct counts, etc.).
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].data_profiling_results', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].data_profiling_results;
GO

CREATE TABLE [$(SchemaName)].data_profiling_results (
    profiling_result_id  BIGINT IDENTITY(1,1) PRIMARY KEY,
    run_id               NVARCHAR(100) NOT NULL,
    source_object_id     INT NOT NULL REFERENCES [$(SchemaName)].source_objects(source_object_id),
    layer                NVARCHAR(20) NOT NULL,
    column_name          NVARCHAR(128) NULL,
    profile_type         NVARCHAR(50) NOT NULL,             -- e.g., MIN_MAX, DISTINCT_COUNT
    profile_params       NVARCHAR(MAX) NULL,                -- JSON with thresholds or sampling %
    metric_value         NVARCHAR(200) NULL,                -- Serialized metrics JSON
    sample_size          BIGINT NULL,
    row_count            BIGINT NULL,
    profiling_time       DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME())
);
GO


