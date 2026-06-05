# Foundations of Big Data Engineering — A 0 → Senior Curriculum

*A competency-mapped course design with tiered reading lists (canonical textbooks → cited academic literature → industry/practitioner sources). It takes a learner from **zero** — never having heard of data engineering — to the point of performing the role at a **senior level**, by forcing the systems-internals layer beneath each tool to the surface and grading every unit on a runnable artifact.*

Hands-on labs in this repository: [`docs/modules.md`](modules.md) · setup: [`docs/setup.md`](setup.md).

---

## Who this is for and how to use it

- **Complete beginners** — start at Tier A (modules 01–03) and work strictly in order; do every lab.
- **Working analysts / data scientists** moving toward data engineering — skim Tier A for gaps, invest in Tier B (the Spark/warehousing/streaming core).
- **Engineers targeting senior big-data roles** — the keystone is module 04 (Spark internals); Tier C is the architecture/research extension.

**What "data engineering" means here:** building the systems that move, store, transform, and serve data reliably and at scale — the relational and dimensional models beneath analytics, the distributed execution model beneath Spark, the streaming and lakehouse patterns beneath modern platforms, and the governance that keeps it trustworthy. This curriculum teaches each of those from first principles, not as recipes.

---

## Repo alignment (modules 01–10)

This repo implements numbered folders under `modules/`. Curriculum sections below retain original numbering where noted.

- **Repo 01** [`01_python_model`](../modules/01_python_model/) — Python language model (curriculum Module 1)
- **DSA** — Data structures & algorithms (curriculum Module 2) — **separate repository**; study in parallel with repo 02
- **Repo 02** [`02_sql_relational`](../modules/02_sql_relational/) — SQL (curriculum Module 3)
- **Repo 03** [`03_bi_tools`](../modules/03_bi_tools/) — BI tools (split from curriculum Module 5)
- **Repo 04** [`04_spark_internals`](../modules/04_spark_internals/) — Spark internals (curriculum Module 4)
- **Repo 05** [`05_warehousing`](../modules/05_warehousing/) — Warehousing / Kimball (curriculum Module 5, warehousing only)
- **Repo 06** [`06_streaming_kafka`](../modules/06_streaming_kafka/) — Kafka (curriculum Module 6)
- **Repo 07** [`07_ai_assisted_dev`](../modules/07_ai_assisted_dev/) — AI-assisted engineering (curriculum Module 8)
- **Repo 08** [`08_lakehouse_medallion`](../modules/08_lakehouse_medallion/) — Lakehouse, Delta, medallion (reframes curriculum Module 9 capstone; portable concepts, not a vendor course)
- **Repo 09** [`09_cloud_portability`](../modules/09_cloud_portability/) — Cloud object storage & portability across AWS/GCP/Azure via local emulators (cross-cutting)
- **Repo 10** [`10_dbt_orchestration`](../modules/10_dbt_orchestration/) — Orchestration, dbt transformations, data validation, and the data catalog
- **Curriculum Module 7** (Java OOP / design patterns) — optional; for roles requiring a JVM/J2EE stack; not a repo folder

Optional local textbook extracts: `references/` (gitignored). Do not commit long verbatim paste from publishers.

---

## 1. Design principles

Most people enter data engineering through a tool — a notebook, a DataFrame API, a BI canvas — and learn the surface without the layer beneath it. That layer is exactly what senior interviews probe and what production failures expose. Two principles follow.

1. **Teach the internals first.** Every module forces the layer beneath the API to the surface — the data model beneath Python syntax, the execution model beneath the DataFrame, the relational algebra beneath SQL, the storage/compute decoupling beneath the cloud. Tools change; these models do not.
2. **Calibrate against the machine, not against confidence.** Assessment is performance-based (debug a real OOM, read a physical plan, prove a loop invariant, write a recursive CTE) rather than recall-based, so self-assessed skill tracks demonstrated skill.

### The competencies that separate notebook-level from senior-level

These are the concepts that most reliably distinguish someone who *uses* the tools from someone who *understands the system*. Each maps to a module below.

- **Python language model** — mutability/immutability, the built-in data structures and their methods, the `array`/`list`/`ndarray` distinction, dunder methods (`__init__`, `__new__`, `__call__`, `__hash__`, `__eq__`), and OOP vs. procedural vs. scripting as language paradigms.
- **Spark internals** — the `spark-submit` lifecycle (driver, executors, DAG, logical→physical plan, Catalyst, jobs/stages/tasks, cluster managers), diagnosing executor *and* driver OOM, partitioning, skew, shuffle, and tuning beyond toy data sizes. The common failure mode is a notebook-local mental model rather than a cluster-distributed one.
- **Relational databases / SQL** — VIEWs, CTEs / the `WITH` clause, temporary vs. virtual tables, and cost-based query tuning with `EXPLAIN`.
- **Dimensional modeling / BI** — dimensions vs. measures (Kimball / Tableau), facts vs. dimensions, star vs. snowflake, slowly changing dimensions, and the lakehouse framing.
- **Algorithms / DSA** — loop invariants, indexing arithmetic, complexity reasoning, and decomposing a problem before writing code.
- **AI-assisted development** — using agentic coding tools effectively, and the purpose of a `CLAUDE.md`-style project memory file in conserving context and tokens.

---

## Repo module 01 — Python language model

## Module 1 — The Python Language Model & Object Orientation
**Level:** Tier A → B · **Covers:** mutability/immutability, built-in data structures, dunder methods, OOP vs. procedural vs. scripting, and building accurate self-calibration.

### Tier 1 — Primary textbooks
- **Luciano Ramalho, *Fluent Python*, 2nd ed. (O'Reilly, 2022).** The definitive treatment of the Python data model — mutable vs. immutable sequences, hashability, and the special ("dunder") methods (`__init__`, `__new__`, `__call__`, `__hash__`, `__eq__`). This single book closes nearly every Python fundamentals gap.
- **David Beazley, *Python Distilled* (Addison-Wesley, 2021).** Concise, rigorous coverage of objects, the type system, and execution model.
- **Brett Slatkin, *Effective Python*, 2nd ed. (Addison-Wesley, 2019).** 90 idioms that build correct mental models; pairs well with calibration-focused assessment.

### Tier 2 — Academic / foundational
- **Robert W. Sebesta, *Concepts of Programming Languages*, 11th+ ed. (Pearson).** Grounds the paradigm question — what *imperative/procedural*, *object-oriented*, and *scripting* actually mean as language paradigms, language-agnostically.
- **Abelson, Sussman & Sussman, *Structure and Interpretation of Computer Programs*, 2nd ed. (MIT Press, 1996; free online).** First-principles treatment of state, mutation, and abstraction — directly addresses *why* mutability matters, not just which types are mutable.

### Tier 3 — Industry / official
- **The Python Language Reference — "Data Model"** (docs.python.org). The *primary source* for special methods and the mutable/immutable distinction.
- **CPython `array`, `collections`, `dataclasses` module docs.** Settles the "does Python have an array?" question (yes — the `array` module and, in practice, `list`/NumPy `ndarray`).
- **Anthony Shaw, *CPython Internals* (Real Python, 2021).** How objects, reference counting, and immutability are implemented under the interpreter.

---

## External — DSA (parallel with repo 02 SQL)

## Module 2 — Data Structures, Algorithms & Problem Decomposition
**Level:** Tier A · **Covers:** loop invariants, indexing arithmetic, complexity reasoning, and decomposing a problem before coding (e.g. deriving a relation like `2·row − 1` for a pattern before writing the loop).

### Tier 1 — Primary textbooks
- **Cormen, Leiserson, Rivest & Stein (CLRS), *Introduction to Algorithms*, 4th ed. (MIT Press, 2022).** The canonical reference; the loop-invariant methodology in Ch. 2 is the core technique for reasoning about correctness.
- **Steven Skiena, *The Algorithm Design Manual*, 3rd ed. (Springer, 2020).** The most *practical* DSA text — strong on how to reason toward a solution under time pressure.
- **Sedgewick & Wayne, *Algorithms*, 4th ed. (Addison-Wesley, 2011).** Excellent implementations and empirical complexity analysis.

### Tier 2 — Academic / foundational
- **George Pólya, *How to Solve It* (Princeton, 1945; still in print).** Problem-decomposition heuristics — the antidote to jumping to code before establishing the invariant.
- **Knuth, *The Art of Computer Programming*, Vols. 1–3 (Addison-Wesley).** Reference-grade rigor for complexity and combinatorial reasoning.

### Tier 3 — Industry / practice
- **NeetCode / LeetCode patterns, and *Cracking the Coding Interview* (McDowell, 6th ed.).** Deliberate practice on the standard interview format.
- **Python `timeit` / `cProfile` docs.** Make Big-O reasoning empirical, reinforcing calibration.

---

## Repo module 02 — SQL

## Module 3 — Relational Databases, SQL & Query Optimization
**Level:** Tier A → C · **Covers:** views, CTEs/`WITH`, temporary vs. virtual tables, and cost-based query tuning.

### Tier 1 — Primary textbooks
- **Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed. (McGraw-Hill, 2019).** Covers the relational model, **views**, **recursive CTEs**, and the relational algebra beneath SQL.
- **Garcia-Molina, Ullman & Widom, *Database Systems: The Complete Book*, 2nd ed. (Pearson, 2008).** The "Stanford" book; outstanding on query processing and optimization.
- **Ramakrishnan & Gehrke, *Database Management Systems*, 3rd ed. (McGraw-Hill, 2003).** Strong systems-level treatment.

### Tier 2 — Academic / foundational
- **E. F. Codd, "A Relational Model of Data for Large Shared Data Banks," *Communications of the ACM* 13(6), 1970.** The founding paper of the entire field; defines what a *view* is in principle.
- **Selinger et al., "Access Path Selection in a Relational Database Management System," *SIGMOD* 1979.** The System R cost-based optimizer — the theoretical basis of modern query tuning.
- **Chamberlin & Boyce, "SEQUEL: A Structured English Query Language," *SIGMOD* 1974.** Origin of SQL itself.

### Tier 3 — Industry / official
- **PostgreSQL documentation — "WITH Queries (CTEs)," "CREATE VIEW," and "Using EXPLAIN."** Authoritative, free, and the engine used by this repo's labs.
- **Markus Winand, *Use The Index, Luke!* (use-the-index-luke.com) and *SQL Performance Explained*.** The best practitioner resource on indexing and tuning.
- **Oracle Database SQL Language Reference — views, CTEs (`WITH`), materialized views.** A common enterprise dialect for comparison.

---

## Repo module 04 — Spark internals

## Module 4 — Distributed Systems & Apache Spark Internals  *(the keystone module)*
**Level:** Tier B → C · **Covers:** the single largest and most role-critical area — driver/executor architecture, the `spark-submit` lifecycle, DAG → jobs/stages/tasks, logical→physical plans, the Catalyst optimizer, cluster managers, executor *and* driver OOM, partitioning, skew, shuffle, and tuning at real scale.

### Tier 1 — Primary textbooks
- **Martin Kleppmann & Chris Riccomini, *Designing Data-Intensive Applications*, 2nd ed. (O'Reilly, Feb 2026).** The single best book for the *why* beneath distributed data systems — partitioning, replication, batch vs. stream, fault tolerance. Thoroughly revised from the 2017 first edition (~650 pages).
- **Holden Karau & Rachel Warren, *High Performance Spark*, 2nd ed. (O'Reilly, updated for Apache Spark 4).** Deep dives into the DAG scheduler, task execution, memory management, partitioning, and shuffle — i.e., *exactly* how to diagnose executor/driver OOM and a multi-hour job. The most targeted text for Spark performance.
- **Damji, Wenig, Das & Lee, *Learning Spark*, 2nd ed. (O'Reilly/Databricks, 2020)** and **Chambers & Zaharia, *Spark: The Definitive Guide* (O'Reilly, 2018).** The execution model, Structured APIs, and the driver/executor cluster picture.
- **Tanenbaum & Van Steen, *Distributed Systems*, 4th ed. (2023; free PDF at distributed-systems.net).** The general distributed-systems foundation under all of the above.

### Tier 2 — Academic literature (the canon)
- **Dean & Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters," *OSDI* 2004.** The origin of the whole batch-processing lineage.
- **Zaharia et al., "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing," *NSDI* 2012.** *The* Spark paper — defines RDDs, lineage, and the driver/executor model. Required reading for anyone working in PySpark.
- **Armbrust et al., "Spark SQL: Relational Data Processing in Spark," *SIGMOD* 2015.** Defines the **Catalyst optimizer** and the logical→physical plan pipeline.
- **Ghemawat, Gobioff & Leung, "The Google File System," *SOSP* 2003.** The ancestor of HDFS.
- **Dean & Barroso, "The Tail at Scale," *CACM* 2013.** Builds latency-and-scale intuition (gigabytes vs. terabytes).

### Tier 3 — Industry / official
- **Apache Spark documentation — "Cluster Mode Overview," "Submitting Applications," and the "Tuning Guide."** The authoritative source for the `spark-submit` lifecycle, driver vs. executor roles, and memory configuration (`spark.executor.memory`, `spark.driver.memory`, `spark.sql.shuffle.partitions`).
- **Jacek Laskowski, *The Internals of Apache Spark* and *The Internals of Spark SQL* (free gitbooks).** Line-by-line depth on the scheduler, stages/tasks, and Catalyst.
- **Databricks Engineering Blog — Catalyst, Tungsten, Adaptive Query Execution (AQE), and Photon.** How modern Spark actually optimizes and where skew/spill come from.
- **Hands-on: the Spark UI and `df.explain(mode="formatted")`.** Reading real DAGs and physical plans is the fastest cure for a notebook-local mental model.

---

## Repo modules 03 and 05 — BI and warehousing

## Module 5 — Data Warehousing, Dimensional Modeling & BI
**Level:** Tier B · **Covers:** dimensions vs. measures (Tableau/Power BI), star schemas, facts vs. dimensions, slowly changing dimensions, and the lakehouse framing.

### Tier 1 — Primary textbooks
- **Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit*, 3rd ed. (Wiley, 2013).** The source of the **dimension/measure** vocabulary — Tableau's "dimensions and measures" are Kimball's dimensions and facts. Essential.
- **Joe Reis & Matt Housley, *Fundamentals of Data Engineering* (O'Reilly, 2022).** The modern, lakehouse-era framing — ingestion, transformation, serving, governance — that connects warehousing to medallion architecture.

### Tier 2 — Academic literature
- **Chaudhuri & Dayal, "An Overview of Data Warehousing and OLAP Technology," *SIGMOD Record* 1997.** The classic survey of star schemas, facts, and dimensions.
- **Gray et al., "Data Cube: A Relational Aggregation Operator…," *Data Mining and Knowledge Discovery* 1(1), 1997.** Formalizes aggregation/measures across dimensions.

### Tier 3 — Industry / official
- **Tableau documentation — "Dimensions and Measures" (and green vs. blue pills).** The authoritative answer to a question many practitioners get wrong.
- **dbt and Delta Lake documentation.** Modern dimensional modeling and the medallion architecture, formally.

---

## Repo module 06 — Kafka

## Module 6 — Event Streaming & Kafka
**Level:** Tier B → C · **Covers:** Kafka (common in production data platforms) and the watermark/window/trigger model that underlies stream processing (e.g. Apache Beam / Dataflow and Spark Structured Streaming).

### Tier 1 — Primary textbooks
- **Narkhede, Shapira & Palino, *Kafka: The Definitive Guide*, 2nd ed. (O'Reilly, 2021).** Architecture, partitions, consumer groups, exactly-once semantics.
- **Akidau, Chernyak & Lax, *Streaming Systems* (O'Reilly, 2018).** Event time vs. processing time, windows, watermarks, triggers — the conceptual core of all modern stream processing.

### Tier 2 — Academic literature
- **Kreps, Narkhede & Rao, "Kafka: A Distributed Messaging System for Log Processing," *NetDB* 2011.** The origin paper.
- **Akidau et al., "The Dataflow Model…," *PVLDB* 8(12), 2015.** The theoretical basis of Beam/Dataflow watermarks and triggers.
- **Zaharia et al., "Discretized Streams," *SOSP* 2013** and **"Structured Streaming," *SIGMOD* 2018.** Spark's streaming model.

### Tier 3 — Industry / official
- **Confluent Developer / Apache Kafka documentation.** Authoritative, with hands-on tutorials.
- **Jay Kreps, "The Log: What every software engineer should know about real-time data's unifying abstraction" (LinkedIn Engineering).** Seminal industry essay.

---

## Optional — Java OOP (not in this repo)

## Module 7 — Object-Oriented Design & Design Patterns (Java/J2EE track)
**Level:** Tier A → B · **Covers:** Core Java/J2EE + OOP + design patterns, for roles on a JVM stack; reinforces the OOP concepts from Module 1.

### Tier 1 — Primary textbooks
- **Joshua Bloch, *Effective Java*, 3rd ed. (Addison-Wesley, 2018).** The definitive Java OOP text — immutability, equals/hashCode, builders, generics.
- **Gamma, Helm, Johnson & Vlissides (Gang of Four), *Design Patterns: Elements of Reusable Object-Oriented Software* (Addison-Wesley, 1994).** The canonical patterns reference.
- **Freeman & Robson, *Head First Design Patterns*, 2nd ed. (O'Reilly, 2020).** The most accessible on-ramp to GoF patterns.

### Tier 2 — Academic / foundational
- **Liskov & Wing, "A Behavioral Notion of Subtyping," *ACM TOPLAS* 16(6), 1994.** The Liskov Substitution Principle — the formal core of correct OOP design.

### Tier 3 — Industry
- **Oracle Java Tutorials and the Jakarta EE (J2EE successor) documentation.** Current, authoritative.
- **Martin Fowler, *Refactoring*, 2nd ed. (2018) and martinfowler.com.** Patterns and design in living practice.

---

## Repo module 07 — AI-assisted engineering

## Module 8 — AI-Assisted Software Engineering
**Level:** Tier B · **Covers:** working effectively with agentic coding tools (Claude Code, Codex, Copilot, and similar) and the role of a project-memory file (`CLAUDE.md`) in conserving context — increasingly expected in modern engineering roles.

### Tier 1 — Primary text (emerging field; one true textbook so far)
- **Chip Huyen, *AI Engineering* (O'Reilly, 2025).** The leading text on building with foundation models — context management, evaluation, and integrating LLMs into engineering workflows.

### Tier 2 — Research / grey literature
- **Peng et al., "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot" (arXiv, 2023).** Empirical grounding for why firms increasingly require this.
- **The prompt-engineering and agent literature** (e.g., work on chain-of-thought, ReAct-style tool use). Read for the conceptual model of how agentic coding tools reason and call tools.

### Tier 3 — Industry / official
- **Anthropic, "Claude Code: Best practices for agentic coding" (anthropic.com/engineering).** Patterns proven across Anthropic's internal teams.
- **Claude Code documentation — "Manage Claude's Memory" / `CLAUDE.md`.** `CLAUDE.md` is a special file automatically pulled into context at the start of a session, used to document build/test commands, conventions, and project rules. Effective files are kept tight (practitioner consensus puts the high-signal range well under ~200 lines) so they conserve context and tokens rather than competing with the actual task.
- **Anthropic, "Building effective agents" and the context-engineering posts.** How to structure agent workflows beyond a single UI.

---

## Repo module 08 — Lakehouse and medallion

## Module 9 — Capstone: Data Governance at Scale
**Level:** Tier C · **Covers:** integrating the prior modules into a governed, distributed, streaming medallion pipeline with measured performance tuning — lineage, data quality, stewardship, and table formats at scale.

### Tier 1 — Primary references
- **DAMA International, *DAMA-DMBOK: Data Management Body of Knowledge*, 2nd ed. (Technics, 2017).** The canonical governance reference formalizing lineage, quality, and stewardship.
- **Reis & Housley, *Fundamentals of Data Engineering* (carried from Module 5)** for the end-to-end lifecycle.

### Tier 2 — Standards / regulatory
- **BCBS 239, "Principles for effective risk data aggregation and risk reporting" (Basel Committee, 2013).** A widely-cited standard; reading the source formalizes lineage and aggregation principles for regulated (e.g. banking) contexts.

### Tier 3 — Industry
- **Lakehouse and data-catalog documentation (e.g. Unity Catalog); the Delta Lake and Apache Iceberg specifications.** Governed table formats at scale — Parquet/ORC/Avro, ACID, time travel.

---

## Repo module 09 — Cloud & object storage portability

## Module 10 — Cloud Data Platforms & Storage Portability  *(cross-cutting)*
**Level:** Tier B · **Covers:** the *portable* layer of cloud data engineering — object storage and a single storage abstraction — across AWS, GCP, and Azure, using **local emulators** (LocalStack, fake-gcs-server, Azurite) so it honors the repo's "local Docker only — no cloud APIs, no spend" rule. Most data-engineering roles assume at least one cloud; this module builds the cross-cloud mental model rather than tying you to one vendor.

### Tier 1 — Primary references
- **Reis & Housley, *Fundamentals of Data Engineering* (carried from Module 5).** The cloud-native data lifecycle, storage abstractions, and the storage/compute decoupling object storage enables.
- **Provider architecture-center docs** — AWS Well-Architected, Google Cloud Architecture Framework, Azure Architecture Center.

### Tier 2 — Foundational
- **Ghemawat, Gobioff & Leung, "The Google File System," *SOSP* 2003** (carried from Module 4) — the lineage from distributed file systems to object stores.
- **DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store," *SOSP* 2007.** The consistency/availability tradeoffs underlying cloud object stores.

### Tier 3 — Industry / official
- **fsspec and the Arrow/Parquet filesystem docs.** The single-interface, swap-by-config pattern this module is built around.
- **S3 / Cloud Storage / Azure Blob (ADLS Gen2) documentation**, and the **LocalStack / fake-gcs-server / Azurite** project docs for the emulators.

---

## Repo module 10 — Orchestration, dbt and the data catalog

## Module 11 — Transformation, Orchestration, Data Quality & Cataloging  *(the ELT/operations layer)*
**Level:** Tier B · **Covers:** the layer that turns raw data into trustworthy, documented tables on a schedule — **dbt** transformations, **executable data-quality tests** (validation and referential reconciliation), **data catalogs and metadata/lineage**, pipeline orchestration (Airflow/Dagster) and CI/CD (GitLab/GitHub Actions), and warehouse portability (BigQuery and peers). Runs locally on DuckDB.

### Tier 1 — Primary references
- **Joe Reis & Matt Housley, *Fundamentals of Data Engineering* (O'Reilly, 2022).** The transformation/serving stages of the lifecycle and the role of orchestration and metadata.
- **dbt documentation — models, sources, tests, and `docs generate`.** The reference for ELT-in-SQL, the testing framework, and the manifest/catalog metadata that powers lineage.

### Tier 2 — Foundational
- **Halevy, Korn et al., "Goods: Organizing Google's Datasets," *SIGMOD* 2016.** Enterprise-scale dataset cataloging and metadata management.
- **The data-contract / data-quality literature** (e.g. Great Expectations docs; "data as a product" writing). Why validation and reconciliation belong *in* the pipeline.

### Tier 3 — Industry / official
- **Airflow and Dagster documentation.** DAG scheduling, retries, and software-defined assets — how the ordered steps in `run_pipeline.py` run in production.
- **GitLab CI/CD and GitHub Actions documentation.** Reading and writing pipeline YAML (`stages`, `jobs`, `needs`/`dependencies`); this repo ships both as working examples.
- **BigQuery documentation — partitioning, clustering, and cost controls** (and the equivalent for Snowflake/Redshift/Databricks). The same dbt SQL runs on each by swapping the adapter; the differences are physical design and the bytes-scanned cost model.
- **Data-catalog platforms** — dbt docs, DataHub, OpenMetadata, Unity Catalog. What ingests dbt's metadata to deliver discoverability and governance.

---

## Identified concept gaps (coverage audit)

A pass over the modules plus typical senior job requirements surfaces these. Status reflects this repository.

- **Cloud / multi-cloud** — **covered** by repo module 09 (object storage portability across AWS/GCP/Azure on local emulators).
- **Dimensional modeling depth** (SCD2, snowflake, OLAP cube) — **covered** by repo module 05's `dimensional_modeling.py` and `olap_analytics.py`.
- **Orchestration & transformation frameworks** (Airflow / Dagster, **dbt**) — **covered** by repo module 10 (`run_pipeline.py` + dbt project).
- **Data quality / validation / reconciliation** — **covered** by repo module 10's dbt `not_null`/`unique`/`relationships` tests (and medallion `WHERE` filters in 08).
- **Data catalog & metadata management** — **covered** by repo module 10 (`dbt docs generate` → manifest/catalog, lineage graph).
- **CI/CD** — **covered**: `.github/workflows/ci.yml` runs `make check`; `.gitlab-ci.yml` mirrors it for pipeline-YAML literacy.
- **Cloud warehouse design** (BigQuery partitioning/clustering, cost model) — **covered conceptually** in module 10 `concepts.md`; the same dbt SQL runs on BigQuery by swapping the adapter.
- **Governance & compliance** (PIPEDA / HIPAA / GDPR / BCBS 239, de-identification) — **covered** in module 08 `governance_compliance.md`.
- **Stakeholder engagement & analytical communication** — **covered** in module 03 `notes/stakeholder_engagement.md`.
- **Table formats hands-on** (Delta / Iceberg ACID, time travel) — *partial.* Module 08 covers the concepts and a Parquet medallion; a real transactional table-format lab (e.g. delta-rs or pyiceberg, local) would close it.

### Where specific job-requirement themes are exercised

| Requirement theme | Where in the stack |
|---|---|
| SQL for data validation & reconciliation | repo 02 (views/CTEs/EXPLAIN) + repo 10 (dbt tests, referential `relationships`) |
| Large datasets (100s of GB structured, TBs of documents) | repo 04 (Spark at scale, `make seed-large`) + repo 10 `concepts.md` (same pattern at any size) |
| Many object schemas & complex relationships | repo 02 (recursive CTE / joins) + repo 10 (sources, `ref()`, relationships tests, lineage) |
| GitLab CI/CD pipeline-YAML literacy | `.gitlab-ci.yml` + `.github/workflows/ci.yml` + repo 10 `concepts.md` |
| BigQuery (SQL, table design, partitioning, optimization) | repo 10 `concepts.md` (adapter swap; partition/cluster/cost) + repo 05 (dimensional design) |
| Healthcare data compliance (PIPEDA, HIPAA) | repo 08 `governance_compliance.md` |
| Data catalog tools & metadata management | repo 10 (dbt manifest/catalog, lineage) |
| Stakeholder engagement & analytical skills | repo 03 `notes/stakeholder_engagement.md` |

---

## 3. Suggested sequencing & priority

For learners targeting **PySpark / big-data engineering** roles, sequence to hit the keystone fastest while repairing foundations in parallel (repo module numbers):

1. **Weeks 1–4 (parallel):** Repo **01** (Python) + repo **02** (SQL: views/CTEs) — quickest wins; build calibration early. Study **DSA** (external) in parallel with 02.
2. **Weeks 3–10 (core):** Repo **04** (Spark internals) — largest investment; keep DSA practice alongside for plan-reading and complexity reasoning.
3. **Weeks 8–12:** Repo **03** (BI) + repo **05** (warehousing) + repo **06** (Kafka) + repo **09** (cloud) + repo **10** (dbt / orchestration / catalog).
4. **Throughout:** Repo **07** (AI-assisted engineering) — adopt a `CLAUDE.md` on day one.
5. **Optional / role-dependent:** Curriculum Module 7 (Java/OOP) for JVM-stack roles.
6. **Finish:** Repo **08** (lakehouse / medallion capstone, incl. governance & compliance) — integrative, portfolio-grade.

**One closing note on assessment.** Because confidence should track competence, grade every module on a live artifact, not recall: read and explain a real physical plan, reproduce and fix an executor *and* a driver OOM, write a recursive CTE against a real schema, run an object-store roundtrip across three clouds, and ship a `CLAUDE.md` that demonstrably cuts a project's token use. Skill is earned against the machine, not asserted.
