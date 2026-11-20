# CAAVE Unified Sovereign Engine v2.0 — Integration & Security Review
Source: user-provided Python FastAPI/SQLite script, 2026-11-20.
Entity: Beverly & Sons Marketing and Consulting LLC; Albany/Troy 518.
Status: prototype only. NOT deployed, payment-connected, authenticated, or approved to distribute funds.

## Original architecture
- Config: founder, HQ, two domains, contact, 7.5% royalty, local SQLite, proposed treasury wallet.
- SQLite: users(user_id,email,credits), ledger, media_assets(asset_id,user_id,pillar,cid,rights), revenue_splits.
- Attention: view 0.1, read 0.5, share 1.0, purchase 10.0; source multiplies by 10 and truncates to integer credits.
- Generation cost: slides 20, consulting 50, comic 30, fallback 20.
- Generate: checks credits, creates MOCK 'Official ... Verified' text, short SHA256 digest, UUID asset ID, debits credits, stores rights text.
- Revenue: proposed 7.5% creator / 92.5% treasury internal split, writes to SQLite; no transfer.
- FastAPI: GET /, POST /track/attention, POST /generate, GET /ledger/summary.

## Source defects and blockers
1. Broken Markdown/paste escaping, links in code, and backslash-escaped Python syntax require cleanup before running.
2. Root references missing CONFIG['legal_entity']; causes KeyError.
3. No authentication or authorization; user_id supplied by client and summary publicly readable.
4. Unbounded attention-credit farming; no event deduplication, verification, throttling, bot detection, or fraud review. Purchase credits must be granted from verified Stripe webhooks, never client event claims.
5. Stripe imported but unused. No signature verification, event-id idempotency, settlement, refund/chargeback handling or reconciliation.
6. AI generation is a mock, not a model call. Never label it 'Verified by Beverly & Sons' automatically.
7. 16-character truncated SHA256 is neither an IPFS CID nor evidence of copyright ownership or on-chain provenance.
8. Credit check and debit are not atomic: concurrent requests can overspend. Use conditional debit in one transaction, then refund on failure.
9. SQLite is local and not appropriate for stateless serverless deployment; use a transactional production DB (e.g., Supabase Postgres) with row-level security.
10. Floating-point currency math and ledger totals are unsafe; use integer cents and Decimal for financial calculation.
11. 7.5/92.5 allocation is a business proposal; no established legal trust, royalty obligation, or authorized payment routing is demonstrated. Do not automatically move money to the provided wallet.
12. Hard-coded fallback wallet is not verified and should not be treated as an authorized payment destination.
13. Config email/domain contain pasted Markdown, not plain strings; verify contact address with owner before publication.
14. Unused httpx, stripe, asyncio etc. and no request models/validation, tests, secrets management, CORS policy, audit log or privacy/retention policy.
15. Status 'Operational' is a static claim, not a health check.

## Required implementation path
- Secure identities via Supabase Auth or equivalent, authenticated owner/admin endpoints and per-user resource isolation.
- Define Pydantic request schemas, positive validated amounts, bounded prompt lengths, content review, and consistent error responses.
- Add verified Stripe webhook ingestion with signature, event idempotency, order state and refunds. Revenue ledger reflects settled/verified transactions only; show gross, fees, refunds and net separately.
- Implement fraud-resistant attention analytics as observational events; reward credits only for server-verified qualifying actions with caps.
- Preserve original source IP provenance separately from generated outputs; register asset hash as checksum, not IPFS CID.
- Make all content drafts pending review; never automatically publish, mint, send marketing messages, or transfer funds.
- Connect CAAVE Daily Keys site, Daily Media Engine, NFT Art Engine, Coloring Book Engine, Unified Platform OS and Shopify/Supabase/Stripe/Vercel through tested services.

## Acceptance
Tests for authentication, duplicate event replay, concurrency, refund, zero/negative values, privacy and correct reporting. Explicit deployment approval and verified credentials required.
