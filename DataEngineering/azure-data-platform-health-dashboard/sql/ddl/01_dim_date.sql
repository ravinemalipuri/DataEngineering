CREATE TABLE dw.DimDate (
    DateKey INT NOT NULL PRIMARY KEY,
    [Date] DATE NOT NULL,
    [Year] SMALLINT NOT NULL,
    [Quarter] TINYINT NOT NULL,
    [Month] TINYINT NOT NULL,
    MonthName VARCHAR(20) NOT NULL,
    [Day] TINYINT NOT NULL,
    DayOfWeek TINYINT NOT NULL,
    DayName VARCHAR(20) NOT NULL,
    WeekOfYear TINYINT NOT NULL,
    IsWeekend BIT NOT NULL
);
GO
CREATE INDEX IX_DimDate_Date ON dw.DimDate([Date]);
GO
