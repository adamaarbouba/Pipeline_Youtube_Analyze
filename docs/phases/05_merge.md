# Phase 5 - Merge Raw Data

File:

```text
src/merge_raw.py
```

Inputs:

```text
data/raw/youtube_raw.json
data/raw/youtube_video_details_raw.json
```

The script creates a lookup by `video_id`, then combines playlist data and video-detail data.

The processed record is:

```json
{
  "videoId": "...",
  "title": "...",
  "publishedAt": "...",
  "duration": "...",
  "viewCount": "...",
  "likeCount": "...",
  "commentCount": "..."
}
```

Output:

```text
data/processed/youtube_merged.json
```

Run manually:

```bash
./scripts/test_pipeline.sh task3
```
