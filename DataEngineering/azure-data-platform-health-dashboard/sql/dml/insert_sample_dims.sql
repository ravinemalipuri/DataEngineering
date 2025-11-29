INSERT INTO dw.DimPipeline (PipelineId, PipelineName, Environment, SourceSystem, Domain, OwnerEmail, CreatedOn)
VALUES
('adf-pl-sales-ingest', 'ADF Sales Ingest', 'Prod', 'Salesforce', 'Sales', 'sales.owner@example.com', SYSDATETIME()),
('adf-pl-sap-orders',  'ADF SAP Orders',   'Prod', 'SAP',        'SupplyChain', 'sc.owner@example.com', SYSDATETIME());

INSERT INTO dw.DimIntegrationRuntime (IRName, IRType, Region, Environment)
VALUES
('AutoResolveIntegrationRuntime', 'Azure', 'East US', 'Prod'),
('SelfHosted-IR-01', 'SelfHosted', 'OnPrem', 'Prod');

INSERT INTO dw.DimSourceSystem (SourceName, SystemType, Description, Environment)
VALUES
('Salesforce', 'SaaS', 'CRM SFDC', 'Prod'),
('SAP',        'ERP',  'SAP ECC',  'Prod');
