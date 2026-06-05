# Modules and labs

Each folder under [`modules/`](../modules/) is a prove-it unit. The algorithmic reasoning the role needs is taught as **Python data-manipulation patterns** in module 01's `notes/array-string-patterns.md`, derived backward from the data-engineering work — not as a standalone DSA discipline.

- **01 — Python** · [01_python_model](../modules/01_python_model/) · light infra + concept ramp · local only · notes: `python-foundations.md` (never-programmed on-ramp), `array-string-patterns.md` (Python data-manipulation patterns) → `exercises.py` (data model) · `uv run pytest modules/01_python_model/tests`
- **02 — SQL** · [02_sql_relational](../modules/02_sql_relational/) · **built** · `postgres` · notes: `sql-foundations.md`, `sql-patterns.md` (analytical patterns → runnable views) · `make seed`, `make up`, `make load-sql`, `make sql` · artifacts: `data/sql_plans/`
- **03 — BI** · [03_bi_tools](../modules/03_bi_tools/) · **built** (concepts) · local notes · Power BI storage modes / measure-vs-column / dynamic RLS · `uv run pytest modules/03_bi_tools/tests`
- **04 — PySpark** · [04_spark_internals](../modules/04_spark_internals/) · **built** · `spark-master`, workers · `make up`, `make seed`, `make spark-submit`, `make oom-lab` · artifacts: `data/explain/`
- **05 — Warehousing** · [05_warehousing](../modules/05_warehousing/) · **built** · DuckDB · `make seed`, `uv run pytest modules/05_warehousing/tests` · SCD2, star/snowflake, ROLLUP/CUBE
- **06 — Kafka** · [06_streaming_kafka](../modules/06_streaming_kafka/) · **built** (roundtrip + concepts) · `kafka` · event-time/windows/watermarks/CDC notes · `make up`, `uv run pytest modules/06_streaming_kafka/tests`
- **07 — AI-assisted** · [07_ai_assisted_dev](../modules/07_ai_assisted_dev/) · agent files · repo root `CLAUDE.md`, `.cursor/rules/`
- **08 — Lakehouse** · [08_lakehouse_medallion](../modules/08_lakehouse_medallion/) · **built** · local `data/medallion/` + DuckDB table-format lab (idempotent MERGE / schema enforce+evolve / time travel) · `make seed`, pipeline + lab + pytest
- **09 — Cloud portability** · [09_cloud_portability](../modules/09_cloud_portability/) · **built** · `localstack`/`fake-gcs`/`azurite` · `make up-cloud`, `uv sync --extra cloud`, `uv run pytest modules/09_cloud_portability/tests -m cloud`
- **10 — dbt / orchestration / catalog** · [10_dbt_orchestration](../modules/10_dbt_orchestration/) · **built** · DuckDB · `make seed`, `uv sync --extra dbt`, `make dbt-run`, `make test-dbt` · dbt tests, lineage, data catalog

At-a-glance ladder (beginner → cap): [`progression.md`](progression.md). Reading lists
and sequencing: [`curriculum.md`](curriculum.md). Depth/breadth ceiling:
[`scope-cap.md`](scope-cap.md) — the repo is capped at the interview-prep level (01 Python
stays intentionally light; it's the least role-relevant module).
