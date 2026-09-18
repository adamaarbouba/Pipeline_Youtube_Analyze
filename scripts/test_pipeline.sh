#!/usr/bin/env bash
set -euo pipefail

STAGING_DAG="extract_to_staging"
CORE_DAG="staging_to_core"

section() {
  echo
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

run_worker() {
  docker compose run --rm --entrypoint bash airflow-worker -c "$1"
}

containers() {
  section "CONTAINERS"
  docker compose ps
}

dag_check() {
  section "DAGS"
  docker exec airflow-scheduler airflow dags list | grep -E "$STAGING_DAG|$CORE_DAG"
  echo
  docker exec airflow-scheduler airflow dags list-import-errors
}

celery_check() {
  section "CELERY"
  docker exec airflow-worker \
    celery --app airflow.providers.celery.executors.celery_executor.app inspect ping
}

task1() {
  section "1 - EXTRACT PLAYLIST"
  run_worker "python /opt/airflow/src/extract_youtube.py"
}

task2() {
  section "2 - EXTRACT VIDEO DETAILS"
  run_worker "python /opt/airflow/src/extract_video_details.py"
}

task3() {
  section "3 - MERGE RAW DATA"
  run_worker "python /opt/airflow/src/merge_raw.py"
}

task4() {
  section "4 - LOAD STAGING"
  run_worker "python /opt/airflow/src/load_staging.py"
}

task5() {
  section "5 - LOAD CORE"
  run_worker "python /opt/airflow/src/load_core.py"
}

manual() {
  task1
  task2
  task3
  task4
  task5
}

postgres_check() {
  section "POSTGRES"
  docker exec postgres bash -lc '
    PGPASSWORD="$ELT_DATABASE_PASSWORD" psql \
      -U "$ELT_DATABASE_USERNAME" \
      -d "$ELT_DATABASE_NAME" \
      -c "\dt" \
      -c "SELECT COUNT(*) AS staging_rows FROM youtube_staging;" \
      -c "SELECT COUNT(*) AS core_rows FROM youtube_core;" \
      -c "SELECT video_id, title, view_count, like_count FROM youtube_core LIMIT 5;"
  '
}

trigger() {
  section "TRIGGER FULL AIRFLOW PIPELINE"
  docker exec airflow-scheduler airflow dags unpause "$STAGING_DAG" >/dev/null
  docker exec airflow-scheduler airflow dags unpause "$CORE_DAG" >/dev/null
  docker exec airflow-scheduler airflow dags trigger "$STAGING_DAG"
}

runs() {
  section "STAGING DAG RUNS"
  docker exec airflow-scheduler airflow dags list-runs -d "$STAGING_DAG"
  section "CORE DAG RUNS"
  docker exec airflow-scheduler airflow dags list-runs -d "$CORE_DAG"
}

files() {
  section "GENERATED FILES"
  ls -lh data/raw data/processed
}

logs() {
  section "SCHEDULER LOGS"
  docker logs airflow-scheduler --tail 100
  section "WORKER LOGS"
  docker logs airflow-worker --tail 100
}

check() {
  containers
  dag_check
  celery_check
  files
  postgres_check
}

usage() {
  cat <<'TXT'
Usage: ./scripts/test_pipeline.sh <command>

Commands:
  containers   Docker service status
  dag-check    DAGs and import errors
  celery       Celery worker ping
  task1        Extract channel/uploads playlist
  task2        Extract video details
  task3        Merge raw JSON
  task4        Load staging table
  task5        Clean and upsert core table
  manual       Run task1 -> task5 manually
  postgres     Check staging/core data
  trigger      Trigger extract_to_staging DAG
  runs         Show both DAG run histories
  files        Show generated JSON files
  logs         Show scheduler/worker logs
  check        Run non-API health checks
TXT
}

case "${1:-}" in
  containers) containers ;;
  dag-check) dag_check ;;
  celery) celery_check ;;
  task1) task1 ;;
  task2) task2 ;;
  task3) task3 ;;
  task4) task4 ;;
  task5) task5 ;;
  manual) manual ;;
  postgres) postgres_check ;;
  trigger) trigger ;;
  runs) runs ;;
  files) files ;;
  logs) logs ;;
  check) check ;;
  *) usage ;;
esac
