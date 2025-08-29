from tinytuya import OutletDevice
import asyncio
import socket
from .base_device import AsyncBaseDevice
import logging


class AsyncTuyaDevice(AsyncBaseDevice):
    def __init__(self, name: str, device_id: str, device_type: str, ip: str, local_key: str, version: float = 3.3):
        super().__init__(name, device_id, device_type, ip, version)
        self.local_key = local_key
        self._device = OutletDevice(device_id, ip, local_key)
        self._device.set_version(version)
        self.logger = logging.getLogger(f"TuyaDevice.{name}")

    async def _check_port(self, ip: str, port: int = 6668, timeout: float = 1.0) -> bool:
        """Асинхронная проверка доступности порта устройства"""
        try:
            loop = asyncio.get_event_loop()
            conn = asyncio.open_connection(ip, port)
            _, writer = await asyncio.wait_for(conn, timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False

    def is_online(self) -> bool:
        """Синхронная проверка - просто пинг устройства"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.ip, 6668))
            sock.close()
            return result == 0
        except:
            return False

    async def is_online_async(self) -> bool:
        """Асинхронная проверка доступности устройства"""
        return await self._check_port(self.ip)

    async def status(self) -> dict:
        """Получаем статус устройства"""
        try:
            status = await asyncio.wait_for(
                self._async_execute(self._device.status),
                timeout=3.0
            )
            return status or {}
        except:
            return {}

    async def turn_on(self):
        if await self.is_online_async():
            await self._async_execute(self._device.turn_on)

    async def turn_off(self):
        if await self.is_online_async():
            await self._async_execute(self._device.turn_off)

    async def get_device_info(self) -> dict:
        """Получает полную информацию об устройстве"""
        try:
            status = await self.status()
            return {
                'name': self.name,
                'device_id': self.device_id,
                'is_online': await self.is_online_async(),
                'switches': {
                    'switch_1': status.get('dps', {}).get('1'),
                    'switch_2': status.get('dps', {}).get('2'),
                },
                'has_switch_2': '2' in status.get('dps', {}),
                'relay_status': status.get('dps', {}).get('relay_status')
            }
        except Exception as e:
            self.logger.error(f"Failed to get device info: {str(e)}")
            return None

    async def is_on(self, switch_num: int = 1) -> bool:
        """Проверяет состояние переключателя"""
        status = await self.status()
        return bool(status.get('dps', {}).get(str(switch_num)))