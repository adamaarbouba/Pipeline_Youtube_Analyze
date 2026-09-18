import os

import psycopg2


def connect_database():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_CONN_HOST"),
        port=os.getenv("POSTGRES_CONN_PORT"),
        dbname=os.getenv("ELT_DATABASE_NAME"),
        user=os.getenv("ELT_DATABASE_USERNAME"),
        password=os.getenv("ELT_DATABASE_PASSWORD"),
    )


def main():
    with connect_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM youtube_staging;")
            staging_count = cursor.fetchone()[0]

            if staging_count == 0:
                raise ValueError("youtube_staging is empty")

            cursor.execute(
                """
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
                """
            )

            cursor.execute(
                """
                INSERT INTO youtube_core (
                    video_id,
                    title,
                    published_at,
                    duration,
                    view_count,
                    like_count,
                    comment_count
                )
                SELECT
                    TRIM(video_id),
                    TRIM(title),
                    NULLIF(TRIM(published_at), '')::TIMESTAMPTZ,
                    NULLIF(TRIM(duration), ''),
                    NULLIF(TRIM(view_count), '')::BIGINT,
                    NULLIF(TRIM(like_count), '')::BIGINT,
                    NULLIF(TRIM(comment_count), '')::BIGINT
                FROM youtube_staging
                WHERE
                    NULLIF(TRIM(video_id), '') IS NOT NULL
                    AND NULLIF(TRIM(title), '') IS NOT NULL
                ON CONFLICT (video_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    published_at = EXCLUDED.published_at,
                    duration = EXCLUDED.duration,
                    view_count = EXCLUDED.view_count,
                    like_count = EXCLUDED.like_count,
                    comment_count = EXCLUDED.comment_count,
                    updated_at = CURRENT_TIMESTAMP;
                """
            )

            print(f"Core rows processed: {cursor.rowcount}")


if __name__ == "__main__":
    main()
