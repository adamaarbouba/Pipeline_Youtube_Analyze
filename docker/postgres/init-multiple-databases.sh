#!/usr/bin/env bash
set -euo pipefail

create_user_and_database() {
  local database="$1"
  local username="$2"
  local password="$3"

  if ! psql -U "$POSTGRES_USER" -d postgres -tAc \
    "SELECT 1 FROM pg_roles WHERE rolname='${username}'" | grep -q 1; then
    psql -U "$POSTGRES_USER" -d postgres -v ON_ERROR_STOP=1 \
      -c "CREATE USER \"${username}\" WITH PASSWORD '${password}';"
  fi

  if ! psql -U "$POSTGRES_USER" -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname='${database}'" | grep -q 1; then
    createdb -U "$POSTGRES_USER" -O "$username" "$database"
  fi
}

create_user_and_database \
  "$METADATA_DATABASE_NAME" \
  "$METADATA_DATABASE_USERNAME" \
  "$METADATA_DATABASE_PASSWORD"

create_user_and_database \
  "$CELERY_BACKEND_NAME" \
  "$CELERY_BACKEND_USERNAME" \
  "$CELERY_BACKEND_PASSWORD"

create_user_and_database \
  "$ELT_DATABASE_NAME" \
  "$ELT_DATABASE_USERNAME" \
  "$ELT_DATABASE_PASSWORD"

psql -U "$POSTGRES_USER" -d "$ELT_DATABASE_NAME" -v ON_ERROR_STOP=1 \
  -f /docker/postgres/create-elt-tables.sql

psql -U "$POSTGRES_USER" -d "$ELT_DATABASE_NAME" -v ON_ERROR_STOP=1 <<EOSQL
ALTER TABLE youtube_staging OWNER TO "$ELT_DATABASE_USERNAME";
ALTER TABLE youtube_core OWNER TO "$ELT_DATABASE_USERNAME";
EOSQL
