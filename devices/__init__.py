import asyncio
import os
from dotenv import load_dotenv
from .tuya_device import AsyncTuyaDevice

load_dotenv()


def load_devices():
    devices = []
    i = 1
    while True:
        name = os.getenv(f"DEVICE_{i}_NAME")
        if not name:
            break

        devices.append(AsyncTuyaDevice(
            name=name,
            device_id=os.getenv(f"DEVICE_{i}_ID"),
            device_type=os.getenv(f"DEVICE_{i}_TYPE", "outlet"),
            ip=os.getenv(f"DEVICE_{i}_IP"),
            local_key=os.getenv(f"DEVICE_{i}_KEY"),
            version=float(os.getenv(f"DEVICE_{i}_VERSION", 3.3))
        ))
        i += 1
    return devices


async def load_devices_with_status():
    """Загружает устройства и сразу проверяет их статус параллельно"""
    devices = load_devices()

    async def check_device(device):
        return device, await device.is_online_async()

    results = await asyncio.gather(*[check_device(d) for d in devices])
    return results


async def async_load_devices():
    """Асинхронная загрузка устройств"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_devices)
