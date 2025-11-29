CREATE TABLE dw.DimIntegrationRuntime (
    IRKey INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    IRName NVARCHAR(256) NOT NULL,
    IRType NVARCHAR(50) NOT NULL,
    Region NVARCHAR(100) NULL,
    Environment NVARCHAR(50) NULL,
    IsActive BIT NOT NULL DEFAULT (1)
);
GO
CREATE UNIQUE INDEX UX_DimIR_Name_Env
    ON dw.DimIntegrationRuntime (IRName, Environment);
GO
