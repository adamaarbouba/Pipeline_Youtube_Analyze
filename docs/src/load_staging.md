# `src/load_staging.py`

Loads `youtube_merged.json` into PostgreSQL.

The loader first verifies that the input is a non-empty list. It then creates `youtube_staging` if necessary, truncates the previous snapshot and bulk-inserts the current snapshot with `execute_values`.

Staging intentionally uses text columns for source values because cleaning and type conversion happen in the next phase.
