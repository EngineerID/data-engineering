"""Prove-it tests for Module 06 — Kafka roundtrip."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

import pytest

pytest.importorskip("kafka")

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import roundtrip  # noqa: E402

pytestmark = pytest.mark.kafka


def _kafka_reachable() -> bool:
    host, _, port_str = roundtrip.BOOTSTRAP.partition(":")
    port = int(port_str or "9092")
    try:
        with socket.create_connection((host or "localhost", port), timeout=2):
            return True
    except OSError:
        return False


def test_kafka_roundtrip() -> None:
    if not _kafka_reachable():
        pytest.skip("Kafka not reachable — run: make up")
    received = roundtrip.roundtrip(3)
    assert received == 3


def test_consumer_group_uses_configured_group() -> None:
    assert roundtrip.GROUP_ID == "def_learning_roundtrip"
