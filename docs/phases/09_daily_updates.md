# Phase 9 - Daily Updates

The daily update is handled by the `extract_to_staging` DAG.

Schedule:

```text
0 14 * * *
```

At each run the pipeline fetches the complete current uploads playlist.

Example:

```text
Day 1: 341 videos
Day 2: 342 videos
```

On Day 2:

1. The staging table is replaced with the 342-video snapshot.
2. Core sees 341 existing `video_id` values and updates their current statistics.
3. The new `video_id` has no conflict and is inserted.

No separate polling DAG is required.

The current core logic does not delete old core rows when a video disappears from the channel. This avoids accidental data loss from a temporary or incomplete API extraction.
