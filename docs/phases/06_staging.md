# Phase 6 - PostgreSQL Staging

File:

```text
src/load_staging.py
```

Input:

```text
data/processed/youtube_merged.json
```

The staging table deliberately keeps API values as text:

```text
youtube_staging
├── video_id TEXT
├── title TEXT
├── published_at TEXT
├── duration TEXT
├── view_count TEXT
├── like_count TEXT
├── comment_count TEXT
└── loaded_at TIMESTAMPTZ
```

Each run performs:

```sql
TRUNCATE TABLE youtube_staging;
```

then bulk-inserts the latest complete channel snapshot.

This means staging represents the most recent extraction, not historical versions.

Run manually:

```bash
./scripts/test_pipeline.sh task4
```
