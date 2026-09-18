# `docker/postgres/create-elt-tables.sql`

Defines the warehouse tables created on a fresh PostgreSQL volume.

## `youtube_staging`

Source-like text columns plus `loaded_at`.

## `youtube_core`

Typed analytics columns with:

```text
video_id PRIMARY KEY
published_at TIMESTAMPTZ
view_count BIGINT
like_count BIGINT
comment_count BIGINT
created_at
updated_at
```

The Python loaders also use `CREATE TABLE IF NOT EXISTS`, so the pipeline can recover if tables are missing on an existing development database.
