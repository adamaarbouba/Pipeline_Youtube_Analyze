# Phase 7 - Clean and Load Core

File:

```text
src/load_core.py
```

Input:

```text
youtube_staging
```

Core is the typed analytics-ready table:

```text
youtube_core
├── video_id TEXT PRIMARY KEY
├── title TEXT NOT NULL
├── published_at TIMESTAMPTZ
├── duration TEXT
├── view_count BIGINT
├── like_count BIGINT
├── comment_count BIGINT
├── created_at TIMESTAMPTZ
└── updated_at TIMESTAMPTZ
```

Cleaning is intentionally minimal:

```text
TRIM text fields
empty string -> NULL
published_at text -> TIMESTAMPTZ
count text -> BIGINT
empty video IDs/titles -> skipped
```

The loader uses PostgreSQL upsert logic:

```sql
ON CONFLICT (video_id)
DO UPDATE
```

Result:

```text
new video      -> INSERT
existing video -> UPDATE statistics/details
```

Run manually:

```bash
./scripts/test_pipeline.sh task5
```
