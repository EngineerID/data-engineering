# Streaming concepts — two-question-drill answers

Streaming is **lighter** for the target DBA role (probed only if it appears on the CV),
so this module is docs-first: the runnable `roundtrip.py` proves a Kafka produce/consume,
and these notes answer the streaming section of the drill at depth. Paraphrased; cite
*Reis & Housley — Fundamentals of Data Engineering* and the Spark Structured Streaming
docs. See [`../../docs/scope-cap.md`](../../docs/scope-cap.md) for why we stop here.

## Spark Structured Streaming — "streaming" under the hood

It's **micro-batch**: the engine runs the same DataFrame query repeatedly over small new
slices of the input, maintaining results incrementally. (A low-latency *continuous* mode
exists but is rarely used.) So you write a batch query once and it runs as a stream.

- **Checkpoint** stores the **offsets processed** and the **running state** (aggregations,
  dedup keys). Delete it and the stream loses its place: it either reprocesses from
  scratch or skips data, and stateful operators reset — checkpoints are what make
  restart-safe, exactly-once-ish processing possible.

## Micro-batch tradeoff

Smaller batch interval = lower latency but **more overhead per batch** and smaller files
(the "small files problem") and less throughput. Too small and scheduling overhead
dominates; you spend more time starting batches than processing. Tune interval to the
latency you actually need, not the lowest possible.

## Event-time vs processing-time

- **Event-time** = when the event happened (carried in the record). **Processing-time** =
  when the engine saw it. Confuse them and you get a concrete bug: a mobile client offline
  for an hour sends events that, bucketed by *arrival*, all land in the wrong window — your
  "9am sales" actually happened at 8am. Always window on event-time for correctness.
- The engine reads event-time from a **column you designate**; if the source clock is
  skewed, your windows are skewed — you can't fix bad timestamps downstream.

## Windows

- **Tumbling** — fixed, non-overlapping (hourly revenue).
- **Sliding** — fixed size, overlapping by a slide interval (5-min average updated every
  1 min).
- **Session** — dynamic, closed by a **gap** parameter: a window ends when no event
  arrives for the gap duration (a user's browsing session). The gap decides "the activity
  stopped."

## Watermarks

A watermark = `max(event_time seen) − delay`. It tells the engine how long to wait for
late data before **finalizing and emitting** a window and dropping its state. Data that
arrives **past the watermark is dropped** (ignored for that window). Picking the delay
trades **latency/state size vs completeness**: a longer delay catches more late data but
holds state longer and emits later.

## Triggers × output modes

- Trigger modes: default (micro-batch ASAP), fixed-interval, **`once` / `availableNow`**
  (process all available data then stop — great for scheduled "stream as batch" backfills).
- Output modes: **append** (only new finalized rows — needs a watermark for aggregations),
  **update** (changed rows), **complete** (whole result table — only for bounded
  aggregations). The trigger decides *when*; the output mode decides *what* is emitted.

## State & Timers

Explicit per-key state (`flatMapGroupsWithState`) solves what windowing can't: arbitrary
session logic, custom dedup, cross-event rules. The risk is **unbounded state** (keys that
never expire → memory grows forever); bound it with timeouts/TTL and watermarks so state
is evicted.

## CDC + idempotent MERGE (the relational on-ramp)

**CDC** streams row-level changes from a source DB. **Log-based** (read the WAL/binlog) is
low-overhead and catches deletes; **query-based** (poll a timestamp/`updated_at`) is
simpler but misses deletes and hard-deletes, and can miss intra-poll changes. Handle
**deletes** by emitting tombstones; handle **out-of-order** events with a sequence/LSN and
an idempotent **MERGE** keyed on the primary key — a replayed event updates in place, no
duplicate. This is the same idempotency primitive as
[module 02](../02_sql_relational/sql/06_merge_upsert.sql) and
[module 08](../08_lakehouse_medallion/table_format_lab.py).

## What `roundtrip.py` proves

A real Kafka produce → consume with an isolated consumer group per run (offset/group
mechanics). It does **not** implement windowing/watermarks — those are explained here, not
operated, by design (scope cap).
