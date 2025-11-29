CREATE TABLE dw.DimPipeline (
    PipelineKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    PipelineId NVARCHAR(200) NOT NULL,
    PipelineName NVARCHAR(256) NOT NULL,
    Environment NVARCHAR(50) NOT NULL,
    SourceSystem NVARCHAR(100) NULL,
    Domain NVARCHAR(100) NULL,
    OwnerEmail NVARCHAR(256) NULL,
    IsActive BIT NOT NULL DEFAULT (1),
    CreatedOn DATETIME2(3) NULL,
    ModifiedOn DATETIME2(3) NULL
);
GO
CREATE UNIQUE INDEX UX_DimPipeline_PipelineId_Env
    ON dw.DimPipeline (PipelineId, Environment);
GO
