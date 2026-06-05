# Module 05 — Data Warehousing & Dimensional Modeling

**Status:** built

Closes the *dimensions vs measures* gap (Kimball / Tableau) and the warehousing
core: grain, slowly changing dimensions, star vs snowflake, and OLAP aggregation.
Everything runs locally on **DuckDB** over `make seed` Parquet — **no Docker**.

## What's in this folder

- `query_star_schema.py` — regional sales aggregate (intro)
- `dimensional_modeling.py` — fan-out trap, **SCD Type 2**, star vs snowflake
- `olap_analytics.py` — **ROLLUP/CUBE/GROUPING SETS**, window running totals, materialized gold
- `tests/` — `test_warehousing_duckdb.py`, `test_dimensional_modeling.py`, `test_olap_analytics.py`

## Infrastructure

Local DuckDB over `data/parquet/` (requires `make seed`). DuckDB is a project
dependency — no services to start.

## Run

**WSL / macOS / Linux (Makefile):**

```bash
make seed
uv run python modules/05_warehousing/dimensional_modeling.py
uv run python modules/05_warehousing/olap_analytics.py
uv run pytest modules/05_warehousing/tests
```

**Windows (native, no WSL)** — see [`docs/setup.md`](../../docs/setup.md):

```powershell
.\tasks.ps1 seed
.\.venv\Scripts\python.exe modules\05_warehousing\dimensional_modeling.py
.\.venv\Scripts\python.exe modules\05_warehousing\olap_analytics.py
.\tasks.ps1 test
```

## Prove-it exercises

1. **Grain & the fan-out trap** — `fanout_trap()` proves a 2× duplicated dimension
   doubles `SUM(sales_amount)`. Acceptance: `inflated_total == 2 × true_total`.
2. **SCD Type 2** — `build_scd2()` versions a customer dimension across two
   snapshots. Acceptance: exactly one `is_current` row per customer; every 7th
   customer carries a historical row (`customers // 7`).
3. **Star vs snowflake** — `star_category_revenue()` and `snowflake_category_revenue()`
   return identical revenue; the snowflake form pays an extra join. Acceptance:
   the two results are equal.
4. **ROLLUP / CUBE** — `rollup_region_category()` yields subtotals + one grand-total
   row whose revenue equals the sum of the detail rows. Acceptance: grand total
   reconciles to the detail sum.
5. **Window functions** — `running_total_by_region()` produces a non-decreasing
   cumulative total ending at the grand total, plus a revenue rank.
6. **Materialized aggregate** — `materialized_region_revenue()` pre-computes a
   gold table with one row per region (the materialized-view / gold-layer pattern).

## Concepts → code

| Kimball / OLAP concept | Where |
|---|---|
| Dimension vs measure | every `GROUP BY <dim>` over `SUM(sales_amount)` |
| Grain / additivity | `fanout_trap()` |
| Slowly changing dimension (Type 2) | `build_scd2()` |
| Normalization tradeoff | `star_` vs `snowflake_category_revenue()` |
| Data cube (Gray 1997) | `cube_region_category()` |
| Pre-aggregation / materialized view | `materialized_region_revenue()` |

## Further reading

[`docs/curriculum.md` — Repo modules 03 and 05](../../docs/curriculum.md#repo-modules-03-and-05--bi-and-warehousing)
