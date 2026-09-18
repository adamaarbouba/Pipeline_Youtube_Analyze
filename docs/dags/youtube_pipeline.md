# `dags/youtube_pipeline.py`

Defines the two Airflow DAGs used by the project.

## `extract_to_staging`

Scheduled daily at 14:00 Africa/Casablanca.

Tasks:

```text
extract_playlist
extract_video_details
merge_data
load_staging
trigger_core
```

Every task is a `BashOperator` that runs one script from `/opt/airflow/src` except `trigger_core`, which uses `TriggerDagRunOperator`.

## `staging_to_core`

Unscheduled (`schedule=None`). It is started by `trigger_core` after DAG 1 succeeds.

Task:

```text
load_core
```
