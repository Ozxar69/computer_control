from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from data import PERSENT

# Получаем устройство вывода звука
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def get_volume():
    current_volume = str(int(volume.GetMasterVolumeLevelScalar() * PERSENT))
    return current_volume


def set_volume(item):
    # Устанавливаем уровень громкости (от 0.0 до 1.0)
    item /= 100
    volume.SetMasterVolumeLevelScalar(item, None)
    return True
