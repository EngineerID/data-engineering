# Delta-style table concepts (portable)

## ACID on object storage

Delta Lake (and similar formats) add transaction logs atop Parquet so readers see consistent snapshots. Writers commit new files plus log entries atomically.

## Time travel

Table version history lets you query `VERSION AS OF` or read older snapshots for audit and replay.

## Schema evolution

New columns can be added with merge semantics; incompatible changes require explicit migration plans.

## Relation to this repo

Module 08 light pass uses **local Parquet layers** under `data/medallion/` to practice medallion *layering* without a Delta JAR. Compare mentally to how Bronze/Silver/Gold map to governed tables in a lakehouse platform.

## Your write-up

Expand this section with one paragraph per bullet tying each concept to `retail.fact_sales` grain and lineage in `data/medallion/lineage.json`.
