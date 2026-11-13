"""FastAPI application entry point.

Provides a health check endpoint that also returns a value read from a simple in‑memory store.
"""

from fastapi import FastAPI
from .db import get_database_value
from fastapi.staticfiles import StaticFiles

# Mount static files (frontend) at root
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

app = FastAPI()

@app.get("/api/health")
async def health() -> dict:
    """Return health status together with a sample value from the "database".

    The value is fetched from :func:`backend.app.db.get_database_value` which
    currently returns a static integer but can be replaced with a real DB query.
    """
    return {
        "status": "healthy",
        "version": "1.0.0-mvp",
        "db_value": get_database_value(),
    }
