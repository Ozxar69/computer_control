import os
from datetime import datetime, timedelta

import pytz

_flag = False
_end_time = None
_MOSCOW_TZ = pytz.timezone("Europe/Moscow")


def set_shutdown_timer(minutes: int) -> dict:
    global _flag, _end_time
    seconds = minutes * 60
    os.system(f'shutdown -s -t {seconds} -c " "')
    _flag = True
    _end_time = datetime.now(_MOSCOW_TZ) + timedelta(minutes=minutes)
    return {"success": True, "finish_time": _end_time.strftime("%H:%M")}


def check_shutdown_status() -> bool:
    return _flag


def cancel_shutdown_timer() -> bool:
    global _flag, _end_time
    os.system("shutdown /a")
    _flag = False
    _end_time = None
    return True


def get_shutdown_info() -> dict:
    if not _flag or _end_time is None:
        return {"shutdown_active": False, "finish_time": None, "remaining": None}

    remaining = _end_time - datetime.now(_MOSCOW_TZ)
    if remaining.total_seconds() <= 0:
        return {"shutdown_active": False, "finish_time": None, "remaining": None}

    mins, secs = divmod(remaining.total_seconds(), 60)
    return {
        "shutdown_active": True,
        "finish_time": _end_time.strftime("%H:%M"),
        "remaining": f"{int(mins):02}:{int(secs):02}",
    }
