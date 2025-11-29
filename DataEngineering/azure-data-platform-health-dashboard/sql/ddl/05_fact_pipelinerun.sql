CREATE TABLE dw.FactPipelineRun (
    PipelineRunKey BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    PipelineRunId NVARCHAR(200) NOT NULL,
    PipelineId NVARCHAR(200) NOT NULL,
    Environment NVARCHAR(50) NOT NULL,
    PipelineKey INT NULL,
    DateKey INT NULL,
    IRKey INT NULL,
    SourceKey INT NULL,
    StartTime DATETIME2(3) NOT NULL,
    EndTime DATETIME2(3) NULL,
    DurationSeconds INT NULL,
    Status NVARCHAR(50) NOT NULL,
    SlaCutoffTime DATETIME2(3) NULL,
    IsSlaBreached BIT NULL,
    TokensUsed DECIMAL(18,4) NULL,
    BillingCost DECIMAL(18,6) NULL,
    RowsProcessed BIGINT NULL,
    BytesProcessed BIGINT NULL,
    InsertedOn DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedOn DATETIME2(3) NULL
);
GO
CREATE UNIQUE INDEX UX_FactPipelineRun_RunId_Env
    ON dw.FactPipelineRun (PipelineRunId, Environment);
GO
