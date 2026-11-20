#!/usr/bin/env python3
"""Beverly & Sons CAAVE Empire v4.0 — secure integration scaffold.
No live transfers, fabricated revenue, unsolicited mass posting, or automatic minting.
"""
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from decimal import Decimal
from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel, Field

DB_PATH = Path(os.getenv("CAAVE_V4_DB", "caave_empire_v4.db"))
LLC_NAME = "Beverly & Sons Marketing and Consulting LLC"
BASE44_APPS = {
    "content_main":"6961656499e21f59875878d3",
    "assets":"6953416c18ae0e72c345e51a",
    "user_progress":"69214df5afa5a8eff0093881",
    "analytics":"69861e619b787ca54624f0b9",
    "characters":"6962c9f1b8822783d32b1ad2",
    "products":"6927dbb002ff7c99050a371b",
    "courses":"69619d67b1a79dab1e225ccd",
    "story_templates":"692e5980cd130da524cfb8f4",
    "leads":"692b96a1919afe7d08c4e4dd",
}
IP_CATALOG = [
    {"id":"codex-001","title":"147 Codex Chakra Nodes","pillar":"147_CODEX","price_cents":999},
    {"id":"teach-001","title":"T.E.A.C.H.I.N.G. Day 1","pillar":"TEACHING","price_cents":1700},
    {"id":"wealth-001","title":"W.E.A.L.T.H. Wealth Wheel","pillar":"WEALTH","price_cents":1700},
    {"id":"calm-001","title":"SEE Calming Starter","pillar":"CALMING","price_cents":700},
]
GUILDS = ("base44","content","checkout","beam","analytics","review")
app = FastAPI(title="Beverly & Sons CAAVE Empire v4.0", version="4.0.0")

@contextmanager
def db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY, stripe_event_id TEXT NOT NULL UNIQUE,
            stripe_session_id TEXT, amount_cents INTEGER NOT NULL,
            currency TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS beam_drafts (
            id INTEGER PRIMARY KEY, asset_id TEXT NOT NULL,
            base44_app TEXT, status TEXT NOT NULL DEFAULT 'draft',
            qr_url TEXT, checkout_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        """)
init_db()

def split_cents(amount):
    treasury = amount * 60 // 100
    creator = amount * 20 // 100
    return {"treasury_cents":treasury,"creator_cents":creator,
            "gaming_cents":amount-treasury-creator,
            "note":"Accounting plan only; no cryptocurrency transfer."}

@app.get("/")
def dashboard():
    return {"company":LLC_NAME,"version":"4.0","mode":"review_first",
            "guilds":GUILDS,"planned_workers":120,"running_workers":0,
            "connected_apps_configured":len(BASE44_APPS),
            "stripe_configured":bool(os.getenv("STRIPE_SECRET_KEY")),
            "base44_configured":bool(os.getenv("BASE44_API_KEY")),
            "enjin_configured":bool(os.getenv("ENJIN_KEY")),
            "note":"Configuration flags do not confirm a successful connection."}

@app.get("/catalog")
def catalog():
    return IP_CATALOG

@app.get("/revenue")
def revenue():
    with db() as c:
        count,total=c.execute(
            "SELECT COUNT(*),COALESCE(SUM(amount_cents),0) FROM payments WHERE currency='usd'"
        ).fetchone()
    return {"verified_usd_cents":total,"verified_usd":round(total/100,2),
            "recorded_payments":count,"allocation_plan":split_cents(total)}

@app.get("/revenue/{app_id}")
def app_revenue(app_id:str):
    if app_id not in BASE44_APPS.values():
        raise HTTPException(404,"Unknown Base44 app")
    return {"app_id":app_id,"attributed_revenue_usd":None,
            "note":"Per-app attribution requires verified payment metadata."}

@app.post("/stripe-webhook")
async def stripe_webhook(request:Request, stripe_signature:str|None=Header(None)):
    if not stripe_signature:
        raise HTTPException(400,"Missing Stripe-Signature")
    secret=os.getenv("STRIPE_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(503,"Stripe webhook secret not configured")
    try:
        import stripe
        event=stripe.Webhook.construct_event(await request.body(),stripe_signature,secret)
    except (ValueError,Exception) as exc:
        # Return a generic failure; never expose webhook payloads or secrets.
        raise HTTPException(400,"Invalid webhook payload or signature") from None
    if event["type"]=="checkout.session.completed":
        session=event["data"]["object"]
        if session.get("payment_status")=="paid":
            amount=session.get("amount_total")
            currency=session.get("currency")
            if isinstance(amount,int) and amount>=0 and currency:
                with db() as c:
                    c.execute("""INSERT OR IGNORE INTO payments
                        (stripe_event_id,stripe_session_id,amount_cents,currency)
                        VALUES (?,?,?,?)""",
                        (event["id"],session.get("id"),amount,currency.lower()))
    return {"received":True}

@app.post("/beam/deploy")
def deploy_beam():
    raise HTTPException(403,"Live beam deployment disabled until Enjin auth, asset ownership and approval flow are verified")

@app.get("/health")
def health():
    return {"ok":True,"mode":"review_first"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=int(os.getenv("PORT","8001")))
