#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -U pip >/dev/null
python3 -m pip install -U nox >/dev/null

nox -s backend_lint