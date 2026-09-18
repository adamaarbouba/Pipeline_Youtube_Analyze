# `src/load_core.py`

Transforms the staging snapshot into the typed core table.

Before loading, it refuses to run if staging is empty.

Transformations:

```text
TRIM(video_id)
TRIM(title)
empty strings -> NULL
published_at -> TIMESTAMPTZ
view/like/comment counts -> BIGINT
```

The core table uses `video_id` as its primary key. `ON CONFLICT` updates existing videos while new IDs are inserted.
