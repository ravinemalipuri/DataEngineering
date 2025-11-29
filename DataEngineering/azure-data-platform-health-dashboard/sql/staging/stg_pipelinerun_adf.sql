CREATE TABLE stg.PipelineRun_ADF (
    SourceSystem NVARCHAR(50) NOT NULL,
    Environment NVARCHAR(50) NOT NULL,
    PipelineRunId NVARCHAR(200) NOT NULL,
    PipelineId NVARCHAR(200) NOT NULL,
    PipelineName NVARCHAR(256) NOT NULL,
    IRName NVARCHAR(256) NULL,
    StartTime DATETIME2(3) NOT NULL,
    EndTime DATETIME2(3) NULL,
    Status NVARCHAR(50) NOT NULL,
    RowsProcessed BIGINT NULL,
    BytesProcessed BIGINT NULL,
    TokensUsed DECIMAL(18,4) NULL,
    BillingCost DECIMAL(18,6) NULL,
    InsertedOn DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
