from aiogram import types
from aiogram.filters import Command

from bot.buttons import (
    get_change_brightness_buttons,
    get_change_volume_buttons,
    get_user_buttons,
get_change_shutdown_buttons,
get_cancel_shutdown_buttons,
)
from utils.utils import finish_time
from utils.timer import timer
from data import (
    CANCEL_BUTTON_CLICK,
    CANCEL_CONFIRM_TEXT,
    CHANGE_BRIGHTNESS,
    CHANGE_TO_BRIGHTNESS,
    CHANGE_TO_VOLUME,
    CHANGE_VOLUME,
    FALSE_TEXT,
    MONITOR,
    MONITOR_BUTTON_CLICK,
    START_BUTTON,
    START_REPLAY,
    SUCCESS_BRIGHTNESS_MESSAGE,
    SUCCESS_BRIGHTNESS_TEXT,
    SUCCESS_TEXT,
    SUCCESS_VOLUME_TEXT,
    VOLUME,
    VOLUME_BUTTON_CLICK,
POWER_BUTTON_CLICK,
POWER,
CHANGE_TO_POWER,
CHANGE_TO_POWER_TIMER,
ACCESS_DENIED,
CHANGE_SHUTDOWN,
SUCCESS_SHUTDOWN_TEXT,
SUCCESS_SHUTDOWN_MESSAGE,
CANCEL_SHUTDOWN,
SUCCESS_CANCEL_SHUTDOWN_MESSAGE,
SUCCESS_CANCEL_SHUTDOWN_TEXT,

)
from system.power_management import check_shutdown_status, set_shutdown_timer, cancel_shutdown_timer
from screen.screen_control import get_brightness, set_brightness
from volume.volume_control import get_volume, set_volume
from admin import check_user


def register_handlers(dp):

    @dp.message(Command(START_BUTTON))
    async def send_welcome(message: types.Message):
        user_id = message.from_user.id
        if check_user(user_id):
            reply_markup = get_user_buttons()
            await message.reply(START_REPLAY, reply_markup=reply_markup)
        else:
            await message.reply(ACCESS_DENIED)

    @dp.callback_query(lambda c: c.data == VOLUME_BUTTON_CLICK)
    async def handle_button_click(callback_query: types.CallbackQuery):
        volume = get_volume()
        await callback_query.answer(VOLUME)
        await callback_query.message.delete()
        reply_markup = get_change_volume_buttons()
        await callback_query.message.answer(
            CHANGE_TO_VOLUME.format(volume=volume), reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data == CANCEL_BUTTON_CLICK)
    async def cancel_button(callback_query: types.CallbackQuery):
        await callback_query.answer(CANCEL_CONFIRM_TEXT)
        await callback_query.message.delete()
        reply_markup = get_user_buttons()
        await callback_query.message.answer(
            text=START_REPLAY, reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_VOLUME))
    async def change_volume(callback_query: types.CallbackQuery):
        volume_level = callback_query.data.split("_")[-1]
        await callback_query.message.delete()
        changing_volume = set_volume(int(volume_level))
        reply_markup = get_user_buttons()
        if changing_volume:
            volume_level = get_volume()
            await callback_query.answer(
                SUCCESS_VOLUME_TEXT.format(volume=volume_level)
            )

            await callback_query.message.answer(
                text=SUCCESS_TEXT.format(volume=volume_level),
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )

    @dp.callback_query(lambda c: c.data == MONITOR_BUTTON_CLICK)
    async def handle_button_click(callback_query: types.CallbackQuery):
        brightness = get_brightness()
        await callback_query.answer(MONITOR)
        await callback_query.message.delete()
        reply_markup = get_change_brightness_buttons()
        await callback_query.message.answer(
            CHANGE_TO_BRIGHTNESS.format(brightness=brightness[0]),
            reply_markup=reply_markup,
        )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_BRIGHTNESS))
    async def change_volume(callback_query: types.CallbackQuery):
        brightness_level = callback_query.data.split("_")[-1]
        await callback_query.message.delete()
        changing_brightness = set_brightness(int(brightness_level))
        reply_markup = get_user_buttons()
        if changing_brightness:
            brightness_level = get_brightness()
            await callback_query.answer(
                SUCCESS_BRIGHTNESS_TEXT.format(brightness=brightness_level[0])
            )

            await callback_query.message.answer(
                text=SUCCESS_BRIGHTNESS_MESSAGE.format(
                    brightness=brightness_level[0]
                ),
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )

    @dp.callback_query(lambda c: c.data == POWER_BUTTON_CLICK)
    async def handle_button_click(callback_query: types.CallbackQuery):
        shutdown_status = check_shutdown_status()
        await callback_query.answer(POWER)
        await callback_query.message.delete()
        print(shutdown_status)
        if not shutdown_status:

            reply_markup = get_change_shutdown_buttons()
            await callback_query.message.answer(
                CHANGE_TO_POWER, reply_markup=reply_markup
            )
        else:
            reply_markup = get_cancel_shutdown_buttons()

            await callback_query.message.answer(
                CHANGE_TO_POWER_TIMER.format(time=timer.check_timer()),
                reply_markup=reply_markup
            )


    @dp.callback_query(lambda c: c.data.startswith(CHANGE_SHUTDOWN))
    async def change_shutdown(callback_query: types.CallbackQuery):
        shutdown_time = callback_query.data.split("_")[-1]
        print(shutdown_time)
        await callback_query.message.delete()

        set_shutdown = set_shutdown_timer(int(shutdown_time))
        timer.start_timer(int(shutdown_time))
        reply_markup = get_user_buttons()
        if set_shutdown:
            await callback_query.answer(
                SUCCESS_SHUTDOWN_TEXT
            )
            finish = finish_time(int(shutdown_time))
            await callback_query.message.answer(
                text=SUCCESS_SHUTDOWN_MESSAGE.format(
                    finish_time=finish
                ),
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )

    @dp.callback_query(lambda c: c.data.startswith(CANCEL_SHUTDOWN))
    async def cancel_shutdown(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        reply_markup = get_user_buttons()
        cancel = cancel_shutdown_timer()
        if cancel:
            await callback_query.answer(
                SUCCESS_CANCEL_SHUTDOWN_TEXT
            )
            await callback_query.message.answer(
                text=SUCCESS_CANCEL_SHUTDOWN_MESSAGE,
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )
