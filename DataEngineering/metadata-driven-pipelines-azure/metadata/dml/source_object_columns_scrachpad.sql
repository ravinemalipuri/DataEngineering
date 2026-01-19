DECLARE @adls_url   NVARCHAR(MAX) = N'abfss://xyz@abc.dfs.core.windows.net/bronze/sources/SSISPackages/extract/'
DECLARE @sas        NVARCHAR(MAX) = N'?sv=...';  -- include leading ?; omit if using managed identity via EXTERNAL DATA SOURCE
DECLARE @source_system_name NVARCHAR(200) = N'AS400_DB2_DEV';
DECLARE @table_filter      NVARCHAR(200) = NULL; -- e.g., N'dbo.PARTS_MASTER_INACT' or NULL for all
-- ===

--=== LOOKUP SOURCE SYSTEM ID ===
DECLARE @source_system_id INT =
(
    SELECT source_system_id
    FROM dbo.source_systems
    WHERE source_system_name = @source_system_name
);
IF @source_system_id IS NULL
    THROW 50000, 'Source system not found: ' + @source_system_name, 1;

--=== STAGE LINEAGE CSV FROM ADLS VIA OPENROWSET (serverless style) ===
IF OBJECT_ID('tempdb..#lineage') IS NOT NULL DROP TABLE #lineage;

CREATE TABLE #lineage
(
    package_file              NVARCHAR(260),
    source_table              NVARCHAR(260),
    source_column             NVARCHAR(260),
    source_data_type          NVARCHAR(260),
    target_table              NVARCHAR(260),
    target_column             NVARCHAR(260),
    target_data_type          NVARCHAR(260),
    alias_col                 NVARCHAR(260),
    transformation_component  NVARCHAR(260),
    transformation_expression NVARCHAR(MAX)
);

------added by Mani--------

DECLARE @fullpath NVARCHAR(MAX) = @adls_url + @sas;

DECLARE @openrowset NVARCHAR(MAX) = N'
INSERT INTO #lineage
SELECT *
FROM OPENROWSET(
    BULK ' + QUOTENAME(@fullpath, '''') + ',
    FORMAT=''CSV'',
    FIRSTROW=2
) AS rows
';

EXEC (@openrowset);

-- Optional filter to one table
IF @table_filter IS NOT NULL
  BEGIN  DELETE FROM #lineage WHERE target_table <> @table_filter;
  END

--=== INSERT NEW COLUMNS ONLY ===
;WITH cols AS (
    SELECT
        so.source_object_id,
        l.target_table,
        l.target_column        AS raw_column_name,
        l.target_data_type     AS data_type,
        ROW_NUMBER() OVER (PARTITION BY l.target_table ORDER BY l.target_column) AS ordinal_position
    FROM #lineage l
    JOIN dbo.source_objects so
      ON so.source_system_id = @source_system_id
     AND so.source_object_name = l.target_table
)
INSERT INTO dbo.source_object_columns (
    source_object_id,
    ordinal_position,
    raw_column_name,
    data_type,
    nullable_flag,
    dq_rule_set,
    dq_severity,
    is_active
)
SELECT
    c.source_object_id,
    c.ordinal_position,
    c.raw_column_name,
    COALESCE(NULLIF(LTRIM(RTRIM(c.data_type)), ''), N'NVARCHAR(MAX)') AS data_type,
    1 AS nullable_flag,
    NULL AS dq_rule_set,
    ''WARN'' AS dq_severity,
    1 AS is_active
FROM cols c
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.source_object_columns soc
    WHERE soc.source_object_id = c.source_object_id
      AND soc.raw_column_name = c.raw_column_name
);

PRINT ''Done.'';