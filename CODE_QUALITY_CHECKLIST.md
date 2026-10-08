# Code Quality Checklist (AutoForge Lab)

Use this checklist before opening a PR or tagging a release.

---

## ✅ Backend (Python / FastAPI)

### Correctness

- [ ] New behavior has tests (`pytest`)
- [ ] No failing tests locally
- [ ] New endpoints return stable JSON shapes
- [ ] Exceptions are handled (no silent failure)
- [ ] Timestamp / timezone handling is consistent

### Architecture

- [ ] Business logic stays out of routes
- [ ] Collectors do not parse or validate (single responsibility)
- [ ] Validators are pure functions (no I/O)
- [ ] Extractors are deterministic and side-effect free
- [ ] Store layer owns DB writes

### Safety / Crawling

- [ ] robots.txt rules respected
- [ ] Throttling enforced per host
- [ ] Timeouts set for network and browser automation
- [ ] No bypass/abuse patterns

### Observability

- [ ] Logs are structured and meaningful
- [ ] Errors include actionable context
- [ ] “Pro Tip” comments added only when they teach something real

---

## ✅ Frontend (React / Vite)

- [ ] API logic stays in `api.ts` (or a dedicated API module)
- [ ] UI does not hardcode backend URLs (uses env var)
- [ ] Errors display friendly messaging (no silent UI failure)
- [ ] No console spam in production builds

---

## ✅ Docker / Compose

- [ ] `docker-compose up -d --build` works from repo root
- [ ] Services expose expected ports
- [ ] Backend health is reachable
- [ ] No secrets committed to repo
- [ ] `.gitignore` includes local env + build artifacts

---

## ✅ Documentation

- [ ] README updated (features, setup, troubleshooting)
- [ ] ARCHITECTURE updated if structure changed
- [ ] CONTRIBUTING updated if workflow changed
- [ ] New modules have docstrings and a small usage note

---

## ✅ Security

- [ ] SECURITY.md reviewed for correctness
- [ ] Dependency updates reviewed (`pip`, `npm`)
- [ ] No credentials/tokens in logs, examples, or tests

---

## ✅ Release Readiness

- [ ] CI passes on main branch
- [ ] Coverage has not regressed unexpectedly
- [ ] Changelog notes (if applicable)
