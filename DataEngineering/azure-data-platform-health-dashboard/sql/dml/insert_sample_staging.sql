-- ====================================================================
-- Insert Sample Staging Data
-- ====================================================================
-- This script inserts sample data into staging tables to demonstrate
-- the ETL process. Adjust the data as needed for your use case.
-- ====================================================================

INSERT INTO stg.PipelineRun_ADF (
    SourceSystem, Environment, PipelineRunId, PipelineId, PipelineName,
    IRName, StartTime, EndTime, Status, RowsProcessed, BytesProcessed, TokensUsed, BillingCost
)
VALUES
('ADF', 'Prod', 'run-001', 'adf-pl-sales-ingest', 'ADF Sales Ingest',
 'AutoResolveIntegrationRuntime', '2025-01-01T01:00:00', '2025-01-01T01:10:00',
 'Succeeded', 100000, 104857600, 10.5, 0.75),
('ADF', 'Prod', 'run-002', 'adf-pl-sap-orders', 'ADF SAP Orders',
 'AutoResolveIntegrationRuntime', '2025-01-01T02:00:00', '2025-01-01T02:30:00',
 'Failed', 50000, 52428800, 8.0, 0.60),
('ADF', 'Prod', 'run-003', 'adf-pl-sales-ingest', 'ADF Sales Ingest',
 'SelfHosted-IR-01', '2025-01-01T03:00:00', '2025-01-01T03:15:00',
 'Succeeded', 150000, 157286400, 12.3, 0.85),
('ADF', 'Prod', 'run-004', 'adf-pl-sap-orders', 'ADF SAP Orders',
 'AutoResolveIntegrationRuntime', '2025-01-01T04:00:00', '2025-01-01T04:20:00',
 'Succeeded', 75000, 78643200, 9.5, 0.70),
('ADF', 'Prod', 'run-005', 'adf-pl-sales-ingest', 'ADF Sales Ingest',
 'AutoResolveIntegrationRuntime', '2025-01-02T01:00:00', '2025-01-02T01:12:00',
 'Succeeded', 110000, 115343360, 11.2, 0.78),
('ADF', 'Prod', 'run-006', 'adf-pl-sap-orders', 'ADF SAP Orders',
 'AutoResolveIntegrationRuntime', '2025-01-02T02:00:00', '2025-01-02T02:18:00',
 'Succeeded', 85000, 89128960, 9.8, 0.72),
('ADF', 'Prod', 'run-007', 'adf-pl-sales-ingest', 'ADF Sales Ingest',
 'AutoResolveIntegrationRuntime', '2025-01-03T01:00:00', '2025-01-03T01:11:00',
 'Succeeded', 105000, 110100480, 10.8, 0.76),
('ADF', 'Prod', 'run-008', 'adf-pl-sap-orders', 'ADF SAP Orders',
 'SelfHosted-IR-01', '2025-01-03T02:00:00', '2025-01-03T02:22:00',
 'Succeeded', 90000, 94371840, 10.0, 0.74);

INSERT INTO stg.ActivityRun_ADF (
    SourceSystem, Environment, ActivityRunId, PipelineRunId, PipelineName,
    ActivityName, ActivityType, IRName, StartTime, EndTime, Status,
    RowsRead, RowsWritten, BytesRead, BytesWritten
)
VALUES
('ADF', 'Prod', 'act-001', 'run-001', 'ADF Sales Ingest',
 'CopyFromSFDC', 'Copy', 'AutoResolveIntegrationRuntime',
 '2025-01-01T01:01:00', '2025-01-01T01:09:00', 'Succeeded',
 100000, 100000, 52428800, 104857600),
('ADF', 'Prod', 'act-002', 'run-002', 'ADF SAP Orders',
 'CopyFromSAP', 'Copy', 'AutoResolveIntegrationRuntime',
 '2025-01-01T02:05:00', '2025-01-01T02:25:00', 'Failed',
 50000, 25000, 26214400, 52428800);

INSERT INTO stg.ComputeUsage (
    SourceSystem, Environment, UsageDate, UsageStartTime, UsageEndTime,
    UsageUnit, UsageQuantity, Cost, PipelineRunId, JobId, JobRunId, ClusterId, WarehouseId, CustomTagsJson
)
VALUES
('Databricks', 'Prod', '2025-01-01', '2025-01-01T01:00:00', '2025-01-01T01:15:00',
 'DBU', 5.0, 0.50, 'run-001', 'job-123', 'jobrun-123-1', 'cluster-01', NULL, '{"adf_run_id":"run-001"}'),
('Databricks', 'Prod', '2025-01-01', '2025-01-01T02:00:00', '2025-01-01T02:20:00',
 'DBU', 4.0, 0.40, 'run-002', 'job-456', 'jobrun-456-1', 'cluster-02', NULL, '{"adf_run_id":"run-002"}'),
('Databricks', 'Prod', '2025-01-01', '2025-01-01T03:00:00', '2025-01-01T03:18:00',
 'DBU', 6.5, 0.65, 'run-003', 'job-789', 'jobrun-789-1', 'cluster-01', NULL, '{"adf_run_id":"run-003"}'),
('Databricks', 'Prod', '2025-01-02', '2025-01-02T01:00:00', '2025-01-02T01:14:00',
 'DBU', 5.2, 0.52, 'run-005', 'job-123', 'jobrun-123-2', 'cluster-01', NULL, '{"adf_run_id":"run-005"}'),
('Databricks', 'Prod', '2025-01-03', '2025-01-03T01:00:00', '2025-01-03T01:13:00',
 'DBU', 5.4, 0.54, 'run-007', 'job-123', 'jobrun-123-3', 'cluster-01', NULL, '{"adf_run_id":"run-007"}');

INSERT INTO stg.DQEvents (
    Environment, PipelineRunId, CheckName, CheckType, Status, FailedRowCount, DetailsJson, EventTime
)
VALUES
('Prod', 'run-001', 'NullCheck_CustomerId', 'Completeness', 'Pass', 0, NULL, '2025-01-01T01:11:00'),
('Prod', 'run-002', 'NullCheck_OrderId', 'Completeness', 'Fail', 25, '{"threshold":0}', '2025-01-01T02:35:00'),
('Prod', 'run-003', 'RangeCheck_SalesAmount', 'Validity', 'Pass', 0, '{"min_value":0,"max_value":1000000}', '2025-01-01T03:16:00'),
('Prod', 'run-004', 'DuplicateCheck_OrderNumber', 'Uniqueness', 'Pass', 0, NULL, '2025-01-01T04:21:00'),
('Prod', 'run-005', 'ReferentialCheck_CustomerId', 'ReferentialIntegrity', 'Pass', 0, '{"referenced_table":"dim_customer"}', '2025-01-02T01:13:00'),
('Prod', 'run-006', 'NullCheck_ProductId', 'Completeness', 'Pass', 0, NULL, '2025-01-02T02:19:00'),
('Prod', 'run-007', 'RangeCheck_Quantity', 'Validity', 'Pass', 0, '{"min_value":1,"max_value":10000}', '2025-01-03T01:12:00'),
('Prod', 'run-008', 'DuplicateCheck_InvoiceNumber', 'Uniqueness', 'Pass', 0, NULL, '2025-01-03T02:23:00');
