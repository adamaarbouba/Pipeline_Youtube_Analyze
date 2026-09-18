import json
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "youtube_merged.json"


def connect_database():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_CONN_HOST"),
        port=os.getenv("POSTGRES_CONN_PORT"),
        dbname=os.getenv("ELT_DATABASE_NAME"),
        user=os.getenv("ELT_DATABASE_USERNAME"),
        password=os.getenv("ELT_DATABASE_PASSWORD"),
    )


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"File not found: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        videos = json.load(file)

    if not isinstance(videos, list) or not videos:
        raise ValueError("Merged data must be a non-empty list")

    rows = [
        (
            video.get("videoId"),
            video.get("title"),
            video.get("publishedAt"),
            video.get("duration"),
            video.get("viewCount"),
            video.get("likeCount"),
            video.get("commentCount"),
        )
        for video in videos
    ]

    with connect_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
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
                """
            )

            cursor.execute("TRUNCATE TABLE youtube_staging;")

            execute_values(
                cursor,
                """
                INSERT INTO youtube_staging (
                    video_id,
                    title,
                    published_at,
                    duration,
                    view_count,
                    like_count,
                    comment_count
                ) VALUES %s
                """,
                rows,
            )

    print(f"Staging rows loaded: {len(rows)}")


if __name__ == "__main__":
    main()
