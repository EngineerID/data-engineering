# Stakeholder engagement & analytical communication

BI is where data engineering meets people. The technical model is only useful if
stakeholders trust it and can act on it. These notes are a starter; extend with
examples from your own work.

## Requirements gathering

Turn a vague ask into a measurable spec before building anything:

- **Question** — what decision will this dashboard/report drive?
- **Grain** — at what level (per order? per customer per day?) — see
  [`grain_checklist.md`](grain_checklist.md).
- **Metrics** — exact definitions (is "active user" 30-day or 7-day?).
- **Dimensions / filters** — how will they slice it (region, segment, date)?
- **Freshness & SLA** — how current must the data be?
- **Audience & access** — who sees what (ties to row-level security in
  [`tool_comparison.md`](tool_comparison.md)).

## Translating between worlds

The senior skill is bidirectional translation:

- **Business → model** — "revenue by region last quarter" becomes a fact grain, a
  `SUM(measure)` over `dimension`s, and a date filter.
- **Model → business** — explain *why* two reports disagree (different grain,
  filter, or a fan-out join double-counting a measure) in plain language.

## Analytical skills that build trust

- **Reconciliation** — tie a new report back to a system of record; show the
  numbers match (the `relationships`/`EXCEPT` checks from module 10).
- **Sanity checks** — totals, null rates, period-over-period sense.
- **Documenting definitions** — push metric definitions into the semantic layer /
  data catalog (module 10) so "the number" means one thing org-wide.

## Common failure modes

- Shipping a dashboard nobody asked the right question for.
- Two teams reporting different "revenue" because grain/filters differ.
- No lineage, so when a number looks wrong nobody can trace it — see
  [`lineage_example.md`](lineage_example.md).
