# Phase 2 - Docker Infrastructure

Start the complete stack:

```bash
docker compose up -d --build
```

Services:

```text
postgres
redis
airflow-init
airflow-webserver
airflow-scheduler
airflow-worker
```

PostgreSQL stores three databases:

```text
airflow_metadata_db  -> Airflow metadata
celery_results_db    -> Celery task results
elt_db               -> YouTube staging/core warehouse
```

Redis is the Celery message broker.

Airflow uses `CeleryExecutor`:

```text
Scheduler -> Redis -> Worker -> Celery result database
```

The Airflow UI is exposed on:

```text
http://localhost:8080
```
