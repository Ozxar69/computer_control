import asyncio

from aiogram import types
from aiogram.filters import Command

from admin import access
from bot.buttons import (
    get_cancel_shutdown_buttons,
    get_change_brightness_buttons,
    get_change_shutdown_buttons,
    get_change_volume_buttons,
    get_keyboard_buttons,
    get_user_buttons, get_devices_buttons_async, get_main_menu_buttons,
    create_device_control_buttons,
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
    VOLUME_BUTTON_CLICK, HOME_BUTTON_CLICK, SMART_HOME_MANAGEMENT,
    LIGHTS_MENU_CLICK, LOADING_LIGHTS_MSG, LIGHT, NO_LIGHTS_MSG,
    LIGHTS_MENU_TITLE, ERROR_MSG_TEMPLATE, OUTLETS_MENU_CLICK,
    LOADING_OUTLETS_MSG, OUTLET, NO_OUTLETS_MSG, OUTLETS_MENU_TITLE,
    BACK_TO_MAIN_CLICK, STATUS_ON, STATUS_OFF, DEVICE_INFO_TEMPLATE,
)

from keyboard.keyboard import play_pause
from screen.screen_control import get_brightness, set_brightness
from system.power_management import (
    cancel_shutdown_timer,
    check_shutdown_status,
    set_shutdown_timer,
)
from devices import load_devices_with_status, async_load_devices
from utils.timer import timer
from utils.utils import finish_time
from volume.volume_control import get_volume, set_volume

finish = ""


def register_handlers(dp):

    @dp.message(Command(START_BUTTON))
    @access
    async def send_welcome(message: types.Message):
        reply_markup = get_user_buttons()
        await message.reply(START_REPLAY, reply_markup=reply_markup)

    @dp.callback_query(lambda c: c.data == VOLUME_BUTTON_CLICK)
    @access
    async def handle_button_click(callback_query: types.CallbackQuery):
        volume = get_volume()
        await callback_query.answer(VOLUME)
        await callback_query.message.delete()
        reply_markup = get_change_volume_buttons()
        await callback_query.message.answer(
            CHANGE_TO_VOLUME.format(volume=volume), reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data == CANCEL_BUTTON_CLICK)
    @access
    async def cancel_button(callback_query: types.CallbackQuery):
        await callback_query.answer(CANCEL_CONFIRM_TEXT)
        await callback_query.message.delete()
        reply_markup = get_user_buttons()
        await callback_query.message.answer(
            text=START_REPLAY, reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data.startswith(CHANGE_VOLUME))
    @access
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
    @access
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
    @access
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
    @access
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
    @access
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
    @access
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
    @access
    async def keyboard_button_click(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        await callback_query.answer(KEYBOARD)
        reply_markup = get_keyboard_buttons()
        await callback_query.message.answer(
            CHANGE_TO_KEYBOARD,
            reply_markup=reply_markup,
        )

    @dp.callback_query(lambda c: c.data.startswith(SPACE_CLICK))
    @access
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

    @dp.callback_query(lambda c: c.data == HOME_BUTTON_CLICK)
    @access
    async def show_smart_home_main(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        reply_markup = await get_main_menu_buttons()
        await callback_query.message.answer(
            text=SMART_HOME_MANAGEMENT,
            reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data == LIGHTS_MENU_CLICK)
    @access
    async def show_lights_menu(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        loading_msg = await callback_query.message.answer(
            LOADING_LIGHTS_MSG)
        try:
            devices = await load_devices_with_status()
            lights = [(d, s) for d, s in devices if d.device_type == LIGHT]

            if not lights:
                await loading_msg.edit_text(NO_LIGHTS_MSG)
                await asyncio.sleep(2)
                await loading_msg.delete()
                return

            reply_markup = await get_devices_buttons_async(lights)
            await loading_msg.delete()
            await callback_query.message.answer(
                text=LIGHTS_MENU_TITLE,
                reply_markup=reply_markup
            )
        except Exception as e:
            await loading_msg.edit_text(ERROR_MSG_TEMPLATE.format(error=str(e)))
            await asyncio.sleep(3)
            await loading_msg.delete()

    @dp.callback_query(lambda c: c.data == OUTLETS_MENU_CLICK)
    @access
    async def show_outlets_menu(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        loading_msg = await callback_query.message.answer(
            LOADING_OUTLETS_MSG)
        try:
            devices = await load_devices_with_status()
            outlets = [(d, s) for d, s in devices if d.device_type == OUTLET]

            if not outlets:
                await loading_msg.edit_text(NO_OUTLETS_MSG)
                await asyncio.sleep(2)
                await loading_msg.delete()
                return

            reply_markup = await get_devices_buttons_async(outlets)
            await loading_msg.delete()
            await callback_query.message.answer(
                text=OUTLETS_MENU_TITLE,
                reply_markup=reply_markup
            )
        except Exception as e:
            await loading_msg.edit_text(ERROR_MSG_TEMPLATE.format(error=str(e)))
            await asyncio.sleep(3)
            await loading_msg.delete()

    @dp.callback_query(lambda c: c.data == BACK_TO_MAIN_CLICK)
    @access
    async def handle_back_to_main(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
        reply_markup = await get_main_menu_buttons()
        await callback_query.message.answer(
            text=SMART_HOME_MANAGEMENT,
            reply_markup=reply_markup
        )

    @dp.callback_query(lambda c: c.data.startswith("DEVICE_TOGGLE_"))
    @access
    async def handle_device_toggle(callback_query: types.CallbackQuery):
        parts = callback_query.data.split("_")
        device_id = parts[2]
        switch_num = parts[3]

        device = next((d for d in await async_load_devices() if d.device_id == device_id),
                      None)
        if not device:
            await callback_query.answer("Устройство не найдено")
            return

        try:
            if switch_num == '1':
                await device.turn_off() if await device.is_on() else await device.turn_on()
            elif switch_num == '2':
                # Для второго переключателя используем прямое управление DPS
                current = (await device.status()).get('dps', {}).get('2', False)
                await device._async_execute(
                    lambda: device._device.set_value(2, not current))


            # Получаем обновлённые данные устройства
            device_info = await device.get_device_info()
            status = STATUS_ON if device_info['switches'][
                'switch_1'] else STATUS_OFF

            # Формируем новое сообщение
            message = DEVICE_INFO_TEMPLATE.format(
                name=device_info['name'],
                status=status,
                additional_info=f"Переключатель 2: {'Вкл' if device_info['switches']['switch_2'] else 'Выкл'}\n"
                if device_info['has_switch_2'] else ""
            )

            # Обновляем клавиатуру
            reply_markup = create_device_control_buttons(device_info)

            # Редактируем сообщение
            await callback_query.message.edit_text(
                text=message,
                reply_markup=reply_markup
            )
            await callback_query.answer("Состояние изменено")
        except Exception as e:
            await callback_query.answer(f"Ошибка: {str(e)}")


    @dp.callback_query(lambda c: c.data.startswith("DEVICE_"))
    @access
    async def handle_device_control(
            callback_query: types.CallbackQuery,
            device_id: str = None
    ):
        if not device_id:
            device_id = callback_query.data.split("_")[-1]

        # Находим устройство
        device = next((d for d in await async_load_devices() if d.device_id == device_id),
                      None)
        if not device:
            await callback_query.answer("Устройство не найдено")
            return

        # Получаем информацию об устройстве
        device_info = await device.get_device_info()
        if not device_info:
            await callback_query.answer("Не удалось получить статус устройства")
            return

        # Формируем сообщение
        status = STATUS_ON if device_info['switches']['switch_1'] else STATUS_OFF
        additional_info = ""
        if device_info['has_switch_2']:
            additional_info += f"Дополнительный: {STATUS_ON if device_info['switches']['switch_2'] else STATUS_OFF}\n"

        message = DEVICE_INFO_TEMPLATE.format(
            name=device_info['name'],
            status=status,
            additional_info=additional_info
        )

        # Создаем клавиатуру управления
        reply_markup = create_device_control_buttons(device_info)

        await callback_query.message.edit_text(
            text=message,
            reply_markup=reply_markup
        )
        await callback_query.answer()

