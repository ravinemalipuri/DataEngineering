/*
    Sample metadata records for source_systems.
    Adjust values before loading into the target environment.
*/
:setvar DatabaseName metadata_db
:setvar SchemaName dbo

USE [$(DatabaseName)];
GO

SET IDENTITY_INSERT [$(SchemaName)].source_systems ON;

INSERT INTO [$(SchemaName)].source_systems (
    source_system_id,
    source_system_name,
    system_type,
    connection_secret_name,
    default_database,
    is_active,
    business_owner_name,
    business_owner_email,
    technical_owner_name,
    technical_owner_email,
    escalation_emails,
    created_time,
    updated_time
) VALUES
(1, 'DB2_CORE', 'DB2', 'kv-secret-db2-core', 'DB2CORE', 1,
 'Maria Gomez', 'maria.gomez@contoso.com',
 'Ops OnCall', 'ops@dataplatform.com',
 '["ops@dataplatform.com","lead@dataplatform.com"]',
 SYSUTCDATETIME(), SYSUTCDATETIME()),
(2, 'SALESFORCE_CRM', 'SALESFORCE', 'kv-secret-sf-crm', NULL, 1,
 'Liam Carter', 'liam.carter@contoso.com',
 'CRM Squad', 'crm.support@dataplatform.com',
 '["crm.support@dataplatform.com"]',
 SYSUTCDATETIME(), SYSUTCDATETIME());

SET IDENTITY_INSERT [$(SchemaName)].source_systems OFF;
GO


