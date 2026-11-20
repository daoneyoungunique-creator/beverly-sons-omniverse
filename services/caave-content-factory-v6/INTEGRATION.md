# Beverly & Sons AI Content Factory v6.0 — Source Integration
Entity: Beverly & Sons Marketing and Consulting LLC
Source: user-uploaded 920-line Python/Flask script (email dated Apr 22, 2026).
Status: source architecture registered; production app not deployed.

## Ten IP domains
WEALTH — W.E.A.L.T.H.: Wisdom, Entities, Assets, Legacy, Transfer, Harmony.
TEACH — T.E.A.C.H.I.N.G.: Truth, Education, Action, Character, Honor, Identity, Nobility, Generations.
HHOS — H.H.O.S.: Honesty, Humility, Obedience, Sacrifice, Psychology of Fear, Power & Peace.
SUPREME — Supreme Mathematics, ten principles.
PYRAMID — Power, Youth, Resistance, Action, Movement, Independence, Determination.
CALMING — Centered, Aware, Loving, Mindful, Intentional, Nurturing, Grateful.
MIRROR — Manifest, Intention, Reflect, Restore, Organize, Rebuild.
LEGACY — Lineage, Empire, Generations, Ancestry, Continuity, Years.
EMPIRE — Enterprise, Mastery, Power, Influence, Revenue, Expansion.
MASTER — Mentor, Architect, Strategist, Teacher, Engineer, Researcher.

Note: The TEACH expansion here differs from the previously uploaded NFT Art Model's T.E.A.C.H.I.N.G. expansion. Preserve both source variants; do not silently overwrite either.

## Ten formats and source-proposed prices
slides $47, story $97, news $0, comic $197, quiz $197, vocabulary $47, mental_health $97, affirmations $47, supreme_math $37, consulting $997.
These are **draft pricing values in the source**, not approved or live Stripe/Shopify prices.

## Source endpoints
GET / — factory status (hardcoded 'operational').
GET /health — local process health.
GET /api/catalog — format/IP listing.
POST /api/generate/<format_type> — returns a ContentPackage and a constructed checkout_endpoint.
Data model: id, ip_domain, format_type, title, content, price_cents, base44_app_id, created_at.

## Daily Keys integration
For each approved Key, create content-package drafts from the same source IP: artwork caption, free lesson, affirmation, 8-second video prompt, story/comic script, printable coloring page, quiz and vocabulary, and relevant storefront offer. Link to the previously registered Key 328 record. Reuse unique source IDs and enforce editorial/rights review before publication.

## Engineering issues to fix
1. Generator methods produce placeholder strings and random quiz answers, not validated educational content. Never certify a learner from arbitrary answer keys.
2. No persistent storage: packages live only in a Python list; Base44 and revenue hub are configuration strings, not verified connections.
3. Checkout URL is constructed without Stripe payment session, order verification or delivery.
4. No user authentication, authorization, rate limits, prompt limits, or tenant separation.
5. News 'Verified primary sources' is a hardcoded claim; source URLs and verification are absent.
6. Mental health content is educational only, not therapy; avoid automatic 'resilience certification' and unfounded claims.
7. The BULLY_PROTOCOL dictionary duplicates key 'L', so 'Light' is overwritten by 'Leave'; use an ordered list of steps instead.
8. The '432Hz or 528Hz for cellular alignment' assertion is not established by the code; avoid presenting this as medical fact.
9. Some finance examples (IUL performance, compounding) are oversimplified and need fact-checking before publication.
10. User-facing paid offers must be reviewed for actual deliverables, approved price, consumer disclosures, tax and refund handling.
11. Flask debug=False is not sufficient production hardening; use a production server, secure secrets and storage.

## Integration contract
CAAVE Daily Keys -> editorial queue -> AI Content Factory -> rights/evidence QA -> approved art & lessons -> social post drafts -> public site -> Stripe-verified checkout -> private digital delivery -> analytics and reconciliation.

The uploaded script is a Flask prototype and is **not** the same runtime as the previously supplied FastAPI Sovereign Engine. Keep them separate until a deliberate service boundary or migration is implemented.
