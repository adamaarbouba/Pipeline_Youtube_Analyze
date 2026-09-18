# `requirements.txt`

Project Python dependencies:

```text
google-api-python-client  YouTube Data API v3 client
python-dotenv              local `.env` loading
psycopg2-binary            PostgreSQL driver
```

Airflow itself comes from the Docker base image and is constrained during the image build to keep dependency resolution compatible.
