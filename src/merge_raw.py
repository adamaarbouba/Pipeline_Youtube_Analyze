import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_raw.json"
DETAILS_FILE = PROJECT_ROOT / "data" / "raw" / "youtube_video_details_raw.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "youtube_merged.json"


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    playlist_data = load_json(PLAYLIST_FILE)
    details_data = load_json(DETAILS_FILE)

    details_by_id = {}
    for page in details_data.get("videoPages", []):
        for item in page.get("items", []):
            if item.get("id"):
                details_by_id[item["id"]] = item

    merged = []

    for page in playlist_data.get("playlistPages", []):
        for playlist_item in page.get("items", []):
            video_id = playlist_item.get("contentDetails", {}).get("videoId")
            if not video_id:
                continue

            detail = details_by_id.get(video_id, {})
            snippet = detail.get("snippet", {})
            playlist_snippet = playlist_item.get("snippet", {})
            content = detail.get("contentDetails", {})
            statistics = detail.get("statistics", {})

            merged.append(
                {
                    "videoId": video_id,
                    "title": snippet.get("title", playlist_snippet.get("title")),
                    "publishedAt": snippet.get(
                        "publishedAt", playlist_snippet.get("publishedAt")
                    ),
                    "duration": content.get("duration"),
                    "viewCount": statistics.get("viewCount"),
                    "likeCount": statistics.get("likeCount"),
                    "commentCount": statistics.get("commentCount"),
                }
            )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(merged, file, ensure_ascii=False, indent=4)

    print(f"Merged videos: {len(merged)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
