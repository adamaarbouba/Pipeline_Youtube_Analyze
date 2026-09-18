# Phase 3 - Extract Channel and Uploads Playlist

File:

```text
src/extract_youtube.py
```

Purpose:

1. Read `API_KEY` and `CHANNEL_HANDLE`.
2. Find the channel through the YouTube Data API v3.
3. Get the channel uploads playlist ID.
4. Paginate through the complete uploads playlist.
5. Save every raw API response.

Output:

```text
data/raw/youtube_raw.json
```

The raw layer intentionally preserves the API response instead of selecting only analytics fields.

Run manually:

```bash
./scripts/test_pipeline.sh task1
```
