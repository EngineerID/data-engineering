# Module 01 — Python Language Model & Algorithmic Foundations

**Status:** light infra (by design — least role-relevant; see `docs/scope-cap.md`),
but now carries the **concept ramp** from the interview-prep package: a clean climb
from *never-programmed* to the two interview-relevant ceilings (problem decomposition
and the Python data model). The runnable infra stays minimal on purpose; the
*explanatory* depth is docs-first, exactly as the scope cap prescribes.

## The ladder (barebones beginner → ceiling)

This module is two tracks standing on one shared foundation. Read top to bottom:

- **Rung 0 — Foundations** · [`notes/python-foundations.md`](notes/python-foundations.md) — for someone who has never programmed: variables, lists, dicts, loops, functions, `self`.
- **Rung 1a — Python data-manipulation patterns** · [`notes/array-string-patterns.md`](notes/array-string-patterns.md) — for someone who can read the code and now learns *why* the patterns work (hash map, sliding window, two pointers, sort+dedup).
- **Rung 1b — Data-model track** · [`exercises.py`](exercises.py) + tests — the same foundation in the OOP direction: mutability, the dunder protocol, the sequence interface.

Tracks 1a and 1b are **parallel**, not sequential: 1a builds problem-decomposition
instinct (Python data manipulation), 1b builds Python-data-model fluency (the
language-model strand). Both are reachable directly from rung 0. The notes
cross-link to the code (`python-foundations` §3/§9/§10 point at `exercises.py`'s
hashability, mutability, and `class`/`self`), so the concept doc and the runnable
proof stay one click apart with no repeated prose.

## What's in this folder

- `notes/python-foundations.md` — the never-programmed on-ramp (concepts only).
- `notes/array-string-patterns.md` — array/string algorithmic patterns + trade-offs.
- `exercises.py` — `MutableDemo`, `Vector2`, `MiniSequence` (the data-model ceiling).
- `tests/test_python_model.py` — prove-it tests.

## Infrastructure

Local Python only (no Docker services).

## Run

```bash
uv run pytest modules/01_python_model/tests
```

Native Windows: `.\tasks.ps1 test` (or run pytest from the project `.venv` directly).

## Prove-it exercises

1. **Mutability drill** — list/dict mutation vs frozen `Vector2`
   (the runnable form of `python-foundations.md` §9, in-place `.sort()`).
2. **Dunder methods** — `__repr__`, `__eq__`, `__hash__` on `Vector2`
   (the runnable form of why a value can be a dict key — `python-foundations.md` §3).
3. **Data model API** — `MiniSequence` supports `len`, indexing, iteration
   (the protocol behind `python-foundations.md` §2/§5).

The data-manipulation patterns note (`notes/array-string-patterns.md`) is
**explanation-only by design**: the scope cap keeps Module 01 light, and the drill for
these patterns asks you to *reason about* an invariant and a trade-off, not to ship a
graded LeetCode harness.
Each pattern in the note carries its own invariant and the bug it prevents — that is
the two-question bar for this track.

## Further reading

- [`docs/curriculum.md` — Repo module 01 (Python language model)](../../docs/curriculum.md#repo-module-01--python-language-model)
  — the curriculum module the data-manipulation patterns in `notes/array-string-patterns.md` serve
