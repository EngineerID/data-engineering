# Power BI vs Tableau — retail star schema

## Connectivity

### Power BI

Import or DirectQuery to Postgres `retail` schema; Parquet via DuckDB export optional.

### Tableau

Postgres connector or Hyper extract from Parquet under `data/parquet/`.

## Refresh

### Power BI

Scheduled refresh on import mode; DirectQuery is live.

### Tableau

Extract refresh schedule or live connection.

## Row-level security

### Power BI

Dynamic RLS with `USERPRINCIPALNAME()` filters on `dim_store.region`.

### Tableau

User filters or Entitlement tables mapping users to `region`.

## Your comparison notes

Add screenshots or personal notes below when you complete the exercise.
