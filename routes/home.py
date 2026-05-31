import asyncio
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from devices import load_devices, load_devices_with_status

logger = logging.getLogger(__name__)
router = APIRouter()


class ToggleRequest(BaseModel):
    switch: int = 1


@router.get("/devices")
async def get_devices():
    results = await load_devices_with_status()
    devices_list = [
        {
            "id": d.device_id,
            "name": d.name,
            "type": d.device_type,
            "is_online": online,
        }
        for d, online in results
    ]
    logger.info("Devices listed: %d total", len(devices_list))
    return devices_list


@router.get("/devices/{device_id}")
async def get_device(device_id: str):
    devices = load_devices()
    device = next((d for d in devices if d.device_id == device_id), None)
    if not device:
        logger.warning("Device not found: %s", device_id)
        raise HTTPException(status_code=404, detail="Device not found")
    info = await device.get_device_info()
    logger.info("Device info: %s → online=%s", device.name, info.get("is_online"))
    return info


@router.post("/devices/{device_id}/toggle")
async def toggle_device(device_id: str, body: ToggleRequest):
    devices = load_devices()
    device = next((d for d in devices if d.device_id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    if body.switch == 1:
        if await device.is_on():
            await device.turn_off()
        else:
            await device.turn_on()
    elif body.switch == 2:
        status = await device.status()
        dps = status.get("dps", {}) if isinstance(status, dict) else {}
        # tinytuya может отдавать ключи как int (2) или как str ('2')
        current_val = dps.get("2", dps.get(2, False))
        current = bool(current_val)
        await device._async_execute(
            lambda: device._device.set_value(2, not current)
        )

    logger.info("Device toggled: %s switch %d", device.name, body.switch)
    # Устройства Tuya не всегда моментально отдают обновлённый status.
    # Дадим им немного времени, иначе бот может показать "старое" состояние
    # и получить Telegram error "message is not modified".
    await asyncio.sleep(0.8)
    return await device.get_device_info()
