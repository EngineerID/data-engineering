# Module 06 — Event Streaming & Kafka

**Status:** light

## What's in this folder

- `roundtrip.py` — produce/consume JSON on topic `def_learning_events`
- `concepts.md` — streaming two-question-drill answers (micro-batch, event-time, windows, watermarks, triggers, CDC + idempotent MERGE)
- `tests/test_kafka_roundtrip.py` — integration test (`-m kafka`)
- `tests/test_streaming_concepts.py` — concepts note structure (no broker needed)

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
3. **Concepts** — `concepts.md` answers the streaming drill (structure checked by test)

## Interview bar (maps to the two-question drill)

- **Structured Streaming** — Q1 it's micro-batch under the hood; Q2 the checkpoint stores
  offsets + state, delete it and the stream loses its place.
- **Event-time / watermarks / windows** — a concrete late-data bug, what the watermark
  drops, and tumbling/sliding/session use cases. See `concepts.md`.
- **CDC** — log-based vs query-based; deletes + out-of-order handled by idempotent MERGE
  (the same primitive as modules 02 and 08).

Streaming is intentionally docs-first here (lighter for this role) — see
[`../../docs/scope-cap.md`](../../docs/scope-cap.md).

## Further reading

[`docs/curriculum.md` — Repo module 06](../../docs/curriculum.md#repo-module-06--kafka)
