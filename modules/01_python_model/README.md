# Module 01 — Python Language Model

**Status:** light (by design — least relevant to the target DBA role; see `docs/scope-cap.md`)

## What's in this folder

- `exercises.py` — `MutableDemo`, `Vector2`, `MiniSequence`
- `tests/test_python_model.py` — prove-it tests

## Infrastructure

Local Python only (no Docker services).

## Run

```bash
uv run pytest modules/01_python_model/tests
```

## Prove-it exercises

1. **Mutability drill** — list/dict mutation vs frozen `Vector2`
2. **Dunder methods** — `__repr__`, `__eq__`, `__hash__` on `Vector2`
3. **Data model API** — `MiniSequence` supports `len`, indexing, iteration

## Further reading

[`docs/curriculum.md` — Repo module 01](../../docs/curriculum.md#repo-module-01--python-language-model)
