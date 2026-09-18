# Phase 8 - Airflow Orchestration

DAG file:

```text
dags/youtube_pipeline.py
```

There are exactly two DAGs.

## DAG 1 - `extract_to_staging`

Runs every day at 14:00 in the `Africa/Casablanca` timezone.

```text
extract_playlist
      |
      v
extract_video_details
      |
      v
merge_data
      |
      v
load_staging
      |
      v
trigger_core
```

## DAG 2 - `staging_to_core`

Has no schedule:

```python
schedule=None
```

It is triggered by DAG 1 only after staging succeeds.

```text
load_core
```

This separation makes the ETL phases easy to understand while avoiding duplicate API extraction.
