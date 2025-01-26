from aiogram import types
from aiogram.filters import Command

from bot.buttons import (
    get_change_brightness_buttons,
    get_change_volume_buttons,
    get_user_buttons,
)
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
    SUCSESS_BRIGHTNESS_MESSAGE,
    SUCSESS_BRIGHTNESS_TEXT,
    SUCSESS_TEXT,
    SUCSESS_VOLUME_TEXT,
    VOLUME,
    VOLUME_BUTTON_CLICK,
)
from screen.screen_control import get_brightness, set_brightness
from volume.volume_control import get_volume, set_volume


def register_handlers(dp):

    @dp.message(Command(START_BUTTON))
    async def send_welcome(message: types.Message):

        reply_markup = get_user_buttons()
        await message.reply(START_REPLAY, reply_markup=reply_markup)

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
                SUCSESS_VOLUME_TEXT.format(volume=volume_level)
            )

            await callback_query.message.answer(
                text=SUCSESS_TEXT.format(volume=volume_level),
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
                SUCSESS_BRIGHTNESS_TEXT.format(brightness=brightness_level[0])
            )

            await callback_query.message.answer(
                text=SUCSESS_BRIGHTNESS_MESSAGE.format(
                    brightness=brightness_level[0]
                ),
                reply_markup=reply_markup,
            )
        else:
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(
                text=FALSE_TEXT, reply_markup=reply_markup
            )
