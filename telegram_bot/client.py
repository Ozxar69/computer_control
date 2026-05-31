import logging
import os

import httpx

logger = logging.getLogger(__name__)

FASTAPI_URL = os.getenv("FASTAPI_URL")
_API_KEY = os.getenv("CC_API_KEY")
_TIMEOUT = 15.0

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
        try:
            response.raise_for_status()
        except Exception as e:
            # Добавляем контекст, чтобы по логам было понятно, что вернул FastAPI
            logger.error(
                "api_post failed: url=%s status=%s error=%s body=%s",
                str(response.url),
                response.status_code,
                type(e).__name__,
                response.text[:500],
            )
            raise

        try:
            return response.json()
        except Exception as e:
            logger.error(
                "api_post JSON decode error: url=%s status=%s error=%s body=%s",
                str(response.url),
                response.status_code,
                type(e).__name__,
                response.text[:500],
            )
            raise


async def api_delete(path: str) -> dict:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.delete(
            f"{FASTAPI_URL}{path}", headers=_headers(), timeout=_TIMEOUT
        )
        response.raise_for_status()
        return response.json()


_HEALTH_TIMEOUT = 3.0


async def is_api_available() -> bool:
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                f"{FASTAPI_URL}/health",
                headers=_headers(),
                timeout=_HEALTH_TIMEOUT,
            )
            return response.status_code == 200
    except Exception:
        return False
