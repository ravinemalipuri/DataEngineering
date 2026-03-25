/*
    Sample records for data_quality_results.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

INSERT INTO [$(SchemaName)].data_quality_results (
    run_id,
    source_object_id,
    layer,
    column_name,
    check_type,
    check_params,
    status,
    metric_value,
    failure_count,
    row_count,
    dq_severity,
    run_time
) VALUES
('RUN_20241101_01', 1, 'BRONZE', 'customer_id', 'NOT_NULL', '{}', 'PASS', '{"null_count":0}', 0, 125000, 'FAIL', SYSUTCDATETIME()),
('RUN_20241101_01', 1, 'BRONZE', 'first_name', 'MAX_LENGTH', '{"max":100}', 'PASS', '{"violations":0}', 0, 125000, 'WARN', SYSUTCDATETIME()),
('RUN_20241101_01', 2, 'SILVER', 'account_name', 'NOT_NULL', '{}', 'FAIL', '{"null_count":12}', 12, 42000, 'FAIL', SYSUTCDATETIME());
GO


