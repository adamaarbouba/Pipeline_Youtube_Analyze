# `.env.example`

Template for all runtime environment variables.

Never commit the real `.env` because it contains the YouTube API key, database passwords, Airflow credentials and Fernet key.

Create the working file with:

```bash
cp .env.example .env
nvim .env
```
