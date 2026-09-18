# `Dockerfile`

Builds the custom Airflow image used by all Airflow services.

Base image:

```text
apache/airflow:2.9.2-python3.10
```

The image installs the project dependencies from `requirements.txt` while constraining Airflow to the same version as the base image.

Build directly:

```bash
docker build -t youtube-airflow .
```

Normal project usage builds it through Compose:

```bash
docker compose up -d --build
```
