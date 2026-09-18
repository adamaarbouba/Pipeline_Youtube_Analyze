# Project Documentation

This directory mirrors the project and documents every meaningful phase and file.

## Architecture

```text
YouTube API
    |
    v
[1] Extract channel + uploads playlist
    |
    v
data/raw/youtube_raw.json
    |
    v
[2] Extract details for every video
    |
    v
data/raw/youtube_video_details_raw.json
    |
    v
[3] Merge useful fields
    |
    v
data/processed/youtube_merged.json
    |
    v
[4] Load latest snapshot into youtube_staging
    |
    v
[5] Clean, cast and upsert into youtube_core
```

## Airflow orchestration

```text
extract_to_staging
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
        |
        v
staging_to_core
  load_core
```

## Phase documentation

1. [`phases/01_environment.md`](phases/01_environment.md)
2. [`phases/02_infrastructure.md`](phases/02_infrastructure.md)
3. [`phases/03_extract_playlist.md`](phases/03_extract_playlist.md)
4. [`phases/04_extract_video_details.md`](phases/04_extract_video_details.md)
5. [`phases/05_merge.md`](phases/05_merge.md)
6. [`phases/06_staging.md`](phases/06_staging.md)
7. [`phases/07_core.md`](phases/07_core.md)
8. [`phases/08_airflow.md`](phases/08_airflow.md)
9. [`phases/09_daily_updates.md`](phases/09_daily_updates.md)
10. [`phases/10_testing.md`](phases/10_testing.md)

## Mirrored file documentation

```text
docs/
├── Dockerfile.md
├── docker-compose.md
├── requirements.md
├── env-example.md
├── dags/
│   └── youtube_pipeline.md
├── src/
│   ├── extract_youtube.md
│   ├── extract_video_details.md
│   ├── merge_raw.md
│   ├── load_staging.md
│   └── load_core.md
├── docker/
│   └── postgres/
│       ├── init-multiple-databases.md
│       └── create-elt-tables.md
└── scripts/
    ├── test_pipeline.md
    └── commands.md
```
