/*
    Sample metadata records for source_object_columns.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

INSERT INTO [$(SchemaName)].source_object_columns (
    source_object_id,
    ordinal_position,
    raw_column_name,
    data_type,
    nullable_flag,
    dq_rule_set,
    dq_severity,
    is_active,
    created_time,
    updated_time
) VALUES
(1, 1, 'CUSTOMER_ID', 'STRING', 0, '{"NOT_NULL":{}}', 'FAIL', 1, SYSUTCDATETIME(), SYSUTCDATETIME()),
(1, 2, 'FIRST_NAME', 'STRING', 1, '{"MAX_LENGTH":{"max":100}}', 'WARN', 1, SYSUTCDATETIME(), SYSUTCDATETIME()),
(1, 3, 'AMOUNT', 'DECIMAL(18,2)', 0, '{"RANGE_CHECK":{"min":0}}', 'WARN', 1, SYSUTCDATETIME(), SYSUTCDATETIME()),
(1, 4, 'LAST_MODIFIED_TS', 'TIMESTAMP', 0, NULL, 'WARN', 1, SYSUTCDATETIME(), SYSUTCDATETIME()),
(2, 1, 'ACCOUNT_ID', 'STRING', 0, '{"NOT_NULL":{}}', 'FAIL', 1, SYSUTCDATETIME(), SYSUTCDATETIME()),
(2, 2, 'ACCOUNT_NAME', 'STRING', 0, '{"NOT_NULL":{}}', 'FAIL', 1, SYSUTCDATETIME(), SYSUTCDATETIME()),
(2, 3, 'INDUSTRY', 'STRING', 1, '{"VALID_VALUES":{"values":["TECH","FINANCE","OTHER"]}}', 'WARN', 1, SYSUTCDATETIME(), SYSUTCDATETIME());
GO


