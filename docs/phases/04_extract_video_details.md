# Phase 4 - Extract Video Details

File:

```text
src/extract_video_details.py
```

Input:

```text
data/raw/youtube_raw.json
```

The script collects every video ID from the uploads playlist and removes duplicates while keeping order.

The YouTube videos endpoint accepts up to 50 IDs per request, so IDs are processed in batches of 50.

Requested sections:

```text
snippet
contentDetails
statistics
status
topicDetails
```

Output:

```text
data/raw/youtube_video_details_raw.json
```

Run manually:

```bash
./scripts/test_pipeline.sh task2
```
