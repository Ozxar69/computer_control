from aiogram import types
from aiogram.filters import Command

from admin import acsess
from bot.buttons import (
    get_cancel_shutdown_buttons,
    get_change_brightness_buttons,
    get_change_shutdown_buttons,
    get_change_volume_buttons,
    get_keyboard_buttons,
    get_user_buttons,
)
from data import (
    CANCEL_BUTTON_CLICK,
    CANCEL_CONFIRM_TEXT,
    CANCEL_SHUTDOWN,
    CHANGE_BRIGHTNESS,
    CHANGE_SHUTDOWN,
    CHANGE_TO_BRIGHTNESS,
    CHANGE_TO_KEYBOARD,
    CHANGE_TO_POWER,
    CHANGE_TO_POWER_TIMER,
    CHANGE_TO_VOLUME,
    CHANGE_VOLUME,
    FALSE_TEXT,
    KEYBOARD,
    KEYBOARD_BUTTON_CLICK,
    MONITOR,
    MONITOR_BUTTON_CLICK,
    POWER,
    POWER_BUTTON_CLICK,
    SPACE_BUTTON_TEXT,
    SPACE_CLICK,
    START_BUTTON,
    START_REPLAY,
    SUCCESS_BRIGHTNESS_MESSAGE,
    SUCCESS_BRIGHTNESS_TEXT,
    SUCCESS_CANCEL_SHUTDOWN_MESSAGE,
    SUCCESS_CANCEL_SHUTDOWN_TEXT,
    SUCCESS_SHUTDOWN_MESSAGE,
    SUCCESS_SHUTDOWN_TEXT,
    SUCCESS_TEXT,
    SUCCESS_VOLUME_TEXT,
    VOLUME,
    VOLUME_BUTTON_CLICK,
)
from keyboard.keyboard import play_pause
from screen.screen_control import get_brightness, set_brightness
from system.power_management import (
    cancel_shutdown_timer,
    check_shutdown_status,
    set_shutdown_timer,
)
from utils.timer import timer
from utils.utils import finish_time
from volume.volume_control import get_volume, set_volume

finish = ""


def register_handlers(dp):

    @dp.message(Command(START_BUTTON))
    @acsess
    async def send_welcome(message: types.Message):
        reply_markup = get_user_buttons()
        await message.reply(START_REPLAY, reply_markup=reply_markup)

    @dp.callback_query(lambda c: c.data == VOLUME_BUTTON_CLICK)
    @acsess
    async def handle_button_click(callback_query: types.CallbackQuery):
        volume = get_volume()
        await callback_query.answer(VOLUME)
        await callback_query.message.delete()
        reply_markup = get_change_volume_buttons()
        await callback_query.message.answer(
            CHANGE_TO_VOLUME.format(volume=volume), reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data == CANCEL_BUTTON_CLICK)
    @acsess
    async def cancel_button(callback_query: types.CallbackQuery):
        await callback_query.answer(CANCEL_CONFIRM_TEXT)
        await callback_query.message.delete()
        reply_markup = get_user_buttons()
        await callback_query.message.answer(
            text=START_REPLAY, reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_VOLUME))
    @acsess
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
    @acsess
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
    @acsess
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
    @acsess
    async def handle_button_click(callback_query: types.CallbackQuery):
        shutdown_status = check_shutdown_status()
        await callback_query.answer(POWER)
        await callback_query.message.delete()
        if not shutdown_status:

            reply_markup = get_change_shutdown_buttons()
            await callback_query.message.answer(
                CHANGE_TO_POWER, reply_markup=reply_markup
            )
        else:
            reply_markup = get_cancel_shutdown_buttons()

            await callback_query.message.answer(
                CHANGE_TO_POWER_TIMER.format(
                    time=finish, minutes=timer.check_timer()
                ),
                reply_markup=reply_markup,
            )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_SHUTDOWN))
    @acsess
    async def change_shutdown(callback_query: types.CallbackQuery):
        global finish
        shutdown_time = callback_query.data.split("_")[-1]
        await callback_query.message.delete()

        set_shutdown = set_shutdown_timer(int(shutdown_time))
        timer.start_timer(int(shutdown_time))
        reply_markup = get_user_buttons()
        if set_shutdown:
            await callback_query.answer(SUCCESS_SHUTDOWN_TEXT)
            finish = finish_time(int(shutdown_time))

            await callback_query.message.answer(
                text=SUCCESS_SHUTDOWN_MESSAGE.format(finish_time=finish),
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )

    @dp.callback_query(lambda c: c.data.startswith(CANCEL_SHUTDOWN))
    @acsess
    async def cancel_shutdown(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        reply_markup = get_user_buttons()
        cancel = cancel_shutdown_timer()
        if cancel:
            await callback_query.answer(SUCCESS_CANCEL_SHUTDOWN_TEXT)
            await callback_query.message.answer(
                text=SUCCESS_CANCEL_SHUTDOWN_MESSAGE,
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )

    @dp.callback_query(lambda c: c.data.startswith(KEYBOARD_BUTTON_CLICK))
    @acsess
    async def keyboard_button_click(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.answer(KEYBOARD)
        reply_markup = get_keyboard_buttons()
        await callback_query.message.answer(
            CHANGE_TO_KEYBOARD,
            reply_markup=reply_markup,
        )

    @dp.callback_query(lambda c: c.data.startswith(SPACE_CLICK))
    @acsess
    async def keyboard_click(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.answer(SPACE_BUTTON_TEXT)
        if play_pause():
            reply_markup = get_keyboard_buttons()
            await callback_query.message.answer(
                CHANGE_TO_KEYBOARD,
                reply_markup=reply_markup,
            )
        else:
            reply_markup = get_user_buttons()
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )
