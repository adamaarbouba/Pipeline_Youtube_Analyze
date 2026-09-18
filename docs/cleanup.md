# Codebase Cleanup

The cleaned project keeps the same pipeline behavior but removes stale and duplicated pieces.

Changes made:

```text
Removed old dags/my_1_dag.py
Renamed Dag_staging.py -> dags/youtube_pipeline.py
Kept exactly two DAGs: extract_to_staging and staging_to_core
Removed generated Airflow logs from the source archive
Removed generated raw/processed JSON from the source archive
Removed the real .env from the distributable archive
Added .gitignore and a complete .env.example
Standardized all file paths with PROJECT_ROOT
Wrapped source scripts in main() functions
Simplified source code and DAG definitions
Aligned youtube_core schema with load_core.py
Made fresh PostgreSQL initialization create metadata, Celery and ELT databases
Made fresh PostgreSQL initialization create the staging/core tables
Updated the test script for both current DAGs and the core phase
Updated commands.txt
Added full mirrored documentation under docs/
```

The runtime behavior remains:

```text
extract -> raw -> details -> merge -> staging -> core
```
