# Data governance & compliance — concepts

Paraphrased notes; cite *DAMA-DMBOK*, *Reis & Housley — Fundamentals of Data
Engineering*, and the relevant regulation/standard. General concepts, not legal
advice.

## Why governance lives in the capstone

The medallion pipeline ([`medallion_pipeline.py`](medallion_pipeline.py)) already
produces **lineage** metadata. Governance is the discipline around that: knowing
what data you hold, who can use it, whether it's correct, and proving it to an
auditor. DAMA-DMBOK frames this as data quality, metadata, security, and
stewardship.

## Personally identifiable / sensitive data

- **PII** — identifies a person (name, email, address, government IDs). In this
  repo, `dim_customer.customer_name` is the stand-in; treat it as sensitive.
- **Classification** — tag columns (public / internal / PII / sensitive) in the
  data catalog (module 10 `schema.yml` `meta`) so policy can be enforced and
  audited from metadata.

## Regulatory regimes (know which applies)

| Regime | Scope | Core obligations (paraphrased) |
|---|---|---|
| **HIPAA** (US) | Protected Health Information | Safeguards, minimum-necessary access, de-identification (Safe Harbor / Expert Determination), breach notification |
| **PIPEDA** (Canada) | Personal info in commercial activity | Consent, purpose limitation, access/correction rights, safeguards |
| **GDPR** (EU) | Personal data | Lawful basis, data-subject rights, minimization, records of processing |
| **BCBS 239** (banking) | Risk data aggregation | Accuracy, completeness, timeliness, and traceable lineage of risk reports |

The portable skill: identify the regime, then implement the same primitives —
classification, access control, de-identification, retention, and lineage.

## De-identification techniques

- **Masking / redaction** — hide all or part of a value (`****@domain.com`).
- **Pseudonymization** — replace identifiers with reversible tokens held
  separately (reversible only with the key).
- **Anonymization** — irreversibly remove identifiers; aim for k-anonymity so a
  row can't be re-identified by combining quasi-identifiers.
- **Aggregation** — report only at a grain coarse enough to protect individuals
  (the gold layer's regional totals already do this).

## Pipeline controls (where each lands here)

- **Lineage** — `data/medallion/lineage.json` + dbt `manifest.json` (module 10):
  trace any gold number back to its bronze source. This is the BCBS 239 / audit
  requirement.
- **Data quality** — bronze→silver `WHERE` filters here; dbt tests in module 10
  (not-null/unique/relationships) make quality checks executable.
- **Access control** — row-level security at the BI layer
  ([`../03_bi_tools/notes/tool_comparison.md`](../03_bi_tools/notes/tool_comparison.md)).
- **Catalog & stewardship** — descriptions/ownership/classification in metadata
  so the catalog (module 10) is the single source of truth for governance.

## Prove-it extension

Add a `classification` tag to PII columns in the module 10 `schema.yml`, then show
the gold layer exposes only aggregated, non-identifying data — a minimal, auditable
de-identification story end to end.
