from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import (
    CANCEL_BUTTON_CLICK,
    CANCEL_BUTTON_TEXT,
    CANCEL_SHUTDOWN,
    CANCEL_SHUTDOWN_TEXT,
    CHANGE_BRIGHTNESS,
    CHANGE_SHUTDOWN,
    CHANGE_VOLUME,
    KEYBOARD,
    KEYBOARD_BUTTON_CLICK,
    MONITOR,
    MONITOR_BUTTON_CLICK,
    MUTE_VOLUME_TEXT,
    NIGHT_SWITCH_TEXT,
    POWER,
    POWER_BUTTON_CLICK,
    SHUTDOWN_NOW,
    SPACE_BUTTON_TEXT,
    SPACE_CLICK,
    SWITCH_OUTPUT_DEVICE,
    VOLUME,
    VOLUME_BUTTON_CLICK,
)

cancel_button = [
    InlineKeyboardButton(text=CANCEL_BUTTON_TEXT, callback_data=CANCEL_BUTTON_CLICK)
]
cancel_shutdown = [
    InlineKeyboardButton(text=CANCEL_SHUTDOWN_TEXT, callback_data=CANCEL_SHUTDOWN)
]


def get_user_buttons():
    buttons = [
        [InlineKeyboardButton(text=VOLUME, callback_data=VOLUME_BUTTON_CLICK)],
        [InlineKeyboardButton(text=MONITOR, callback_data=MONITOR_BUTTON_CLICK)],
        [InlineKeyboardButton(text=POWER, callback_data=POWER_BUTTON_CLICK)],
        [InlineKeyboardButton(text=KEYBOARD, callback_data=KEYBOARD_BUTTON_CLICK)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_change_volume_buttons(switch_targets=None):
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
    targets = switch_targets or []
    if len(targets) >= 2:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=targets[0]["name"],
                    callback_data=SWITCH_OUTPUT_DEVICE + "0",
                ),
                InlineKeyboardButton(
                    text=targets[1]["name"],
                    callback_data=SWITCH_OUTPUT_DEVICE + "1",
                ),
            ]
        )
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
