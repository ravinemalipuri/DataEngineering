/*
    Sample records for schema_change_log.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

INSERT INTO [$(SchemaName)].schema_change_log (
    source_object_id,
    run_id,
    change_type,
    change_detail,
    compatibility_flag,
    action_taken,
    logged_utc
) VALUES
(1, 'RUN_20241105_02', 'COLUMN_ADD', 'Detected new column CREDIT_SCORE', 'COMPATIBLE', 'AUTO_ALTER_TABLE', SYSUTCDATETIME()),
(2, 'RUN_20241107_01', 'TYPE_CHANGE', 'ACCOUNT_NAME length 200 -> 100', 'INCOMPATIBLE', 'PIPELINE_FAILED', SYSUTCDATETIME());
GO


