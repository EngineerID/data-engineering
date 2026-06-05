# Normalization, OLTP vs OLAP, isolation — the conceptual answers

Concepts the runnable SQL doesn't show but the drill asks about. Paraphrased; cite
*Silberschatz — Database System Concepts* and the SQL cheat sheet §10, §14.

## Normalization → 3NF (which anomaly each form removes)

Walk a flat `orders(order_id, customer_name, customer_city, product, qty)` to 3NF:

- **1NF** — atomic values, no repeating groups. One product per row (no `product1,
  product2` columns). Removes: multi-value / repeating-group anomalies.
- **2NF** — no partial dependency on part of a composite key. If the key is
  `(order_id, product)`, `customer_name` depends only on `order_id` → split it out.
  Removes: update anomalies from duplicating order attributes on every line.
- **3NF** — no transitive dependency (non-key → non-key). `customer_city` depends on
  `customer_id`, not on `order_id` → move it to a `customers` table. Removes: the
  anomaly where changing a customer's city means updating many order rows.

**When you stop:** OLTP aims for 3NF (write-correctness, no redundancy). Reporting/Gold
**denormalizes on purpose** — a star schema is deliberately not normalized so BI reads
are one fact-to-dimension hop instead of a six-table join. You keep the redundant copies
consistent by rebuilding them from the normalized source (the ELT/MERGE in this module),
never by hand-editing.

## OLTP vs OLAP (be specific)

Each row is *dimension — OLTP · OLAP*:

- **Workload** — many small reads/writes · few large aggregate scans
- **Schema** — normalized (3NF) · denormalized (star/snowflake)
- **Storage** — row-store · column-store
- **Index** — many narrow B-trees on lookup keys · fewer; sort/zone maps, partition pruning
- **Tuning goal** — latency per transaction · throughput per scan

Running heavy analytical queries on the OLTP box holds locks and trashes the buffer
cache for the transactional workload. Fixes: a **read replica** for reporting, or ship
data to a warehouse/lakehouse (the medallion pipeline in module 08). Replica reads are
eventually consistent — reports can read slightly stale numbers (replication lag).

## Transactions & isolation (cheat sheet §10)

`BEGIN; … COMMIT;` is all-or-nothing (Atomicity). Isolation levels trade correctness
for concurrency:

Each level lists which anomalies it *allows* — dirty read · non-repeatable read · phantom:

- **READ UNCOMMITTED** — dirty: yes · non-repeatable: yes · phantom: yes
- **READ COMMITTED** *(default in PG/MSSQL)* — dirty: no · non-repeatable: yes · phantom: yes
- **REPEATABLE READ** — dirty: no · non-repeatable: no · phantom: yes (blocked in MySQL InnoDB)
- **SERIALIZABLE** — dirty: no · non-repeatable: no · phantom: no

**Deadlock** = two transactions each hold what the other needs; the engine kills one.
Avoid by acquiring locks in a consistent order. Higher isolation = more correctness,
less concurrency. SQL Server's `READ COMMITTED SNAPSHOT` gives readers a consistent
snapshot without blocking writers (Postgres/Oracle do this via MVCC by default).
