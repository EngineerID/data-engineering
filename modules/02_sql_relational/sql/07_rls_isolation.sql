-- Row-Level Security (sql-cheat-sheet §16; two-question-drill: RBAC, Row-level
-- security). Enforce tenant isolation in the engine, not the app — one bad WHERE
-- shouldn't leak across tenants. This is the multi-tenant SaaS (HK/QC) pattern.

DROP TABLE IF EXISTS retail.tenant_metrics CASCADE;
CREATE TABLE retail.tenant_metrics (
    tenant_id TEXT    NOT NULL,
    metric    TEXT    NOT NULL,
    value     NUMERIC NOT NULL
);
INSERT INTO retail.tenant_metrics (tenant_id, metric, value) VALUES
    ('hk', 'revenue', 100), ('hk', 'cost', 40),
    ('qc', 'revenue', 200), ('qc', 'cost', 80);

ALTER TABLE retail.tenant_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE retail.tenant_metrics FORCE ROW LEVEL SECURITY;  -- apply to the owner too

-- Policy: a session only sees rows for its own tenant. current_setting(..., true)
-- returns NULL when unset, so the default (no tenant set) is deny-all — fail closed.
DROP POLICY IF EXISTS tenant_isolation ON retail.tenant_metrics;
CREATE POLICY tenant_isolation ON retail.tenant_metrics
    USING (tenant_id = current_setting('app.tenant_id', true));

-- A non-superuser app role so RLS actually bites (superusers bypass RLS).
-- The test does SET ROLE retail_app; SET app.tenant_id = 'hk'; and sees only HK rows.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'retail_app') THEN
        CREATE ROLE retail_app NOLOGIN;
    END IF;
END $$;
GRANT USAGE ON SCHEMA retail TO retail_app;
GRANT SELECT ON retail.tenant_metrics TO retail_app;

-- SQL Server equivalent: CREATE SECURITY POLICY with an inline table-valued
-- predicate function bound as a FILTER PREDICATE. Same goal, different mechanism.
