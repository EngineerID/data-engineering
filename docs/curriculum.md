# Foundations of Big Data Engineering — A Curriculum to Close the Gap

*A competency-mapped course design with tiered reading lists (canonical textbooks → cited academic literature → industry/practitioner sources), built from the gaps surfaced in two technical interviews and the three attached job descriptions (Citi "PySpark Big Data Senior Developer – VP," Citi "Fullstack Big Data Developer," and the Job Bank "Database Analyst").*

Hands-on labs in this repository: [`docs/modules.md`](modules.md) · setup: [`docs/setup.md`](setup.md).

---

## Repo alignment (modules 01–08)

This repo implements eight numbered folders under `modules/`. Curriculum sections below retain original numbering where noted.

- **Repo 01** [`01_python_model`](../modules/01_python_model/) — Python language model (curriculum Module 1)
- **DSA** — Data structures & algorithms (curriculum Module 2) — **separate repository**; study in parallel with repo 02
- **Repo 02** [`02_sql_relational`](../modules/02_sql_relational/) — SQL (curriculum Module 3)
- **Repo 03** [`03_bi_tools`](../modules/03_bi_tools/) — BI tools (split from curriculum Module 5)
- **Repo 04** [`04_spark_internals`](../modules/04_spark_internals/) — Spark internals (curriculum Module 4)
- **Repo 05** [`05_warehousing`](../modules/05_warehousing/) — Warehousing / Kimball (curriculum Module 5, warehousing only)
- **Repo 06** [`06_streaming_kafka`](../modules/06_streaming_kafka/) — Kafka (curriculum Module 6)
- **Repo 07** [`07_ai_assisted_dev`](../modules/07_ai_assisted_dev/) — AI-assisted engineering (curriculum Module 8)
- **Repo 08** [`08_lakehouse_medallion`](../modules/08_lakehouse_medallion/) — Lakehouse, Delta, medallion (reframes curriculum Module 9 capstone; portable concepts, not a Databricks course)
- **Curriculum Module 7** (Java OOP / design patterns) — optional; Fullstack JD only; not a repo folder

Optional local textbook extracts: `references/` (gitignored). Do not commit long verbatim paste from publishers.

---

## 1. Design rationale: what the interviews actually diagnose

The candidate presents a genuine and uncommon strength at the **applied / data-governance layer** — medallion (Bronze/Silver/Gold) architecture, row-level lineage and provenance, GDPR pseudonymization, BCBS 239 compliance, statistical validation (ADF, Hausman, Breusch–Pagan, bootstrapping), and end-to-end platform delivery on GCP + Databricks. This is real and should be preserved.

The gap is **vertical**: the systems-internals and first-principles layer *underneath* those platform skills is thin. Concretely, across the two transcripts:

- **Python language model** — Could not cleanly define mutability/immutability; could not name 3 mutable types + 5 methods each; unsure whether Python has an `array` type; did not know dunder methods (`__init__`, `__new__`, `__call__`); hedged on OOP vs. procedural vs. scripting. Self-rated **10/10**; fundamentals not solid.
- **Spark internals** — Could not explain the `spark-submit` lifecycle (driver, executors, DAG, logical→physical plan, Catalyst, jobs/stages/tasks, YARN); described PySpark as "a library — create a session, close a session"; could not diagnose executor OOM beyond "break it up / add resources"; did not know what the driver is; never seen driver OOM; no experience past ~5 GB. Self-rated **8/10**; mental model is notebook-local, not cluster-distributed.
- **Relational databases / SQL** — Did not know what a **VIEW** is; did not know **CTEs** / the `WITH` clause; limited temp-table experience. Claims query-tuning experience (Postgres/MySQL).
- **Dimensional modeling / BI** — Did not know **dimensions vs. measures** in Tableau. Claims Tableau/Power BI dashboard experience.
- **Algorithms / DSA** — Struggled to decompose the star-pyramid pattern; confused rows vs. characters; needed heavy guidance to reach `2·row − 1`; weak loop-invariant and complexity reasoning.
- **AI-assisted development** — Did not know the purpose of `CLAUDE.md` or how it conserves context/tokens; had only used agents via a GitHub UI. **Mandatory** requirement in the PySpark JD.

**Two design principles follow:**

1. **Teach the internals first.** Every module forces the layer beneath the API to the surface — the data model beneath Python syntax, the execution model beneath the DataFrame, the relational algebra beneath SQL. That is exactly the layer senior big-data interviews probe and the layer the candidate consistently lacked.
2. **Target calibration explicitly.** Assessment is performance-based (debug a real OOM, read a physical plan, prove a loop invariant) rather than recall-based, so confidence tracks competence.

---

## 2. Program architecture

The gaps span three depths, so the program is tiered. A practicing engineer with this profile would run **Tier A + Tier B** as an intensive bridge (≈2 academic terms); **Tier C** is the graduate/research extension for those moving toward architecture or a thesis.

- **Tier A — Undergraduate foundations** *(closes the "fundamentals" gaps: mutability, views, CTEs, OOP, DSA reasoning).*
- **Tier B — Professional / graduate core** *(the heart: distributed systems and Spark internals, warehousing, streaming, AI-assisted engineering — directly aligned to the JDs).*
- **Tier C — Research / frontier** *(query optimization theory, consistency and consensus, streaming semantics — PhD-level and architecture-track).*

Each module below lists **Tier 1 primary textbooks**, **Tier 2 academic literature** (well-cited, with venue), and **Tier 3 industry/practitioner sources** (official docs, engineering blogs, deep-dive references).

---

## Repo module 01 — Python language model

## Module 1 — The Python Language Model & Object Orientation
**Level:** Tier A → B · **Closes:** mutability/immutability, built-in data structures, dunder methods, OOP vs. procedural vs. scripting, the 10/10 calibration problem.

### Tier 1 — Primary textbooks
- **Luciano Ramalho, *Fluent Python*, 2nd ed. (O'Reilly, 2022).** The definitive treatment of the Python data model — mutable vs. immutable sequences, hashability, and the special ("dunder") methods (`__init__`, `__new__`, `__call__`, `__hash__`, `__eq__`). This single book closes nearly every Python gap in the interview.
- **David Beazley, *Python Distilled* (Addison-Wesley, 2021).** Concise, rigorous coverage of objects, the type system, and execution model.
- **Brett Slatkin, *Effective Python*, 2nd ed. (Addison-Wesley, 2019).** 90 idioms that build correct mental models; pairs well with calibration-focused assessment.

### Tier 2 — Academic / foundational
- **Robert W. Sebesta, *Concepts of Programming Languages*, 11th+ ed. (Pearson).** Grounds the paradigm question the candidate fumbled — what *imperative/procedural*, *object-oriented*, and *scripting* actually mean as language paradigms, language-agnostically.
- **Abelson, Sussman & Sussman, *Structure and Interpretation of Computer Programs*, 2nd ed. (MIT Press, 1996; free online).** First-principles treatment of state, mutation, and abstraction — directly addresses *why* mutability matters, not just which types are mutable.

### Tier 3 — Industry / official
- **The Python Language Reference — "Data Model"** (docs.python.org). The *primary source* for special methods and the mutable/immutable distinction; the candidate's answer should have come from here.
- **CPython `array`, `collections`, `dataclasses` module docs.** Settles the "does Python have an array?" question (yes — the `array` module and, in practice, `list`/NumPy `ndarray`).
- **Anthony Shaw, *CPython Internals* (Real Python, 2021).** How objects, reference counting, and immutability are implemented under the interpreter.

---

## External — DSA (parallel with repo 02 SQL)

## Module 2 — Data Structures, Algorithms & Problem Decomposition
**Level:** Tier A · **Closes:** the star-pyramid struggle — loop invariants, indexing arithmetic, complexity reasoning, decomposing a problem before coding.

### Tier 1 — Primary textbooks
- **Cormen, Leiserson, Rivest & Stein (CLRS), *Introduction to Algorithms*, 4th ed. (MIT Press, 2022).** The canonical reference; the loop-invariant methodology in Ch. 2 is precisely what was missing when deriving the `2·row − 1` relation.
- **Steven Skiena, *The Algorithm Design Manual*, 3rd ed. (Springer, 2020).** The most *practical* DSA text — strong on how to reason toward a solution under interview-style pressure.
- **Sedgewick & Wayne, *Algorithms*, 4th ed. (Addison-Wesley, 2011).** Excellent implementations and empirical complexity analysis.

### Tier 2 — Academic / foundational
- **George Pólya, *How to Solve It* (Princeton, 1945; still in print).** Problem-decomposition heuristics — directly addresses jumping to code before establishing the row/character invariant.
- **Knuth, *The Art of Computer Programming*, Vols. 1–3 (Addison-Wesley).** Reference-grade rigor for complexity and combinatorial reasoning.

### Tier 3 — Industry / practice
- **NeetCode / LeetCode patterns, and *Cracking the Coding Interview* (McDowell, 6th ed.).** Deliberate practice on exactly the interview format that exposed the gap.
- **Python `timeit` / `cProfile` docs.** Make Big-O reasoning empirical, reinforcing calibration.

---

## Repo module 02 — SQL

## Module 3 — Relational Databases, SQL & Query Optimization
**Level:** Tier A → C · **Closes:** views, CTEs/`WITH`, temporary vs. virtual tables, and deepens the query-tuning the candidate claimed.

### Tier 1 — Primary textbooks
- **Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed. (McGraw-Hill, 2019).** Covers the relational model, **views**, **recursive CTEs**, and the relational algebra beneath SQL — the precise concepts missed.
- **Garcia-Molina, Ullman & Widom, *Database Systems: The Complete Book*, 2nd ed. (Pearson, 2008).** The "Stanford" book; outstanding on query processing and optimization.
- **Ramakrishnan & Gehrke, *Database Management Systems*, 3rd ed. (McGraw-Hill, 2003).** Strong systems-level treatment.

### Tier 2 — Academic / foundational
- **E. F. Codd, "A Relational Model of Data for Large Shared Data Banks," *Communications of the ACM* 13(6), 1970.** The founding paper of the entire field; defines what a *view* is in principle.
- **Selinger et al., "Access Path Selection in a Relational Database Management System," *SIGMOD* 1979.** The System R cost-based optimizer — the theoretical basis for the "query tuning" the candidate does in practice.
- **Chamberlin & Boyce, "SEQUEL: A Structured English Query Language," *SIGMOD* 1974.** Origin of SQL itself.

### Tier 3 — Industry / official
- **PostgreSQL documentation — "WITH Queries (CTEs)," "CREATE VIEW," and "Using EXPLAIN."** Authoritative, free, and matches the candidate's Postgres background.
- **Markus Winand, *Use The Index, Luke!* (use-the-index-luke.com) and *SQL Performance Explained*.** The best practitioner resource on indexing and tuning.
- **Oracle Database SQL Language Reference — views, CTEs (`WITH`), materialized views.** Aligned to the Oracle exposure in the second interview.

---

## Repo module 04 — Spark internals

## Module 4 — Distributed Systems & Apache Spark Internals  *(the keystone module)*
**Level:** Tier B → C · **Closes:** the single largest and most JD-critical gap — driver/executor architecture, the `spark-submit` lifecycle, DAG → jobs/stages/tasks, logical→physical plans, the Catalyst optimizer, YARN, executor *and* driver OOM, partitioning, skew, shuffle, and tuning at real scale.

### Tier 1 — Primary textbooks
- **Martin Kleppmann & Chris Riccomini, *Designing Data-Intensive Applications*, 2nd ed. (O'Reilly, Feb 2026).** The single best book for the *why* beneath distributed data systems — partitioning, replication, batch vs. stream, fault tolerance. Thoroughly revised from the 2017 first edition (~650 pages).
- **Holden Karau & Rachel Warren, *High Performance Spark*, 2nd ed. (O'Reilly, updated for Apache Spark 4).** Deep dives into the DAG scheduler, task execution, memory management, partitioning, and shuffle — i.e., *exactly* how to diagnose executor/driver OOM and a 5-hour job. This is the most targeted text for the Spark gaps.
- **Damji, Wenig, Das & Lee, *Learning Spark*, 2nd ed. (O'Reilly/Databricks, 2020)** and **Chambers & Zaharia, *Spark: The Definitive Guide* (O'Reilly, 2018).** The execution model, Structured APIs, and the driver/executor cluster picture the candidate was missing.
- **Tanenbaum & Van Steen, *Distributed Systems*, 4th ed. (2023; free PDF at distributed-systems.net).** The general distributed-systems foundation under all of the above.

### Tier 2 — Academic literature (the canon)
- **Dean & Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters," *OSDI* 2004.** The origin of the whole batch-processing lineage.
- **Zaharia et al., "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing," *NSDI* 2012.** *The* Spark paper — defines RDDs, lineage, and the driver/executor model. Required reading for anyone claiming 8/10 on PySpark.
- **Armbrust et al., "Spark SQL: Relational Data Processing in Spark," *SIGMOD* 2015.** Defines the **Catalyst optimizer** and the logical→physical plan pipeline — the precise architecture the candidate could not describe.
- **Ghemawat, Gobioff & Leung, "The Google File System," *SOSP* 2003.** The ancestor of HDFS (named in the JDs).
- **Dean & Barroso, "The Tail at Scale," *CACM* 2013.** Builds the latency-and-scale intuition the candidate lacked (5 GB vs. terabytes).

### Tier 3 — Industry / official
- **Apache Spark documentation — "Cluster Mode Overview," "Submitting Applications," and the "Tuning Guide."** The authoritative source for the `spark-submit` lifecycle, driver vs. executor roles, and memory configuration (`spark.executor.memory`, `spark.driver.memory`, `spark.sql.shuffle.partitions`).
- **Jacek Laskowski, *The Internals of Apache Spark* and *The Internals of Spark SQL* (free gitbooks).** Line-by-line depth on the scheduler, stages/tasks, and Catalyst.
- **Databricks Engineering Blog — Catalyst, Tungsten, Adaptive Query Execution (AQE), and Photon.** How modern Spark actually optimizes and where skew/spill come from.
- **Hands-on: the Spark UI and `df.explain(mode="formatted")`.** Reading real DAGs and physical plans is the fastest cure for the notebook-local mental model.

---

## Repo modules 03 and 05 — BI and warehousing

## Module 5 — Data Warehousing, Dimensional Modeling & BI
**Level:** Tier B · **Closes:** dimensions vs. measures (Tableau), star schemas, facts vs. dimensions, and the lakehouse the candidate works in but could not formalize.

### Tier 1 — Primary textbooks
- **Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit*, 3rd ed. (Wiley, 2013).** The source of the **dimension/measure** vocabulary the candidate could not define — Tableau's "dimensions and measures" are Kimball's dimensions and facts. Essential.
- **Joe Reis & Matt Housley, *Fundamentals of Data Engineering* (O'Reilly, 2022).** The modern, lakehouse-era framing — ingestion, transformation, serving, governance — that connects warehousing to the candidate's medallion experience.

### Tier 2 — Academic literature
- **Chaudhuri & Dayal, "An Overview of Data Warehousing and OLAP Technology," *SIGMOD Record* 1997.** The classic survey of star schemas, facts, and dimensions.
- **Gray et al., "Data Cube: A Relational Aggregation Operator…," *Data Mining and Knowledge Discovery* 1(1), 1997.** Formalizes aggregation/measures across dimensions.

### Tier 3 — Industry / official
- **Tableau documentation — "Dimensions and Measures" (and green vs. blue pills).** The direct, authoritative answer to the question that was missed.
- **dbt and Databricks SQL / Delta Lake documentation.** Modern dimensional modeling and the medallion architecture, formally.

---

## Repo module 06 — Kafka

## Module 6 — Event Streaming & Kafka
**Level:** Tier B → C · **Closes:** Kafka (mandatory in the PySpark JD) and formalizes the watermark/window/trigger work the candidate already did in Apache Beam — a strength to reinforce.

### Tier 1 — Primary textbooks
- **Narkhede, Shapira & Palino, *Kafka: The Definitive Guide*, 2nd ed. (O'Reilly, 2021).** Architecture, partitions, consumer groups, exactly-once semantics.
- **Akidau, Chernyak & Lax, *Streaming Systems* (O'Reilly, 2018).** Event time vs. processing time, windows, watermarks, triggers — directly maps to the candidate's stated Beam/Dataflow experience.

### Tier 2 — Academic literature
- **Kreps, Narkhede & Rao, "Kafka: A Distributed Messaging System for Log Processing," *NetDB* 2011.** The origin paper.
- **Akidau et al., "The Dataflow Model…," *PVLDB* 8(12), 2015.** The theoretical basis of Beam/Dataflow watermarks and triggers — connects research to the candidate's production work.
- **Zaharia et al., "Discretized Streams," *SOSP* 2013** and **"Structured Streaming," *SIGMOD* 2018.** Spark's streaming model.

### Tier 3 — Industry / official
- **Confluent Developer / Apache Kafka documentation.** Authoritative, with hands-on tutorials.
- **Jay Kreps, "The Log: What every software engineer should know about real-time data's unifying abstraction" (LinkedIn Engineering).** Seminal industry essay.

---

## Optional — Java OOP (not in this repo)

## Module 7 — Object-Oriented Design & Design Patterns (Java/J2EE track)
**Level:** Tier A → B · **Closes:** the Core Java/J2EE + OOP + Design Patterns requirement in the Fullstack JD, and reinforces the OOP concepts the candidate hedged on in Python.

### Tier 1 — Primary textbooks
- **Joshua Bloch, *Effective Java*, 3rd ed. (Addison-Wesley, 2018).** The definitive Java OOP text — immutability, equals/hashCode, builders, generics.
- **Gamma, Helm, Johnson & Vlissides (Gang of Four), *Design Patterns: Elements of Reusable Object-Oriented Software* (Addison-Wesley, 1994).** The canonical patterns reference named in the JD.
- **Freeman & Robson, *Head First Design Patterns*, 2nd ed. (O'Reilly, 2020).** The most accessible on-ramp to GoF patterns.

### Tier 2 — Academic / foundational
- **Liskov & Wing, "A Behavioral Notion of Subtyping," *ACM TOPLAS* 16(6), 1994.** The Liskov Substitution Principle — the formal core of correct OOP design.

### Tier 3 — Industry
- **Oracle Java Tutorials and the Jakarta EE (J2EE successor) documentation.** Current, authoritative.
- **Martin Fowler, *Refactoring*, 2nd ed. (2018) and martinfowler.com.** Patterns and design in living practice.

---

## Repo module 07 — AI-assisted engineering

## Module 8 — AI-Assisted Software Engineering  *(mandatory JD requirement)*
**Level:** Tier B · **Closes:** the `CLAUDE.md` gap and the "AI-first thinker" requirement that the PySpark JD lists as a *mandatory* qualification (Claude Code, Codex, Antigravity, Copilot).

### Tier 1 — Primary text (emerging field; one true textbook so far)
- **Chip Huyen, *AI Engineering* (O'Reilly, 2025).** The leading text on building with foundation models — context management, evaluation, and integrating LLMs into engineering workflows. The strategic frame for the "AI-first" mandate.

### Tier 2 — Research / grey literature
- **Peng et al., "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot" (arXiv, 2023).** Empirical grounding for *why* the firms make this mandatory.
- **The prompt-engineering and agent literature** (e.g., work on chain-of-thought, ReAct-style tool use). Read for the conceptual model of how agentic coding tools reason and call tools.

### Tier 3 — Industry / official  *(the authoritative sources for the exact gap)*
- **Anthropic, "Claude Code: Best practices for agentic coding" (anthropic.com/engineering).** The patterns proven across Anthropic's internal teams; the source the candidate should have known.
- **Claude Code documentation — "Manage Claude's Memory" / `CLAUDE.md`.** `CLAUDE.md` is a special file automatically pulled into context at the start of a session, used to document build/test commands, conventions, and project rules. Effective files are kept tight (practitioner consensus puts the high-signal range well under ~200 lines) so they conserve context and tokens rather than competing with the actual task — precisely the "why" the candidate missed.
- **Anthropic, "Building effective agents" and the context-engineering posts.** How to structure agent workflows beyond a single UI.

---

## Repo module 08 — Lakehouse and medallion

## Module 9 — Capstone: Data Governance at Scale  *(reinforce the strength, add the scale)*
**Level:** Tier C · **Closes:** the one weakness *within* the candidate's strength — governed pipelines were real but only to ~5 GB. The capstone re-platforms a governed medallion pipeline onto genuinely distributed, terabyte-scale, streaming infrastructure with measured performance tuning.

### Tier 1 — Primary references
- **DAMA International, *DAMA-DMBOK: Data Management Body of Knowledge*, 2nd ed. (Technics, 2017).** The canonical governance reference that formalizes the lineage/quality/stewardship work the candidate already does.
- **Reis & Housley, *Fundamentals of Data Engineering* (carried from Module 5)** for the end-to-end lifecycle.

### Tier 2 — Standards / regulatory
- **BCBS 239, "Principles for effective risk data aggregation and risk reporting" (Basel Committee, 2013).** The candidate cites this; reading the source formalizes the lineage and aggregation principles for a banking (Citi) context.

### Tier 3 — Industry
- **Databricks "Lakehouse" and Unity Catalog documentation; the Delta Lake and Apache Iceberg specifications.** Governed table formats at scale — Parquet/ORC/Avro, ACID, time travel.

---

## 3. Suggested sequencing & priority

Given the three JDs all center on **PySpark at scale**, sequence to hit the keystone fastest while repairing foundations in parallel (repo module numbers):

1. **Weeks 1–4 (parallel):** Repo **01** (Python) + repo **02** (SQL: views/CTEs) — quickest wins; fix calibration early. Study **DSA** (external) in parallel with 02.
2. **Weeks 3–10 (core):** Repo **04** (Spark internals) — largest investment; keep DSA practice alongside for plan-reading and complexity reasoning.
3. **Weeks 8–12:** Repo **03** (BI) + repo **05** (warehousing) + repo **06** (Kafka) — named across the JDs.
4. **Throughout:** Repo **07** (AI-assisted engineering) — mandatory JD item; adopt `CLAUDE.md` on day one.
5. **Optional / role-dependent:** Curriculum Module 7 (Java/OOP) for the Fullstack JD only.
6. **Finish:** Repo **08** (lakehouse / medallion capstone) — integrative, portfolio-grade.

**One closing note on assessment.** Because the defining risk was *miscalibration*, grade every module on a live artifact, not recall: read and explain a real physical plan, reproduce and fix an executor *and* a driver OOM, write a recursive CTE against a real schema, and ship a `CLAUDE.md` that demonstrably cuts a project's token use. Confidence should be earned against the machine, not asserted in the interview.
