#!/bin/sh
set -e

valid_boolean() {
  case "$1" in
    true|TRUE|1|yes|YES|y|Y|on|ON|false|FALSE|0|no|NO|n|N|off|OFF)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

boolean_enabled() {
  case "$1" in
    true|TRUE|1|yes|YES|y|Y|on|ON)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

wait_for_database() {
  if [ -z "${DATABASE_URL:-}" ]; then
    echo "DATABASE_URL is not set; skipping database wait."
    return 0
  fi

  echo "Waiting for the configured database to become reachable..."
  python3 - <<'PY'
import os
import sys
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

database_url = os.environ["DATABASE_URL"]
last_error = None

for _ in range(60):
    try:
        engine = create_engine(database_url, future=True, pool_pre_ping=True)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database is reachable.")
        sys.exit(0)
    except SQLAlchemyError as exc:
        last_error = exc
        time.sleep(1)

print(f"Database did not become reachable within 60 seconds: {last_error}", file=sys.stderr)
sys.exit(1)
PY
}

run_migrations() {
  echo "Running Alembic migrations..."
  alembic upgrade head
}

maybe_run_migrations() {
  value="${RUN_MIGRATIONS_ON_STARTUP:-false}"
  if ! valid_boolean "$value"; then
    echo "Invalid RUN_MIGRATIONS_ON_STARTUP value: ${value}" >&2
    echo "Use true or false." >&2
    exit 1
  fi
  if boolean_enabled "$value"; then
    run_migrations
  else
    echo "RUN_MIGRATIONS_ON_STARTUP is false; skipping Alembic migrations."
  fi
}

synchronize_outputs() {
  echo "Synchronizing generated outputs into the database..."
  python3 src/database/sync_outputs.py
}

maybe_synchronize_outputs() {
  case "${SYNC_OUTPUTS_ON_STARTUP:-true}" in
    true|TRUE|1|yes|YES)
      synchronize_outputs
      ;;
    false|FALSE|0|no|NO)
      echo "SYNC_OUTPUTS_ON_STARTUP is false; skipping generated output synchronization."
      ;;
    *)
      echo "Invalid SYNC_OUTPUTS_ON_STARTUP value: ${SYNC_OUTPUTS_ON_STARTUP}" >&2
      echo "Use true or false." >&2
      exit 1
      ;;
  esac
}

validate_api_startup_config() {
  python3 -m src.api.startup_config
}

start_api() {
  validate_api_startup_config
  wait_for_database
  maybe_run_migrations
  maybe_synchronize_outputs
  exec python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port "${API_PORT:-8000}"
}

mode="${1:-api}"
if [ "$#" -gt 0 ]; then
  shift
fi

case "$mode" in
  api)
    if [ "$#" -gt 0 ]; then
      echo "api mode does not accept extra arguments: $*" >&2
      exit 1
    fi
    start_api
    ;;
  migrate)
    if [ "$#" -gt 0 ]; then
      echo "migrate mode does not accept extra arguments: $*" >&2
      exit 1
    fi
    wait_for_database
    run_migrations
    ;;
  sync)
    if [ "$#" -gt 0 ]; then
      echo "sync mode does not accept extra arguments: $*" >&2
      exit 1
    fi
    wait_for_database
    synchronize_outputs
    ;;
  *)
    echo "Unknown container mode: ${mode}" >&2
    echo "Valid modes: api, migrate, sync" >&2
    exit 1
    ;;
esac
