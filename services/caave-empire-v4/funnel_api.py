"""CAAVE Empire v4 API with opt-in and tracked organic product links."""
from api import app
from funnel import router
app.include_router(router)
