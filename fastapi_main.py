import copy
import json
import logging
import os
import queue
import threading
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.config import LOGGING_CONFIG as _UVICORN_LOG_CONFIG

load_dotenv()

from routes.volume import router as volume_router
from routes.brightness import router as brightness_router
from routes.keyboard import router as keyboard_router
from routes.power import router as power_router
from routes.home import router as home_router

SEQ_URL = os.getenv("SEQ_URL")
API_KEY = os.getenv("CC_API_KEY")

if not SEQ_URL:
    raise RuntimeError("SEQ_URL env var is not set")
if not API_KEY:
    raise RuntimeError("CC_API_KEY env var is not set")


class SeqHandler(logging.Handler):
    def __init__(self, url: str, app_name: str = ""):
        super().__init__()
        self._url = f"{url}/api/events/raw"
        self._app = app_name
        self._q: queue.Queue = queue.Queue()
        self._session = requests.Session()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def emit(self, record: logging.LogRecord):
        self._q.put_nowait(record)

    def _worker(self):
        while True:
            record = self._q.get()
            try:
                event: dict = {
                    "@t": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
                    "@mt": record.getMessage(),
                    "@l": record.levelname,
                    "Logger": record.name,
                }
                if self._app:
                    event["Application"] = self._app
                if record.exc_info:
                    event["@x"] = self.formatException(record.exc_info)
                self._session.post(
                    self._url,
                    data=json.dumps(event) + "\n",
                    headers={"Content-Type": "application/vnd.serilog.clef"},
                    timeout=3,
                )
            except Exception:
                pass


_seq_handler = SeqHandler(SEQ_URL, app_name="cc.fastapi")
_seq_handler.setLevel(logging.INFO)
_root = logging.getLogger()
_root.setLevel(logging.INFO)
_root.addHandler(_seq_handler)

logger = logging.getLogger(__name__)


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        key = request.headers.get("X-API-Key", "")
        if key != API_KEY:
            logger.warning(
                "Unauthorized request from %s to %s",
                request.client.host,
                request.url.path,
            )
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.getLogger("screen_brightness_control").setLevel(logging.ERROR)
    logger.info("ComputerControl FastAPI service started on port %s", os.getenv("FASTAPI_PORT"))
    yield
    logger.info("ComputerControl FastAPI service stopped")


app = FastAPI(title="ComputerControl API", version="1.0.0", lifespan=lifespan)
app.add_middleware(ApiKeyMiddleware)

app.include_router(volume_router, prefix="/volume", tags=["volume"])
app.include_router(brightness_router, prefix="/brightness", tags=["brightness"])
app.include_router(keyboard_router, prefix="/keyboard", tags=["keyboard"])
app.include_router(power_router, prefix="/power", tags=["power"])
app.include_router(home_router, prefix="/home", tags=["home"])


if __name__ == "__main__":
    _port = os.getenv("FASTAPI_PORT")
    if not _port:
        raise RuntimeError("FASTAPI_PORT env var is not set")
    _log_config = copy.deepcopy(_UVICORN_LOG_CONFIG)
    _log_config["disable_existing_loggers"] = False
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(_port),
        access_log=False,
        log_config=_log_config,
    )
