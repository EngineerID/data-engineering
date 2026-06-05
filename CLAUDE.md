# Data Engineering Foundations

Hands-on repo closing the gap between **analytics delivery** (SQL, BI, warehousing) and **systems internals** (Spark cluster model, SQL tuning, streaming, lakehouse patterns). Graded artifacts are **runnable jobs + passing tests**, not notebooks.

> **House rule — no pipe tables.** Every Markdown file in this repo (READMEs, notes, docs) uses clean prose and bullet lists, **never GitHub pipe tables**. Convert any table you touch on sight. Full rationale in [Principles](#principles) §5.

## Commands (WSL/macOS/Linux from repo root; native Windows: `.\tasks.ps1 <target>`)

- `make setup` — `uv sync` + pre-commit hooks
- `make up` / `make down` — Docker: Spark (1 master, 2 workers), Postgres 16, Kafka KRaft
- `make up-cloud` / `make down-cloud` — Module 09 cloud emulators (LocalStack/fake-gcs/Azurite)
- `make seed` — Generate star-schema Parquet (~0.01 GB)
- `make seed-large` — ~1 GB for shuffle/OOM labs
- `make load-sql` — Load Parquet into Postgres + apply SQL
- `make spark-submit JOB=path/to/job.py` — Submit to **standalone cluster** (not `local[*]`)
- `make oom-lab` — Module 04 OOM exercise (expect failure)
- `make sql` — psql shell
- `make lint` / `make typecheck` / `make test` — Quality gates
- `make test-cloud` — Module 09 roundtrip (`uv sync --extra cloud` + `make up-cloud`)
- `make dbt-run` / `make test-dbt` — Module 10 dbt build + catalog (`uv sync --extra dbt`)
- `make check` — lint + typecheck + test

## Stack

- Python 3.12, **uv**, package `def_` under `src/def_/`
- **ruff**, **mypy** (strict on `src/def_/`), **pytest**
- Local Docker only — no real cloud APIs (Module 09 uses **local emulators**: LocalStack/fake-gcs/Azurite)
- **duckdb** for Module 05 warehousing exercises; **PySpark** on Bitnami Spark 3.5 cluster
- Cloud backends (`fsspec`, `s3fs`, `gcsfs`, `adlfs`) are an optional extra: `uv sync --extra cloud`
- **dbt** (`dbt-duckdb`) for Module 10 is an optional extra: `uv sync --extra dbt`
- CI: `.github/workflows/ci.yml` runs `make check`; `.gitlab-ci.yml` mirrors it

## Layout

- `src/def_/common/` — Spark session builder, Postgres DSN, paths (cluster-first)
- `src/def_/datagen/` — Kimball-style retail star schema, `--scale-gb`
- `modules/NN_*/` — learning units 01–10; exercises + tests in-module
- `src/def_/common/storage.py` — multi-cloud fsspec abstraction (Module 09)
- `modules/10_dbt_orchestration/dbt_project/` — dbt models, tests, catalog (Module 10)
- `docs/curriculum.md` — committed curriculum and reading lists
- `docs/progression.md` — canonical beginner→cap onboarding map (the at-a-glance module ladder; start sessions here)
- `references/` — **gitignored** optional local textbook extracts only; never commit
- `data/` — **gitignored** generated Parquet and explain artifacts

## Scope cap (read before adding anything)

This repo is **capped at the depth/breadth of the Technical Interview Preparation
Package** (DBA-leaning role: SQL Server/MySQL, stored procs, triggers, indexing,
OLTP/OLAP, warehouse, star schema, RBAC, Power BI + lakehouse/governance concepts).
Before adding scope or depth, read [`docs/scope-cap.md`](docs/scope-cap.md) — it names
the anchor documents and the "which glossary term does this serve?" test. Not a freeze;
a standing instruction.

## Principles

1. **Real cluster over notebooks** — Spark jobs via `spark-submit` against `spark://localhost:7077`; inspect UI :8080 (cluster) and :4040 (app).
2. **Prove it** — Every exercise has pytest acceptance criteria; integration tests skip when Docker is down.
3. **Typed `src/`** — Fully annotated; `make typecheck` must pass before done.
4. **Copyright** — Paraphrase concepts in READMEs; cite as *Book — Chapter N*; never paste long verbatim text from `references/`.
5. **Markdown style — no tables** — Write every `.md` in this repo (READMEs, notes, docs) as **clean prose and bullet lists, never pipe tables**. This is a standing instruction for all future AI and human contributors: before you write or edit a Markdown document, render any tabular thought as a list (one bullet per item, with `·`- or `—`-separated fields inside the bullet) or as short prose. Rationale: pipe tables are brittle to diff, wrap badly in terminals and narrow viewports, and are harder for both humans and tools to read and patch line-by-line. Lists stay readable and machine-parseable at any width. If existing tables are found, convert them on touch.
   - **ASCII for load-bearing tokens.** Identifiers, filenames, paths, dict/storage keys, CLI flags, env vars, and code literals must be plain ASCII — never curly quotes, em dashes, or symbols that can't be typed at a terminal or matched by a string compare. Prose and bullet separators may use the established Unicode set already in use across the repo (`·` `—` `→` `≙` and the ✅/❌ markers in worked examples); do not mass-convert those. The point is to keep anything a machine parses typeable and diff-stable, not to strip punctuation from explanatory text.

## Spark session

Use `def_.common.spark.build_spark_session(name, cluster=True)` for graded jobs. Do not default to `local[*]` except isolated unit tests.

## Environment

Copy `.env.example` → `.env`. Defaults match `infra/docker-compose.yml` (`def_user` / `def_learning`).

## Module status

- **Built:** 02 SQL (views/CTE/index + windows/procs+triggers/idempotent-MERGE/RLS; **+ concept notes**: `notes/sql-foundations.md`, `notes/sql-patterns.md` — analytical patterns mapped to the runnable views), 03 BI (Power BI/DAX concepts), 04 Spark, 05 warehousing (SCD2/OLAP), 06 Kafka (roundtrip + streaming concepts), 08 lakehouse (medallion + DuckDB table-format lab: MERGE/enforce/evolve/time-travel), 09 cloud portability, 10 dbt/catalog, datagen, infra, CI, agent files (07)
- **Light (by design):** 01 Python — minimal runnable infra per `docs/scope-cap.md`, but now carries the interview-prep **concept ramp**: `notes/python-foundations.md` (never-programmed on-ramp) + `notes/array-string-patterns.md` (Python data-manipulation patterns), climbing to the data-model exercises

## UIs

- Spark master: http://localhost:8080
- Spark application: http://localhost:4040 (while a job runs)
