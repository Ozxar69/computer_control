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
    requested = body.value
    try:
        # Иногда `screen_brightness_control` кидает COM/WMI исключение на внешнем мониторе,
        # при этом яркость успевает реально поменяться.
        set_brightness(requested)
        set_failed = False
    except Exception as e:
        set_failed = True
        logger.warning("Failed to set brightness via WMI/COM: %s", e)

    # Не вызываем `get_brightness()` в POST, чтобы не зависеть от скорости/стабильности WMI.
    # Бот и так показывает "requested" значение, а физическое изменение яркости происходит уже в момент set.
    logger.info(
        "Brightness set to %d%% (requested=%d%%, set_failed=%s)",
        requested,
        requested,
        set_failed,
    )
    return {"success": not set_failed, "brightness": requested}
