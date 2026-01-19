/*
    Metadata table: pipeline_run_metrics
    Purpose: capture Fabric pipeline run observability + ingestion throughput.
*/
::setvar DatabaseName metadata_db
::setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].pipeline_run_metrics', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].pipeline_run_metrics;
GO

CREATE TABLE [$(SchemaName)].PipelineRunLogs (
    pipeline_metric_id     INT IDENTITY(1,1) PRIMARY KEY,
    workspaceid
    pipeline_run_id
    pipeline_id
    pipeline_name
    TriggerType
    runStatus
    pipeline_start_time
    pipeline_end_time
    duration_ms
    error_code
    error_message
    retry_count
    sla_breach
    data_volume_mb
    activity_count
    cost_estimate
    run_parameters
    environment

    load_type              NVARCHAR(20) NOT NULL DEFAULT('INCREMENTAL'),
    skip_load              BIT NOT NULL DEFAULT(0),
    batch_load_datetime    DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    load_status            NVARCHAR(50) NOT NULL,
    rows_read              BIGINT NULL,
    rows_copied            BIGINT NULL,
    deltalake_inserted     BIGINT NULL,
    deltalake_updated      BIGINT NULL,
    sql_max_datetime       DATETIME2(3) NULL,
    pipeline_start_time    DATETIME2(3) NULL,
    pipeline_end_time      DATETIME2(3) NULL,
    read_data_volume_mb         DECIMAL(18,2) NULL,
    written_data_volume_mb         DECIMAL(18,2) NULL
);
GO

