import os
import warnings
from contextlib import contextmanager
from ctypes import POINTER, c_int, c_void_p, c_wchar_p, cast as ctypes_cast
from time import sleep
from typing import (
    Any,
    Iterator,
    Optional,
    Sequence,
    TypedDict,
    cast as typing_cast,
)

import comtypes
from comtypes import COMMETHOD, GUID, HRESULT, IUnknown
from dotenv import load_dotenv
from pycaw.api.mmdeviceapi import IMMDeviceEnumerator
from pycaw.constants import CLSID_MMDeviceEnumerator, DEVICE_STATE, EDataFlow, ERole
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

load_dotenv()


def _load_clsid_policy_config() -> GUID:
    raw_guid = os.getenv("CLSID_POLICY_CONFIG", "").strip()
    if not raw_guid:
        raise RuntimeError("CLSID_POLICY_CONFIG is not set in .env")
    return GUID(raw_guid)


def _load_iid_ipolicy_config() -> GUID:
    raw_guid = os.getenv("IID_IPOLICY_CONFIG", "").strip()
    if not raw_guid:
        raise RuntimeError("IID_IPOLICY_CONFIG is not set in .env")
    return GUID(raw_guid)


def _load_primary_output_device_ids() -> tuple[str, ...]:
    raw_ids = os.getenv("PRIMARY_OUTPUT_DEVICE_IDS", "")
    parsed_ids = [item.strip() for item in raw_ids.split(",") if item.strip()]
    return tuple(parsed_ids)


class DeviceInfo(TypedDict):
    id: str
    name: str


class SwitchResult(TypedDict):
    id: str
    name: str
    volume: int


def get_output_devices(
    preferred_device_ids: Optional[Sequence[str]] = None,
) -> list[DeviceInfo]:
    """Возвращает активные output-устройства (опционально из whitelist)."""

    with _com_scope():
        output_devices = _get_render_output_devices()
        preferred_ids = preferred_device_ids or _load_primary_output_device_ids()
        if preferred_ids:
            allowed_ids = set(preferred_ids)
            output_devices = [
                device for device in output_devices if device.id in allowed_ids
            ]
            ordered_devices: list[Any] = []
            for device_id in preferred_ids:
                device = next(
                    (item for item in output_devices if item.id == device_id),
                    None,
                )
                if device is not None:
                    ordered_devices.append(device)
            output_devices = ordered_devices

        result: list[DeviceInfo] = []
        for device in output_devices:
            device_name = getattr(device, "FriendlyName", None) or "Unknown device"
            result.append({"id": str(device.id), "name": str(device_name)})
        return result


class IPolicyConfig(IUnknown):
    """COM-интерфейс для смены default audio endpoint в Windows."""

    _iid_ = _load_iid_ipolicy_config()
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            "GetMixFormat",
            (["in"], c_wchar_p, "device_id"),
            (["out"], c_void_p, "format_ptr"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDeviceFormat",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_int, "is_default"),
            (["out"], c_void_p, "format_ptr"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "ResetDeviceFormat",
            (["in"], c_wchar_p, "device_id"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetDeviceFormat",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_void_p, "endpoint_format"),
            (["in"], c_void_p, "mix_format"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetProcessingPeriod",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_int, "is_default"),
            (["out"], c_void_p, "default_period"),
            (["out"], c_void_p, "minimum_period"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetProcessingPeriod",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_void_p, "period"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetShareMode",
            (["in"], c_wchar_p, "device_id"),
            (["out"], c_void_p, "mode"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetShareMode",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_void_p, "mode"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyValue",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_int, "is_fx_store"),
            (["in"], c_void_p, "key"),
            (["out"], c_void_p, "value"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetPropertyValue",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_int, "is_fx_store"),
            (["in"], c_void_p, "key"),
            (["in"], c_void_p, "value"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetDefaultEndpoint",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_int, "role"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetEndpointVisibility",
            (["in"], c_wchar_p, "device_id"),
            (["in"], c_int, "is_visible"),
        ),
    )


@contextmanager
def _com_scope() -> Iterator[None]:
    """Инициализирует COM в текущем потоке на время вызова."""

    comtypes.CoInitialize()
    try:
        yield
    finally:
        comtypes.CoUninitialize()


def _get_default_endpoint_volume() -> Any:
    """Возвращает COM-объект громкости текущего output-устройства."""

    speakers = AudioUtilities.GetSpeakers()
    with warnings.catch_warnings(record=False):
        warnings.simplefilter("ignore", UserWarning)
        audio_device = AudioUtilities.CreateDevice(speakers)
    return ctypes_cast(
        audio_device.EndpointVolume,
        POINTER(IAudioEndpointVolume),
    )


def _get_render_output_devices() -> list[Any]:
    """Возвращает список активных устройств воспроизведения."""

    enumerator = comtypes.CoCreateInstance(
        CLSID_MMDeviceEnumerator,
        IMMDeviceEnumerator,
        comtypes.CLSCTX_INPROC_SERVER,
    )
    enum_audio_endpoints = getattr(enumerator, "EnumAudioEndpoints")
    collection = enum_audio_endpoints(
        EDataFlow.eRender.value,
        DEVICE_STATE.ACTIVE.value,
    )
    count = collection.GetCount()

    devices = []
    with warnings.catch_warnings(record=False):
        warnings.simplefilter("ignore", UserWarning)
        for index in range(count):
            devices.append(AudioUtilities.CreateDevice(collection.Item(index)))
    return devices


def _set_default_output_device(device_id: str) -> None:
    """Назначает устройство default для Console/Multimedia/Communications."""

    policy_config = comtypes.CoCreateInstance(
        _load_clsid_policy_config(),
        interface=IPolicyConfig,
        clsctx=comtypes.CLSCTX_INPROC_SERVER,
    )
    set_default_endpoint = getattr(policy_config, "SetDefaultEndpoint")
    set_default_endpoint(device_id, ERole.eConsole.value)
    set_default_endpoint(device_id, ERole.eMultimedia.value)
    set_default_endpoint(device_id, ERole.eCommunications.value)


def get_volume() -> str:
    """Возвращает текущую системную громкость в процентах строкой."""

    with _com_scope():
        volume = _get_default_endpoint_volume()
        current_volume = str(int(volume.GetMasterVolumeLevelScalar() * 100))
        return current_volume


def set_volume(item: int) -> bool:
    """Устанавливает системную громкость в процентах (0-100)."""

    with _com_scope():
        volume = _get_default_endpoint_volume()
        item /= 100
        volume.SetMasterVolumeLevelScalar(item, None)
        return True


def get_current_output_device_info() -> DeviceInfo:
    """Возвращает id и имя текущего default output-устройства."""

    with _com_scope():
        current_device = AudioUtilities.GetSpeakers()
        current_device_id = current_device.GetId()

        with warnings.catch_warnings(record=False):
            warnings.simplefilter("ignore", UserWarning)
            wrapped_device = AudioUtilities.CreateDevice(current_device)

        current_device_name = "Unknown device"
        if wrapped_device and getattr(wrapped_device, "FriendlyName", None):
            current_device_name = wrapped_device.FriendlyName

        return {"id": current_device_id, "name": current_device_name}


def switch_output_device(
    current_device_id: str,
    preferred_device_ids: Optional[Sequence[str]] = None,
    target_device_id: Optional[str] = None,
) -> SwitchResult:
    """Переключает output-устройство и возвращает его id, имя и громкость."""

    with _com_scope():
        output_devices = _get_render_output_devices()
        if preferred_device_ids is None:
            preferred_device_ids = _load_primary_output_device_ids()
        if preferred_device_ids:
            allowed_ids = set(preferred_device_ids)
            output_devices = [
                device for device in output_devices if device.id in allowed_ids
            ]

        if not output_devices:
            raise RuntimeError("Нет доступных устройств вывода для переключения.")

        target_device: Optional[Any] = None
        if target_device_id:
            target_device = next(
                (device for device in output_devices if device.id == target_device_id),
                None,
            )
            if target_device is None:
                raise RuntimeError("Выбранное устройство недоступно.")
            if str(getattr(target_device, "id")) == current_device_id:
                raise RuntimeError("Устройство уже активно.")
        else:
            target_device = next(
                (
                    device
                    for device in output_devices
                    if device.id != current_device_id
                ),
                None,
            )
        if target_device is None and preferred_device_ids:
            ordered_ids = [
                device_id
                for device_id in preferred_device_ids
                if device_id != current_device_id
            ]
            for device_id in ordered_ids:
                target_device = next(
                    (
                        device
                        for device in output_devices
                        if device.id == device_id
                    ),
                    None,
                )
                if target_device is not None:
                    break
        if target_device is None:
            raise RuntimeError(
                "Не удалось найти другое активное устройство вывода."
            )

        target_device_id = str(getattr(target_device, "id"))
        _set_default_output_device(target_device_id)

        actual_device_info = None
        for _ in range(10):
            actual_device_info = get_current_output_device_info()
            if actual_device_info["id"] == target_device_id:
                break
            sleep(0.1)

        if (
            actual_device_info is None
            or actual_device_info["id"] != target_device_id
        ):
            raise RuntimeError(
                "Windows не переключила активное устройство вывода."
            )

        actual_device = next(
            (
                device
                for device in output_devices
                if device.id == actual_device_info["id"]
            ),
            None,
        )
        endpoint_volume = getattr(actual_device, "EndpointVolume", None)
        target_volume = 0
        get_master_scalar = getattr(
            endpoint_volume,
            "GetMasterVolumeLevelScalar",
            None,
        )
        if callable(get_master_scalar):
            scalar_value = typing_cast(float, get_master_scalar())
            target_volume = int(scalar_value * 100)

        target_name = actual_device_info["name"] or "Unknown device"
        return {
            "id": target_device_id,
            "name": target_name,
            "volume": target_volume,
        }


if __name__ == "__main__":
    current_device_info = get_current_output_device_info()
    print(f"Текущее устройство: {current_device_info['name']}")
    print(f"ID устройства: {current_device_info['id']}")

    # switched_device_info = switch_output_device(current_device_info["id"])
    # print(f"Переключено на устройство: {switched_device_info['name']}")
    # print(f"ID устройства: {switched_device_info['id']}")
    # print(f"Громкость устройства: {switched_device_info['volume']}%")
