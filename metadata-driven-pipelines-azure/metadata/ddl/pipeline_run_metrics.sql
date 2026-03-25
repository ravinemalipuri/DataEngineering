/*
    Metadata table: pipeline_run_metrics
    Purpose: capture Fabric pipeline run observability + ingestion throughput.
*/
::setvar DatabaseName metadata
::setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].pipeline_run_metrics', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].pipeline_run_metrics;
GO

CREATE TABLE [$(SchemaName)].pipeline_run_metrics (
    pipeline_metric_id        INT IDENTITY(1,1) PRIMARY KEY,
    workspaceid               NVARCHAR(200) NULL,
    pipeline_run_id           NVARCHAR(200) NULL,
    pipeline_id               NVARCHAR(200) NULL,
    pipeline_name             NVARCHAR(300) NULL,
    TriggerType               NVARCHAR(100) NULL,
    runStatus                 NVARCHAR(100) NULL,
    pipeline_start_time       DATETIME2(3) NULL,
    pipeline_end_time         DATETIME2(3) NULL,
    duration_ms               BIGINT NULL,
    error_code                NVARCHAR(200) NULL,
    error_message             NVARCHAR(MAX) NULL,
    retry_count               INT NULL,
    sla_breach                BIT NULL,
    data_volume_mb            DECIMAL(18,2) NULL,
    activity_count            INT NULL,
    cost_estimate             DECIMAL(18,2) NULL,
    run_parameters            NVARCHAR(MAX) NULL,
    environment               NVARCHAR(100) NULL,
    source_system_id          INT NOT NULL REFERENCES [$(SchemaName)].source_systems(source_system_id),
    source_system_name        NVARCHAR(200) NULL,
    source_object_name        NVARCHAR(200) NULL,
    load_type                 NVARCHAR(20) NOT NULL DEFAULT('INCREMENTAL'),
    skip_load                 BIT NOT NULL DEFAULT(0),
    batch_load_datetime       DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    load_status               NVARCHAR(50) NOT NULL DEFAULT('UNKNOWN'),
    rows_read                 BIGINT NULL,
    rows_copied               BIGINT NULL,
    deltalake_inserted        BIGINT NULL,
    deltalake_updated         BIGINT NULL,
    sql_max_datetime          DATETIME2(3) NULL,
    read_data_volume_mb       DECIMAL(18,2) NULL,
    written_data_volume_mb    DECIMAL(18,2) NULL
);
GO

