# `src/extract_video_details.py`

Second extraction stage.

Reads video IDs from:

```text
data/raw/youtube_raw.json
```

Removes duplicate IDs, divides them into batches of 50 and calls `videos.list`.

Writes complete raw result pages to:

```text
data/raw/youtube_video_details_raw.json
```
