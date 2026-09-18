# `scripts/test_pipeline.sh`

Small command dispatcher for development and verification.

Supported commands:

```text
containers
dag-check
celery
task1
task2
task3
task4
task5
manual
postgres
trigger
runs
files
logs
check
```

`manual` runs all five data phases directly in a temporary Airflow worker container.

`trigger` starts the real `extract_to_staging` DAG. That DAG triggers `staging_to_core` itself.
