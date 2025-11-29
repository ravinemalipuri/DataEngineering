-- ====================================================================
-- Foreign Key Constraints and Performance Indexes
-- ====================================================================
-- This script adds foreign key relationships and indexes to optimize
-- query performance for the data warehouse fact tables.
-- ====================================================================

-- Foreign Keys for FactPipelineRun
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactPipelineRun_DimPipeline')
BEGIN
    ALTER TABLE dw.FactPipelineRun
    ADD CONSTRAINT FK_FactPipelineRun_DimPipeline
    FOREIGN KEY (PipelineKey) REFERENCES dw.DimPipeline(PipelineKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactPipelineRun_DimDate')
BEGIN
    ALTER TABLE dw.FactPipelineRun
    ADD CONSTRAINT FK_FactPipelineRun_DimDate
    FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactPipelineRun_DimIntegrationRuntime')
BEGIN
    ALTER TABLE dw.FactPipelineRun
    ADD CONSTRAINT FK_FactPipelineRun_DimIntegrationRuntime
    FOREIGN KEY (IRKey) REFERENCES dw.DimIntegrationRuntime(IRKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactPipelineRun_DimSourceSystem')
BEGIN
    ALTER TABLE dw.FactPipelineRun
    ADD CONSTRAINT FK_FactPipelineRun_DimSourceSystem
    FOREIGN KEY (SourceKey) REFERENCES dw.DimSourceSystem(SourceKey);
END
GO

-- Foreign Keys for FactActivityRun
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactActivityRun_FactPipelineRun')
BEGIN
    ALTER TABLE dw.FactActivityRun
    ADD CONSTRAINT FK_FactActivityRun_FactPipelineRun
    FOREIGN KEY (PipelineRunKey) REFERENCES dw.FactPipelineRun(PipelineRunKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactActivityRun_DimPipeline')
BEGIN
    ALTER TABLE dw.FactActivityRun
    ADD CONSTRAINT FK_FactActivityRun_DimPipeline
    FOREIGN KEY (PipelineKey) REFERENCES dw.DimPipeline(PipelineKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactActivityRun_DimDate')
BEGIN
    ALTER TABLE dw.FactActivityRun
    ADD CONSTRAINT FK_FactActivityRun_DimDate
    FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey);
END
GO

-- Foreign Keys for FactComputeUsage
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactComputeUsage_DimDate')
BEGIN
    ALTER TABLE dw.FactComputeUsage
    ADD CONSTRAINT FK_FactComputeUsage_DimDate
    FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactComputeUsage_FactPipelineRun')
BEGIN
    ALTER TABLE dw.FactComputeUsage
    ADD CONSTRAINT FK_FactComputeUsage_FactPipelineRun
    FOREIGN KEY (PipelineRunKey) REFERENCES dw.FactPipelineRun(PipelineRunKey);
END
GO

-- Foreign Keys for FactDQEvents
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactDQEvents_DimDate')
BEGIN
    ALTER TABLE dw.FactDQEvents
    ADD CONSTRAINT FK_FactDQEvents_DimDate
    FOREIGN KEY (DateKey) REFERENCES dw.DimDate(DateKey);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_FactDQEvents_FactPipelineRun')
BEGIN
    ALTER TABLE dw.FactDQEvents
    ADD CONSTRAINT FK_FactDQEvents_FactPipelineRun
    FOREIGN KEY (PipelineRunKey) REFERENCES dw.FactPipelineRun(PipelineRunKey);
END
GO

-- Performance Indexes for FactPipelineRun
CREATE NONCLUSTERED INDEX IX_FactPipelineRun_DateKey_Status
    ON dw.FactPipelineRun (DateKey, Status)
    INCLUDE (PipelineKey, IRKey, TokensUsed, BillingCost, DurationSeconds);
GO

CREATE NONCLUSTERED INDEX IX_FactPipelineRun_PipelineKey_StartTime
    ON dw.FactPipelineRun (PipelineKey, StartTime DESC)
    INCLUDE (Status, TokensUsed, BillingCost, DurationSeconds);
GO

CREATE NONCLUSTERED INDEX IX_FactPipelineRun_IRKey_DateKey
    ON dw.FactPipelineRun (IRKey, DateKey)
    INCLUDE (TokensUsed, BillingCost);
GO

-- Performance Indexes for FactActivityRun
CREATE NONCLUSTERED INDEX IX_FactActivityRun_PipelineRunKey
    ON dw.FactActivityRun (PipelineRunKey)
    INCLUDE (ActivityName, Status, DurationSeconds, RowsRead, RowsWritten);
GO

CREATE NONCLUSTERED INDEX IX_FactActivityRun_DateKey_Status
    ON dw.FactActivityRun (DateKey, Status)
    INCLUDE (PipelineKey, DurationSeconds);
GO

-- Performance Indexes for FactComputeUsage
CREATE NONCLUSTERED INDEX IX_FactComputeUsage_DateKey_UsageUnit
    ON dw.FactComputeUsage (DateKey, UsageUnit)
    INCLUDE (UsageQuantity, Cost, PipelineRunKey);
GO

CREATE NONCLUSTERED INDEX IX_FactComputeUsage_PipelineRunKey
    ON dw.FactComputeUsage (PipelineRunKey)
    INCLUDE (UsageUnit, UsageQuantity, Cost);
GO

-- Performance Indexes for FactDQEvents
CREATE NONCLUSTERED INDEX IX_FactDQEvents_DateKey_Status
    ON dw.FactDQEvents (DateKey, Status)
    INCLUDE (PipelineRunKey, CheckName, FailedRowCount);
GO

CREATE NONCLUSTERED INDEX IX_FactDQEvents_PipelineRunKey
    ON dw.FactDQEvents (PipelineRunKey)
    INCLUDE (CheckName, Status, FailedRowCount);
GO

