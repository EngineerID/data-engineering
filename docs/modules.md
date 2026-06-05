# Modules and labs

Each folder under [`modules/`](../modules/) is a prove-it unit. **DSA** (algorithms) is studied in a **separate repository** in parallel with repo module 02.

- **01 — Python** · [01_python_model](../modules/01_python_model/) · light · local only · `uv run pytest modules/01_python_model/tests`
- **02 — SQL** · [02_sql_relational](../modules/02_sql_relational/) · **built** · `postgres` · `make seed`, `make up`, `make load-sql`, `make sql` · artifacts: `data/sql_plans/`
- **03 — BI** · [03_bi_tools](../modules/03_bi_tools/) · light · local notes · `uv run pytest modules/03_bi_tools/tests`
- **04 — PySpark** · [04_spark_internals](../modules/04_spark_internals/) · **built** · `spark-master`, workers · `make up`, `make seed`, `make spark-submit`, `make oom-lab` · artifacts: `data/explain/`
- **05 — Warehousing** · [05_warehousing](../modules/05_warehousing/) · **built** · DuckDB · `make seed`, `uv run pytest modules/05_warehousing/tests` · SCD2, star/snowflake, ROLLUP/CUBE
- **06 — Kafka** · [06_streaming_kafka](../modules/06_streaming_kafka/) · light · `kafka` · `make up`, `uv run pytest modules/06_streaming_kafka/tests -m kafka`
- **07 — AI-assisted** · [07_ai_assisted_dev](../modules/07_ai_assisted_dev/) · agent files · repo root `CLAUDE.md`, `.cursor/rules/`
- **08 — Lakehouse** · [08_lakehouse_medallion](../modules/08_lakehouse_medallion/) · light · local `data/medallion/` · `make seed`, pipeline script + pytest
- **09 — Cloud portability** · [09_cloud_portability](../modules/09_cloud_portability/) · **built** · `localstack`/`fake-gcs`/`azurite` · `make up-cloud`, `uv sync --extra cloud`, `uv run pytest modules/09_cloud_portability/tests -m cloud`
- **10 — dbt / orchestration / catalog** · [10_dbt_orchestration](../modules/10_dbt_orchestration/) · **built** · DuckDB · `make seed`, `uv sync --extra dbt`, `make dbt-run`, `make test-dbt` · dbt tests, lineage, data catalog

Reading lists and sequencing: [`curriculum.md`](curriculum.md).
