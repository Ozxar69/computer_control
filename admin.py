import os
from functools import wraps

from aiogram import types
from dotenv import load_dotenv

from data import ACCESS_DENIED, ADMIN_IDS

load_dotenv()

ADMIN = os.getenv(ADMIN_IDS)


def acsess(func):
    @wraps(func)
    async def decorated(*args, **kwargs):
        callback_query = None
        message = None
        for arg in args:
            if isinstance(arg, types.CallbackQuery):
                callback_query = arg
                message = callback_query
                break
            elif isinstance(arg, types.Message):
                message = arg
                break

        if not message and not callback_query:
            return ACCESS_DENIED

        user_id = message.from_user.id
        print(user_id)
        if user_id == int(ADMIN):
            return await func(*args, **kwargs)
        else:
            if callback_query:
                await callback_query.answer(ACCESS_DENIED)
            else:
                await message.reply(ACCESS_DENIED)
            return

    return decorated
