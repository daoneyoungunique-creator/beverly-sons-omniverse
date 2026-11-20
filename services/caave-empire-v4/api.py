"""Deployable ASGI entrypoint. Keeps existing main.py routes intact."""
from main import app
from dashboard import router
from checkout import create_checkout
from fastapi import HTTPException, Header
import os

app.include_router(router)

@app.post("/checkout/{asset_id}")
def checkout(asset_id: str, x_caave_admin_token: str | None = Header(default=None)):
    import secrets
    configured = os.getenv("CAAVE_ADMIN_TOKEN")
    if not configured or not x_caave_admin_token or not secrets.compare_digest(x_caave_admin_token,configured):
        raise HTTPException(403,"Authorized operator required")
    from main import IP_CATALOG
    asset = next((a for a in IP_CATALOG if a["id"] == asset_id),None)
    if asset is None:
        raise HTTPException(404,"Unknown asset")
    try:
        return create_checkout(asset,asset_id=asset_id)
    except (RuntimeError,ValueError):
        raise HTTPException(503,"Checkout is not configured")
