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
    VOLUME,
    VOLUME_BUTTON_CLICK,
)

cancel_button = [
    InlineKeyboardButton(
        text=CANCEL_BUTTON_TEXT, callback_data=CANCEL_BUTTON_CLICK
    )
]
cancel_shutdown = [
    InlineKeyboardButton(
        text=CANCEL_SHUTDOWN_TEXT, callback_data=CANCEL_SHUTDOWN
    )
]


def get_user_buttons():
    """Создает пользовательские кнопки."""
    buttons = [
        [InlineKeyboardButton(text=VOLUME, callback_data=VOLUME_BUTTON_CLICK)],
        [
            InlineKeyboardButton(
                text=MONITOR, callback_data=MONITOR_BUTTON_CLICK
            )
        ],
        [InlineKeyboardButton(text=POWER, callback_data=POWER_BUTTON_CLICK)],
        [
            InlineKeyboardButton(
                text=KEYBOARD, callback_data=KEYBOARD_BUTTON_CLICK
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_change_volume_buttons():
    first_block = [
        InlineKeyboardButton(
            text=str(item) + "%", callback_data=CHANGE_VOLUME + str(item)
        )
        for item in range(5, 56, 5)
    ]

    second_block = [
        InlineKeyboardButton(
            text=str(item) + "%", callback_data=CHANGE_VOLUME + str(item)
        )
        for item in range(55, 101, 5)
    ]
    first_row = [
        InlineKeyboardButton(
            text=MUTE_VOLUME_TEXT, callback_data=CHANGE_VOLUME + "0"
        )
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

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


def get_change_brightness_buttons():
    buttons = [
        InlineKeyboardButton(
            text=str(item) + "%", callback_data=CHANGE_BRIGHTNESS + str(item)
        )
        for item in range(25, 101, 25)
    ]

    keyboard = [
        [
            InlineKeyboardButton(
                text=NIGHT_SWITCH_TEXT, callback_data=CHANGE_BRIGHTNESS + "0"
            )
        ]
    ]
    for i in range(2):
        row = [buttons[i], buttons[i + 2]]
        keyboard.append(row)
    keyboard.append(cancel_button)
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


def get_change_shutdown_buttons():
    shutdown_now = [
        InlineKeyboardButton(
            text=SHUTDOWN_NOW, callback_data=CHANGE_SHUTDOWN + "1"
        )
    ]
    first_column_shutdown = [
        InlineKeyboardButton(
            text=str(item) + " мин", callback_data=CHANGE_SHUTDOWN + str(item)
        )
        for item in range(10, 30, 5)
    ]
    second_column_shutdown = [
        InlineKeyboardButton(
            text=str(item) + " мин", callback_data=CHANGE_SHUTDOWN + str(item)
        )
        for item in range(30, 61, 10)
    ]
    third_column_shutdown = [
        InlineKeyboardButton(
            text=str(item) + " мин", callback_data=CHANGE_SHUTDOWN + str(item)
        )
        for item in range(90, 181, 30)
    ]
    keyboard = [shutdown_now]
    for item in range(4):
        row = [
            first_column_shutdown[item],
            second_column_shutdown[item],
            third_column_shutdown[item],
        ]
        keyboard.append(row)
    keyboard.append(cancel_shutdown)
    keyboard.append(cancel_button)
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


def get_cancel_shutdown_buttons():
    keyboard = [cancel_shutdown, cancel_button]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


def get_keyboard_buttons():
    space_button = [
        InlineKeyboardButton(text=SPACE_BUTTON_TEXT, callback_data=SPACE_CLICK)
    ]
    keyboard = [space_button, cancel_button]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup
