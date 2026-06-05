# Module 03 — BI Tools (Power BI, Tableau & Notes)

**Status:** built (concepts — notes-first by design; Power BI is the role's BI tool)

## What's in this folder

- `notes/grain_checklist.md`, `notes/lineage_example.md`, `notes/tool_comparison.md`
- `notes/power_bi_dax.md` — Import/DirectQuery/Composite, measure vs calculated column, dynamic RLS, KPI (the BI drill answers)
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
5. **Power BI / DAX** — `notes/power_bi_dax.md` answers the BI two-question drill (storage modes, measure vs column, RLS)

## Interview bar (maps to the two-question drill)

- **Power BI** — Q1 Import vs DirectQuery vs Composite; Q2 measure vs calculated column
  and why it matters for performance. See `notes/power_bi_dax.md`.
- **Tableau / Looker Studio** — live vs extract; LOD expressions; Looker's freshness ceiling
  (`notes/tool_comparison.md`).
- **KPI** — what separates a KPI from a metric, and how to guard a gameable one.

## Further reading

[`docs/curriculum.md` — Repo modules 03 and 05](../../docs/curriculum.md#repo-modules-03-and-05--bi-and-warehousing)
