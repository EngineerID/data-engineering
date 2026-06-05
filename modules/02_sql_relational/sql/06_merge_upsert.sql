-- Idempotent upsert / MERGE (sql-cheat-sheet §8; two-question-drill: Idempotent
-- MERGE, CDC). The relational twin of the idempotent Delta MERGE: insert-or-update
-- on a natural key so a re-run (or a retried CDC event) produces no duplicates.
--
-- Dialect map (same idea, different syntax):
--   Postgres   : INSERT ... ON CONFLICT (key) DO UPDATE  (used below)
--   MySQL      : INSERT ... ON DUPLICATE KEY UPDATE
--   SQL Server / Databricks: MERGE INTO ... WHEN MATCHED ... WHEN NOT MATCHED ...

DROP TABLE IF EXISTS retail.gold_kpi CASCADE;
CREATE TABLE retail.gold_kpi (
    region     TEXT          NOT NULL,
    period     TEXT          NOT NULL,        -- 'YYYY-MM'
    value      NUMERIC(16, 2) NOT NULL,
    updated_at TIMESTAMPTZ   NOT NULL DEFAULT now(),
    PRIMARY KEY (region, period)              -- the natural key that makes upsert safe
);

-- Reusable upsert wrapped in a procedure so a test can run it twice and prove the
-- row count is identical the second time (idempotency).
CREATE OR REPLACE PROCEDURE retail.upsert_gold_kpi()
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO retail.gold_kpi (region, period, value)
    SELECT
        s.region,
        d.year || '-' || LPAD(d.month::text, 2, '0') AS period,
        SUM(f.sales_amount) AS value
    FROM retail.fact_sales AS f
    JOIN retail.dim_store AS s ON s.store_key = f.store_key
    JOIN retail.dim_date AS d ON d.date_key = f.date_key
    GROUP BY s.region, d.year, d.month
    ON CONFLICT (region, period)
    DO UPDATE SET value = EXCLUDED.value, updated_at = now();
END;
$$;

CALL retail.upsert_gold_kpi();
