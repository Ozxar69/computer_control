from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import (
    CANCEL_BUTTON_CLICK,
    CANCEL_BUTTON_TEXT,
    CHANGE_BRIGHTNESS,
    CHANGE_VOLUME,
    MONITOR,
    MONITOR_BUTTON_CLICK,
    MUTE_VOLUME_TEXT,
    NIGHT_SWITCH_TEXT,
    VOLUME,
    VOLUME_BUTTON_CLICK,
)

cancel_button = [
    InlineKeyboardButton(
        text=CANCEL_BUTTON_TEXT, callback_data=CANCEL_BUTTON_CLICK
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

    keyboard = []
    keyboard.append(first_row)
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
