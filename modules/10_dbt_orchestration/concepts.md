# Orchestration, the data catalog & warehouse portability — concepts

Paraphrased notes; cite *Reis & Housley — Fundamentals of Data Engineering* and
the dbt / provider docs. Don't paste long vendor text.

## ELT and the transformation DAG

dbt does the **T** in ELT: raw data already landed (here, `make seed` Parquet),
and SQL `models` transform it in place. `ref()` between models builds a
dependency graph; `dbt build` topologically sorts it so `staging` runs before the
`marts` that depend on it. This is the same staging → marts (bronze → silver →
gold) shape as the medallion pipeline in module 08, expressed declaratively.

## Orchestration: who runs the DAG

`run_pipeline.py` runs the steps in order in-process. In production the *same*
ordered steps are scheduled:

| Orchestrator | How the DAG is expressed |
|---|---|
| **Airflow** | a `DAG` of `BashOperator`/`DbtRunOperator` tasks, scheduled by cron-like intervals |
| **Dagster** | software-defined *assets*; dbt models become assets via `dagster-dbt` |
| **GitLab CI / GitHub Actions** | pipeline *stages* (`seed → build → test → docs`) in YAML, triggered on push/schedule |

The skill is recognizing that "orchestration" is just *dependency ordering +
scheduling + retries + observability* over tasks you already have. Reading a
pipeline YAML (stages, jobs, `needs:`/`dependencies:`) is enough to operate one;
authoring production DAGs is the next step up.

## Data validation & reconciliation (dbt tests)

dbt `schema.yml` tests compile to SQL that must return **zero rows**:

- `not_null`, `unique` — column/key integrity.
- `relationships` — every FK value exists in the parent table. This is
  **referential reconciliation**: it proves the fact table agrees with its
  dimensions, the same check you'd run with SQL `EXCEPT`/anti-joins to reconcile
  two systems.
- `accepted_values`, custom/singular tests, and `dbt-utils` (e.g. equal row
  counts between source and model) extend this to full reconciliation suites.

Tests run as part of `dbt build`, so a failing data-quality check fails the
pipeline — validation is not a separate manual step.

## Data catalog & metadata management

`dbt docs generate` produces two metadata artifacts under `target/`:

- **`manifest.json`** — every model/source/test, its SQL, columns, descriptions,
  and the **lineage graph** (`parent_map` / `child_map`).
- **`catalog.json`** — column types and stats from the warehouse.

These are exactly what a **data catalog** (dbt docs site, DataHub, OpenMetadata,
Unity Catalog, Collibra) ingests to give a searchable inventory: *what tables
exist, what each column means, who owns it, and what feeds what*. Improving
**discoverability and governance** means keeping descriptions and ownership in
`schema.yml` so they flow into that catalog automatically. The lineage graph is
also how you do impact analysis ("if I change this source, what breaks?").

## Warehouse portability — BigQuery and friends

dbt models are warehouse-agnostic SQL; you change the **adapter**, not the models:

| Adapter | Engine | Used here |
|---|---|---|
| `dbt-duckdb` | DuckDB (local) | ✅ this lab |
| `dbt-bigquery` | Google BigQuery | swap profile to run the same models in BQ |
| `dbt-snowflake`, `dbt-redshift`, `dbt-databricks` | other cloud warehouses | same models |

**BigQuery specifics worth knowing** (they map to local equivalents you can
reason about with DuckDB/Parquet):

- **Partitioning** — partition large tables by date/ingestion time so queries
  prune to a few partitions (the BQ analog of Parquet/Hive directory
  partitioning and partition pruning).
- **Clustering** — sort within partitions on high-selectivity columns to cut
  scanned bytes; analogous to sort order / zone maps.
- **Cost model** — BigQuery bills on **bytes scanned**; partition + cluster +
  `select` only needed columns to control cost. This is the cloud-warehouse
  version of "less I/O = cheaper and faster."
- **Table design** — wide denormalized tables and nested/`STRUCT`/`ARRAY` columns
  are idiomatic in BQ, versus strict star schemas in classic warehouses.

## Scaling to many schemas and large data

- **Many objects / complex relationships** — a real warehouse has dozens to
  hundreds of related tables (e.g. 70+ objects). dbt keeps this tractable:
  `sources` document the inputs, `ref()` encodes relationships, and
  `relationships` tests enforce them. The lineage graph is what makes a model
  with that many objects navigable.
- **Large datasets** — the transformation pattern is identical at 0.01 GB and at
  300 GB+; only the engine and partitioning change. Use `make seed-large` to feel
  it locally, push partition pruning to the engine, and never `SELECT *` across a
  large fact when a few columns suffice.
