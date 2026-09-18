# `docker-compose.yaml`

Defines the full local platform.

Services:

```text
postgres          PostgreSQL 13
redis             Celery broker
airflow-init      database migration + Airflow web user setup
airflow-webserver Airflow UI
airflow-scheduler DAG scheduler
airflow-worker    Celery task worker
```

The Airflow services share the same custom image, environment variables, source mounts and database configuration.

Important mounts:

```text
./dags -> /opt/airflow/dags
./src  -> /opt/airflow/src
./data -> /opt/airflow/data
./logs -> /opt/airflow/logs
```

PostgreSQL uses a named volume so data survives normal container restarts.
