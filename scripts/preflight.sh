#!/usr/bin/env bash
set -euo pipefail

DB_PORT="${POSTGRES_PORT:-5432}"
API_PORT="${HOST_API_PORT:-8000}"
FE_PORT="${HOST_FRONTEND_PORT:-5173}"

if docker compose version >/dev/null 2>&1; then
  if [[ -n "$(docker compose ps --services --status running 2>/dev/null)" ]]; then
    echo "✅ Port preflight skipped: compose services are already running for this project"
    exit 0
  fi
fi

is_port_in_use() {
  local port="$1"

  if command -v ss >/dev/null 2>&1; then
    ss -ltn "( sport = :${port} )" | grep -q LISTEN
    return $?
  fi

  if command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"${port}" -sTCP:LISTEN >/dev/null 2>&1
    return $?
  fi

  echo "⚠️ Could not check ports because neither 'ss' nor 'lsof' is available." >&2
  return 1
}

occupied=()

if is_port_in_use "${DB_PORT}"; then occupied+=("POSTGRES_PORT=${DB_PORT}"); fi
if is_port_in_use "${API_PORT}"; then occupied+=("HOST_API_PORT=${API_PORT}"); fi
if is_port_in_use "${FE_PORT}"; then occupied+=("HOST_FRONTEND_PORT=${FE_PORT}"); fi

if (( ${#occupied[@]} > 0 )); then
  echo "❌ Port preflight failed. The following host ports are already in use:" >&2
  for item in "${occupied[@]}"; do
    echo "  - ${item}" >&2
  done

  echo >&2
  echo "Try this instead:" >&2
  echo "POSTGRES_PORT=5433 HOST_API_PORT=8001 HOST_FRONTEND_PORT=5174 ./scripts/up.sh" >&2
  exit 1
fi

echo "✅ Port preflight passed (DB:${DB_PORT}, API:${API_PORT}, FE:${FE_PORT})"