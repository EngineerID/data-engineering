# Module 02 — Relational Databases, SQL & Query Optimization

## What's in this folder

- `sql/01_views.sql`, `sql/02_recursive_cte.sql`, `sql/03_index_demo.sql`
- `load_to_postgres.py` — load Parquet into Postgres and apply scripts
- `tests/test_sql_slice.py` — prove-it tests (`-m postgres`)

## Infrastructure

Docker service: **postgres** (`infra/docker-compose.yml`). Requires `make seed` first (shared datagen).

## Run

```bash
make seed
make up
make load-sql
uv run pytest modules/02_sql_relational/tests -m postgres
```

Optional: `make sql` for an interactive `psql` shell.

## Prove-it exercises

1. **VIEW over star join** — Acceptance: `retail.v_sales_by_region` returns one row per distinct `region` in `dim_store`, with non-null `total_sales`.
2. **Recursive CTE** — Acceptance: `retail.v_category_tree` row count equals `product_hierarchy` rows; tree reaches level-3 nodes.
3. **Index tuning** — Acceptance: `EXPLAIN ANALYZE` on `customer_key = 42` shows an Index Scan after creating `idx_fact_customer_key`; plan artifacts saved under `data/sql_plans/`.

## Further reading

[`docs/curriculum.md` — Repo module 02](../docs/curriculum.md#repo-module-02--sql)
