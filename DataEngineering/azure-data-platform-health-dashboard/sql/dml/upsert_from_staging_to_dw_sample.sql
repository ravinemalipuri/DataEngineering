-- ====================================================================
-- Upsert from Staging to Data Warehouse - Comprehensive ETL Script
-- ====================================================================
-- This script transforms and loads data from staging tables into the
-- dimensional data warehouse tables following star schema patterns.
-- It handles dimension lookups, surrogate key generation, and fact table
-- inserts/updates using MERGE operations for idempotency.
-- ====================================================================

-- Step 1: Upsert Dimensions from ADF Pipeline Runs
-- --------------------------------------------------------------------
-- Upsert DimPipeline from ADF staging data
MERGE dw.DimPipeline AS tgt
USING (
    SELECT DISTINCT 
        PipelineId, 
        PipelineName, 
        Environment, 
        SourceSystem
    FROM stg.PipelineRun_ADF
) AS src
ON tgt.PipelineId = src.PipelineId AND tgt.Environment = src.Environment
WHEN NOT MATCHED THEN
    INSERT (PipelineId, PipelineName, Environment, SourceSystem, CreatedOn)
    VALUES (src.PipelineId, src.PipelineName, src.Environment, src.SourceSystem, SYSUTCDATETIME())
WHEN MATCHED AND (tgt.PipelineName <> src.PipelineName OR tgt.SourceSystem <> src.SourceSystem) THEN
    UPDATE SET 
        tgt.PipelineName = src.PipelineName,
        tgt.SourceSystem = src.SourceSystem,
        tgt.ModifiedOn = SYSUTCDATETIME();
GO

-- Upsert DimIntegrationRuntime from ADF staging data
MERGE dw.DimIntegrationRuntime AS tgt
USING (
    SELECT DISTINCT 
        IRName,
        Environment
    FROM stg.PipelineRun_ADF
    WHERE IRName IS NOT NULL
) AS src
ON tgt.IRName = src.IRName AND tgt.Environment = src.Environment
WHEN NOT MATCHED THEN
    INSERT (IRName, IRType, Region, Environment)
    VALUES (src.IRName, 'Azure', NULL, src.Environment);
GO

-- Upsert DimSourceSystem from staging data
MERGE dw.DimSourceSystem AS tgt
USING (
    SELECT DISTINCT SourceSystem AS SourceName, Environment
    FROM stg.PipelineRun_ADF
    UNION
    SELECT DISTINCT SourceSystem AS SourceName, Environment
    FROM stg.ActivityRun_ADF
    UNION
    SELECT DISTINCT SourceSystem AS SourceName, Environment
    FROM stg.ComputeUsage
) AS src
ON tgt.SourceName = src.SourceName AND tgt.Environment = src.Environment
WHEN NOT MATCHED THEN
    INSERT (SourceName, SystemType, Description, Environment)
    VALUES (src.SourceName, 'Unknown', NULL, src.Environment);
GO

-- Step 2: Upsert FactPipelineRun from ADF staging
-- --------------------------------------------------------------------
MERGE dw.FactPipelineRun AS tgt
USING (
    SELECT
        s.PipelineRunId,
        s.PipelineId,
        s.Environment,
        dP.PipelineKey,
        CONVERT(INT, FORMAT(CAST(s.StartTime AS DATE), 'yyyyMMdd')) AS DateKey,
        dIR.IRKey,
        dSS.SourceKey,
        s.StartTime,
        s.EndTime,
        DATEDIFF(SECOND, s.StartTime, s.EndTime) AS DurationSeconds,
        s.Status,
        s.TokensUsed,
        s.BillingCost,
        s.RowsProcessed,
        s.BytesProcessed
    FROM stg.PipelineRun_ADF s
    LEFT JOIN dw.DimPipeline dP
        ON dP.PipelineId = s.PipelineId AND dP.Environment = s.Environment
    LEFT JOIN dw.DimIntegrationRuntime dIR
        ON dIR.IRName = s.IRName AND dIR.Environment = s.Environment
    LEFT JOIN dw.DimSourceSystem dSS
        ON dSS.SourceName = s.SourceSystem AND dSS.Environment = s.Environment
) AS src
ON tgt.PipelineRunId = src.PipelineRunId AND tgt.Environment = src.Environment
WHEN MATCHED THEN
    UPDATE SET
        tgt.PipelineId = src.PipelineId,
        tgt.PipelineKey = src.PipelineKey,
        tgt.DateKey = src.DateKey,
        tgt.IRKey = src.IRKey,
        tgt.SourceKey = src.SourceKey,
        tgt.StartTime = src.StartTime,
        tgt.EndTime = src.EndTime,
        tgt.DurationSeconds = src.DurationSeconds,
        tgt.Status = src.Status,
        tgt.TokensUsed = src.TokensUsed,
        tgt.BillingCost = src.BillingCost,
        tgt.RowsProcessed = src.RowsProcessed,
        tgt.BytesProcessed = src.BytesProcessed,
        tgt.UpdatedOn = SYSUTCDATETIME()
WHEN NOT MATCHED THEN
    INSERT (
        PipelineRunId, PipelineId, Environment, PipelineKey, DateKey, IRKey, SourceKey,
        StartTime, EndTime, DurationSeconds, Status,
        TokensUsed, BillingCost, RowsProcessed, BytesProcessed, InsertedOn
    )
    VALUES (
        src.PipelineRunId, src.PipelineId, src.Environment, src.PipelineKey, src.DateKey, 
        src.IRKey, src.SourceKey,
        src.StartTime, src.EndTime, src.DurationSeconds, src.Status,
        src.TokensUsed, src.BillingCost, src.RowsProcessed, src.BytesProcessed, SYSUTCDATETIME()
    );
GO

-- Step 3: Upsert FactActivityRun from ADF staging
-- --------------------------------------------------------------------
MERGE dw.FactActivityRun AS tgt
USING (
    SELECT
        s.ActivityRunId,
        s.PipelineRunId,
        s.ActivityName,
        s.ActivityType,
        s.Environment,
        fpr.PipelineRunKey,
        dP.PipelineKey,
        CONVERT(INT, FORMAT(CAST(s.StartTime AS DATE), 'yyyyMMdd')) AS DateKey,
        s.StartTime,
        s.EndTime,
        DATEDIFF(SECOND, s.StartTime, s.EndTime) AS DurationSeconds,
        s.Status,
        s.RowsRead,
        s.RowsWritten,
        s.BytesRead,
        s.BytesWritten,
        s.IRName
    FROM stg.ActivityRun_ADF s
    LEFT JOIN dw.FactPipelineRun fpr
        ON fpr.PipelineRunId = s.PipelineRunId AND fpr.Environment = s.Environment
    LEFT JOIN dw.DimPipeline dP
        ON dP.PipelineName = s.PipelineName AND dP.Environment = s.Environment
) AS src
ON tgt.ActivityRunId = src.ActivityRunId AND tgt.Environment = src.Environment
WHEN MATCHED THEN
    UPDATE SET
        tgt.PipelineRunId = src.PipelineRunId,
        tgt.PipelineRunKey = src.PipelineRunKey,
        tgt.PipelineKey = src.PipelineKey,
        tgt.DateKey = src.DateKey,
        tgt.StartTime = src.StartTime,
        tgt.EndTime = src.EndTime,
        tgt.DurationSeconds = src.DurationSeconds,
        tgt.Status = src.Status,
        tgt.RowsRead = src.RowsRead,
        tgt.RowsWritten = src.RowsWritten,
        tgt.BytesRead = src.BytesRead,
        tgt.BytesWritten = src.BytesWritten,
        tgt.IRName = src.IRName,
        tgt.UpdatedOn = SYSUTCDATETIME()
WHEN NOT MATCHED THEN
    INSERT (
        ActivityRunId, PipelineRunId, ActivityName, ActivityType, Environment,
        PipelineRunKey, PipelineKey, DateKey,
        StartTime, EndTime, DurationSeconds, Status,
        RowsRead, RowsWritten, BytesRead, BytesWritten, IRName, InsertedOn
    )
    VALUES (
        src.ActivityRunId, src.PipelineRunId, src.ActivityName, src.ActivityType, src.Environment,
        src.PipelineRunKey, src.PipelineKey, src.DateKey,
        src.StartTime, src.EndTime, src.DurationSeconds, src.Status,
        src.RowsRead, src.RowsWritten, src.BytesRead, src.BytesWritten, src.IRName, SYSUTCDATETIME()
    );
GO

-- Step 4: Upsert FactComputeUsage from staging
-- --------------------------------------------------------------------
MERGE dw.FactComputeUsage AS tgt
USING (
    SELECT
        CONVERT(INT, FORMAT(s.UsageDate, 'yyyyMMdd')) AS DateKey,
        s.Environment,
        s.PipelineRunId,
        fpr.PipelineRunKey,
        s.JobId,
        s.JobRunId,
        s.ClusterId,
        s.WarehouseId,
        s.UsageStartTime,
        s.UsageEndTime,
        s.UsageUnit,
        s.UsageQuantity,
        s.Cost,
        NULL AS AdfRunTag,
        s.CustomTagsJson
    FROM stg.ComputeUsage s
    LEFT JOIN dw.FactPipelineRun fpr
        ON fpr.PipelineRunId = s.PipelineRunId AND fpr.Environment = s.Environment
) AS src
ON tgt.DateKey = src.DateKey 
    AND tgt.Environment = src.Environment
    AND tgt.UsageStartTime = src.UsageStartTime
    AND tgt.UsageUnit = src.UsageUnit
    AND (tgt.PipelineRunId = src.PipelineRunId OR (tgt.PipelineRunId IS NULL AND src.PipelineRunId IS NULL))
WHEN MATCHED THEN
    UPDATE SET
        tgt.PipelineRunKey = src.PipelineRunKey,
        tgt.JobId = src.JobId,
        tgt.JobRunId = src.JobRunId,
        tgt.ClusterId = src.ClusterId,
        tgt.WarehouseId = src.WarehouseId,
        tgt.UsageEndTime = src.UsageEndTime,
        tgt.UsageQuantity = src.UsageQuantity,
        tgt.Cost = src.Cost,
        tgt.CustomTagsJson = src.CustomTagsJson
WHEN NOT MATCHED THEN
    INSERT (
        DateKey, Environment, PipelineRunId, PipelineRunKey,
        JobId, JobRunId, ClusterId, WarehouseId,
        UsageStartTime, UsageEndTime, UsageUnit, UsageQuantity, Cost,
        AdfRunTag, CustomTagsJson, InsertedOn
    )
    VALUES (
        src.DateKey, src.Environment, src.PipelineRunId, src.PipelineRunKey,
        src.JobId, src.JobRunId, src.ClusterId, src.WarehouseId,
        src.UsageStartTime, src.UsageEndTime, src.UsageUnit, src.UsageQuantity, src.Cost,
        src.AdfRunTag, src.CustomTagsJson, SYSUTCDATETIME()
    );
GO

-- Step 5: Upsert FactDQEvents from staging
-- --------------------------------------------------------------------
MERGE dw.FactDQEvents AS tgt
USING (
    SELECT
        CONVERT(INT, FORMAT(CAST(s.EventTime AS DATE), 'yyyyMMdd')) AS DateKey,
        s.PipelineRunId,
        fpr.PipelineRunKey,
        s.CheckName,
        s.CheckType,
        s.Status,
        s.FailedRowCount,
        s.DetailsJson
    FROM stg.DQEvents s
    LEFT JOIN dw.FactPipelineRun fpr
        ON fpr.PipelineRunId = s.PipelineRunId AND fpr.Environment = s.Environment
) AS src
ON tgt.PipelineRunId = src.PipelineRunId 
    AND tgt.CheckName = src.CheckName
    AND tgt.DateKey = src.DateKey
WHEN MATCHED THEN
    UPDATE SET
        tgt.PipelineRunKey = src.PipelineRunKey,
        tgt.CheckType = src.CheckType,
        tgt.Status = src.Status,
        tgt.FailedRowCount = src.FailedRowCount,
        tgt.DetailsJson = src.DetailsJson
WHEN NOT MATCHED THEN
    INSERT (
        DateKey, PipelineRunId, PipelineRunKey, CheckName, CheckType,
        Status, FailedRowCount, DetailsJson, InsertedOn
    )
    VALUES (
        src.DateKey, src.PipelineRunId, src.PipelineRunKey, src.CheckName, src.CheckType,
        src.Status, src.FailedRowCount, src.DetailsJson, SYSUTCDATETIME()
    );
GO

PRINT 'ETL from staging to data warehouse completed successfully.';
GO
