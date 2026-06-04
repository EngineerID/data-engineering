"""Module 06 — produce and consume JSON events on local Kafka."""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

TOPIC = "def_learning_events"
BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
GROUP_ID = "def_learning_roundtrip"


def _producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def roundtrip(count: int = 5) -> int:
    """Produce `count` messages and return how many were consumed for this run."""
    run_id = str(uuid.uuid4())
    producer = _producer()
    for i in range(count):
        payload: dict[str, Any] = {"run_id": run_id, "seq": i, "event": "sale"}
        producer.send(TOPIC, payload)
    producer.flush()
    producer.close()

    time.sleep(1.0)
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id=f"{GROUP_ID}_{run_id}",
        auto_offset_reset="earliest",
        consumer_timeout_ms=10_000,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    seen = 0
    for message in consumer:
        value = message.value
        if isinstance(value, dict) and value.get("run_id") == run_id:
            seen += 1
    consumer.close()
    return seen


def main() -> None:
    try:
        received = roundtrip(5)
    except NoBrokersAvailable as exc:
        raise SystemExit(f"Kafka not available at {BOOTSTRAP}: {exc}") from exc
    print(f"received={received}")
    if received != 5:
        raise SystemExit(f"expected 5 messages, got {received}")


if __name__ == "__main__":
    main()
