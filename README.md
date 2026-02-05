# AutoForge Lab ⚙️

AutoForge Lab is a containerized Python automation and crawling stack built for engineers who want a clean, extensible pipeline for:

- Web crawling
- Structured extraction
- Validation + normalization
- Storage
- Scheduled jobs
- Browser automation (Playwright + Selenium)
- Testable, modular OOP pipelines

It is designed to be practical, hackable, and self-hostable — not bloated, not vendor-locked.

---

# 🚀 Features

- FastAPI backend API
- PostgreSQL storage
- APScheduler worker jobs
- OOP crawler pipeline:
  - Collector → Extractor → Validator → Store
- Robots.txt enforcement
- Per-host throttling
- Playwright collector
- Selenium collector
- Pandas-ready data handling
- Pytest test suite
- Dockerized full stack
- Simple React + Vite frontend dashboard
- Script-driven dev workflow (no Make required)

---

# 🧱 Architecture Overview

```

Collectors
├── RequestsCollector
├── PlaywrightCollector
└── SeleniumCollector

```

    ↓

```

Extractors
→ parse titles, links, fields

```

    ↓

```

Validators
→ normalize + clean + reject bad records

```

    ↓

```

Store Layer
→ PostgreSQL persistence

```

    ↓

```

API + UI
→ FastAPI + React dashboard

```

    ↓

```

Scheduler Worker
→ recurring crawl jobs

```

---

# 🐳 Stack

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- APScheduler
- Pytest
- Pandas
- Playwright
- Selenium

## Data

- PostgreSQL 16

## Frontend

- React
- Vite
- TypeScript

## Runtime

- Docker
- docker-compose

---

# ⚡ Quick Start

## 1️⃣ Clone

```bash
git clone <your-repo-url>
cd autoforge-lab
```

## 2️⃣ Start the Stack

```bash
./scripts/up.sh
```

Services:

- Backend API → [http://localhost:8000](http://localhost:8000)
- Frontend → [http://localhost:5173](http://localhost:5173)
- Database → localhost:5432

---

## 3️⃣ Health Check

```bash
curl http://localhost:8000/health
```

Expected:

```json
{ "ok": true }
```

---

# 🧪 Dev Commands

## Start stack

```bash
./scripts/up.sh
```

## Stop stack

```bash
./scripts/down.sh
```

## Logs

```bash
./scripts/logs.sh
./scripts/logs-api.sh
./scripts/logs-worker.sh
```

## Tests

```bash
./scripts/test.sh
```

## Lint

```bash
./scripts/lint.sh
```

## Format

```bash
./scripts/format.sh
```

## Type checks

```bash
./scripts/types.sh
```

---

# 🕷 Crawling Pipeline (OOP Design)

Each crawl flows through composable stages:

## Collector

Responsible only for fetching content.

Examples:

- RequestsCollector → HTTP
- PlaywrightCollector → headless browser
- SeleniumCollector → full browser automation

## Extractor

Parses raw content into structured fields.

## Validator

Cleans, normalizes, rejects invalid records.

## Store

Writes validated records to DB.

---

# 🤖 Worker Scheduler

The worker container runs scheduled jobs:

- Crawl samplers
- Record refresh jobs
- Pipeline runs

Default interval: every 15 minutes.

Manual trigger:

```bash
docker-compose exec worker python -c \
"from app.scheduler.jobs import run_crawl_sampler; run_crawl_sampler()"
```

---

# 🔐 Safety Features

- robots.txt checks
- crawl blocking when disallowed
- per-host throttling
- timeout enforcement
- structured logging
- no stealth scraping patterns

---

# 📊 Data & Pandas

Records can be exported and processed with Pandas easily:

```python
import pandas as pd
df = pd.read_json("records.json")
```

Designed for downstream analytics and ML pipelines.

---

# 🧪 Testing

Pytest suite included.

Runs inside container for consistency:

```bash
./scripts/test.sh
```

CI runs pytest + coverage on pull requests.

---

# 🧩 Extending the System

Add a new collector:

```
app/crawling/collectors/my_collector.py
```

Subclass base collector and plug into pipeline config.

Add a new extractor or validator the same way — pipeline is intentionally modular.

---

# 🛠 Pro Tips

- Keep collectors dumb — no parsing inside them
- Put normalization in validators
- Keep routes thin — push logic to services
- Always test new extractors with pytest fixtures
- Respect robots.txt — don’t remove the guardrails

---

# 🤝 Contributing

See:

```
CONTRIBUTING.md
CODE_QUALITY_CHECKLIST.md
SECURITY.md
```

Pull requests welcome if they keep the architecture clean and responsibility boundaries intact.
