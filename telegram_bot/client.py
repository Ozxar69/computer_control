import logging
import os

import httpx

logger = logging.getLogger(__name__)

FASTAPI_URL = os.getenv("FASTAPI_URL")
_API_KEY = os.getenv("CC_API_KEY")
_TIMEOUT = 5.0

if not FASTAPI_URL:
    raise RuntimeError("FASTAPI_URL env var is not set")
if not _API_KEY:
    raise RuntimeError("CC_API_KEY env var is not set")


def _headers() -> dict:
    return {"X-API-Key": _API_KEY}


async def api_get(path: str) -> dict:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            f"{FASTAPI_URL}{path}", headers=_headers(), timeout=_TIMEOUT
        )
        response.raise_for_status()
        return response.json()


async def api_post(path: str, data: dict = None) -> dict:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(
            f"{FASTAPI_URL}{path}",
            json=data or {},
            headers=_headers(),
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()


async def api_delete(path: str) -> dict:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.delete(
            f"{FASTAPI_URL}{path}", headers=_headers(), timeout=_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
