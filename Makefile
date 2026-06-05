# Data Engineering Foundations — run from WSL at repo root.
.PHONY: setup up down up-cloud down-cloud lint typecheck test test-cloud test-dbt dbt-run seed spark-submit sql check load-sql oom-lab

UV := uv
COMPOSE := docker compose -f infra/docker-compose.yml
PYTHONPATH := src:.

export PYTHONPATH

setup:
	$(UV) sync --all-groups
	$(UV) run pre-commit install

up:
	$(COMPOSE) up -d
	@echo "Spark master UI: http://localhost:8080"
	@echo "Spark app UI (when job runs): http://localhost:4040"

down:
	$(COMPOSE) down

up-cloud:
	$(COMPOSE) --profile cloud up -d localstack fake-gcs azurite
	@echo "LocalStack S3: http://localhost:4566  | fake-gcs: http://localhost:4443  | Azurite: http://localhost:10000"

down-cloud:
	$(COMPOSE) --profile cloud down

lint:
	$(UV) run ruff check src modules tests
	$(UV) run ruff format --check src modules tests

typecheck:
	$(UV) run mypy

test:
	$(UV) run pytest -m "not spark and not kafka and not cloud and not dbt" \
		--ignore=modules/04_spark_internals/tests \
		--ignore=modules/06_streaming_kafka/tests

test-cloud:
	$(UV) run pytest modules/09_cloud_portability/tests -m cloud

test-dbt:
	$(UV) run pytest modules/10_dbt_orchestration/tests -m dbt

dbt-run:
	$(UV) run python modules/10_dbt_orchestration/run_pipeline.py

test-all:
	$(UV) run pytest

seed:
	$(UV) run python -m def_.datagen.cli --scale-gb 0.01

seed-large:
	$(UV) run python -m def_.datagen.cli --scale-gb 1.0

load-sql:
	$(UV) run python modules/02_sql_relational/load_to_postgres.py

sql:
	PGPASSWORD=$${POSTGRES_PASSWORD:-def_pass} psql -h $${POSTGRES_HOST:-localhost} -p $${POSTGRES_PORT:-5432} -U $${POSTGRES_USER:-def_user} -d $${POSTGRES_DB:-def_learning}

spark-submit:
	@test -n "$(JOB)" || (echo "Usage: make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py" && exit 1)
	$(COMPOSE) exec -T -e PYTHONPATH=/workspace/src spark-master spark-submit \
		--master spark://spark-master:7077 \
		--deploy-mode client \
		--conf spark.driver.host=spark-master \
		--conf spark.driver.bindAddress=0.0.0.0 \
		/workspace/$(JOB)

oom-lab:
	@echo "WARNING: This job is designed to fail with executor OOM. Run only when cluster is up."
	$(MAKE) spark-submit JOB=modules/04_spark_internals/oom_exercise.py

check: lint typecheck test
