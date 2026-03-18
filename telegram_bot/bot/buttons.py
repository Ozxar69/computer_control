from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import (
    BACK_BUTTON_TEXT,
    BACK_TO_MAIN_CLICK,
    CANCEL_BUTTON_CLICK,
    CANCEL_BUTTON_TEXT,
    CANCEL_SHUTDOWN,
    CANCEL_SHUTDOWN_TEXT,
    CHANGE_BRIGHTNESS,
    CHANGE_SHUTDOWN,
    CHANGE_VOLUME,
    DEVICE_BUTTON_TEXT,
    DEVICE_CLICK_PREFIX,
    EXTRA_SWITCH_BUTTON,
    HOME_BUTTON,
    HOME_BUTTON_CLICK,
    KEYBOARD,
    KEYBOARD_BUTTON_CLICK,
    LIGHTS_BUTTON_TEXT,
    LIGHTS_MENU_CLICK,
    MAIN_SWITCH_BUTTON,
    MONITOR,
    MONITOR_BUTTON_CLICK,
    MUTE_VOLUME_TEXT,
    NIGHT_SWITCH_TEXT,
    OFFLINE_ICON,
    ONLINE_ICON,
    OUTLETS_BUTTON_TEXT,
    OUTLETS_MENU_CLICK,
    POWER,
    POWER_BUTTON_CLICK,
    SHUTDOWN_NOW,
    SPACE_BUTTON_TEXT,
    SPACE_CLICK,
    VOLUME,
    VOLUME_BUTTON_CLICK,
)

cancel_button = [
    InlineKeyboardButton(text=CANCEL_BUTTON_TEXT, callback_data=CANCEL_BUTTON_CLICK)
]
cancel_shutdown = [
    InlineKeyboardButton(text=CANCEL_SHUTDOWN_TEXT, callback_data=CANCEL_SHUTDOWN)
]
back_button = [
    InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=BACK_TO_MAIN_CLICK)
]


def get_user_buttons():
    buttons = [
        [InlineKeyboardButton(text=VOLUME, callback_data=VOLUME_BUTTON_CLICK)],
        [InlineKeyboardButton(text=MONITOR, callback_data=MONITOR_BUTTON_CLICK)],
        [InlineKeyboardButton(text=POWER, callback_data=POWER_BUTTON_CLICK)],
        [InlineKeyboardButton(text=KEYBOARD, callback_data=KEYBOARD_BUTTON_CLICK)],
        [InlineKeyboardButton(text=HOME_BUTTON, callback_data=HOME_BUTTON_CLICK)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_change_volume_buttons():
    first_block = [
        InlineKeyboardButton(text=f"{i}%", callback_data=CHANGE_VOLUME + str(i))
        for i in range(5, 56, 5)
    ]
    second_block = [
        InlineKeyboardButton(text=f"{i}%", callback_data=CHANGE_VOLUME + str(i))
        for i in range(55, 101, 5)
    ]
    first_row = [
        InlineKeyboardButton(text=MUTE_VOLUME_TEXT, callback_data=CHANGE_VOLUME + "0")
    ]
    keyboard = [first_row]
    for i in range(5):
        row = []
        if i < len(first_block):
            row.append(first_block[i])
        if i + 5 < len(first_block):
            row.append(first_block[i + 5])
        if i < len(second_block):
            row.append(second_block[i])
        if i + 5 < len(second_block):
            row.append(second_block[i + 5])
        keyboard.append(row)
    keyboard.append(cancel_button)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_change_brightness_buttons():
    buttons = [
        InlineKeyboardButton(text=f"{i}%", callback_data=CHANGE_BRIGHTNESS + str(i))
        for i in range(25, 101, 25)
    ]
    keyboard = [
        [InlineKeyboardButton(text=NIGHT_SWITCH_TEXT, callback_data=CHANGE_BRIGHTNESS + "0")]
    ]
    for i in range(2):
        keyboard.append([buttons[i], buttons[i + 2]])
    keyboard.append(cancel_button)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_change_shutdown_buttons():
    shutdown_now = [
        InlineKeyboardButton(text=SHUTDOWN_NOW, callback_data=CHANGE_SHUTDOWN + "1")
    ]
    col1 = [
        InlineKeyboardButton(text=f"{i} мин", callback_data=CHANGE_SHUTDOWN + str(i))
        for i in range(10, 30, 5)
    ]
    col2 = [
        InlineKeyboardButton(text=f"{i} мин", callback_data=CHANGE_SHUTDOWN + str(i))
        for i in range(30, 61, 10)
    ]
    col3 = [
        InlineKeyboardButton(text=f"{i} мин", callback_data=CHANGE_SHUTDOWN + str(i))
        for i in range(90, 181, 30)
    ]
    keyboard = [shutdown_now]
    for i in range(4):
        keyboard.append([col1[i], col2[i], col3[i]])
    keyboard.append(cancel_shutdown)
    keyboard.append(cancel_button)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_cancel_shutdown_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[cancel_shutdown, cancel_button])


def get_keyboard_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=SPACE_BUTTON_TEXT, callback_data=SPACE_CLICK)],
            cancel_button,
        ]
    )


async def get_main_menu_buttons():
    buttons = [
        [InlineKeyboardButton(text=LIGHTS_BUTTON_TEXT, callback_data=LIGHTS_MENU_CLICK)],
        [InlineKeyboardButton(text=OUTLETS_BUTTON_TEXT, callback_data=OUTLETS_MENU_CLICK)],
        cancel_button,
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_devices_buttons_from_api(devices: list) -> InlineKeyboardMarkup:
    """Кнопки для списка устройств из API-ответа (list of dicts)."""
    buttons = []
    for device in devices:
        status_icon = ONLINE_ICON if device["is_online"] else OFFLINE_ICON
        buttons.append([
            InlineKeyboardButton(
                text=DEVICE_BUTTON_TEXT.format(status=status_icon, name=device["name"]),
                callback_data=f"{DEVICE_CLICK_PREFIX}{device['id']}",
            )
        ])
    buttons.append(back_button)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_device_control_buttons(device_info: dict) -> InlineKeyboardMarkup:
    buttons = []

    main_state = "Выключить" if device_info["switches"]["switch_1"] else "Включить"
    buttons.append([
        InlineKeyboardButton(
            text=MAIN_SWITCH_BUTTON.format(state=main_state),
            callback_data=f"DEVICE_TOGGLE_{device_info['device_id']}_1",
        )
    ])

    if device_info["has_switch_2"]:
        extra_state = "Выключить" if device_info["switches"]["switch_2"] else "Включить"
        buttons.append([
            InlineKeyboardButton(
                text=EXTRA_SWITCH_BUTTON.format(state=extra_state),
                callback_data=f"DEVICE_TOGGLE_{device_info['device_id']}_2",
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="↩️ Назад", callback_data=HOME_BUTTON_CLICK)
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
