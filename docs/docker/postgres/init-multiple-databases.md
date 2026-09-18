# `docker/postgres/init-multiple-databases.sh`

Executed by the official PostgreSQL image only when a new database volume is initialized.

Creates three role/database pairs:

```text
Airflow metadata
Celery results
YouTube ELT warehouse
```

After the databases exist, it runs `create-elt-tables.sql` against the ELT database and assigns table ownership to the ELT user.

Important: Docker's PostgreSQL initialization directory runs only for an empty data volume. Existing volumes are not reinitialized.
