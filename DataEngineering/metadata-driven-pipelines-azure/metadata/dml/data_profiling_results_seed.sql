/*
    Sample records for data_profiling_results.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

INSERT INTO [$(SchemaName)].data_profiling_results (
    run_id,
    source_object_id,
    layer,
    column_name,
    profile_type,
    profile_params,
    metric_value,
    sample_size,
    row_count,
    profiling_time
) VALUES
('RUN_20241101_01', 1, 'BRONZE', 'amount', 'MIN_MAX', '{"sample_pct":10}', '{"min":0.00,"max":24500.11}', 12500, 125000, SYSUTCDATETIME()),
('RUN_20241101_01', 1, 'BRONZE', 'customer_id', 'DISTINCT_COUNT', '{"approx":true}', '{"distinct":9800}', 12500, 125000, SYSUTCDATETIME()),
('RUN_20241101_01', 2, 'SILVER', 'industry', 'TOP_VALUES', '{"top":5}', '{"values":[["TECH",12000],["FINANCE",9000]]}', 4200, 42000, SYSUTCDATETIME());
GO


