# AutoForge Lab — Architecture Guide

This document describes the architecture of **AutoForge Lab**, an automation and crawler platform built with FastAPI, PostgreSQL, Docker, and React.

The system is designed to be:

- modular
- testable
- automation-friendly
- safe for responsible crawling
- easy to extend with new collectors and validators

---

# 🧭 High-Level Overview

AutoForge Lab is composed of four primary runtime components:

1. Frontend (React + Vite)
2. Backend API (FastAPI)
3. Worker Scheduler (APScheduler)
4. Database (PostgreSQL)

All services run in Docker containers and communicate over the compose network.

---

# 🏗 System Diagram

```

┌────────────────────┐
│     Frontend       │
│  React + Vite UI   │
│  Port :5173        │
└─────────┬──────────┘
│ HTTP (REST)
▼
┌────────────────────┐
│     FastAPI        │
│     Backend        │
│     Port :8000     │
│                    │
│  /health           │
│  /crawl/records    │
│  /crawl/run        │
│  /crawl/jobs       │
└───────┬────────────┘
│
│ SQLAlchemy
▼
┌────────────────────┐
│   PostgreSQL       │
│   crawl_records    │
│   job_runs         │
└────────────────────┘

```

    ▲
    │ shared models + pipeline
    │

```

┌────────────────────┐
│     Worker         │
│ APScheduler Loop   │
│ run_crawl_sampler  │
│ every N minutes    │
└────────────────────┘

```

---

# 🔄 Crawl Pipeline (OOP Design)

The crawl system uses an object-oriented pipeline pattern.

```

Collector → Extractor → Validator → Store

```

## Collector

Responsible for retrieving raw content.

Examples:

- HTTPCollector (requests/httpx)
- PlaywrightCollector (browser automation)
- SeleniumCollector (browser automation)

Collectors return:

```

CollectorResult

* url
* status_code
* content
* headers

```

---

## Extractor

Parses raw HTML or data into structured fields.

Typical responsibilities:

- HTML parsing (BeautifulSoup / lxml)
- title extraction
- link extraction
- metadata capture

Extractors should be:

- deterministic
- side-effect free
- testable

---

## Validator

Ensures data quality and normalization.

Examples:

- regex cleanup
- whitespace normalization
- title normalization
- URL validation
- tag normalization

**Pro Tip:** Validators should never fetch data — only transform or reject.

---

## Store Layer

Responsible for persistence.

Uses:

- SQLAlchemy ORM
- PostgreSQL
- transaction-safe commits

Models:

- CrawlRecord
- JobRun

---

# ⏱ Scheduling Model

The worker container runs APScheduler.

Scheduler responsibilities:

- run crawl sampler on interval
- log job start/finish
- record status
- isolate recurring automation from API thread

Two execution modes exist:

## Scheduled

Worker triggers crawl on interval.

## Manual

API endpoint `/crawl/run` creates a JobRun and triggers crawl in a background task.

---

# 🔐 Responsible Crawling Controls

The crawl pipeline includes safety features:

- robots.txt checks
- crawl blocking if disallowed
- host throttling
- structured crawl logging
- status tracking

If robots.txt disallows:

```

status = CrawlBlockedByRobots

```

No fetch occurs.

---

# 📊 Analytics Layer

Optional analytics helpers live outside the ingestion pipeline.

Module:

```

app/analytics/pandas_reports.py

```

Responsibilities:

- convert DB rows → pandas DataFrame
- source distribution reports
- recent activity windows
- aggregation helpers

**Design Rule:**
Analytics must not mutate crawl data.

---

# 🌐 API Layer

FastAPI routers expose system state.

## Health

```

GET /health

```

## Records

```

GET /crawl/records?limit=100

```

## Manual Run

```

POST /crawl/run

```

## Job History

```

GET /crawl/jobs

```

---

# 🧱 Container Layout

```

backend/
app/
api/
crawling/
analytics/
db/
models/
scheduler/
validators/

frontend/
src/app/

docker-compose.yml

```

---

# 🧪 Testing Strategy

pytest suite covers:

- API health
- crawl endpoints
- normalization logic
- pipeline helpers

Tests avoid network dependency where possible.

---

# 🧩 Extension Points

Engineers can safely extend:

- new collectors
- new validators
- new extractors
- analytics modules
- alerting rules
- anomaly detection
- ML classifiers

Design goal: add modules without rewriting core pipeline.

---

# 🧠 Design Principles

- OOP over script chains
- validation-first ingestion
- side-effect isolation
- safe crawling by default
- containerized reproducibility
- testable units
- explicit scheduling

---

# 🚀 Future Architecture Options

Possible upgrades:

- distributed worker queue
- message broker
- crawl priority scoring
- ML classification layer
- rule engine
- alert triggers
- streaming ingestion

AutoForge Lab is intentionally built to support these evolutions.
