# Module 06 — Event Streaming & Kafka

**Status:** light

## What's in this folder

- `roundtrip.py` — produce/consume JSON on topic `def_learning_events`
- `tests/test_kafka_roundtrip.py` — integration test (`-m kafka`)

## Infrastructure

Docker service: **kafka** (`infra/docker-compose.yml`, `localhost:9092`).

## Run

```bash
make up
uv run python modules/06_streaming_kafka/roundtrip.py
uv run pytest modules/06_streaming_kafka/tests -m kafka
```

## Prove-it exercises

1. **Produce/consume** — `roundtrip.py` receives all messages for a run id
2. **Consumer groups** — each run uses an isolated group id (`def_learning_roundtrip_<uuid>`)

## Further reading

[`docs/curriculum.md` — Repo module 06](../../docs/curriculum.md#repo-module-06--kafka)
