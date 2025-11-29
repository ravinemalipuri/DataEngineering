CREATE TABLE stg.ComputeUsage (
    SourceSystem NVARCHAR(50) NOT NULL,
    Environment NVARCHAR(50) NOT NULL,
    UsageDate DATE NOT NULL,
    UsageStartTime DATETIME2(3) NOT NULL,
    UsageEndTime DATETIME2(3) NOT NULL,
    UsageUnit NVARCHAR(50) NOT NULL,
    UsageQuantity DECIMAL(18,6) NOT NULL,
    Cost DECIMAL(18,6) NULL,
    PipelineRunId NVARCHAR(200) NULL,
    JobId NVARCHAR(200) NULL,
    JobRunId NVARCHAR(200) NULL,
    ClusterId NVARCHAR(200) NULL,
    WarehouseId NVARCHAR(200) NULL,
    CustomTagsJson NVARCHAR(MAX) NULL,
    InsertedOn DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
