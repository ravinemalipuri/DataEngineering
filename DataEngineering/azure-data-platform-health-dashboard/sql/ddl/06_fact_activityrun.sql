CREATE TABLE dw.FactActivityRun (
    ActivityRunKey BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    ActivityRunId NVARCHAR(200) NOT NULL,
    PipelineRunId NVARCHAR(200) NOT NULL,
    ActivityName NVARCHAR(256) NOT NULL,
    ActivityType NVARCHAR(100) NOT NULL,
    Environment NVARCHAR(50) NOT NULL,
    PipelineRunKey BIGINT NULL,
    PipelineKey INT NULL,
    DateKey INT NULL,
    StartTime DATETIME2(3) NOT NULL,
    EndTime DATETIME2(3) NULL,
    DurationSeconds INT NULL,
    Status NVARCHAR(50) NOT NULL,
    RowsRead BIGINT NULL,
    RowsWritten BIGINT NULL,
    BytesRead BIGINT NULL,
    BytesWritten BIGINT NULL,
    IRName NVARCHAR(256) NULL,
    InsertedOn DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedOn DATETIME2(3) NULL
);
GO
