# MVQUEEN Shopify Backend

Dedicated Shopify backend boundary for MVQUEEN_OS.

## Phase 1 runtime

The backend now has a minimal FastAPI runtime with safe endpoints:

- `GET /health` — local service health and safety mode.
- `GET /api/shopify/status` — reports whether Shopify credentials are configured without exposing the token.
- `/docs` — local API documentation during development.

Run from `apps/mvqueen-shopify-backend` with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000/health`.

## Shopify configuration

Set these as environment variables in the runtime/deployment environment; never commit them:

- `SHOPIFY_STORE_DOMAIN`
- `SHOPIFY_ACCESS_TOKEN`
- `SHOPIFY_API_VERSION=2026-07`
- `SHOPIFY_DRY_RUN=true`
- `MVQUEEN_ENV=development`

The existing GraphQL client under `15_Scripts_And_Code/mvqueen_engine` remains the reusable domain/automation layer. The backend is the Shopify app boundary around that engine.

## Safety

- Begin read-only.
- Keep writes behind explicit dry-run controls.
- Preserve handles, SKUs, variants, inventory, and existing media unless explicitly authorized.
- Validate GraphQL operations against the live Shopify schema before execution.
- Retain the legacy REST layer during migration.
- Use separate Shopify app configurations for development, staging, and production.
- Do not actively develop against the live production installation.
