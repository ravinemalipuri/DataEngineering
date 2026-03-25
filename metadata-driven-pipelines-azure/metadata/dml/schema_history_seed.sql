/*
    Sample records for schema_history snapshots.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

INSERT INTO [$(SchemaName)].schema_history (
    source_object_id,
    run_id,
    column_name,
    data_type,
    nullable_flag,
    captured_time
) VALUES
(1, 'RUN_20241101_01', 'customer_id', 'string', 0, SYSUTCDATETIME()),
(1, 'RUN_20241101_01', 'first_name', 'string', 1, SYSUTCDATETIME()),
(1, 'RUN_20241101_01', 'amount', 'decimal(18,2)', 0, SYSUTCDATETIME()),
(2, 'RUN_20241101_01', 'account_id', 'string', 0, SYSUTCDATETIME()),
(2, 'RUN_20241101_01', 'account_name', 'string', 0, SYSUTCDATETIME());
GO


