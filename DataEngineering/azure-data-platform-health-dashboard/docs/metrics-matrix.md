# Metrics Matrix

This document provides a comprehensive list of all metrics available in the Azure Data Platform Health Dashboard, including their definitions, source tables, DAX measures, and Power BI page assignments.

## Metric Categories

1. **Pipeline Performance Metrics**
2. **Cost Metrics**
3. **Regression Metrics**
4. **Integration Runtime (IR) Usage Metrics**

---

## 1. Pipeline Performance Metrics

### 1.1 Run Count Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Pipeline Runs | Total number of pipeline runs across all time | FactPipelineRun | `TotalPipelineRuns` | All Pages |
| Successful Pipeline Runs | Count of runs with Status = "Succeeded" | FactPipelineRun | `SuccessfulPipelineRuns` | Page 2 |
| Failed Pipeline Runs | Count of runs with Status = "Failed" | FactPipelineRun | `FailedPipelineRuns` | Page 2 |
| Pipeline Success Rate (%) | Percentage of successful runs | FactPipelineRun | `PipelineSuccessRate` | Page 2 |
| Total Runs (Last 24H) | Pipeline runs in the last 24 hours | FactPipelineRun | `TotalPipelineRuns_Last24H` | Page 1 |
| Run Count by IR | Pipeline runs grouped by Integration Runtime | FactPipelineRun, DimIntegrationRuntime | `RunCountByIR` | Page 3 |
| Run Count by IR (Last 24H) | IR-level run count in last 24 hours | FactPipelineRun, DimIntegrationRuntime | `RunCountByIR_Last24H` | Page 3 |

### 1.2 Duration Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Duration (seconds) | Sum of all pipeline run durations | FactPipelineRun | `TotalDurationSeconds` | Page 2 |
| Average Duration (seconds) | Average pipeline run duration | FactPipelineRun | `AvgDurationSeconds` | Page 2 |
| Average Duration (minutes) | Average duration converted to minutes | FactPipelineRun | `AvgDurationMinutes` | Page 2 |
| Average Duration (Last 24H) | Average duration in last 24 hours | FactPipelineRun | `AvgDurationSeconds_Last24H` | Page 2 |
| Baseline Avg Duration (7D) | 7-day baseline average duration | FactPipelineRun | `BaselineAvgDurationSeconds_7D` | Page 2 |
| Current Avg Duration (24H) | Current period average duration | FactPipelineRun | `CurrentAvgDurationSeconds_24H` | Page 2 |

### 1.3 Throughput Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Rows Processed | Sum of rows processed across all runs | FactPipelineRun | `TotalRowsProcessed` | Page 2 |
| Total Bytes Processed | Sum of bytes processed across all runs | FactPipelineRun | `TotalBytesProcessed` | Page 2 |
| Average Throughput (rows/sec) | Average processing rate | FactPipelineRun | `AvgThroughputRowsPerSec` | Page 2 |

---

## 2. Cost Metrics

### 2.1 Billing Cost Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Billing Cost | Sum of billing costs from all pipeline runs | FactPipelineRun | `TotalBillingCost` | All Pages |
| Total Billing Cost (Last 24H) | Billing cost in last 24 hours | FactPipelineRun | `TotalBillingCost_Last24H` | Page 1 |
| Total Billing Cost (Last 7D) | Billing cost in last 7 days | FactPipelineRun | `TotalBillingCost_Last7D` | Page 3 |
| Total Billing Cost (Last 30D) | Billing cost in last 30 days | FactPipelineRun | `TotalBillingCost_Last30D` | Page 3 |
| Average Billing Cost Per Run | Average cost per pipeline run | FactPipelineRun | `AvgBillingCostPerRun` | Page 1 |
| Total Cost by IR | Cost grouped by Integration Runtime | FactPipelineRun, DimIntegrationRuntime | `TotalCostByIR` | Page 3 |
| Total Cost by IR (Last 24H) | IR-level cost in last 24 hours | FactPipelineRun, DimIntegrationRuntime | `TotalCostByIR_Last24H` | Page 3 |
| Total Cost by IR (Last 7D) | IR-level cost in last 7 days | FactPipelineRun, DimIntegrationRuntime | `TotalCostByIR_Last7D` | Page 3 |
| Daily Cost Trend | Daily cost over time | FactPipelineRun, DimDate | `DailyCost` | Page 3 |
| Daily Cost by IR | Daily IR-level cost trend | FactPipelineRun, DimDate, DimIntegrationRuntime | `DailyCostByIR` | Page 3 |
| Average Cost Per Run by IR | Average cost per run by IR | FactPipelineRun, DimIntegrationRuntime | `AvgCostPerRunByIR` | Page 3 |

### 2.2 Compute Usage Cost Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Compute Usage Cost | Sum of compute usage costs (DBUs, tokens) | FactComputeUsage | `TotalComputeUsageCost` | Page 3 |
| Total Compute Usage Cost (Last 24H) | Compute cost in last 24 hours | FactComputeUsage | `TotalComputeUsageCost_Last24H` | Page 3 |
| Total Cost | Combined pipeline and compute costs | FactPipelineRun, FactComputeUsage | `TotalCost` | Page 1 |
| Total Cost (Last 24H) | Combined cost in last 24 hours | FactPipelineRun, FactComputeUsage | `TotalCost_Last24H` | Page 1 |

### 2.3 Cost Efficiency Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Average Cost Per Token | Average cost per token used | FactPipelineRun | `AvgCostPerToken` | Page 1 |
| Average Cost Per Row | Average cost per row processed | FactPipelineRun | `AvgCostPerRow` | Page 1 |

---

## 3. Token Usage Metrics

### 3.1 Token Consumption Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Tokens Used | Sum of tokens consumed across all runs | FactPipelineRun | `TotalTokensUsed` | Page 1 |
| Average Tokens Per Run | Average token consumption per run | FactPipelineRun | `AvgTokensPerRun` | Page 2 |
| Total Tokens (Last 24H) | Token consumption in last 24 hours | FactPipelineRun | `TotalTokensUsed_Last24H` | Page 1 |
| Average Tokens Per Run (Last 24H) | Average tokens per run in last 24H | FactPipelineRun | `AvgTokensPerRun_Last24H` | Page 1 |
| Total Tokens by IR | Token consumption grouped by IR | FactPipelineRun, DimIntegrationRuntime | `TotalTokensByIR` | Page 3 |
| Total Tokens by IR (Last 24H) | IR-level tokens in last 24H | FactPipelineRun, DimIntegrationRuntime | `TotalTokensByIR_Last24H` | Page 3 |
| Total Tokens by IR (Last 7D) | IR-level tokens in last 7 days | FactPipelineRun, DimIntegrationRuntime | `TotalTokensByIR_Last7D` | Page 3 |
| Daily Tokens by IR | Daily IR-level token trend | FactPipelineRun, DimDate, DimIntegrationRuntime | `DailyTokensByIR` | Page 3 |
| Average Tokens Per Run by IR | Average tokens per run by IR | FactPipelineRun, DimIntegrationRuntime | `AvgTokensPerRunByIR` | Page 3 |

---

## 4. Regression Metrics

### 4.1 Baseline Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Baseline Avg Tokens Per Run (7D) | 7-day average tokens per run (baseline) | FactPipelineRun | `BaselineAvgTokensPerRun_7D` | Page 2 |
| Baseline Avg Duration (7D) | 7-day average duration (baseline) | FactPipelineRun | `BaselineAvgDurationSeconds_7D` | Page 2 |
| Baseline Run Count (7D) | Run count in baseline period | FactPipelineRun | `BaselineRunCount_7D` | Page 2 |
| Pipeline Baseline Avg Tokens (7D) | Pipeline-specific baseline | FactPipelineRun, DimPipeline | `PipelineBaselineAvgTokens_7D` | Page 2 |

### 4.2 Current Period Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Current Avg Tokens Per Run (24H) | Current period average tokens | FactPipelineRun | `CurrentAvgTokensPerRun_24H` | Page 2 |
| Current Avg Duration (24H) | Current period average duration | FactPipelineRun | `CurrentAvgDurationSeconds_24H` | Page 2 |
| Current Run Count (24H) | Run count in current period | FactPipelineRun | `CurrentRunCount_24H` | Page 2 |
| Pipeline Current Avg Tokens (24H) | Pipeline-specific current average | FactPipelineRun, DimPipeline | `PipelineCurrentAvgTokens_24H` | Page 2 |

### 4.3 Regression Calculation Metrics

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Token Regression % | Percentage change in token usage vs baseline | FactPipelineRun | `TokenRegressionPercent` | Page 2 |
| Duration Regression % | Percentage change in duration vs baseline | FactPipelineRun | `DurationRegressionPercent` | Page 2 |
| Has Token Regression | Boolean: True if regression > 10% | FactPipelineRun | `HasTokenRegression` | Page 2 |
| Has Duration Regression | Boolean: True if regression > 10% | FactPipelineRun | `HasDurationRegression` | Page 2 |
| Performance Regression Score | Combined regression score (0-100) | FactPipelineRun | `PerformanceRegressionScore` | Page 2 |
| Pipeline Token Regression % | Pipeline-specific token regression | FactPipelineRun, DimPipeline | `PipelineTokenRegressionPercent` | Page 2 |

---

## 5. Integration Runtime (IR) Usage Metrics

### 5.1 IR-Level Aggregates

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total Tokens by IR | Total tokens consumed by IR | FactPipelineRun, DimIntegrationRuntime | `TotalTokensByIR` | Page 3 |
| Total Cost by IR | Total cost attributed to IR | FactPipelineRun, DimIntegrationRuntime | `TotalCostByIR` | Page 3 |
| Average Tokens Per Run by IR | Average tokens per run by IR | FactPipelineRun, DimIntegrationRuntime | `AvgTokensPerRunByIR` | Page 3 |
| Average Cost Per Run by IR | Average cost per run by IR | FactPipelineRun, DimIntegrationRuntime | `AvgCostPerRunByIR` | Page 3 |

### 5.2 DBU Usage Metrics (Databricks)

| Metric Name | Definition | Source Table | DAX Measure | Power BI Page |
|------------|-----------|-------------|-------------|---------------|
| Total DBU Usage | Total Databricks Units (DBUs) consumed | FactComputeUsage | `TotalDBUByIR` | Page 3 |
| Total DBU Cost | Total cost of DBU usage | FactComputeUsage | `TotalDBUCost` | Page 3 |
| Total DBU (Last 24H) | DBU usage in last 24 hours | FactComputeUsage | `TotalDBU_Last24H` | Page 3 |
| Total DBU Cost (Last 24H) | DBU cost in last 24 hours | FactComputeUsage | `TotalDBUCost_Last24H` | Page 3 |
| Daily DBU Usage | Daily DBU consumption trend | FactComputeUsage, DimDate | `DailyDBUUsage` | Page 3 |
| Daily DBU Cost | Daily DBU cost trend | FactComputeUsage, DimDate | `DailyDBUCost` | Page 3 |
| Average DBU Per Hour | Average DBU consumption per hour | FactComputeUsage | `AvgDBUPerHour` | Page 3 |

---

## 6. Power BI Page Assignments

### Page 1: Top 10 Costliest Pipelines (Last 24 Hours)

**Primary Metrics**:
- Total Cost (Last 24H) - `TotalCost_Last24H`
- Total Tokens (Last 24H) - `TotalTokensUsed_Last24H`
- Total DBUs (Last 24H) - `TotalDBU_Last24H`
- Total Billing Cost (Last 24H) - `TotalBillingCost_Last24H`
- Average Cost Per Run - `AvgBillingCostPerRun`
- Total Pipeline Runs (Last 24H) - `TotalPipelineRuns_Last24H`

**Visualizations**:
- Table/Matrix: Top 10 pipelines by cost
- Bar Chart: Cost breakdown by pipeline
- Cards: Key aggregate metrics

### Page 2: Performance Regression vs Last Week

**Primary Metrics**:
- Token Regression % - `TokenRegressionPercent`
- Duration Regression % - `DurationRegressionPercent`
- Baseline Avg Tokens (7D) - `BaselineAvgTokensPerRun_7D`
- Current Avg Tokens (24H) - `CurrentAvgTokensPerRun_24H`
- Pipeline Token Regression % - `PipelineTokenRegressionPercent`
- Performance Regression Score - `PerformanceRegressionScore`

**Visualizations**:
- Table: Pipelines with regression
- Scatter Chart: Token regression analysis
- Line Chart: Token trend comparison
- Cards: Summary regression metrics

### Page 3: Cost & Token/DBU Trends by IR

**Primary Metrics**:
- Daily Cost by IR - `DailyCostByIR`
- Daily Tokens by IR - `DailyTokensByIR`
- Daily DBU Usage - `DailyDBUUsage`
- Total Cost by IR (Last 7D) - `TotalCostByIR_Last7D`
- Total Tokens by IR (Last 7D) - `TotalTokensByIR_Last7D`
- Average Tokens Per Run by IR - `AvgTokensPerRunByIR`

**Visualizations**:
- Line Charts: Daily trends by IR
- Stacked Bar Chart: Cost distribution by IR
- Donut Chart: Cost share by IR
- Table: IR usage summary

---

## 7. Metric Calculation Notes

### Regression Calculation

Regression metrics compare current period (last 24 hours) against baseline period (previous 7 days, excluding today).

**Formula**:
```
Regression % = ((Current - Baseline) / Baseline) * 100
```

Positive values indicate regression (performance degradation).
Negative values indicate improvement.

### Date Key Resolution

All metrics use `DateKey` from `DimDate` for time-based filtering:
- `DateKey` format: `YYYYMMDD` (e.g., `20250101` for January 1, 2025)
- Relationships link fact tables to `DimDate` for calendar filtering

### Null Handling

- DAX measures use `DIVIDE()` function with zero-division protection
- Null values are excluded from aggregations by default
- Use `ISBLANK()` checks for explicit null handling where needed

---

## 8. Future Metrics (Planned)

- **Efficiency Metrics**: Tokens per row processed, Cost per row processed
- **Anomaly Detection**: Statistical outliers in token/duration usage
- **Forecasting**: Predictive cost and usage forecasts
- **SLA Metrics**: SLA breach rates, average time to SLA breach
- **Resource Utilization**: IR utilization %, idle time metrics
