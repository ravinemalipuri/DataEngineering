/*
    Sample records for schema_compatibility_rules.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

INSERT INTO [$(SchemaName)].schema_compatibility_rules (
    profile_name,
    allow_column_drop,
    allow_type_widen,
    allow_type_narrow,
    allow_nullable_change,
    auto_add_columns,
    created_time
) VALUES
('DEFAULT', 0, 1, 0, 1, 1, SYSUTCDATETIME()),
('LANDING_ZONE', 1, 1, 0, 1, 1, SYSUTCDATETIME());
GO


