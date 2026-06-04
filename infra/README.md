# Infrastructure (Docker)

Compose file for local labs: [`docker-compose.yml`](docker-compose.yml).

From the **repository root**:

```bash
make up
make down
```

## Services

- **postgres** — `localhost:5432`, db `def_learning`, user `def_user` (module 02)
- **spark-master** + **spark-worker-1/2** — RPC `7077`, UI `8080`, app UI `4040` (module 04)
- **kafka** — KRaft broker `localhost:9092` (module 06)

Repo root is mounted at `/workspace` inside Spark containers so `make spark-submit JOB=modules/...` paths work unchanged.
