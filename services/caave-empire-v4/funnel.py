"""Review-first organic funnel. Lead data is never exposed by public API."""
import os, sqlite3, secrets, re, hashlib
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlencode
from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel, EmailStr, Field
from fastapi.responses import HTMLResponse, RedirectResponse

router=APIRouter()
SHOPIFY_PRODUCT="https://beverlyandsons.com/products/who-am-i"
STRIPE_PRODUCT="https://buy.stripe.com/cNi4gz8I427V8gr32Dg7e00"
DB=os.getenv("CAAVE_FUNNEL_DB","caave_funnel.db")
def connect():
    c=sqlite3.connect(DB,timeout=10)
    c.execute("""CREATE TABLE IF NOT EXISTS leads(
      id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, consent_at TEXT NOT NULL,
      source TEXT NOT NULL, unsubscribed INTEGER NOT NULL DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS events(
      id INTEGER PRIMARY KEY, event TEXT NOT NULL, source TEXT NOT NULL,
      occurred_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    c.commit()
    return c

class OptIn(BaseModel):
    email: EmailStr
    consent: bool
    source: str = Field(default="organic",max_length=48)

def source_label(value):
    value=re.sub(r"[^a-z0-9_-]","",value.lower())[:48]
    return value or "organic"

@router.get("/funnel",response_class=HTMLResponse)
def landing():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WHO AM I? | Beverly &amp; Sons</title>
<style>body{background:#0d1830;color:#f5e6c1;font:17px system-ui;padding:1.5rem}main{max-width:640px;margin:auto}
a,button{color:#0d1830;background:#d7ae51;padding:12px;border-radius:7px;display:inline-block;margin:8px 0}
input{padding:10px;max-width:95%}small{display:block;color:#c9c4b8;margin:12px 0}</style></head><body><main>
<h1>WHO AM I?™</h1><p>A 365-day guided self-study through personality, virtue, character, growth and inner peace.</p>
<p>Digital self-study. Choose the store checkout or Stripe checkout below. Prices may differ by channel; review the final checkout before paying.</p>
<a href="/go/shopify?source=organic">Shopify product</a>
<a href="/go/stripe?source=organic">Stripe checkout</a>
<h2>Get occasional Beverly &amp; Sons updates</h2>
<form id="lead"><label>Email <input name="email" type="email" required autocomplete="email"></label>
<p><label><input type="checkbox" name="consent" required> I agree to receive optional Beverly &amp; Sons marketing emails. I can unsubscribe anytime.</label></p>
<button type="submit">Join updates</button></form><p id="message" role="status"></p>
<small>No purchase required to subscribe. We do not send messages until an approved email provider and unsubscribe workflow are configured.</small>
<script>document.querySelector('#lead').addEventListener('submit',async e=>{
e.preventDefault();let f=e.target;
let r=await fetch('/leads/opt-in',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({email:f.email.value,consent:f.consent.checked,source:'organic'})});
document.querySelector('#message').textContent=r.ok?'Your consent has been recorded.':'Could not record your request.';
});</script></main></body></html>"""

@router.post("/leads/opt-in",status_code=202)
def opt_in(data:OptIn):
    if not data.consent:
        raise HTTPException(422,"Explicit marketing consent is required")
    if not os.getenv("CAAVE_FUNNEL_DB"):
        raise HTTPException(503,"Persistent lead storage not configured")
    with connect() as c:
        c.execute("""INSERT INTO leads(email,consent_at,source,unsubscribed)
          VALUES(?,?,?,0) ON CONFLICT(email) DO UPDATE SET
          consent_at=excluded.consent_at,source=excluded.source,unsubscribed=0""",
          (str(data.email).lower(),datetime.now(timezone.utc).isoformat(),source_label(data.source)))
    return {"accepted":True,"emails_sent":False}

@router.get("/go/{channel}")
def outbound(channel:str,source:str="organic"):
    if channel not in ("shopify","stripe"):
        raise HTTPException(404,"Unknown checkout")
    src=source_label(source)
    with connect() as c:
        c.execute("INSERT INTO events(event,source) VALUES(?,?)",(f"outbound_{channel}",src))
    target=SHOPIFY_PRODUCT if channel=="shopify" else STRIPE_PRODUCT
    # Do not attach customer email, identifiers or other PII to checkout URLs.
    return RedirectResponse(target,status_code=302)

@router.get("/funnel/metrics")
def metrics(x_caave_admin_token:str|None=Header(None)):
    token=os.getenv("CAAVE_ADMIN_TOKEN")
    if not token or not x_caave_admin_token or not secrets.compare_digest(token,x_caave_admin_token):
        raise HTTPException(403,"Operator authorization required")
    with connect() as c:
        leads=c.execute("SELECT COUNT(*) FROM leads WHERE unsubscribed=0").fetchone()[0]
        events=c.execute("SELECT event,source,COUNT(*) FROM events GROUP BY event,source").fetchall()
    return {"opted_in_leads":leads,"outbound_clicks":[{"event":e,"source":s,"count":n} for e,s,n in events],
            "note":"Clicks are not purchases. Verify orders in Stripe/Shopify."}
