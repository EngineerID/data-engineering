-- Stored procedures + triggers (sql-cheat-sheet §12; two-question-drill: Trigger,
-- Stored procedure). The DBA-core seam: a trigger is the relational mirror of an
-- audit Cloud Function; a stored procedure is reusable server-side logic.
-- Postgres dialect here; SQL Server/MySQL differences noted in the README.

-- Audit trail target. JSONB old/new captures the full row diff.
DROP TABLE IF EXISTS retail.audit_log CASCADE;
CREATE TABLE retail.audit_log (
    audit_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name  TEXT        NOT NULL,
    operation   TEXT        NOT NULL,
    row_key     TEXT,
    old_value   JSONB,
    new_value   JSONB,
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- A small managed table whose edits we want audited.
DROP TABLE IF EXISTS retail.kpi_targets CASCADE;
CREATE TABLE retail.kpi_targets (
    region        TEXT          PRIMARY KEY,
    target_amount NUMERIC(14, 2) NOT NULL,
    updated_at    TIMESTAMPTZ   NOT NULL DEFAULT now()
);
INSERT INTO retail.kpi_targets (region, target_amount)
SELECT DISTINCT region, 100000 FROM retail.dim_store;

-- Trigger function: fires automatically, writes a before/after image to audit_log.
-- Keep triggers to data-integrity/audit concerns; business logic stays in code.
CREATE OR REPLACE FUNCTION retail.fn_audit_kpi_targets()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO retail.audit_log (table_name, operation, row_key, old_value, new_value)
    VALUES ('kpi_targets', TG_OP, NEW.region, to_jsonb(OLD), to_jsonb(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_audit_kpi_targets ON retail.kpi_targets;
CREATE TRIGGER trg_audit_kpi_targets
    AFTER UPDATE ON retail.kpi_targets
    FOR EACH ROW EXECUTE FUNCTION retail.fn_audit_kpi_targets();

-- Fire it once so the audit trail is non-empty and the test can prove it worked.
UPDATE retail.kpi_targets SET target_amount = target_amount * 1.10;

-- Stored procedure: the "validate-and-promote" / refresh step. TRUNCATE-and-rebuild
-- makes it idempotent (re-running yields the same table, no duplicates).
CREATE TABLE IF NOT EXISTS retail.gold_regional_kpi (
    region        TEXT          PRIMARY KEY,
    revenue       NUMERIC(16, 2) NOT NULL,
    target_amount NUMERIC(14, 2),
    attainment    NUMERIC(6, 3),
    refreshed_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE OR REPLACE PROCEDURE retail.refresh_regional_kpi()
LANGUAGE plpgsql AS $$
BEGIN
    TRUNCATE retail.gold_regional_kpi;
    INSERT INTO retail.gold_regional_kpi (region, revenue, target_amount, attainment)
    SELECT
        s.region,
        SUM(f.sales_amount),
        t.target_amount,
        ROUND((SUM(f.sales_amount) / NULLIF(t.target_amount, 0))::numeric, 3)
    FROM retail.fact_sales AS f
    JOIN retail.dim_store AS s ON s.store_key = f.store_key
    LEFT JOIN retail.kpi_targets AS t ON t.region = s.region
    GROUP BY s.region, t.target_amount;
END;
$$;

CALL retail.refresh_regional_kpi();
