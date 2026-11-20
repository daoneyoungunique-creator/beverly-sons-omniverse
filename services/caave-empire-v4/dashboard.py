"""Shared read-only dashboard routes."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CAAVE Empire Dashboard</title>
<style>body{background:#101725;color:#f4e6be;font:16px system-ui;margin:2rem}
main{max-width:900px;margin:auto}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1rem}
article{border:1px solid #806b3c;border-radius:12px;padding:1.3rem}strong{font-size:1.5rem}
small{color:#c7c3b8}</style></head><body><main><h1>BEVERLY &amp; SONS · CAAVE EMPIRE</h1>
<p>Read-only verified revenue dashboard. No wallet transfers or minting.</p>
<div class="cards"><article><h2>Verified revenue</h2><strong id="revenue">Loading</strong></article>
<article><h2>Payments</h2><strong id="payments">Loading</strong></article>
<article><h2>Operations</h2><strong>Review first</strong></article></div>
<p><small>Refresh to retrieve latest recorded Stripe webhook transactions.</small></p></main>
<script>
fetch('/revenue').then(r=>r.json()).then(d=>{
document.getElementById('revenue').textContent='$'+Number(d.verified_usd).toFixed(2);
document.getElementById('payments').textContent=String(d.recorded_payments);
}).catch(()=>{document.getElementById('revenue').textContent='Unavailable';
document.getElementById('payments').textContent='Unavailable';});
</script></body></html>"""
