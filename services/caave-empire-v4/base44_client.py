"""Read-only-by-default Base44 client. Never logs credentials."""
import os
from urllib.parse import quote
import httpx

class Base44Client:
    def __init__(self, api_key=None, transport=None):
        self.api_key = api_key if api_key is not None else os.getenv("BASE44_API_KEY")
        self.transport = transport

    async def fetch_entities(self, app_id, entity_type, filters=None):
        if not self.api_key:
            raise RuntimeError("BASE44_API_KEY is not configured")
        if not app_id.isalnum() or not entity_type.replace("_","").isalnum():
            raise ValueError("Invalid Base44 identifier")
        async with httpx.AsyncClient(timeout=15, transport=self.transport) as client:
            response = await client.get(
                f"https://app.base44.com/api/apps/{quote(app_id)}/entities/{quote(entity_type)}",
                headers={"api_key": self.api_key, "Accept":"application/json"},
                params=filters or {})
            response.raise_for_status()
            return response.json()
