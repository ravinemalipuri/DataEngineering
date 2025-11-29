CREATE TABLE dw.DimSourceSystem (
    SourceKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    SourceName NVARCHAR(200) NOT NULL,
    SystemType NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    Environment NVARCHAR(50) NULL,
    IsActive BIT NOT NULL DEFAULT (1)
);
GO
CREATE UNIQUE INDEX UX_DimSourceSystem_Name_Env
    ON dw.DimSourceSystem (SourceName, Environment);
GO
