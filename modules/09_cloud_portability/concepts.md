# Cloud object storage & portability — concepts

Paraphrased notes; cite sources as *Reis & Housley — Fundamentals of Data
Engineering* and the cloud provider docs. Do not paste long vendor text.

## Object storage vs HDFS

- **HDFS** (module 04 lineage): blocks on data nodes, co-located with compute,
  strong directory semantics, mutable appends. Scaling storage means scaling
  the cluster.
- **Object storage** (S3 / GCS / Blob): flat key→bytes namespace, storage fully
  decoupled from compute, effectively infinite, cheap. "Directories" are a
  prefix illusion. This decoupling is what makes the lakehouse (module 08) and
  elastic Spark possible — spin compute up and down over the same bucket.

## The three clouds, mapped

| Concept | AWS | GCP | Azure |
|---|---|---|---|
| Object store | S3 | Cloud Storage (GCS) | Blob / ADLS Gen2 |
| Bucket/container | bucket | bucket | container |
| Identity | IAM | IAM | Entra ID + RBAC / SAS |
| Managed Spark | EMR / Glue | Dataproc | Synapse / Databricks |
| Warehouse | Redshift | BigQuery | Synapse / Fabric |
| Catalog | Glue Data Catalog | Dataplex | Unity Catalog / Purview |

## Where the abstraction leaks

A single `fsspec` interface hides most differences, but a senior engineer knows
the seams:

1. **Consistency** — all three are now strongly read-after-write consistent for
   new objects, but listing and overwrite semantics still differ in latency.
2. **IAM models** — AWS IAM policies, GCP IAM bindings, and Azure RBAC + SAS
   tokens are *not* interchangeable; portability stops at the auth boundary.
3. **Hierarchical namespace** — ADLS Gen2 has real directories (atomic rename);
   plain S3/GCS do not, which changes how table formats commit.
4. **Egress cost** — reads inside a region are cheap; cross-region/cross-cloud
   egress is the silent budget killer behind "just replicate it."
5. **Table formats** — Delta and Iceberg (module 08) commit via a log/manifest
   precisely to get atomicity *on top of* eventually-listed object stores.

## Why emulators (and their limits)

LocalStack, fake-gcs-server, and Azurite reproduce the API surface so jobs run
unchanged with zero spend and zero credentials — ideal for learning and CI. They
do **not** reproduce IAM enforcement, regional latency, throttling, or egress
cost. Treat green emulator tests as "the code path works," not "this is
production-ready on that cloud."
