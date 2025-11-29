CREATE TABLE stg.ActivityRun_ADF (
    SourceSystem NVARCHAR(50) NOT NULL,
    Environment NVARCHAR(50) NOT NULL,
    ActivityRunId NVARCHAR(200) NOT NULL,
    PipelineRunId NVARCHAR(200) NOT NULL,
    PipelineName NVARCHAR(256) NOT NULL,
    ActivityName NVARCHAR(256) NOT NULL,
    ActivityType NVARCHAR(100) NOT NULL,
    IRName NVARCHAR(256) NULL,
    StartTime DATETIME2(3) NOT NULL,
    EndTime DATETIME2(3) NULL,
    Status NVARCHAR(50) NOT NULL,
    RowsRead BIGINT NULL,
    RowsWritten BIGINT NULL,
    BytesRead BIGINT NULL,
    BytesWritten BIGINT NULL,
    InsertedOn DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
