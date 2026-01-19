/*
    Metadata views: provide read-friendly projections over core tables to reduce
    blocking when metadata is consumed frequently by pipelines.

    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

/* Drop existing views if present */
IF OBJECT_ID('[$(SchemaName)].vw_source_systems', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_source_systems;
IF OBJECT_ID('[$(SchemaName)].vw_source_objects', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_source_objects;
IF OBJECT_ID('[$(SchemaName)].vw_source_object_columns', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_source_object_columns;
IF OBJECT_ID('[$(SchemaName)].vw_schema_history', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_schema_history;
IF OBJECT_ID('[$(SchemaName)].vw_schema_change_log', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_schema_change_log;
IF OBJECT_ID('[$(SchemaName)].vw_data_quality_results', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_data_quality_results;
IF OBJECT_ID('[$(SchemaName)].vw_data_profiling_results', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_data_profiling_results;
GO

/* Read-friendly views with NOLOCK hints to minimize blocking */
CREATE VIEW [$(SchemaName)].vw_source_systems
AS
SELECT * FROM [$(SchemaName)].source_systems WITH (NOLOCK);
GO

CREATE VIEW [$(SchemaName)].vw_source_objects
AS
SELECT * FROM [$(SchemaName)].source_objects WITH (NOLOCK);
GO

CREATE VIEW [$(SchemaName)].vw_source_object_columns
AS
SELECT * FROM [$(SchemaName)].source_object_columns WITH (NOLOCK);
GO

CREATE VIEW [$(SchemaName)].vw_schema_history
AS
SELECT * FROM [$(SchemaName)].schema_history WITH (NOLOCK);
GO

CREATE VIEW [$(SchemaName)].vw_schema_change_log
AS
SELECT * FROM [$(SchemaName)].schema_change_log WITH (NOLOCK);
GO

CREATE VIEW [$(SchemaName)].vw_data_quality_results
AS
SELECT * FROM [$(SchemaName)].data_quality_results WITH (NOLOCK);
GO

CREATE VIEW [$(SchemaName)].vw_data_profiling_results
AS
SELECT * FROM [$(SchemaName)].data_profiling_results WITH (NOLOCK);
GO

