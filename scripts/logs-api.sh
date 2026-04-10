#!/usr/bin/env bash
set -euo pipefail

if docker compose version >/dev/null 2>&1; then
	COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
	COMPOSE_CMD=(docker-compose)
else
	echo "❌ Docker Compose not found. Install Docker Compose v2 (preferred) or docker-compose." >&2
	exit 127
fi

"${COMPOSE_CMD[@]}" logs -f --tail=200 backend