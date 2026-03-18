import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from screen.screen_control import get_brightness, set_brightness

logger = logging.getLogger(__name__)
router = APIRouter()


class BrightnessSetRequest(BaseModel):
    value: int = Field(..., ge=0, le=100)


def _safe_get_brightness() -> int:
    try:
        return get_brightness()[0]
    except Exception:
        return -1


@router.get("/")
def read_brightness():
    brightness = _safe_get_brightness()
    logger.info("Brightness requested: %d%%", brightness)
    return {"brightness": brightness}


@router.post("/")
def write_brightness(body: BrightnessSetRequest):
    set_brightness(body.value)
    brightness = _safe_get_brightness()
    actual = brightness if brightness != -1 else body.value
    logger.info("Brightness set to %d%%", actual)
    return {"success": True, "brightness": actual}
