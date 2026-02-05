# Contributing to AutoForge Lab

Thank you for your interest in contributing.

This project is designed to be:

- educational
- modular
- safe
- extensible
- automation-focused

We welcome improvements, extensions, and fixes.

---

# 🧭 Contribution Types

You can contribute:

- new collectors
- validators
- extractors
- analytics modules
- tests
- documentation
- bug fixes
- performance improvements

---

# ⚙️ Setup

Clone repo:

```

git clone <repo>
cd autoforge-lab

```

Run stack:

```

docker-compose up -d --build

```

Backend health:

```

curl [http://localhost:8000/health](http://localhost:8000/health)

```

---

# 🧪 Run Tests

```

docker-compose exec backend pytest

```

All new features should include tests when reasonable.

---

# 🧱 Code Style Guidelines

## Python

- Prefer OOP modules over large functions
- Keep collectors isolated
- Validators must be pure functions
- Avoid hidden side effects
- Add docstrings for public classes
- Add “Pro Tip” comments where useful

## FastAPI

- Routers should be thin
- Business logic lives outside routes
- DB access via session dependency

## Frontend

- Keep API logic in api.ts
- UI components should not embed fetch logic
- Prefer small reusable functions

---

# 🔐 Crawling Rules (Important)

Contributions involving crawling must:

- respect robots.txt
- include throttling
- include user agent
- avoid abusive patterns
- log crawl decisions

Unsafe crawlers will not be merged.

---

# 🧩 Adding a New Collector

Create:

```

app/crawling/<name>_collector.py

```

Requirements:

- subclass BaseCollector
- return CollectorResult
- include timeout controls
- include docstring
- include usage comment

Add test if possible.

---

# 🧪 Testing Expectations

Add tests for:

- validators
- parsing logic
- new routes
- normalization rules

Avoid real network calls in tests.

Use fixtures or mocks.

---

# 📝 Documentation

If you add:

- new module
- new pipeline step
- new collector

Update:

- README
- ARCHITECTURE.md (if structural)
- docstrings

---

# 🚫 Do Not Submit

- vendor scraping scripts
- credential harvesting
- bypass tools
- abuse-oriented automation
- destructive tests

This project is for responsible automation engineering.

---

# 🔄 Pull Request Process

1. Fork repo
2. Create branch
3. Add feature or fix
4. Add tests
5. Run tests
6. Update docs if needed
7. Submit PR with clear description

---

# 💬 Commit Message Style

Prefer:

```

collector: add playwright collector
validator: add sku normalization
api: fix job timestamp handling
tests: add crawl run endpoint test

```

---

# 🧠 Design Philosophy

AutoForge Lab favors:

- clarity over cleverness
- safety over speed
- modularity over shortcuts
- testability over magic

Build systems others can reason about.

---

# 🙏 Thank You

Good automation systems are built by engineers who care about correctness and safety.

We appreciate your contribution.
