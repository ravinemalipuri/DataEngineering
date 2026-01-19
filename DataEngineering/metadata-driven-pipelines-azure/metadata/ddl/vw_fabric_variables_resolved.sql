/*
    Metadata view: vw_fabric_variables_resolved
    Purpose: Exposes each cataloged variable per environment with its resolved value.
    Parameters:
        $(DatabaseName) - target database
        $(SchemaName)   - target schema (e.g., dbo)
*/
::setvar DatabaseName metadata_db
::setvar SchemaName dbo

USE [$(DatabaseName)];
GO

IF OBJECT_ID('[$(SchemaName)].vw_fabric_variables_resolved', 'V') IS NOT NULL
    DROP VIEW [$(SchemaName)].vw_fabric_variables_resolved;
GO

CREATE VIEW [$(SchemaName)].vw_fabric_variables_resolved
AS
SELECT
    variable_name,
    scope_level,
    category,
    purpose,
    CASE
        WHEN scope_level = 'factory' THEN default_value
        WHEN scope_level = 'workspace' AND env = 'dev'  THEN dev_value
        WHEN scope_level = 'workspace' AND env = 'test' THEN test_value
        WHEN scope_level = 'workspace' AND env = 'prod' THEN prod_value
        ELSE default_value
    END AS resolved_value,
    is_secret
FROM [$(SchemaName)].fabric_variable_catalog
CROSS JOIN (SELECT 'dev' AS env UNION ALL SELECT 'test' UNION ALL SELECT 'prod') e
WHERE is_active = 1;
GO


