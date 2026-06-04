# Module 05 — Data Warehousing & Dimensional Modeling

**Status:** light

## What's in this folder

- `query_star_schema.py` — DuckDB regional sales aggregate
- `tests/test_warehousing_duckdb.py` — grain and row-count checks

## Infrastructure

Local DuckDB over `data/parquet/` (requires `make seed`).

## Run

```bash
make seed
uv run python modules/05_warehousing/query_star_schema.py
uv run pytest modules/05_warehousing/tests
```

## Prove-it exercises

1. **Star schema in DuckDB** — regional aggregate returns one row per `dim_store.region`
2. **Measures vs dimensions** — `sales_amount` is summed at correct grain (not double-counted)

## Further reading

[`docs/curriculum.md` — Repo modules 03 and 05](../../docs/curriculum.md#repo-modules-03-and-05--bi-and-warehousing)
