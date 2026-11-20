#!/usr/bin/env python3
"""CAAVE Empire: review-first content, NFT drafts, KDP metadata and verified revenue feed.
No fabricated sales, fake blockchain transactions, automatic investing or live minting.
"""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

DB_PATH = Path(os.getenv("CAAVE_EMPIRE_DB", "empire_mint_feed.db"))
SUPREME_MATH = {0:"CIPHER",1:"KNOWLEDGE",2:"WISDOM",3:"UNDERSTANDING",
 4:"CULTURE/FREEDOM",5:"POWER/REFINEMENT",6:"EQUALITY",7:"GOD",
 8:"BUILD/DESTROY",9:"BORN"}
SEASON_1 = [
 {"issue_number":1,"series":"Wisdom Warriors","title":"Fear Understood"},
 {"issue_number":2,"series":"Wisdom Warriors","title":"Discipline Over Emotion"},
 {"issue_number":3,"series":"Wisdom Warriors","title":"The Weight of Wisdom"},
]
ROLES = ("marketing","content","monetization","treasury","investment")
app = FastAPI(title="CAAVE Empire Monetization + NFT + KDP Engine", version="1.0.0")

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS feed (
          id INTEGER PRIMARY KEY, content TEXT NOT NULL, agent TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'draft', timestamp TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS revenue (
          id INTEGER PRIMARY KEY, source TEXT NOT NULL, amount_cents INTEGER NOT NULL,
          currency TEXT NOT NULL DEFAULT 'USD', external_id TEXT UNIQUE,
          verified INTEGER NOT NULL DEFAULT 0, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS treasury_plans (
          id INTEGER PRIMARY KEY, asset TEXT NOT NULL, allocation_cents INTEGER NOT NULL,
          status TEXT NOT NULL DEFAULT 'proposed', timestamp TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS mints (
          id INTEGER PRIMARY KEY, issue_number INTEGER NOT NULL, series TEXT NOT NULL,
          title TEXT NOT NULL, token_id TEXT, tx_hash TEXT, ipfs_image TEXT,
          ipfs_metadata TEXT, status TEXT NOT NULL DEFAULT 'draft',
          kdp_ready INTEGER NOT NULL DEFAULT 0, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);
        """)

init_db()

def math_formula(day: int):
    return {"day":day,"formula":" + ".join(SUPREME_MATH[int(x)] for x in str(day)),
            "digits":[int(x) for x in str(day)]}

def rarity(day: int):
    if day in {7,77,177,277,365}: return "GOD TIER"
    if day % 100 == 0: return "LEGENDARY"
    if day % 30 == 0: return "EPIC"
    if day % 7 == 0: return "RARE"
    if day % 3 == 0: return "UNCOMMON"
    return "COMMON"

def revenue_split(amount_cents: int):
    return {"treasury_cents":amount_cents*60//100,
            "creator_cents":amount_cents*20//100,
            "gaming_cents":amount_cents-(amount_cents*60//100)-(amount_cents*20//100)}

class Issue(BaseModel):
    issue_number: int = Field(ge=1)
    series: str = Field(min_length=1)
    title: str = Field(min_length=1)

@app.get("/health")
def health():
    return {"ok":True,"mode":"draft_only","timestamp":datetime.now(timezone.utc).isoformat()}

@app.get("/feed")
def feed(limit:int=Query(50,ge=1,le=100),before_id:int|None=None):
    with db() as c:
        if before_id is None:
            rows=c.execute("SELECT * FROM feed ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
        else:
            rows=c.execute("SELECT * FROM feed WHERE id < ? ORDER BY id DESC LIMIT ?",(before_id,limit)).fetchall()
    return {"items":[dict(r) for r in rows],"next_before_id":rows[-1]["id"] if len(rows)==limit else None}

@app.get("/revenue")
def revenue():
    with db() as c:
        rows=c.execute("SELECT * FROM revenue WHERE verified=1 ORDER BY id DESC LIMIT 100").fetchall()
        total=c.execute("SELECT COALESCE(SUM(amount_cents),0) FROM revenue WHERE verified=1 AND currency='USD'").fetchone()[0]
    return {"verified_usd_cents":total,"verified_usd":round(total/100,2),"entries":[dict(r) for r in rows]}

@app.get("/treasury")
def treasury():
    with db() as c:
        rows=c.execute("SELECT * FROM treasury_plans ORDER BY id DESC LIMIT 100").fetchall()
    return {"plans":[dict(r) for r in rows],"note":"Proposals only; no investments are executed."}

@app.get("/mints")
def mints():
    with db() as c:
        rows=c.execute("SELECT * FROM mints ORDER BY id DESC LIMIT 100").fetchall()
    return {"items":[dict(r) for r in rows],"note":"Drafts are not on-chain tokens."}

@app.get("/kdp/metadata")
def kdp_metadata():
    return [{"title":i["title"],"series":i["series"],"volume":i["issue_number"],
             "format":"print-edition metadata draft","status":"review_required"} for i in SEASON_1]

@app.get("/supreme-math/{day}")
def supreme_math(day:int):
    if not 0 <= day <= 365: raise HTTPException(400,"Day must be 0 through 365")
    return {**math_formula(day),"rarity":rarity(day)}

@app.post("/drafts/seed")
def seed_drafts():
    # This write endpoint is disabled on public deployments by default.
    if os.getenv("CAAVE_ALLOW_LOCAL_SEED") != "true":
        raise HTTPException(403,"Draft seeding disabled; enable only in a private environment.")
    with db() as c:
        for i in SEASON_1:
            exists=c.execute("SELECT id FROM mints WHERE series=? AND issue_number=?",
                             (i["series"],i["issue_number"])).fetchone()
            if not exists:
                c.execute("INSERT INTO mints(issue_number,series,title) VALUES(?,?,?)",
                          (i["issue_number"],i["series"],i["title"]))
    return {"status":"drafts_created","minted":False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=int(os.getenv("PORT","8002")))
