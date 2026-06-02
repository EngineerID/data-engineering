-- SQL Performance Explained — indexing chapter: index created/dropped in tests.
-- Baseline plans are captured by pytest via EXPLAIN ANALYZE.
DROP INDEX IF EXISTS retail.idx_fact_customer_key;
