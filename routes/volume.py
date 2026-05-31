import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from volume.volume_control import (
    get_current_output_device_info,
    get_output_devices,
    get_volume,
    set_volume,
    switch_output_device,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class VolumeSetRequest(BaseModel):
    value: int = Field(..., ge=0, le=100)


class SwitchOutputRequest(BaseModel):
    target_device_id: str = Field(..., min_length=1)


def _compact_device_name(device_name: str) -> str:
    if "(" in device_name and ")" in device_name:
        short_name = device_name.split("(", maxsplit=1)[0].strip()
        if short_name:
            return short_name
    return device_name


@router.get("/")
def read_volume():
    volume = int(get_volume())
    device_info = get_current_output_device_info()
    device_name = _compact_device_name(device_info["name"])
    output_devices = get_output_devices()
    switch_targets = [
        {
            "id": item["id"],
            "name": _compact_device_name(item["name"]),
        }
        for item in output_devices
        if item["id"] != device_info["id"]
    ]
    logger.info("Volume requested: %d%%", volume)
    return {
        "volume": volume,
        "device_id": device_info["id"],
        "device_name": device_name,
        "switch_targets": switch_targets,
    }


@router.post("/")
def write_volume(body: VolumeSetRequest):
    set_volume(body.value)
    volume = int(get_volume())
    device_info = get_current_output_device_info()
    device_name = _compact_device_name(device_info["name"])
    logger.info("Volume set to %d%%", volume)
    return {
        "success": True,
        "volume": volume,
        "device_id": device_info["id"],
        "device_name": device_name,
    }


@router.post("/switch-output")
def write_switch_output(body: SwitchOutputRequest):
    current_device = get_current_output_device_info()
    switched = switch_output_device(
        current_device["id"],
        target_device_id=body.target_device_id,
    )
    logger.info("Output device switched to %s", switched["name"])
    return {
        "success": True,
        "volume": switched["volume"],
        "device_id": switched["id"],
        "device_name": _compact_device_name(switched["name"]),
    }
