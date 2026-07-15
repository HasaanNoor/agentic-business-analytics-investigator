#!/bin/sh
set -e

COMPOSE=${COMPOSE:-"docker compose"}
BASE_URL=${BASE_URL:-"http://localhost:8000"}
FRONTEND_URL=${FRONTEND_URL:-"http://localhost:3000"}
KEEP_STACK=${KEEP_STACK:-false}
VERIFY_DOCKER_BUILD=${VERIFY_DOCKER_BUILD:-true}

cleanup() {
  if [ "$KEEP_STACK" != "true" ]; then
    $COMPOSE down
  fi
}

trap cleanup EXIT

if [ "$VERIFY_DOCKER_BUILD" = "true" ]; then
  $COMPOSE config >/dev/null
  $COMPOSE up -d --build
else
  $COMPOSE config >/dev/null
  $COMPOSE up -d
fi

$COMPOSE ps

echo "Waiting for API readiness..."
attempt=0
until curl -fsS "$BASE_URL/health/ready" >/tmp/agentic_bai_ready.json; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 60 ]; then
    echo "API did not become ready. Recent api logs:" >&2
    $COMPOSE logs api >&2
    exit 1
  fi
  sleep 2
done

python3 - <<'PY'
import json
from pathlib import Path

payload = json.loads(Path("/tmp/agentic_bai_ready.json").read_text())
if not payload.get("ready"):
    raise SystemExit(f"API is not ready: {payload}")
if not payload.get("database", {}).get("available"):
    raise SystemExit(f"Database is not available: {payload}")
print("Health check reports the API and database are ready.")
PY

echo "Waiting for frontend readiness..."
attempt=0
until curl -fsS "$FRONTEND_URL/" >/dev/null; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 60 ]; then
    echo "Frontend did not become ready. Recent frontend logs:" >&2
    $COMPOSE logs frontend >&2
    exit 1
  fi
  sleep 2
done

curl -fsS "$BASE_URL/health" >/dev/null
curl -fsS "$BASE_URL/health/live" >/dev/null
curl -fsS "$BASE_URL/health/ready" >/dev/null
curl -fsS "$BASE_URL/kpis?limit=5" >/dev/null
curl -fsS "$BASE_URL/incidents" >/dev/null
curl -fsS "$BASE_URL/forecasts" >/dev/null
curl -fsS "$BASE_URL/explanations?limit=5" >/dev/null
curl -fsS "$BASE_URL/reports/actionable" >/dev/null
curl -fsS "$BASE_URL/rag/search?query=shipping%20delay&top_k=2" >/dev/null
curl -fsS "$FRONTEND_URL/" >/dev/null
curl -fsS "$FRONTEND_URL/api/health" >/dev/null
curl -fsS "$FRONTEND_URL/api/health/live" >/dev/null
curl -fsS "$FRONTEND_URL/api/health/ready" >/dev/null

$COMPOSE exec -T api alembic current
$COMPOSE run --rm api migrate
$COMPOSE run --rm api sync

echo "Docker stack verification completed."
