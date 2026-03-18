import asyncio
import logging

from aiogram import types
from aiogram.filters import Command

from admin import access
from bot.buttons import (
    create_device_control_buttons,
    get_cancel_shutdown_buttons,
    get_change_brightness_buttons,
    get_change_shutdown_buttons,
    get_change_volume_buttons,
    get_devices_buttons_from_api,
    get_keyboard_buttons,
    get_main_menu_buttons,
    get_user_buttons,
)
from client import api_delete, api_get, api_post
from data import (
    BACK_TO_MAIN_CLICK,
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
    DEVICE_INFO_TEMPLATE,
    ERROR_MSG_TEMPLATE,
    FALSE_TEXT,
    KEYBOARD,
    KEYBOARD_BUTTON_CLICK,
    LIGHT,
    LIGHTS_MENU_CLICK,
    LIGHTS_MENU_TITLE,
    LOADING_LIGHTS_MSG,
    LOADING_OUTLETS_MSG,
    LOG_BRIGHTNESS_GET_ERROR,
    LOG_BRIGHTNESS_SET,
    LOG_BRIGHTNESS_SET_ERROR,
    LOG_DEVICE_INFO_ERROR,
    LOG_DEVICE_TOGGLE_ERROR,
    LOG_LIGHTS_LOAD_ERROR,
    LOG_OUTLETS_LOAD_ERROR,
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
    NO_LIGHTS_MSG,
    NO_OUTLETS_MSG,
    OUTLET,
    OUTLETS_MENU_CLICK,
    OUTLETS_MENU_TITLE,
    POWER,
    POWER_BUTTON_CLICK,
    SMART_HOME_MANAGEMENT,
    HOME_BUTTON_CLICK,
    SPACE_BUTTON_TEXT,
    SPACE_CLICK,
    START_BUTTON,
    START_REPLAY,
    STATUS_OFF,
    STATUS_ON,
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

logger = logging.getLogger(__name__)


def register_handlers(dp):

    @dp.message(Command(START_BUTTON))
    @access
    async def send_welcome(message: types.Message):
        logger.info(LOG_START_COMMAND, message.from_user.id)
        await message.reply(START_REPLAY, reply_markup=get_user_buttons())

    # ── VOLUME ──────────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == VOLUME_BUTTON_CLICK)
    @access
    async def handle_volume_menu(callback_query: types.CallbackQuery):
        try:
            data = await api_get("/volume")
            volume = data["volume"]
        except Exception as e:
            logger.error(LOG_VOLUME_GET_ERROR, e)
            volume = "?"
        await callback_query.answer(VOLUME)
        await callback_query.message.delete()
        await callback_query.message.answer(
            CHANGE_TO_VOLUME.format(volume=volume),
            reply_markup=get_change_volume_buttons(),
        )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_VOLUME))
    @access
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
            logger.error(LOG_BRIGHTNESS_SET_ERROR, e)
            await callback_query.answer(FALSE_TEXT)
            await callback_query.message.answer(text=FALSE_TEXT, reply_markup=get_user_buttons())

    # ── POWER ───────────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == POWER_BUTTON_CLICK)
    @access
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

    # ── SMART HOME ───────────────────────────────────────────────────────────

    @dp.callback_query(lambda c: c.data == HOME_BUTTON_CLICK)
    @access
    async def show_smart_home_main(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.message.answer(
            text=SMART_HOME_MANAGEMENT,
            reply_markup=await get_main_menu_buttons(),
        )

    @dp.callback_query(lambda c: c.data == LIGHTS_MENU_CLICK)
    @access
    async def show_lights_menu(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        loading_msg = await callback_query.message.answer(LOADING_LIGHTS_MSG)
        try:
            devices = await api_get("/home/devices")
            lights = [d for d in devices if d["type"] == LIGHT]
            if not lights:
                await loading_msg.edit_text(NO_LIGHTS_MSG)
                await asyncio.sleep(2)
                await loading_msg.delete()
                return
            await loading_msg.delete()
            await callback_query.message.answer(
                text=LIGHTS_MENU_TITLE,
                reply_markup=get_devices_buttons_from_api(lights),
            )
        except Exception as e:
            logger.error(LOG_LIGHTS_LOAD_ERROR, e)
            await loading_msg.edit_text(ERROR_MSG_TEMPLATE.format(error=str(e)))
            await asyncio.sleep(3)
            await loading_msg.delete()

    @dp.callback_query(lambda c: c.data == OUTLETS_MENU_CLICK)
    @access
    async def show_outlets_menu(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        loading_msg = await callback_query.message.answer(LOADING_OUTLETS_MSG)
        try:
            devices = await api_get("/home/devices")
            outlets = [d for d in devices if d["type"] == OUTLET]
            if not outlets:
                await loading_msg.edit_text(NO_OUTLETS_MSG)
                await asyncio.sleep(2)
                await loading_msg.delete()
                return
            await loading_msg.delete()
            await callback_query.message.answer(
                text=OUTLETS_MENU_TITLE,
                reply_markup=get_devices_buttons_from_api(outlets),
            )
        except Exception as e:
            logger.error(LOG_OUTLETS_LOAD_ERROR, e)
            await loading_msg.edit_text(ERROR_MSG_TEMPLATE.format(error=str(e)))
            await asyncio.sleep(3)
            await loading_msg.delete()

    @dp.callback_query(lambda c: c.data == BACK_TO_MAIN_CLICK)
    @access
    async def handle_back_to_main(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.message.answer(
            text=SMART_HOME_MANAGEMENT,
            reply_markup=await get_main_menu_buttons(),
        )

    @dp.callback_query(lambda c: c.data.startswith("DEVICE_TOGGLE_"))
    @access
    async def handle_device_toggle(callback_query: types.CallbackQuery):
        parts = callback_query.data.split("_")
        device_id = parts[2]
        switch_num = int(parts[3])
        try:
            device_info = await api_post(
                f"/home/devices/{device_id}/toggle", {"switch": switch_num}
            )
            status = STATUS_ON if device_info["switches"]["switch_1"] else STATUS_OFF
            additional_info = ""
            if device_info["has_switch_2"]:
                sw2 = "Вкл" if device_info["switches"]["switch_2"] else "Выкл"
                additional_info = f"Переключатель 2: {sw2}\n"
            message = DEVICE_INFO_TEMPLATE.format(
                name=device_info["name"],
                status=status,
                additional_info=additional_info,
            )
            await callback_query.message.edit_text(
                text=message,
                reply_markup=create_device_control_buttons(device_info),
            )
            await callback_query.answer("Состояние изменено")
        except Exception as e:
            logger.error(LOG_DEVICE_TOGGLE_ERROR, device_id, e)
            await callback_query.answer(f"Ошибка: {str(e)}")

    @dp.callback_query(lambda c: c.data.startswith("DEVICE_"))
    @access
    async def handle_device_control(callback_query: types.CallbackQuery):
        device_id = callback_query.data.split("_")[-1]
        try:
            device_info = await api_get(f"/home/devices/{device_id}")
            if not device_info:
                await callback_query.answer("Не удалось получить статус устройства")
                return
            status = STATUS_ON if device_info["switches"]["switch_1"] else STATUS_OFF
            additional_info = ""
            if device_info["has_switch_2"]:
                sw2 = STATUS_ON if device_info["switches"]["switch_2"] else STATUS_OFF
                additional_info = f"Дополнительный: {sw2}\n"
            message = DEVICE_INFO_TEMPLATE.format(
                name=device_info["name"],
                status=status,
                additional_info=additional_info,
            )
            await callback_query.message.edit_text(
                text=message,
                reply_markup=create_device_control_buttons(device_info),
            )
            await callback_query.answer()
        except Exception as e:
            logger.error(LOG_DEVICE_INFO_ERROR, device_id, e)
            await callback_query.answer("Устройство не найдено")
