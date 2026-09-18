import json
import os
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.discovery import build


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_raw.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_video_details_raw.json"


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY is required")

    if not PLAYLIST_FILE.exists():
        raise FileNotFoundError(f"File not found: {PLAYLIST_FILE}")

    with PLAYLIST_FILE.open("r", encoding="utf-8") as file:
        playlist_data = json.load(file)

    video_ids = []
    for page in playlist_data.get("playlistPages", []):
        for item in page.get("items", []):
            video_id = item.get("contentDetails", {}).get("videoId")
            if video_id:
                video_ids.append(video_id)

    video_ids = list(dict.fromkeys(video_ids))

    if not video_ids:
        raise ValueError("No video IDs found")

    youtube = build("youtube", "v3", developerKey=api_key)
    video_pages = []

    for index in range(0, len(video_ids), 50):
        batch = video_ids[index : index + 50]
        response = (
            youtube.videos()
            .list(
                part="snippet,contentDetails,statistics,status,topicDetails",
                id=",".join(batch),
            )
            .execute()
        )
        video_pages.append(response)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "requestedVideoCount": len(video_ids),
                "videoIds": video_ids,
                "videoPages": video_pages,
            },
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(f"Videos requested: {len(video_ids)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
