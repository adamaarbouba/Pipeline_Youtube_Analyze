# `src/extract_youtube.py`

First extraction stage.

Reads:

```text
API_KEY
CHANNEL_HANDLE
```

Calls:

```text
channels.list
playlistItems.list
```

Pagination continues until the YouTube API stops returning `nextPageToken`.

Writes:

```text
data/raw/youtube_raw.json
```

The file contains the channel response and every raw playlist page.
