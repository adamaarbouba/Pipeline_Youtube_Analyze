# Phase 10 - Testing

The central test helper is:

```text
scripts/test_pipeline.sh
```

Quick health check:

```bash
./scripts/test_pipeline.sh check
```

Test every phase manually:

```bash
./scripts/test_pipeline.sh manual
```

Trigger the real Airflow chain:

```bash
./scripts/test_pipeline.sh trigger
```

Check both DAG histories:

```bash
./scripts/test_pipeline.sh runs
```

Check warehouse data:

```bash
./scripts/test_pipeline.sh postgres
```

Expected flow:

```text
extract_to_staging success
        |
        v
staging_to_core success
        |
        v
youtube_staging populated
        |
        v
youtube_core populated
```
