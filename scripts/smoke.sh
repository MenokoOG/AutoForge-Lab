#!/usr/bin/env bash
set -euo pipefail

echo "🔎 Smoke test: services + API health"

docker-compose ps >/dev/null

if ! docker-compose ps | grep -q backend; then
  echo "❌ backend not listed"
  docker-compose ps
  exit 1
fi

if ! docker-compose ps | grep -q worker; then
  echo "❌ worker not listed"
  docker-compose ps
  exit 1
fi

if command -v curl >/dev/null 2>&1; then
  echo "➡️  Checking http://localhost:8000/health"
  curl -fsS http://localhost:8000/health >/dev/null
else
  echo "⚠️ curl not found; skipping HTTP check"
fi

echo "✅ Smoke test passed"