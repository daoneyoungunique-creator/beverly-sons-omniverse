# CAAVE Empire v4 — integration service

Review-first FastAPI service for Base44 reads, Stripe Checkout, signed Stripe webhook accounting, and a shared read-only dashboard.

## Local setup
```bash
cd services/caave-empire-v4
python -m venv .venv
pip install -r requirements.txt
pytest -q
uvicorn api:app --reload --port 8001
```
Dashboard: http://localhost:8001/dashboard

Copy `.env.example` to a private environment file and configure variables in your hosting provider. Do not commit secrets. The service does not automatically load a .env file; export the variables or use your hosting provider's secret manager.

## Checkout
POST /checkout/{asset_id} requires the private `X-CAAVE-Admin-Token` header. Do not expose this token in browser JavaScript. Call the endpoint only from a trusted backend. Set real HTTPS success/cancel URLs and a rotated Stripe secret key.

## Stripe webhook
Point Stripe to POST /stripe-webhook, configure the signing secret, and test signature verification before production. Only paid checkout.session.completed events are recorded; event IDs are idempotent. Refunds, disputes, taxes, attribution, and fulfillment are **not yet handled**; the ledger is a gross paid-checkout view, not net profit. Do not rely on it for financial statements.

## Base44
`Base44Client` fetches entities via authenticated server-side requests. It does not post or mutate accounts. App IDs are registry references, not proof of a live connection.

## Deployment
`Dockerfile` and `render.yaml` provide a container-based deployment starting point. SQLite on an ephemeral filesystem is **not production-persistent**; provision a persistent disk or migrate to PostgreSQL before accepting live payments. Keep the app private until authentication, CSRF/origin controls, rate limiting, and production observability are reviewed.

No automatic crypto transfers, NFT minting, mass posting, or simulated sales are enabled.
