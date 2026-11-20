import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ["CAAVE_V4_DB"]=":memory:"
from fastapi.testclient import TestClient
from api import app
from main import split_cents
from checkout import create_checkout
import pytest

client=TestClient(app)

def test_health():
    assert client.get("/health").json()["ok"] is True

def test_dashboard():
    r=client.get("/dashboard")
    assert r.status_code==200
    assert "CAAVE EMPIRE" in r.text

def test_checkout_requires_admin():
    assert client.post("/checkout/teach-001").status_code==403

def test_checkout_rejects_unknown_asset(monkeypatch):
    monkeypatch.setenv("CAAVE_ADMIN_TOKEN","test-only-token")
    assert client.post("/checkout/does-not-exist",headers={"x-caave-admin-token":"test-only-token"}).status_code==404

def test_checkout_does_not_run_without_secrets(monkeypatch):
    monkeypatch.setenv("CAAVE_ADMIN_TOKEN","test-only-token")
    monkeypatch.delenv("STRIPE_SECRET_KEY",raising=False)
    assert client.post("/checkout/teach-001",headers={"x-caave-admin-token":"test-only-token"}).status_code==503

def test_webhook_rejects_missing_signature():
    assert client.post("/stripe-webhook",content=b"{}").status_code==400

def test_revenue_starts_zero():
    assert client.get("/revenue").json()["verified_usd"]==0

def test_split_rounding():
    assert sum(v for k,v in split_cents(101).items() if k.endswith("_cents"))==101

def test_checkout_requires_https(monkeypatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY","test-only-not-real")
    with pytest.raises(ValueError):
        create_checkout({"title":"Demo","price_cents":999},asset_id="demo",success_url="http://invalid",cancel_url="https://example.com/cancel")
