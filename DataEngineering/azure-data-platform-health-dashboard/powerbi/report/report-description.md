# Power BI Report Description

## Overview
This document describes the Power BI report structure for the Azure Data Platform Health Dashboard. The report provides insights into pipeline performance, costs, and regression analysis.

## Report Pages

### Page 1: Top 10 Costliest Pipelines (Last 24 Hours)

**Purpose**: Identify the pipelines consuming the most resources in the last 24 hours.

**Visuals**:
1. **Table/Matrix Visual**: Top 10 Pipelines by Cost
   - Columns: Pipeline Name, Total Cost (Last 24H), Total Tokens (Last 24H), Total DBUs (Last 24H), Run Count
   - Sort: By Total Cost (descending)
   - Filters: Date = Last 24 Hours
   - Measure: `TotalBillingCost_Last24H`

2. **Bar Chart**: Cost Breakdown by Pipeline
   - X-Axis: Pipeline Name (Top 10)
   - Y-Axis: Total Billing Cost
   - Measure: `TotalBillingCost_Last24H`
   - Visual Type: Clustered Column Chart

3. **Card Visuals**: Key Metrics
   - Total Cost (Last 24H): `TotalCost_Last24H`
   - Total Tokens (Last 24H): `TotalTokensUsed_Last24H`
   - Total DBUs (Last 24H): `TotalDBU_Last24H`
   - Average Cost per Run: `DIVIDE([TotalBillingCost_Last24H], [TotalPipelineRuns_Last24H], 0)`

**Slicers**:
- Environment (DimPipeline[Environment])
- Date Range (DimDate[Date])

**Filters**:
- FactPipelineRun[StartTime] >= NOW() - 1
- FactPipelineRun[Status] in [Succeeded, Failed, Running]

---

### Page 2: Performance Regression vs Last Week

**Purpose**: Detect pipelines that have degraded in performance compared to the 7-day baseline.

**Visuals**:
1. **Table Visual**: Pipelines with Regression
   - Columns: 
     - Pipeline Name
     - Baseline Avg Tokens (7D): `PipelineBaselineAvgTokens_7D`
     - Current Avg Tokens (24H): `PipelineCurrentAvgTokens_24H`
     - Token Regression %: `PipelineTokenRegressionPercent`
     - Baseline Avg Duration (7D): `BaselineAvgDurationSeconds_7D`
     - Current Avg Duration (24H): `CurrentAvgDurationSeconds_24H`
     - Duration Regression %: `DurationRegressionPercent`
     - Regression Score: `PerformanceRegressionScore`
   - Conditional Formatting: Red background for regression % > 10%
   - Filter: Show only rows where `HasTokenRegression` = TRUE OR `HasDurationRegression` = TRUE

2. **Scatter Chart**: Token Regression Analysis
   - X-Axis: Baseline Avg Tokens (7D)
   - Y-Axis: Current Avg Tokens (24H)
   - Legend: Pipeline Name
   - Size: Regression Score
   - Color: Regression Indicator (Red = Regression, Green = Improvement)

3. **Line Chart**: Token Trend Comparison
   - X-Axis: Date (Last 7 days)
   - Y-Axis: Average Tokens Per Run
   - Series: 
     - Baseline (7-day average line)
     - Current (daily actuals)
   - Measure: `DailyTokensByIR` (grouped by pipeline)

4. **Card Visuals**: Summary Metrics
   - Overall Token Regression %: `TokenRegressionPercent`
   - Overall Duration Regression %: `DurationRegressionPercent`
   - Pipelines with Regression: `COUNTROWS(FILTER(DimPipeline, [HasTokenRegression] || [HasDurationRegression]))`

**Slicers**:
- Environment (DimPipeline[Environment])
- Pipeline (DimPipeline[PipelineName])

**Filters**:
- Date Range: Last 7 days
- Status: Succeeded only

---

### Page 3: Cost & Token/DBU Trends by Integration Runtime

**Purpose**: Analyze cost and usage trends by Integration Runtime over time.

**Visuals**:
1. **Line Chart**: Daily Cost Trend by IR
   - X-Axis: Date (Last 30 days)
   - Y-Axis: Daily Cost
   - Legend: IR Name
   - Measure: `DailyCostByIR`
   - Visual Type: Line Chart with multiple series

2. **Line Chart**: Daily Token Usage Trend by IR
   - X-Axis: Date (Last 30 days)
   - Y-Axis: Daily Tokens
   - Legend: IR Name
   - Measure: `DailyTokensByIR`
   - Visual Type: Line Chart with multiple series

3. **Line Chart**: Daily DBU Usage Trend (if compute usage data available)
   - X-Axis: Date (Last 30 days)
   - Y-Axis: Daily DBUs
   - Legend: IR Name or Job ID
   - Measure: `DailyDBUUsage`
   - Visual Type: Area Chart

4. **Stacked Bar Chart**: Cost Distribution by IR (Last 30 Days)
   - X-Axis: IR Name
   - Y-Axis: Total Cost
   - Measure: `TotalCostByIR_Last7D`
   - Visual Type: Stacked Column Chart

5. **Donut Chart**: Cost Share by IR
   - Values: `TotalCostByIR_Last7D`
   - Legend: IR Name (DimIntegrationRuntime[IRName])
   - Visual Type: Donut Chart

6. **Table Visual**: IR Usage Summary
   - Columns:
     - IR Name
     - Total Runs (Last 7D): `RunCountByIR_Last24H`
     - Total Cost (Last 7D): `TotalCostByIR_Last7D`
     - Total Tokens (Last 7D): `TotalTokensByIR_Last7D`
     - Avg Cost per Run: `AvgCostPerRunByIR`
     - Avg Tokens per Run: `AvgTokensPerRunByIR`
     - Total DBUs (if available): `TotalDBUByIR`

7. **Card Visuals**: Aggregate Metrics
   - Total Cost (All IRs): `TotalCost`
   - Total Tokens (All IRs): `TotalTokensUsed`
   - Total DBUs (All IRs): `TotalDBUByIR`
   - Number of Active IRs: `DISTINCTCOUNT(DimIntegrationRuntime[IRKey])`

**Slicers**:
- Environment (DimIntegrationRuntime[Environment])
- IR Type (DimIntegrationRuntime[IRType])
- Date Range (DimDate[Date])

**Filters**:
- Date Range: Last 30 days
- IR Status: Active only

---

## Data Model Relationships

Ensure the following relationships exist in Power BI:

1. **FactPipelineRun** → **DimPipeline** (Many-to-One on PipelineKey)
2. **FactPipelineRun** → **DimDate** (Many-to-One on DateKey)
3. **FactPipelineRun** → **DimIntegrationRuntime** (Many-to-One on IRKey)
4. **FactPipelineRun** → **DimSourceSystem** (Many-to-One on SourceKey)
5. **FactActivityRun** → **FactPipelineRun** (Many-to-One on PipelineRunKey)
6. **FactActivityRun** → **DimPipeline** (Many-to-One on PipelineKey)
7. **FactActivityRun** → **DimDate** (Many-to-One on DateKey)
8. **FactComputeUsage** → **DimDate** (Many-to-One on DateKey)
9. **FactComputeUsage** → **FactPipelineRun** (Many-to-One on PipelineRunKey)
10. **FactDQEvents** → **DimDate** (Many-to-One on DateKey)
11. **FactDQEvents** → **FactPipelineRun** (Many-to-One on PipelineRunKey)

## Import Instructions

1. **Connect to Azure SQL Database**:
   - Open Power BI Desktop
   - Get Data → Azure → Azure SQL Database
   - Enter server name and database name
   - Use SQL authentication with credentials from deployment

2. **Import Tables**:
   - Select all tables from the `dw` schema:
     - DimDate
     - DimPipeline
     - DimIntegrationRuntime
     - DimSourceSystem
     - FactPipelineRun
     - FactActivityRun
     - FactComputeUsage
     - FactDQEvents

3. **Create Relationships**:
   - Go to Model view
   - Create relationships as listed above
   - Ensure cardinality is correct (Many-to-One)
   - Set cross-filter direction appropriately

4. **Import DAX Measures**:
   - Go to Home → Enter Data (or use Power Query to create measures)
   - Copy measures from the `.dax` files in `powerbi\dax\`
   - Paste into the DAX formula bar to create new measures
   - Alternatively, use Tabular Editor for bulk import

5. **Build Visuals**:
   - Follow the visual specifications above
   - Use the DAX measures in your visualizations
   - Apply filters and slicers as described

## Customization Tips

- **Color Schemes**: Use conditional formatting to highlight regressions in red
- **Tooltips**: Add custom tooltips showing additional context
- **Bookmarks**: Create bookmarks for different views (e.g., by environment)
- **Drillthrough Pages**: Create detail pages for drilling into specific pipelines
- **Alerts**: Set up data alerts for cost thresholds or regression detection

## Sample Queries for Testing

Before building visuals, verify data with these DAX queries:

```dax
// Test: Total runs by pipeline
EVALUATE
SUMMARIZE(
    FactPipelineRun,
    DimPipeline[PipelineName],
    "TotalRuns", COUNTROWS(FactPipelineRun),
    "TotalCost", SUM(FactPipelineRun[BillingCost])
)

// Test: Daily cost trend
EVALUATE
ADDCOLUMNS(
    VALUES(DimDate[Date]),
    "DailyCost", CALCULATE(SUM(FactPipelineRun[BillingCost]))
)
```

