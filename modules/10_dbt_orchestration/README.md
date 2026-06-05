# Module 10 — dbt Transformations, Testing & Data Catalog

**Status:** built · **Covers:** the transformation/orchestration layer most data
platforms run on — **dbt** models, **executable data-quality tests** (validation &
reconciliation), a generated **data catalog** with lineage (metadata management),
and how the same DAG is scheduled in production (Airflow / Dagster / CI). Runs
entirely on **DuckDB** over `make seed` Parquet — no warehouse, no Docker.

## What's in this folder

- `dbt_project/` — a small dbt project: `sources` over raw Parquet → `staging`
  views → `marts` tables, with `schema.yml` tests
- `run_pipeline.py` — minimal orchestrator: `dbt build` → `dbt docs generate` →
  emit a catalog/lineage summary
- `concepts.md` — orchestration, data catalog & metadata, BigQuery mapping,
  validation/reconciliation, scaling to many schemas
- `tests/test_dbt_pipeline.py` — prove-it tests (`-m dbt`)

## Setup

```bash
uv sync --extra dbt        # installs dbt-duckdb
```

## Run

**WSL / macOS / Linux:**

```bash
make seed
make dbt-run               # builds models, runs tests, generates the catalog
make test-dbt
```

**Windows (native):**

```powershell
.\tasks.ps1 seed
.\tasks.ps1 dbt-run
.\tasks.ps1 test-dbt
```

Raw dbt commands (from repo root) also work:

```bash
DBT_DUCKDB_PATH=data/dbt/def.duckdb \
  uv run dbt build --project-dir modules/10_dbt_orchestration/dbt_project \
                   --profiles-dir modules/10_dbt_orchestration/dbt_project \
                   --vars '{parquet_dir: data/parquet}'
```

## Prove-it exercises

1. **Models build on a DAG** — `staging` views feed `marts` tables; `dbt build`
   resolves order from `ref()`. Acceptance: 4 models build, gold mart has one row
   per region.
2. **Tests are data validation** — `not_null` / `unique` enforce keys; a
   `relationships` test reconciles `stg_fact_sales.store_key` against
   `stg_dim_store` (referential integrity across the model). Acceptance: all data
   tests pass on `make dbt-run`.
3. **Catalog & lineage** — `dbt docs generate` writes `manifest.json` +
   `catalog.json`: the metadata a data catalog reads (models, columns,
   descriptions, lineage graph). Acceptance: catalog summary reports sources,
   models, and lineage edges; `target/catalog.json` exists.
4. **Orchestration mapping** — explain in `concepts.md` how `run_pipeline.py`'s
   ordered steps map to an Airflow DAG / Dagster job / GitLab CI stage.

## Concepts → code

| Theme | Where |
|---|---|
| ELT transformation (staging → marts) | `models/staging`, `models/marts` |
| Data validation & reconciliation | `schema.yml` `not_null`/`unique`/`relationships` tests |
| Data catalog & metadata management | `dbt docs generate` → `target/manifest.json`, `catalog.json` |
| Data lineage | `manifest.json` `parent_map` (summarized by `run_pipeline.py`) |
| Orchestration | `run_pipeline.py` (maps to Airflow/Dagster/CI) |
| Cloud warehouse portability (BigQuery) | `concepts.md` — same dbt SQL, swap the adapter |

## Further reading

[`docs/curriculum.md` — Repo module 10](../../docs/curriculum.md#repo-module-10--orchestration-dbt-and-the-data-catalog)
