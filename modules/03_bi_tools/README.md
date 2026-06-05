# Module 03 — BI Tools (Power BI, Tableau & Notes)

**Status:** light

## What's in this folder

- `notes/grain_checklist.md`, `notes/lineage_example.md`, `notes/tool_comparison.md`
- `notes/stakeholder_engagement.md` — requirements gathering, analytical communication, reconciliation
- `tests/test_bi_notes.py` — validates note structure

## Infrastructure

No Docker services. Uses warehouse concepts from modules 02 and 05.

## Run

```bash
uv run pytest modules/03_bi_tools/tests
```

## Prove-it exercises

1. **Semantic model grain** — extend `notes/grain_checklist.md`
2. **Report ↔ warehouse lineage** — extend `notes/lineage_example.md`
3. **Tool comparison** — extend `notes/tool_comparison.md`
4. **Stakeholder engagement** — extend `notes/stakeholder_engagement.md` with a real requirements-to-metric example

## Further reading

[`docs/curriculum.md` — Repo modules 03 and 05](../../docs/curriculum.md#repo-modules-03-and-05--bi-and-warehousing)
