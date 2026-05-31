import logging

from aiogram import types
from aiogram.filters import Command

from admin import access
from availability import require_api
from bot.buttons import (
    get_cancel_shutdown_buttons,
    get_change_brightness_buttons,
    get_change_shutdown_buttons,
    get_change_volume_buttons,
    get_keyboard_buttons,
    get_user_buttons,
)
from client import api_delete, api_get, api_post, is_api_available
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
    LOG_BRIGHTNESS_GET_ERROR,
    LOG_BRIGHTNESS_SET,
    LOG_BRIGHTNESS_SET_ERROR,
    LOG_PLAY_PAUSE,
    LOG_PLAY_PAUSE_ERROR,
    LOG_POWER_GET_ERROR,
    LOG_SHUTDOWN_CANCEL,
    LOG_SHUTDOWN_CANCEL_ERROR,
    LOG_SHUTDOWN_SET,
    LOG_SHUTDOWN_SET_ERROR,
    LOG_START_COMMAND,
    LOG_VOLUME_GET_ERROR,
    LOG_VOLUME_SET,
    LOG_VOLUME_SET_ERROR,
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
    SWITCH_OUTPUT_DEVICE,
    VOLUME,
    VOLUME_BUTTON_CLICK,
    LOG_VOLUME_SWITCH,
    LOG_VOLUME_SWITCH_ERROR,
    PC_OFFLINE_TEXT,
)

logger = logging.getLogger(__name__)


def register_handlers(dp):
    async def show_volume_menu(callback_query: types.CallbackQuery):
        try:
            data = await api_get("/volume")
            volume = data["volume"]
            device_name = data.get("device_name", "Unknown device")
            switch_targets = data.get("switch_targets", [])
        except Exception as e:
            logger.error(LOG_VOLUME_GET_ERROR, e)
            volume = "?"
            device_name = "Unknown device"
            switch_targets = []
        await callback_query.answer(VOLUME)
        await callback_query.message.delete()
        await callback_query.message.answer(
            CHANGE_TO_VOLUME.format(volume=volume, device=device_name),
            reply_markup=get_change_volume_buttons(switch_targets=switch_targets),
        )

    @dp.message(Command(START_BUTTON))
    @access
    async def send_welcome(message: types.Message):
        logger.info(LOG_START_COMMAND, message.from_user.id)
        if not await is_api_available():
            await message.reply(PC_OFFLINE_TEXT)
            return
        await message.reply(START_REPLAY, reply_markup=get_user_buttons())

    # ── VOLUME ──────────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == VOLUME_BUTTON_CLICK)
    @access
    @require_api
    async def handle_volume_menu(callback_query: types.CallbackQuery):
        await show_volume_menu(callback_query)

    @dp.callback_query(lambda c: c.data.startswith(SWITCH_OUTPUT_DEVICE))
    @access
    @require_api
    async def switch_output_device(callback_query: types.CallbackQuery):
        target_index_text = callback_query.data.replace(SWITCH_OUTPUT_DEVICE, "", 1)
        try:
            target_index = int(target_index_text)
            current_data = await api_get("/volume")
            switch_targets = current_data.get("switch_targets", [])
            if target_index < 0 or target_index >= len(switch_targets):
                await callback_query.answer(FALSE_TEXT)
                return

            target_device_id = switch_targets[target_index]["id"]
            data = await api_post(
                "/volume/switch-output",
                {"target_device_id": target_device_id},
            )
            logger.info(
                LOG_VOLUME_SWITCH,
                data.get("device_name", "Unknown device"),
                callback_query.from_user.id,
            )
        except Exception as e:
            logger.error(LOG_VOLUME_SWITCH_ERROR, e)
            await callback_query.answer(FALSE_TEXT)
            return
        await show_volume_menu(callback_query)

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_VOLUME))
    @access
    @require_api
    async def change_volume(callback_query: types.CallbackQuery):
        level = int(callback_query.data.split("_")[-1])
        await callback_query.message.delete()
        try:
            data = await api_post("/volume", {"value": level})
            volume = data["volume"]
            logger.info(LOG_VOLUME_SET, volume, callback_query.from_user.id)
            await callback_query.answer(SUCCESS_VOLUME_TEXT.format(volume=volume))
            await callback_query.message.answer(
                text=SUCCESS_TEXT.format(volume=volume),
                reply_markup=get_user_buttons(),
            )
        except Exception as e:
            logger.error(LOG_VOLUME_SET_ERROR, e)
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(text=FALSE_TEXT, reply_markup=get_user_buttons())

    # ── BRIGHTNESS ──────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == MONITOR_BUTTON_CLICK)
    @access
    @require_api
    async def handle_brightness_menu(callback_query: types.CallbackQuery):
        try:
            data = await api_get("/brightness")
            brightness = data["brightness"]
        except Exception as e:
            logger.error(LOG_BRIGHTNESS_GET_ERROR, e)
            brightness = "?"
        await callback_query.answer(MONITOR)
        await callback_query.message.delete()
        await callback_query.message.answer(
            CHANGE_TO_BRIGHTNESS.format(brightness=brightness),
            reply_markup=get_change_brightness_buttons(),
        )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_BRIGHTNESS))
    @access
    @require_api
    async def change_brightness(callback_query: types.CallbackQuery):
        level = int(callback_query.data.split("_")[-1])
        await callback_query.message.delete()
        try:
            data = await api_post("/brightness", {"value": level})
            brightness = data["brightness"]
            logger.info(LOG_BRIGHTNESS_SET, brightness, callback_query.from_user.id)
            await callback_query.answer(SUCCESS_BRIGHTNESS_TEXT.format(brightness=brightness))
            await callback_query.message.answer(
                text=SUCCESS_BRIGHTNESS_MESSAGE.format(brightness=brightness),
                reply_markup=get_user_buttons(),
            )
        except Exception as e:
            logger.error(
                "Failed to set brightness: type=%s repr=%r str=%s",
                type(e).__name__,
                e,
                str(e),
            )
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(text=FALSE_TEXT, reply_markup=get_user_buttons())

    # ── POWER ───────────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == POWER_BUTTON_CLICK)
    @access
    @require_api
    async def handle_power_menu(callback_query: types.CallbackQuery):
        try:
            data = await api_get("/power")
            shutdown_active = data["shutdown_active"]
        except Exception as e:
            logger.error(LOG_POWER_GET_ERROR, e)
            data = {}
            shutdown_active = False
        await callback_query.answer(POWER)
        await callback_query.message.delete()
        if not shutdown_active:
            await callback_query.message.answer(
                CHANGE_TO_POWER, reply_markup=get_change_shutdown_buttons()
            )
        else:
            await callback_query.message.answer(
                CHANGE_TO_POWER_TIMER.format(
                    time=data.get("finish_time", "?"),
                    minutes=data.get("remaining", "?"),
                ),
                reply_markup=get_cancel_shutdown_buttons(),
            )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_SHUTDOWN))
    @access
    @require_api
    async def change_shutdown(callback_query: types.CallbackQuery):
        minutes = int(callback_query.data.split("_")[-1])
        await callback_query.message.delete()
        try:
            data = await api_post("/power/shutdown", {"minutes": minutes})
            logger.info(LOG_SHUTDOWN_SET, minutes, callback_query.from_user.id)
            await callback_query.answer(SUCCESS_SHUTDOWN_TEXT)
            await callback_query.message.answer(
                text=SUCCESS_SHUTDOWN_MESSAGE.format(finish_time=data.get("finish_time", "?")),
                reply_markup=get_user_buttons(),
            )
        except Exception as e:
            logger.error(LOG_SHUTDOWN_SET_ERROR, e)
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(text=FALSE_TEXT, reply_markup=get_user_buttons())

    @dp.callback_query(lambda c: c.data.startswith(CANCEL_SHUTDOWN))
    @access
    @require_api
    async def cancel_shutdown(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        try:
            await api_delete("/power/shutdown")
            logger.info(LOG_SHUTDOWN_CANCEL, callback_query.from_user.id)
            await callback_query.answer(SUCCESS_CANCEL_SHUTDOWN_TEXT)
            await callback_query.message.answer(
                text=SUCCESS_CANCEL_SHUTDOWN_MESSAGE,
                reply_markup=get_user_buttons(),
            )
        except Exception as e:
            logger.error(LOG_SHUTDOWN_CANCEL_ERROR, e)
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(text=FALSE_TEXT, reply_markup=get_user_buttons())

    # ── KEYBOARD ────────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data.startswith(KEYBOARD_BUTTON_CLICK))
    @access
    async def keyboard_button_click(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.answer(KEYBOARD)
        await callback_query.message.answer(
            CHANGE_TO_KEYBOARD, reply_markup=get_keyboard_buttons()
        )

    @dp.callback_query(lambda c: c.data.startswith(SPACE_CLICK))
    @access
    @require_api
    async def keyboard_click(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.answer(SPACE_BUTTON_TEXT)
        try:
            await api_post("/keyboard/play-pause")
            logger.info(LOG_PLAY_PAUSE, callback_query.from_user.id)
            await callback_query.message.answer(
                CHANGE_TO_KEYBOARD, reply_markup=get_keyboard_buttons()
            )
        except Exception as e:
            logger.error(LOG_PLAY_PAUSE_ERROR, e)
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(text=FALSE_TEXT, reply_markup=get_user_buttons())

    # ── CANCEL ───────────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == CANCEL_BUTTON_CLICK)
    @access
    async def cancel_button(callback_query: types.CallbackQuery):
        await callback_query.answer(CANCEL_CONFIRM_TEXT)
        await callback_query.message.delete()
        await callback_query.message.answer(text=START_REPLAY, reply_markup=get_user_buttons())
