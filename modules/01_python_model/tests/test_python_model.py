"""Prove-it tests for Module 01 — Python data model."""

from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import exercises  # noqa: E402


def test_mutability() -> None:
    demo = exercises.MutableDemo(items=[1, 2])
    demo.append(3)
    assert demo.items == [1, 2, 3]
    with pytest.raises(FrozenInstanceError):
        exercises.Vector2(1.0, 2.0).x = 9.0  # type: ignore[misc]


def test_dunder_methods() -> None:
    a = exercises.Vector2(1.0, 2.0)
    b = exercises.Vector2(1.0, 2.0)
    c = exercises.Vector2(3.0, 4.0)
    assert repr(a) == "Vector2(x=1.0, y=2.0)"
    assert a == b
    assert a != c
    assert {a, b} == {a}


def test_data_model_api() -> None:
    seq = exercises.MiniSequence([10, 20, 30])
    assert len(seq) == 3
    assert seq[1] == 20
    assert list(seq) == [10, 20, 30]
