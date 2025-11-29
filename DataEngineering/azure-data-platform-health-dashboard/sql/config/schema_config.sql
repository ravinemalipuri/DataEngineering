-- ====================================================================
-- Schema Configuration
-- ====================================================================
-- This file defines the schema names used throughout the project.
-- To customize schema names, update these variables and ensure all
-- SQL scripts reference these values.
-- 
-- For production use, consider using SQLCMD variables or parameterized
-- scripts instead of hardcoding schema names.
-- ====================================================================

-- Schema names (configurable at project level)
-- Default: dw (data warehouse) and stg (staging)
-- To change: Update the schema names below and regenerate/create scripts

-- Data Warehouse Schema
DECLARE @DWSchema NVARCHAR(10) = 'dw';  -- Change this to your desired warehouse schema name

-- Staging Schema
DECLARE @StagingSchema NVARCHAR(10) = 'stg';  -- Change this to your desired staging schema name

-- Example usage in queries:
-- SELECT * FROM @DWSchema + '.DimPipeline'
-- SELECT * FROM @StagingSchema + '.PipelineRun_ADF'

-- Note: Most scripts in this repository hardcode 'dw' and 'stg' for simplicity.
-- For a fully parameterized approach, consider using SQLCMD variables or
-- a deployment framework that supports variable substitution.

-- SQLCMD Variable Syntax (alternative approach):
-- :setvar DWSchema "dw"
-- :setvar StagingSchema "stg"
-- SELECT * FROM $(DWSchema).DimPipeline;

