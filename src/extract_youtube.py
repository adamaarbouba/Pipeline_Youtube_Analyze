import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")


if not API_KEY:
    raise ValueError("API_KEY is missing from .env")

if not CHANNEL_HANDLE:
    raise ValueError("CHANNEL_HANDLE is missing from .env")


youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY,
)


# --------------------------------------------------
# 1. Get channel information
# --------------------------------------------------

channel_response = (
    youtube.channels()
    .list(
        part="snippet,contentDetails,statistics",
        forHandle=CHANNEL_HANDLE,
    )
    .execute()
)


if not channel_response.get("items"):
    raise ValueError(f"No YouTube channel found for handle: {CHANNEL_HANDLE}")


channel = channel_response["items"][0]

channel_id = channel["id"]

uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]


print(f"\nChannel ID: {channel_id}")
print(f"Uploads Playlist ID: {uploads_playlist_id}")


# --------------------------------------------------
# 2. Get every page from the uploads playlist
# --------------------------------------------------

playlist_pages = []

next_page_token = None
page_number = 1
total_videos = 0


print("\nFetching uploads...")


while True:
    request = youtube.playlistItems().list(
        part="snippet,contentDetails,status",
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token,
    )

    response = request.execute()

    # Store the ENTIRE raw API response
    playlist_pages.append(response)

    videos_on_page = len(response.get("items", []))

    total_videos += videos_on_page

    print(f"Page {page_number}: {videos_on_page} videos | Total: {total_videos}")

    next_page_token = response.get("nextPageToken")

    if not next_page_token:
        break

    page_number += 1


# --------------------------------------------------
# 3. Combine raw responses
# --------------------------------------------------

raw_data = {
    "channel": channel_response,
    "playlistPages": playlist_pages,
}


# --------------------------------------------------
# 4. Create raw data directory
# --------------------------------------------------

os.makedirs(
    "data/raw",
    exist_ok=True,
)


# --------------------------------------------------
# 5. Save RAW JSON
# --------------------------------------------------

output_file = "data/raw/youtube_raw.json"


with open(
    output_file,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        raw_data,
        file,
        ensure_ascii=False,
        indent=4,
    )


# --------------------------------------------------
# 6. Summary
# --------------------------------------------------

print("\nExtraction complete")
print(f"Pages fetched: {len(playlist_pages)}")
print(f"Videos fetched: {total_videos}")
print(f"Raw data saved to: {output_file}")
