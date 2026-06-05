-- Window-function interview patterns (sql-cheat-sheet §3, §13).
-- These are the "thinks in SQL" shapes: top-N per group, period-over-period,
-- running totals, and dedup-keep-latest. Built as views so tests can assert them.

-- 1) Top-N per group: top 3 products by revenue within each region.
--    ROW_NUMBER() partitions by region, ranks by revenue, filter rn <= 3.
DROP VIEW IF EXISTS retail.v_top_products_per_region;
CREATE VIEW retail.v_top_products_per_region AS
WITH product_region_rev AS (
    SELECT
        s.region,
        p.product_key,
        p.product_name,
        SUM(f.sales_amount) AS revenue
    FROM retail.fact_sales AS f
    JOIN retail.dim_store AS s ON s.store_key = f.store_key
    JOIN retail.dim_product AS p ON p.product_key = f.product_key
    GROUP BY s.region, p.product_key, p.product_name
)
SELECT region, product_key, product_name, revenue, rn
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC) AS rn
    FROM product_region_rev
) AS ranked
WHERE rn <= 3;

-- 2) Period-over-period + running total: monthly revenue with MoM change (LAG)
--    and a cumulative running total (windowed SUM with an explicit frame).
DROP VIEW IF EXISTS retail.v_monthly_revenue;
CREATE VIEW retail.v_monthly_revenue AS
WITH monthly AS (
    SELECT
        d.year,
        d.month,
        SUM(f.sales_amount) AS revenue
    FROM retail.fact_sales AS f
    JOIN retail.dim_date AS d ON d.date_key = f.date_key
    GROUP BY d.year, d.month
)
SELECT
    year,
    month,
    revenue,
    revenue - LAG(revenue) OVER (ORDER BY year, month) AS mom_change,
    SUM(revenue) OVER (
        ORDER BY year, month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM monthly;

-- 3) Deduplicate, keep most recent: the classic "same email ingested twice,
--    keep the latest row" pattern. ROW_NUMBER() per natural key ordered by recency.
DROP TABLE IF EXISTS retail.raw_customer_emails CASCADE;
CREATE TABLE retail.raw_customer_emails (
    email      TEXT NOT NULL,
    full_name  TEXT NOT NULL,
    loaded_at  TIMESTAMPTZ NOT NULL
);
INSERT INTO retail.raw_customer_emails (email, full_name, loaded_at) VALUES
    ('a@example.com', 'Ann Old',  '2026-01-01 09:00+00'),
    ('a@example.com', 'Ann New',  '2026-02-01 09:00+00'),  -- newer wins
    ('b@example.com', 'Bo Solo',  '2026-01-15 09:00+00');

DROP VIEW IF EXISTS retail.v_customer_emails_deduped;
CREATE VIEW retail.v_customer_emails_deduped AS
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY email ORDER BY loaded_at DESC) AS rn
    FROM retail.raw_customer_emails
)
SELECT email, full_name, loaded_at
FROM ranked
WHERE rn = 1;
