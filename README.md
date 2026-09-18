# YouTube Data Pipeline

A Dockerized Airflow pipeline that extracts YouTube channel data, stores raw JSON, builds a merged dataset, loads a PostgreSQL staging table, and cleans/upserts the data into a typed core table.

## Pipeline

```text
YouTube API
   |
   v
extract_youtube.py
   |
   v
extract_video_details.py
   |
   v
merge_raw.py
   |
   v
youtube_staging
   |
   v
load_core.py
   |
   v
youtube_core
```

Airflow splits the work into two DAGs:

```text
extract_to_staging -> staging_to_core
```

The first DAG runs every day at 14:00 Africa/Casablanca time. The second DAG is triggered only after staging finishes successfully.

See [`docs/README.md`](docs/README.md) for the complete phase-by-phase documentation.
