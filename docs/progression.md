# Progression — the absolute-beginner → cap ladder

The one-page map of how this repo's modules already stack, bottom (never programmed)
to top (the interview-prep ceiling). This is **navigation only** — it adds no new
technical depth, it just names the ladder that
[`curriculum.md`](curriculum.md), [`scope-cap.md`](scope-cap.md) and the module
READMEs already imply. For reading lists use [`curriculum.md`](curriculum.md); for
run commands use [`modules.md`](modules.md); for the ceiling and the
"which glossary term does this serve?" test use [`scope-cap.md`](scope-cap.md).

Climb the rungs in order — a single spine, no side tracks. The algorithmic reasoning
the role needs (loop invariants, decomposition, complexity) lives at the Python level
in module 01 and is taught as data manipulation, derived backward from the DE work; it
is not a standalone discipline studied off to the side.

## Level 0 — never programmed

The on-ramp before anything else. Start at
[`modules/01_python_model/notes/python-foundations.md`](../modules/01_python_model/notes/python-foundations.md)
— the never-programmed ramp into the Python language model.

## Level 1 — core manipulation (Python + first SQL)

- **Python data-manipulation patterns** —
  [`modules/01_python_model/notes/array-string-patterns.md`](../modules/01_python_model/notes/array-string-patterns.md)
  · hash map · sliding window · two pointers · loop invariants · indexing arithmetic ·
  problem decomposition. The role's algorithmic reasoning, taught at the Python language
  level rather than as an abstract CS syllabus.
- **First SQL** — the opening queries in repo 02
  ([`modules/02_sql_relational/`](../modules/02_sql_relational/)), before the heavier
  relational work at Level 2.

## Level 2 — relational + dimensional core (the role's heaviest weight)

This is where the DBA-leaning role carries the most weight — invest most here.

- **02 SQL** — [`modules/02_sql_relational/`](../modules/02_sql_relational/) · views ·
  recursive CTEs · index + `EXPLAIN` · stored procedures · triggers · idempotent `MERGE` ·
  row-level security. Mental models in
  [`notes/sql-foundations.md`](../modules/02_sql_relational/notes/sql-foundations.md) and
  [`notes/sql-patterns.md`](../modules/02_sql_relational/notes/sql-patterns.md).
- **05 Warehousing** — [`modules/05_warehousing/`](../modules/05_warehousing/) ·
  star vs. snowflake · SCD2 · OLAP (`ROLLUP`/`CUBE`).

## Level 3 — systems + delivery

- **04 Spark internals** — [`modules/04_spark_internals/`](../modules/04_spark_internals/) ·
  driver/executor model · DAG → jobs/stages/tasks · shuffle · OOM intuition.
- **03 Power BI concepts** — [`modules/03_bi_tools/`](../modules/03_bi_tools/) ·
  storage modes · measure-vs-column · dynamic RLS.
- **06 Kafka** — [`modules/06_streaming_kafka/`](../modules/06_streaming_kafka/) ·
  producer/consumer roundtrip + streaming concepts (event-time/windows/watermarks).

## Level 4 — platform + ops

- **08 Lakehouse** — [`modules/08_lakehouse_medallion/`](../modules/08_lakehouse_medallion/) ·
  medallion pipeline + DuckDB table-format lab (idempotent `MERGE` / schema enforce+evolve /
  time travel).
- **10 dbt / orchestration / catalog** — [`modules/10_dbt_orchestration/`](../modules/10_dbt_orchestration/) ·
  dbt models + tests · lineage · data catalog.
- **09 Cloud portability** — [`modules/09_cloud_portability/`](../modules/09_cloud_portability/) ·
  one storage abstraction across AWS/GCP/Azure on **local emulators**.
- **CI literacy** — `.github/workflows/ci.yml` (runs `make check`) and `.gitlab-ci.yml`
  (mirrors it) for pipeline-YAML reading.
- **07 AI-assisted engineering** — [`modules/07_ai_assisted_dev/`](../modules/07_ai_assisted_dev/) ·
  the repo-root [`CLAUDE.md`](../CLAUDE.md) as project memory.

## Level 5 — governance + THE CAP

- **08 governance & compliance** —
  [`modules/08_lakehouse_medallion/governance_compliance.md`](../modules/08_lakehouse_medallion/governance_compliance.md)
  (lineage, stewardship, PIPEDA/HIPAA/GDPR/BCBS 239).
- **03 stakeholder engagement** —
  [`modules/03_bi_tools/notes/stakeholder_engagement.md`](../modules/03_bi_tools/notes/stakeholder_engagement.md).

**The ceiling, stated explicitly** — every in-scope topic is built to the
**two-question drill** from [`scope-cap.md`](scope-cap.md): you can *run* the happy path,
answer **Q1** (one level past textbook), and answer **Q2** (one tradeoff or one failure
mode). You **explain** at scale; you do not **operate** at scale. That is the top rung —
there is no Level 6.

## Out of scope — hard cap, NOT a backlog

These are **deliberately excluded** per [`scope-cap.md`](scope-cap.md), not gaps waiting to
be filled. Do not raise the cap to add them:

- Real clusters and real cloud spend (local Docker + emulators only).
- Spark AQE / skew tuning beyond shuffle/partitioning/OOM intuition.
- Kafka exactly-once transactional internals.
- A real delta-rs / pyiceberg lab (DuckDB stands in for table-format semantics).
- FinOps / cost-optimization depth.

If one of these tempts you, the answer is the two-question drill, not a new lab.
