# Phase 1 - Environment Configuration

The project starts from `.env.example`.

Create the real environment file:

```bash
cp .env.example .env
nvim .env
```

The main groups are:

- YouTube API: `API_KEY`, `CHANNEL_HANDLE`
- PostgreSQL server: `POSTGRES_CONN_*`
- Airflow metadata database: `METADATA_DATABASE_*`
- Celery result database: `CELERY_BACKEND_*`
- YouTube warehouse database: `ELT_DATABASE_*`
- Airflow runtime: `AIRFLOW_UID`, web username/password, `FERNET_KEY`

Generate a Fernet key with Python:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

The real `.env` is ignored by Git and is not included in the cleaned project archive.
