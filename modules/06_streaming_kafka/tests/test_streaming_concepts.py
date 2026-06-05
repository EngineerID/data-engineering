"""Prove-it test for Module 06 — streaming concepts note structure (no broker needed)."""

from __future__ import annotations

from pathlib import Path

CONCEPTS = Path(__file__).resolve().parents[1] / "concepts.md"

REQUIRED_HEADINGS = [
    "## Spark Structured Streaming",
    "## Event-time vs processing-time",
    "## Windows",
    "## Watermarks",
    "## CDC + idempotent MERGE",
]


def test_concepts_note_structure() -> None:
    assert CONCEPTS.exists(), f"Missing {CONCEPTS}"
    text = CONCEPTS.read_text(encoding="utf-8")
    assert len(text.strip()) > 200
    for heading in REQUIRED_HEADINGS:
        assert heading in text, f"concepts.md missing heading: {heading}"
