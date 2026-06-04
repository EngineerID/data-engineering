# Data Engineering Foundations

Hands-on repo bridging **applied analytics** (SQL, BI, warehousing) and **systems internals** (Spark, SQL tuning, streaming, lakehouse patterns). Assessment is **prove-it**: runnable jobs, captured plans, and passing pytest.

## Start here

- **[Setup](docs/setup.md)** — WSL, Windows, `uv`, Docker (`infra/`), and `make` commands
- **[Curriculum](docs/curriculum.md)** — tiered reading lists and sequencing (committed in `docs/`)
- **[Modules & labs](docs/modules.md)** — which folder, which services, which commands
- **[Module folders](modules/README.md)** — direct links to exercises and READMEs

Optional local textbook extracts only: `references/` (gitignored). Do not commit publisher material there.

## Learner path

1. [README.md](README.md) — you are here
2. [docs/setup.md](docs/setup.md) — WSL, Docker, `uv`, `make`
3. [docs/modules.md](docs/modules.md) — which service and commands per module
4. [modules/NN_*/README.md](modules/README.md) — exercises for the module you are on (e.g. [02 SQL](modules/02_sql_relational/README.md))
5. [docs/curriculum.md](docs/curriculum.md) — reading lists when you need depth

## Quickstart

Run from **WSL** at the repo root. See [setup](docs/setup.md) for Windows without WSL.

```bash
cp .env.example .env
make setup
make up
make seed
make load-sql
make test
make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py
make check
```

## Modules (01–08)

**DSA** is studied in a **separate repository**, in parallel with repo module 02 (SQL).

- **01** [Python](modules/01_python_model/) · light
- **02** [SQL](modules/02_sql_relational/) · **built**
- **03** [BI](modules/03_bi_tools/) · light
- **04** [PySpark](modules/04_spark_internals/) · **built**
- **05** [Warehousing](modules/05_warehousing/) · light
- **06** [Kafka](modules/06_streaming_kafka/) · light
- **07** [AI-assisted](modules/07_ai_assisted_dev/) · agent files
- **08** [Lakehouse](modules/08_lakehouse_medallion/) · light

## Scale knob

```bash
make seed-large
# or: uv run python -m def_.datagen.cli --scale-gb 2.0
```

## Agent context

- [`CLAUDE.md`](CLAUDE.md)
- [`.cursor/rules/`](.cursor/rules/)

## License

Learning use. Keep long textbook paste in local `references/` only.
