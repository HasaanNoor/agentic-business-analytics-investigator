#!/bin/sh
set -e

wait_for_postgres() {
  if [ -z "${DATABASE_URL:-}" ]; then
    echo "DATABASE_URL is not set; skipping PostgreSQL wait."
    return 0
  fi

  echo "Waiting for PostgreSQL to become reachable..."
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
        print("PostgreSQL is reachable.")
        sys.exit(0)
    except SQLAlchemyError as exc:
        last_error = exc
        time.sleep(1)

print(f"PostgreSQL did not become reachable within 60 seconds: {last_error}", file=sys.stderr)
sys.exit(1)
PY
}

run_migrations() {
  echo "Running Alembic migrations..."
  alembic upgrade head
}

sync_outputs() {
  case "${SYNC_OUTPUTS_ON_STARTUP:-true}" in
    true|TRUE|1|yes|YES)
      echo "Synchronizing generated outputs into the database..."
      python3 src/database/sync_outputs.py
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

wait_for_postgres
run_migrations
sync_outputs

exec "$@"
