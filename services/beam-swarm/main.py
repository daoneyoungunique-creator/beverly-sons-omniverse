#!/usr/bin/env python3
"""Beverly & Sons CAAVE Beam Swarm — safe, review-first starter."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

DB_PATH = Path(os.getenv("BEAM_DB_PATH", "caave_beams.db"))
app = FastAPI(title="Beverly & Sons CAAVE Beam Swarm", version="1.0.0")
GUILDS = ("content", "beam", "publish", "track", "promote")
CATALOG = [
    {"id": "001", "title": "T.E.A.C.H.I.N.G. Day 1: Trust Audit", "pillar": "TEACHING", "price": 9.99},
    {"id": "002", "title": "W.E.A.L.T.H. Wealth Wheel", "pillar": "WEALTH", "price": 17.00},
    {"id": "003", "title": "SEE Calming Starter Scan", "pillar": "CALMING", "price": 7.00},
]

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        external_order_id TEXT NOT NULL UNIQUE,
        asset_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0),
        created_at TEXT NOT NULL
    )""")
    conn.commit()
    return conn

class Order(BaseModel):
    external_order_id: str = Field(min_length=1)
    asset_id: str = Field(min_length=1)
    amount_cents: int = Field(ge=0)

@app.get("/")
def home():
    return {"service": "CAAVE Beam Swarm", "mode": "review-first", "guilds": GUILDS,
            "workers_configured": 100, "workers_running": 0,
            "enjin_connected": bool(os.getenv("ENJIN_KEY")),
            "note": "No automatic posting, minting or fabricated claims."}

@app.get("/catalog")
def catalog():
    return CATALOG

@app.get("/revenue")
def revenue():
    with connect() as db:
        count, cents = db.execute(
            "SELECT COUNT(*), COALESCE(SUM(amount_cents), 0) FROM orders"
        ).fetchone()
    return {"recorded_orders": count, "recorded_revenue_usd": round(cents / 100, 2),
            "note": "Only verified transactions should be entered; no estimates."}

@app.post("/orders")
def record_verified_order(order: Order):
    # Explicitly disabled unless protected by a trusted upstream authenticated service.
    from fastapi import HTTPException
    raise HTTPException(status_code=403, detail="Order ingestion disabled until webhook signature verification is implemented.")

@app.get("/health")
def health():
    return {"ok": True, "timestamp": datetime.now(timezone.utc).isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT", "8001")))
