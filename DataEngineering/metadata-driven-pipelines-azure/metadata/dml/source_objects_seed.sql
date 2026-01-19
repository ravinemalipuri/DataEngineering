/*
    Sample metadata records for source_objects.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

SET IDENTITY_INSERT [$(SchemaName)].source_objects ON;

INSERT INTO [$(SchemaName)].source_objects (
    source_object_id,
    source_system_id,
    source_object_name,
    target_layer,
    target_path,
    load_type,
    hash_strategy,
    business_keys,
    watermark_column,
    dq_enabled,
    profiling_enabled,
    dq_fail_behavior,
    schema_compat_profile,
    quarantine_path,
    load_notes,
    last_success_run,
    is_active,
    business_owner_name,
    business_owner_email,
    technical_owner_name,
    technical_owner_email,
    escalation_emails,
    created_time,
    updated_time
) VALUES
(1, 1, 'DB2.CUSTOMER', 'BRONZE', 'Tables/DB2/CUSTOMER',
'INCREMENTAL', 'ROW_HASH', '["CUSTOMER_ID"]', 'LAST_MODIFIED_TS',
 1, 1, 'FAIL', 'DEFAULT', 'Quarantine/DB2/CUSTOMER', 'Row-hash incremental',
 NULL, 1, 'Customer Ops', 'cust.ops@hy.com',
'DB2 Squad', 'db2.support@hy.com', '["db2.support@hy.com"]',
 SYSUTCDATETIME(), SYSUTCDATETIME()),
(2, 2, 'SALESFORCE.ACCOUNT', 'SILVER', 'Tables/SF/ACCOUNT',
'FULL', 'NONE', NULL, NULL,
 1, 0, 'WARN', 'LANDING_ZONE', NULL, 'Full refresh nightly',
 NULL, 1, 'CRM Owners', 'crm.owners@hy.com',
'CRM Squad', 'crm.support@hy.com', '["crm.support@hy.com"]',
 SYSUTCDATETIME(), SYSUTCDATETIME());

SET IDENTITY_INSERT [$(SchemaName)].source_objects OFF;
GO


