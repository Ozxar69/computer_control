import functools
import logging

from aiogram import types

from client import is_api_available
from data import LOG_API_OFFLINE, PC_OFFLINE_ALERT

logger = logging.getLogger(__name__)


def _find_event(args) -> types.CallbackQuery | types.Message | None:
    for arg in args:
        if isinstance(arg, (types.CallbackQuery, types.Message)):
            return arg
    return None


def require_api(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        event = _find_event(args)
        if not await is_api_available():
            if event:
                logger.info(LOG_API_OFFLINE, event.from_user.id)
                if isinstance(event, types.CallbackQuery):
                    await event.answer(PC_OFFLINE_ALERT, show_alert=True)
            return
        return await func(*args, **kwargs)

    return wrapper
