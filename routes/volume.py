import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from volume.volume_control import get_volume, set_volume

logger = logging.getLogger(__name__)
router = APIRouter()


class VolumeSetRequest(BaseModel):
    value: int = Field(..., ge=0, le=100)


@router.get("/")
def read_volume():
    volume = int(get_volume())
    logger.info("Volume requested: %d%%", volume)
    return {"volume": volume}


@router.post("/")
def write_volume(body: VolumeSetRequest):
    set_volume(body.value)
    volume = int(get_volume())
    logger.info("Volume set to %d%%", volume)
    return {"success": True, "volume": volume}
