import json
import os
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.discovery import build


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_raw.json"


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("API_KEY")
    channel_handle = os.getenv("CHANNEL_HANDLE")

    if not api_key or not channel_handle:
        raise ValueError("API_KEY and CHANNEL_HANDLE are required")

    youtube = build("youtube", "v3", developerKey=api_key)

    channel_response = (
        youtube.channels()
        .list(
            part="snippet,contentDetails,statistics",
            forHandle=channel_handle,
        )
        .execute()
    )

    if not channel_response.get("items"):
        raise ValueError(f"No channel found for {channel_handle}")

    channel = channel_response["items"][0]
    playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_pages = []
    page_token = None
    total_videos = 0

    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="snippet,contentDetails,status",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )

        playlist_pages.append(response)
        total_videos += len(response.get("items", []))
        page_token = response.get("nextPageToken")

        if not page_token:
            break

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "channel": channel_response,
                "playlistPages": playlist_pages,
            },
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(f"Videos fetched: {total_videos}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
