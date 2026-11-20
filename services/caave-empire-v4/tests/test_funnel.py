import os,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ["CAAVE_FUNNEL_DB"]=str(Path(tempfile.mkdtemp())/"leads.db")
from fastapi.testclient import TestClient
from funnel_api import app
client=TestClient(app)
def test_landing():
    assert client.get("/funnel").status_code==200
def test_consent_required():
    assert client.post("/leads/opt-in",json={"email":"test@example.com","consent":False}).status_code==422
def test_optin_records_without_sending():
    r=client.post("/leads/opt-in",json={"email":"test@example.com","consent":True,"source":"youtube"})
    assert r.status_code==202 and r.json()["emails_sent"] is False
def test_metrics_private():
    assert client.get("/funnel/metrics").status_code==403
def test_redirect_tracks_without_claiming_purchase():
    r=client.get("/go/shopify?source=youtube",follow_redirects=False)
    assert r.status_code==302 and r.headers["location"].startswith("https://beverlyandsons.com/")
