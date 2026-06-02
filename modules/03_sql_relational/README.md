# Module 03 — Relational Databases, SQL & Query Optimization

## Interview gap this closes

> Did not know what a VIEW is; did not know CTEs / the WITH clause; limited temp-table experience. Claims query-tuning experience (Postgres/MySQL) without fundamentals.

## Reference reading

- *Database System Concepts* (Silberschatz) — Chapters 3–5 (relational model, SQL, views)
- *SQL Performance Explained* (Winand) — Chapters 1–2 (indexing, filtering)

## Prove-it exercises

1. **VIEW over star join** — Acceptance: `retail.v_sales_by_region` returns one row per distinct `region` in `dim_store`, with non-null `total_sales`.
2. **Recursive CTE** — Acceptance: `retail.v_category_tree` row count equals `product_hierarchy` rows; tree reaches level-3 nodes.
3. **Index tuning** — Acceptance: `EXPLAIN ANALYZE` on `customer_key = 42` shows an Index Scan after creating `idx_fact_customer_key`; plan artifacts saved under `data/sql_plans/`.

## Run this slice

```bash
make seed
make up
make load-sql
uv run pytest modules/03_sql_relational/tests -m postgres
```
