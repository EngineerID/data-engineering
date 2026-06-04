-- Silberschatz — views: virtual table over a query (Ch. 4 conceptually).
DROP VIEW IF EXISTS retail.v_sales_by_region;
CREATE VIEW retail.v_sales_by_region AS
SELECT
    s.region,
    SUM(f.sales_amount) AS total_sales,
    COUNT(*) AS line_count
FROM retail.fact_sales AS f
JOIN retail.dim_store AS s ON f.store_key = s.store_key
GROUP BY s.region;
