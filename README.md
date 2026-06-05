# Data Engineering Foundations

Hands-on repo bridging **applied analytics** (SQL, BI, warehousing) and **systems internals** (Spark, SQL tuning, streaming, lakehouse patterns). Assessment is **prove-it**: runnable jobs, captured plans, and passing pytest.

## Start here

- **[Setup](docs/setup.md)** — WSL, Windows, `uv`, Docker (`infra/`), and `make` commands
- **[Progression](docs/progression.md)** — the beginner→cap onboarding ladder on one page
- **[Curriculum](docs/curriculum.md)** — tiered reading lists and sequencing (committed in `docs/`)
- **[Modules & labs](docs/modules.md)** — which folder, which services, which commands
- **[Module folders](modules/README.md)** — direct links to exercises and READMEs

Optional local textbook extracts only: `references/` (gitignored). Do not commit publisher material there.

## Learner path

1. [README.md](README.md) — you are here
2. [docs/progression.md](docs/progression.md) — the absolute-beginner → cap ladder on one page
3. [docs/setup.md](docs/setup.md) — WSL, Docker, `uv`, `make`
4. [docs/modules.md](docs/modules.md) — which service and commands per module
5. [modules/NN_*/README.md](modules/README.md) — exercises for the module you are on (e.g. [02 SQL](modules/02_sql_relational/README.md))
6. [docs/curriculum.md](docs/curriculum.md) — reading lists when you need depth

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

**Native Windows (no WSL)** — same steps via the PowerShell task runner:

```powershell
Copy-Item .env.example .env
.\tasks.ps1 setup
.\tasks.ps1 up
.\tasks.ps1 seed
.\tasks.ps1 test
```

### Cloud module (09)

```bash
uv sync --extra cloud        # install fsspec backends (s3fs/gcsfs/adlfs)
make up-cloud                # LocalStack + fake-gcs + Azurite
uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud aws
make test-cloud
make down-cloud
```

### dbt / orchestration / catalog (10)

```bash
uv sync --extra dbt          # install dbt-duckdb
make dbt-run                 # build models, run data tests, generate the catalog
make test-dbt
```

## Modules (01–10)

- **01** [Python](modules/01_python_model/) · light (by design — least role-relevant)
- **02** [SQL](modules/02_sql_relational/) · **built**
- **03** [BI](modules/03_bi_tools/) · **built** (concepts)
- **04** [PySpark](modules/04_spark_internals/) · **built**
- **05** [Warehousing](modules/05_warehousing/) · **built**
- **06** [Kafka](modules/06_streaming_kafka/) · **built** (roundtrip + concepts)
- **07** [AI-assisted](modules/07_ai_assisted_dev/) · agent files
- **08** [Lakehouse](modules/08_lakehouse_medallion/) · **built**
- **09** [Cloud portability (AWS/GCP/Azure)](modules/09_cloud_portability/) · **built**
- **10** [dbt / orchestration / data catalog](modules/10_dbt_orchestration/) · **built**

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
