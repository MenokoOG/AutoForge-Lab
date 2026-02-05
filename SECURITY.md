# Security Policy

## Supported Versions

This project is community maintained. Security fixes are applied to the latest main branch.

| Version    | Supported      |
| ---------- | -------------- |
| main       | ✅ Yes         |
| older tags | ⚠️ Best effort |

Always upgrade to the latest commit before reporting a vulnerability.

---

## Reporting a Vulnerability

If you discover a security issue, **do not open a public GitHub issue**.

Please report responsibly:

- 📧 Email: menokoog@gmail.com  
  (replace with your real contact)
- Or: Open a **private security advisory** in GitHub if enabled
- Subject line: `SECURITY: <short description>`

Please include:

- Description of the vulnerability
- Steps to reproduce
- Affected endpoints or components
- Proof of concept (if safe)
- Suggested mitigation (optional)

You will receive acknowledgment within **72 hours**.

---

## Scope

This security policy covers:

- FastAPI backend services
- Worker / scheduler jobs
- Crawl pipeline (Collector / Extractor / Validator / Store)
- Playwright and Selenium collectors
- Docker configurations
- Database access layers
- CI workflows
- Dependency chain risks

Out of scope:

- Third-party sites being crawled
- User misconfiguration of Docker / OS
- Local development environment issues

---

## Secure Configuration Guidelines

### Environment Variables

Never commit secrets.

Use `.env` files locally and secret managers in production:

Examples:

- Database credentials
- API tokens
- Proxy credentials
- Browser automation keys
- CI secrets

`.env` must be gitignored.

---

### CORS

Restrict CORS origins in production.

Do NOT deploy with:

```

allow_origins = ["*"]

```

Use explicit domains instead.

---

### Crawling & Automation Safety

The crawler system includes:

- robots.txt enforcement
- host throttling
- timeout controls
- domain allow/deny capability

Do not disable these safeguards in production deployments.

Respect target site policies and laws.

---

### Playwright / Selenium Safety

Browser automation can execute untrusted content.

Recommended:

- Run containers as non-root
- Use network isolation where possible
- Disable file downloads unless required
- Avoid running against authenticated sessions unless necessary
- Never reuse personal browser profiles

---

### Database Safety

- Use least-privilege DB users
- No superuser roles for application runtime
- Rotate credentials regularly
- Enable backups
- Avoid exposing DB ports publicly

---

### Dependency Security

Run regularly:

```

pip-audit
npm audit

```

Update vulnerable packages promptly.

CI should fail on critical vulnerabilities.

---

### Container Security

Recommended:

- Use slim base images
- Rebuild images frequently
- Scan images with:

```

docker scan
trivy
grype

```

- Do not bake secrets into images
- Use read-only containers when possible

---

## Denial of Service Considerations

Crawler and worker systems can generate traffic.

Controls included:

- rate limits
- host throttles
- job scheduling intervals

Do not reduce safeguards without understanding impact.

---

## Responsible Use

This project includes web automation and crawling capabilities.

Users are responsible for:

- Legal compliance
- Terms of service compliance
- Ethical automation practices

The maintainers are not responsible for misuse.

---

## Security Updates

Security fixes will be:

- Documented in commit messages
- Tagged when appropriate
- Announced in release notes

---

## Hall of Thanks

Responsible reporters may be acknowledged here (optional) unless they request anonymity.

---

Stay sharp. Build safely. 🔐
