import asyncio
from abc import ABC, abstractmethod
import logging


class AsyncBaseDevice(ABC):
    def __init__(self, name: str, device_id: str, device_type: str, ip: str, version: float):
        self.name = name
        self.device_id = device_id
        self.device_type = device_type
        self.ip = ip
        self.version = version
        self.logger = logging.getLogger(f"Device_{name}")

    async def _async_execute(self, method, *args):
        """Универсальный метод для асинхронного вызова синхронных функций"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, method, *args)

    @abstractmethod
    async def turn_on(self):
        pass

    @abstractmethod
    async def turn_off(self):
        pass

    @abstractmethod
    async def status(self) -> dict:
        pass

    @abstractmethod
    def is_online(self) -> bool:
        """Синхронная проверка статуса (обязательная)"""
        pass

    @abstractmethod
    async def is_online_async(self) -> bool:
        """Асинхронная проверка статуса (обязательная)"""
        pass
