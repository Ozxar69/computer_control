import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from system.power_management import (
    cancel_shutdown_timer,
    get_shutdown_info,
    set_shutdown_timer,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class ShutdownRequest(BaseModel):
    minutes: int = Field(..., ge=1)


@router.get("/")
def get_power():
    info = get_shutdown_info()
    if info["shutdown_active"]:
        logger.info("Shutdown status: active, remaining=%s", info["remaining"])
    else:
        logger.info("Shutdown status: inactive")
    return info


@router.post("/shutdown")
def do_shutdown(body: ShutdownRequest):
    result = set_shutdown_timer(body.minutes)
    logger.info("Shutdown timer set: %d min", body.minutes)
    return result


@router.delete("/shutdown")
def cancel_shutdown():
    cancel_shutdown_timer()
    logger.info("Shutdown cancelled")
    return {"success": True}
