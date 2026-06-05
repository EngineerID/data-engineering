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

### Cloud emulators (profile `cloud`, module 09)

Started separately so plain `make up` stays lean:

```bash
make up-cloud     # docker compose --profile cloud up -d localstack fake-gcs azurite
make down-cloud
```

- **localstack** — AWS S3 at `localhost:4566`
- **fake-gcs** — GCS at `localhost:4443`
- **azurite** — Azure Blob at `localhost:10000`

All local-only: no real cloud, no credentials, no spend.

Repo root is mounted at `/workspace` inside Spark containers so `make spark-submit JOB=modules/...` paths work unchanged.
