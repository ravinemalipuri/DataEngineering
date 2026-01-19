/*
    Metadata table: data_quality_results
    Purpose: Stores outcomes of metadata-driven data quality & profiling checks.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].data_quality_results', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].data_quality_results;
GO

CREATE TABLE [$(SchemaName)].data_quality_results (
    dq_result_id        BIGINT IDENTITY(1,1) PRIMARY KEY,
    run_id              NVARCHAR(100) NOT NULL,
    source_object_id    INT NOT NULL REFERENCES [$(SchemaName)].source_objects(source_object_id),
    layer               NVARCHAR(20) NOT NULL,
    column_name         NVARCHAR(128) NULL,
    check_type          NVARCHAR(50) NOT NULL,
    check_params        NVARCHAR(MAX) NULL,
    status              NVARCHAR(10) NOT NULL CHECK (status IN ('PASS','FAIL')),
    metric_value        NVARCHAR(200) NULL,
    failure_count       BIGINT NULL,
    row_count           BIGINT NULL,
    dq_severity         NVARCHAR(20) NOT NULL DEFAULT ('WARN'),
    run_time             DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME())
);
GO
