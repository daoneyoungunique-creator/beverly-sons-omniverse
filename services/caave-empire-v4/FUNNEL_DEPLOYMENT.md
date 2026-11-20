# WHO AM I? organic funnel — deployment checklist
Status: SOURCE COMMITTED; NOT DEPLOYED.

## Verified connected services
- Shopify store: beverlyandsons.com, active Who Am I? product, currently $18.99
- Shopify product page: https://beverlyandsons.com/products/who-am-i
- Stripe: WHO AM I? Digital Self-Study active checkout, currently $17.99
- Stripe checkout: https://buy.stripe.com/cNi4gz8I427V8gr32Dg7e00
- Shopify Digital Products connector reachable; product file association and fulfillment NOT verified.
- The two checkout channels have different prices. Do not advertise a single price without identifying the channel.

## Run locally
pip install -r requirements.txt
pip install email-validator
export CAAVE_FUNNEL_DB=/persistent/caave_funnel.db
export CAAVE_ADMIN_TOKEN=<private secret>
uvicorn funnel_api:app --host 127.0.0.1 --port 8001

## Prelaunch blockers
1. Ensure email-validator installed and tests run.
2. Use PostgreSQL or encrypted durable storage for lead PII before production. Current SQLite implementation is a local prototype only.
3. Add unsubscribe mechanism and privacy policy before sending marketing email.
4. Add rate limits, anti-bot measures, CSRF/origin validation and abuse monitoring.
5. Add approved email service only after owner approves templates and recipients; currently sends nothing.
6. Confirm digital file delivery for BOTH Shopify and Stripe checkout separately. Shopify Digital Products installation does not imply Stripe orders deliver through it.
7. Ensure consent records retention, deletion requests, and secure access policies.
8. Confirm final domain, TLS and checkout routing.
9. Run tests and obtain approval before deployment or external publishing.
10. No ad spend, NFT minting, or crypto transfers.
