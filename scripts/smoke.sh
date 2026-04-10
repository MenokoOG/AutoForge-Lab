#!/usr/bin/env bash
set -euo pipefail

echo "🔎 Smoke test: services + API health"

API_PORT="${HOST_API_PORT:-8000}"

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "❌ Docker Compose not found. Install Docker Compose v2 (preferred) or docker-compose." >&2
  exit 127
fi

"${COMPOSE_CMD[@]}" ps >/dev/null

if ! "${COMPOSE_CMD[@]}" ps | grep -q backend; then
  echo "❌ backend not listed"
  "${COMPOSE_CMD[@]}" ps
  exit 1
fi

if ! "${COMPOSE_CMD[@]}" ps | grep -q worker; then
  echo "❌ worker not listed"
  "${COMPOSE_CMD[@]}" ps
  exit 1
fi

if command -v curl >/dev/null 2>&1; then
  echo "➡️  Checking http://localhost:${API_PORT}/health"
  curl -fsS "http://localhost:${API_PORT}/health" >/dev/null
else
  echo "⚠️ curl not found; skipping HTTP check"
fi

echo "✅ Smoke test passed"