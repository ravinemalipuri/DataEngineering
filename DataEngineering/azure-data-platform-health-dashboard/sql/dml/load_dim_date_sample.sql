-- ====================================================================
-- Load Date Dimension Sample Data
-- ====================================================================
-- This script populates the DimDate table with date records for
-- analysis. Adjust the date range as needed for your use case.
-- Default: Loads 30 days of dates starting from 2025-01-01
-- ====================================================================

DECLARE @StartDate DATE = '2025-01-01';
DECLARE @EndDate   DATE = '2025-01-30';  -- 30 days of dates for better analysis

WHILE @StartDate <= @EndDate
BEGIN
    INSERT INTO dw.DimDate (
        DateKey, [Date], [Year], [Quarter], [Month], MonthName,
        [Day], DayOfWeek, DayName, WeekOfYear, IsWeekend
    )
    SELECT
        CONVERT(INT, FORMAT(@StartDate, 'yyyyMMdd')),
        @StartDate,
        YEAR(@StartDate),
        DATEPART(QUARTER, @StartDate),
        MONTH(@StartDate),
        DATENAME(MONTH, @StartDate),
        DAY(@StartDate),
        DATEPART(WEEKDAY, @StartDate),
        DATENAME(WEEKDAY, @StartDate),
        DATEPART(WEEK, @StartDate),
        CASE WHEN DATENAME(WEEKDAY, @StartDate) IN ('Saturday','Sunday') THEN 1 ELSE 0 END;

    SET @StartDate = DATEADD(DAY, 1, @StartDate);
END;
