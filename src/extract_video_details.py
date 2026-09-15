import json
import os
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.discovery import build


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PLAYLIST_RAW_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_raw.json"

VIDEO_RAW_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_video_details_raw.json"


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("API_KEY")


if not API_KEY:
    raise ValueError("API_KEY is missing from .env")


# --------------------------------------------------
# YouTube API client
# --------------------------------------------------

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY,
)


# --------------------------------------------------
# 1. Load playlist raw data
# --------------------------------------------------

if not PLAYLIST_RAW_FILE.exists():
    raise FileNotFoundError(f"Raw playlist file not found: {PLAYLIST_RAW_FILE}")


with open(
    PLAYLIST_RAW_FILE,
    "r",
    encoding="utf-8",
) as file:
    playlist_raw_data = json.load(file)


# --------------------------------------------------
# 2. Extract every video ID
# --------------------------------------------------

video_ids = []


for page in playlist_raw_data.get("playlistPages", []):
    for item in page.get("items", []):
        video_id = item.get("contentDetails", {}).get("videoId")

        if video_id:
            video_ids.append(video_id)


# Remove duplicates while keeping original order
video_ids = list(dict.fromkeys(video_ids))


if not video_ids:
    raise ValueError("No video IDs found in youtube_raw.json")


print(f"\nFound {len(video_ids)} video IDs")


# --------------------------------------------------
# 3. Fetch video details in batches of 50
# --------------------------------------------------

video_pages = []

batch_number = 1


print("\nFetching video details...\n")


for index in range(0, len(video_ids), 50):
    batch = video_ids[index : index + 50]

    response = (
        youtube.videos()
        .list(
            part=("snippet,contentDetails,statistics,status,topicDetails"),
            id=",".join(batch),
        )
        .execute()
    )

    video_pages.append(response)

    returned_videos = len(response.get("items", []))

    print(f"Batch {batch_number}: requested {len(batch)} | received {returned_videos}")

    batch_number += 1


# --------------------------------------------------
# 4. Build raw video data
# --------------------------------------------------

video_raw_data = {
    "requestedVideoCount": len(video_ids),
    "videoIds": video_ids,
    "videoPages": video_pages,
}


# --------------------------------------------------
# 5. Save raw video API responses
# --------------------------------------------------

VIDEO_RAW_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with open(
    VIDEO_RAW_FILE,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        video_raw_data,
        file,
        ensure_ascii=False,
        indent=4,
    )


# --------------------------------------------------
# Summary
# --------------------------------------------------

actual_video_count = sum(len(page.get("items", [])) for page in video_pages)


print("\nExtraction complete")
print(f"Requested videos: {len(video_ids)}")
print(f"Returned videos: {actual_video_count}")
print(f"Batches: {len(video_pages)}")
print(f"Saved to: {VIDEO_RAW_FILE}")
