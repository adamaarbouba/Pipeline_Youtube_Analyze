import json
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PLAYLIST_RAW_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_raw.json"

VIDEO_DETAILS_RAW_FILE = (
    PROJECT_ROOT / "data" / "raw" / "youtube_video_details_raw.json"
)

OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "youtube_merged.json"


# --------------------------------------------------
# 1. Load playlist raw data
# --------------------------------------------------

if not PLAYLIST_RAW_FILE.exists():
    raise FileNotFoundError(f"Playlist raw file not found: {PLAYLIST_RAW_FILE}")


with open(
    PLAYLIST_RAW_FILE,
    "r",
    encoding="utf-8",
) as file:
    playlist_raw = json.load(file)


# --------------------------------------------------
# 2. Load video details raw data
# --------------------------------------------------

if not VIDEO_DETAILS_RAW_FILE.exists():
    raise FileNotFoundError(
        f"Video details raw file not found: {VIDEO_DETAILS_RAW_FILE}"
    )


with open(
    VIDEO_DETAILS_RAW_FILE,
    "r",
    encoding="utf-8",
) as file:
    video_details_raw = json.load(file)


# --------------------------------------------------
# 3. Build lookup table for video details
# --------------------------------------------------

video_details_lookup = {}


for page in video_details_raw.get("videoPages", []):
    for item in page.get("items", []):
        video_id = item.get("id")

        if video_id:
            video_details_lookup[video_id] = item


print(f"Loaded details for {len(video_details_lookup)} videos")


# --------------------------------------------------
# 4. Merge playlist + video details
# --------------------------------------------------

merged_videos = []


for page in playlist_raw.get("playlistPages", []):
    for playlist_item in page.get("items", []):
        content_details = playlist_item.get(
            "contentDetails",
            {},
        )

        playlist_snippet = playlist_item.get(
            "snippet",
            {},
        )

        video_id = content_details.get("videoId")

        if not video_id:
            continue

        video_detail = video_details_lookup.get(
            video_id,
            {},
        )

        video_snippet = video_detail.get(
            "snippet",
            {},
        )

        video_content_details = video_detail.get(
            "contentDetails",
            {},
        )

        statistics = video_detail.get(
            "statistics",
            {},
        )

        merged_video = {
            "videoId": video_id,
            "title": video_snippet.get(
                "title",
                playlist_snippet.get("title"),
            ),
            "publishedAt": video_snippet.get(
                "publishedAt",
                playlist_snippet.get("publishedAt"),
            ),
            "duration": video_content_details.get("duration"),
            "viewCount": statistics.get("viewCount"),
            "likeCount": statistics.get("likeCount"),
            "commentCount": statistics.get("commentCount"),
        }

        merged_videos.append(merged_video)


# --------------------------------------------------
# 5. Create output directory
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# 6. Save merged JSON
# --------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        merged_videos,
        file,
        ensure_ascii=False,
        indent=4,
    )


# --------------------------------------------------
# 7. Summary
# --------------------------------------------------

print()
print("Merge complete")
print(f"Playlist videos: {len(merged_videos)}")
print(f"Video details: {len(video_details_lookup)}")
print(f"Saved to: {OUTPUT_FILE}")
