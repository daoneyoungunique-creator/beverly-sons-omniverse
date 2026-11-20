# CAAVE Digital Products Studio — Phase 1 Code Scaffold
This directory is an isolated TypeScript module scaffold inside the existing Vite/R3F Omniverse repository. It is NOT wired into the game, hosted, or connected to Upload-Post, Stripe, or Supabase.

- src/distribution.ts: approval-gated publishing interface, receipt statuses and safe draft-only adapter
- src/revenue.ts: verified-event validation and deduplication key contract

## Next implementation
1. Choose whether to keep the studio as a separate deployable application.
2. Authenticate server requests and establish Supabase RLS; never trust user_id from request JSON.
3. Verify Upload-Post API endpoint/response contract before implementing real adapter.
4. Verify Stripe webhooks and affiliate/AdSense reports; store only actual provider-confirmed events.
5. Add review UI, durable queue, retry logic, idempotency, rate limits and tests.
6. Run a test post to an authorized account after approval.

No secrets, synthetic earnings, or fictional post URLs are included.
