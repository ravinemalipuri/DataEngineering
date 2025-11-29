/*
    Metadata table: schema_compatibility_rules
    Purpose: Defines policies that classify schema diffs as compatible/incompatible.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].schema_compatibility_rules', 'U') IS NOT NULL
    DROP TABLE [$(SchemaName)].schema_compatibility_rules;
GO

CREATE TABLE [$(SchemaName)].schema_compatibility_rules (
    profile_name            NVARCHAR(50) PRIMARY KEY,
    allow_column_drop       BIT NOT NULL DEFAULT (0),
    allow_type_widen        BIT NOT NULL DEFAULT (1),
    allow_type_narrow       BIT NOT NULL DEFAULT (0),
    allow_nullable_change   BIT NOT NULL DEFAULT (1),
    auto_add_columns        BIT NOT NULL DEFAULT (1),
    created_time            DATETIME2(3) NOT NULL DEFAULT (SYSUTCDATETIME())
);
GO
