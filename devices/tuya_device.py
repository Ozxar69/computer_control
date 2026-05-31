from tinytuya import BulbDevice, OutletDevice
import asyncio
import json
import os
import socket
from .base_device import AsyncBaseDevice
import logging


def _normalize_dps(raw) -> dict:
    """tinytuya иногда отдаёт dps как dict, иногда как JSON-строку; иначе — пустой dict."""
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


def _pick_main_switch_value(dps: dict) -> object:
    """
    Основной «вкл/выкл» у разных устройств Tuya сидит на разных DP.
    Порядок — от самых частых к редким.
    """
    if not isinstance(dps, dict) or not dps:
        return None
    for key in (1, "1", "switch_led", "switch_1", "switch", 20, "20", 101, "101"):
        if key in dps:
            return dps.get(key)
        sk = str(key)
        if sk in dps:
            return dps.get(sk)
    return None


class AsyncTuyaDevice(AsyncBaseDevice):
    def __init__(self, name: str, device_id: str, device_type: str, ip: str, local_key: str, version: float = 3.3):
        super().__init__(name, device_id, device_type, ip, version)
        self.local_key = local_key
        # Лампы (light) у Tuya часто отвечают на DP_QUERY и otherwise дают пустой dps с OutletDevice.
        if (device_type or "").lower() == "light":
            self._device = BulbDevice(device_id, ip, local_key, version=version)
        else:
            self._device = OutletDevice(device_id, ip, local_key)
            self._device.set_version(version)
        try:
            self._device.set_socketTimeout(10)
        except Exception:
            pass
        self.logger = logging.getLogger(f"TuyaDevice.{name}")

    def _fetch_status_sync(self) -> dict:
        """Синхронное чтение статуса с fallback для устройств с пустым dps."""
        dev = self._device
        try:
            dev.set_socketTimeout(10)
        except Exception:
            pass

        def _usable_dps(data: object) -> bool:
            if not isinstance(data, dict):
                return False
            dps = data.get("dps")
            return isinstance(dps, dict) and len(dps) > 0

        data = dev.status()
        if not isinstance(data, dict):
            return {}

        if _usable_dps(data):
            return data

        # Запросить обновление конкретных DP (часто нужно для 3.3/3.4).
        try:
            dev.updatedps([1, 2, 3, 4, 5, 9, 11, 20, 21, 22, 38, 51, 101])
            data2 = dev.status()
            if isinstance(data2, dict) and _usable_dps(data2):
                return data2
        except Exception:
            pass

        # Последний шанс — brute-force DP (долго). Только для света или по явному флагу.
        if (self.device_type or "").lower() == "light" or os.getenv(
            "TUYA_FORCE_DETECT_DPS", ""
        ).strip() in ("1", "true", "yes"):
            try:
                dev.detect_available_dps()
                data3 = dev.status()
                if isinstance(data3, dict):
                    return data3
            except Exception:
                pass

        return data

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
                self._async_execute(self._fetch_status_sync),
                timeout=25.0,
            )
            return status or {}
        except Exception:
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
            debug_device_id = os.getenv("TUYA_DEBUG_DEVICE_ID", "").strip()
            # После turn_on/turn_off устройство иногда отдаёт ещё "старый" status,
            # либо dps может появиться чуть позже. Подождём и перечитаем несколько раз.
            status = {}
            for _ in range(3):
                status = await self.status()
                if isinstance(status, dict) and status.get("dps"):
                    break
                await asyncio.sleep(0.3)

            raw_dps = status.get("dps") if isinstance(status, dict) else None
            dps = _normalize_dps(raw_dps)

            # tinytuya ERR_KEY_OR_VER = 914 — неверный local key или версия протокола (3.3/3.4/3.5)
            err_code = None
            if isinstance(status, dict) and status.get("Err") is not None:
                err_code = str(status.get("Err"))
            if (not dps or len(dps) == 0) and err_code == "914":
                self.logger.warning(
                    "Tuya %s (%s): Err=914 — проверь DEVICE_*_KEY и DEVICE_*_VERSION в .env",
                    self.name,
                    self.device_id,
                )
                return {
                    "name": self.name,
                    "device_id": self.device_id,
                    "is_online": await self.is_online_async(),
                    "switches": None,
                    "has_switch_2": False,
                    "relay_status": None,
                    "tuya_err": "914",
                    "tuya_error_detail": status.get("Error") if isinstance(status, dict) else None,
                }

            if debug_device_id and self.device_id == debug_device_id:
                # Точечная диагностика: какие DPS и значения возвращает конкретное устройство.
                sk = list(status.keys()) if isinstance(status, dict) else None
                err = status.get("Err") if isinstance(status, dict) else None
                self.logger.warning(
                    "TUYA_DEBUG device=%s id=%s status_keys=%s Err=%s dps=%r main_pick=%r",
                    self.name,
                    self.device_id,
                    sk,
                    err,
                    dps,
                    _pick_main_switch_value(dps),
                )

            def _dps_get(dp: dict, key: int) -> object:
                # tinytuya иногда отдаёт ключи как int (1,2), иногда как str ('1','2')
                if not isinstance(dp, dict):
                    return None
                if str(key) in dp:
                    return dp.get(str(key))
                return dp.get(key)

            def _to_bool(v: object) -> bool:
                if v is None:
                    return False
                if isinstance(v, bool):
                    return v
                if isinstance(v, (int, float)):
                    return v != 0
                if isinstance(v, str):
                    vv = v.strip().lower()
                    if vv in ("1", "true", "on", "yes"):
                        return True
                    if vv in ("0", "false", "off", "no", ""):
                        return False
                    try:
                        return float(vv) != 0
                    except Exception:
                        return bool(v)
                return bool(v)

            main_val = _pick_main_switch_value(dps)
            if main_val is None:
                main_val = _dps_get(dps, 1)

            return {
                'name': self.name,
                'device_id': self.device_id,
                'is_online': await self.is_online_async(),
                'switches': {
                    'switch_1': _to_bool(main_val),
                    'switch_2': _to_bool(_dps_get(dps, 2)),
                },
                'has_switch_2': (2 in dps) or ('2' in dps),
                'relay_status': dps.get("relay_status"),
            }
        except Exception as e:
            self.logger.error(f"Failed to get device info: {str(e)}")
            return None

    async def is_on(self, switch_num: int = 1) -> bool:
        """Проверяет состояние переключателя"""
        status = await self.status()
        dps = _normalize_dps(status.get("dps") if isinstance(status, dict) else None)
        if switch_num != 1:
            v = dps.get(str(switch_num), dps.get(switch_num))
        else:
            v = _pick_main_switch_value(dps)
            if v is None:
                v = dps.get("1", dps.get(1))
        if v is None:
            return False
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            vv = v.strip().lower()
            if vv in ("1", "true", "on", "yes"):
                return True
            if vv in ("0", "false", "off", "no", ""):
                return False
        return bool(v)