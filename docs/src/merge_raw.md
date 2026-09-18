# `src/merge_raw.py`

Combines the two raw extraction outputs.

Inputs:

```text
data/raw/youtube_raw.json
data/raw/youtube_video_details_raw.json
```

Output:

```text
data/processed/youtube_merged.json
```

The merged dataset contains the fields required by the warehouse while the original raw files remain unchanged for future use.
