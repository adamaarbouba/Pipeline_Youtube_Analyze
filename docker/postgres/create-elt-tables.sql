CREATE TABLE IF NOT EXISTS youtube_staging (
    video_id TEXT,
    title TEXT,
    published_at TEXT,
    duration TEXT,
    view_count TEXT,
    like_count TEXT,
    comment_count TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS youtube_core (
    video_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    published_at TIMESTAMPTZ,
    duration TEXT,
    view_count BIGINT,
    like_count BIGINT,
    comment_count BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
