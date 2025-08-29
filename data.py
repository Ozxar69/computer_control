START_BUTTON = "start"
START_REPLAY = (
    "Привет!\nЯ помогу тебе управлять твоим компьютером.\nВыбери функцию:\n"
)
VOLUME = "🔉Громкость"
VOLUME_BUTTON_CLICK = "volume_click"

TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"

PERCENT = 100

CHANGE_TO_VOLUME = (
    "Меню управления громкостью\n\n"
    "Громкость сейчас: {volume}%\n\n"
    "Если хочешь изменить, выбери значение\n"
)

CANCEL_BUTTON_TEXT = "🔙 Отмена"
CANCEL_BUTTON_CLICK = "cancel"
CANCEL_CONFIRM_TEXT = "Хорошо, операция отменена"

CHANGE_VOLUME = "change_volume_"
MUTE_VOLUME_TEXT = "Выключить звук"

SUCCESS_TEXT = (
    "Операция выполнена!\n\n"
    "Уровень громкости сейчас: {volume}%\n\n"
    "Выбери функцию:\n\n"
)
SUCCESS_VOLUME_TEXT = "Уровень громкости изменен на: {volume}%"

FALSE_TEXT = "Произошла ошибка. Не удалось выполнить операцию"

MONITOR = "🖥 Экран"
MONITOR_BUTTON_CLICK = "monitor"

NIGHT_SWITCH_TEXT = "🌙 Ночной режим"
CHANGE_BRIGHTNESS = "change_brightness_"

CHANGE_TO_BRIGHTNESS = (
    "Меню управления яркостью\n\n"
    "Яркость сейчас: {brightness}%\n\n"
    "Если хочешь изменить, выбери значение\n"
)

SUCCESS_BRIGHTNESS_TEXT = "Уровень яркости изменен на: {brightness}%"
SUCCESS_BRIGHTNESS_MESSAGE = (
    "Операция выполнена!\n\n"
    "Уровень яркости сейчас: {brightness}%\n\n"
    "Выбери функцию:\n\n"
)
POWER = "🔌 Электропитание"
POWER_BUTTON_CLICK = "power"

SHUTDOWN_NOW = "Выключить сейчас"
CHANGE_SHUTDOWN = "change_shutdown_"
CANCEL_SHUTDOWN_TEXT = "Отменить выключение"
CANCEL_SHUTDOWN = "cancel_shutdown"

CHANGE_TO_POWER = (
    "Меню управления электропитанием\n\n"
    "Сейчас таймер не установлен\n\n"
    "Если хочешь установить, выбери время\n"
)

SUCCESS_SHUTDOWN_TEXT = "Таймер успешно установлен!"

ADMIN_IDS = "ADMIN_IDS"

ACCESS_DENIED = "Access denied."

SUCCESS_SHUTDOWN_MESSAGE = (
    "Операция выполнена!\n\n"
    "Компьютер будет выключен в {finish_time}\n\n"
    "Выбери функцию:\n\n"
)

SUCCESS_CANCEL_SHUTDOWN_TEXT = "Выключение отменено!"

SUCCESS_CANCEL_SHUTDOWN_MESSAGE = "Выключение отменено\n\nВыбери функцию:\n\n"

CHANGE_TO_POWER_TIMER = (
    "Меню управления электропитанием\n"
    "Сейчас таймер установлен\n\n"
    "Компьютер выключится в {time}\n"
    "Осталось примерно - {minutes}\n\n"
    "Можешь отменить\n"
)
KEYBOARD = "⌨️Клавиатура"
KEYBOARD_BUTTON_CLICK = "keyboard"
SPACE_BUTTON_TEXT = "Пауза/продолжить"
SPACE_CLICK = "space"

CHANGE_TO_KEYBOARD = (
    "Меню управления клавиатурой\n\n"
    "Можешь управлять нажатием клавиш\n"
    "Если активно видео, то пробелом можно нажать на паузу или возобновить его"
)

# Управление умным домом
HOME_BUTTON_CLICK = "HOME_CLICK"
HOME_BUTTON = "🏠 Дом"
DEVICES_BUTTON_TEXT = "{name} {status}"  # Формат: "Розетка гостиная ●"
SMART_HOME_MANAGEMENT = "Главное меню управления устройствами\n\nВыбери категорию:"
LIGHTS_MENU_TITLE = "💡 Управление освещением:"
OUTLETS_MENU_TITLE = "🔌 Управление розетками:"
LOADING_LIGHTS_MSG = "🔍 Загружаю список света..."
LOADING_OUTLETS_MSG = "🔍 Загружаю список розеток..."
NO_LIGHTS_MSG = "⚠️ Нет доступных устройств освещения"
NO_OUTLETS_MSG = "⚠️ Нет доступных розеток"
ERROR_MSG_TEMPLATE = "⚠️ Ошибка: {error}"

# Button Texts
HOME_BUTTON_TEXT = "🏠 Дом"
LIGHTS_BUTTON_TEXT = "💡 Свет"
OUTLETS_BUTTON_TEXT = "🔌 Розетки"
BACK_BUTTON_TEXT = "🔙 Назад"
ONLINE_ICON = "🟢"
OFFLINE_ICON = "🔴"
DEVICE_BUTTON_TEXT = "{status} {name}"  # Example: "🟢 Ванна"

# Callback Data

LIGHTS_MENU_CLICK = "LIGHTS_MENU"
OUTLETS_MENU_CLICK = "OUTLETS_MENU"
BACK_TO_MAIN_CLICK = "SMART_HOME_MAIN"
DEVICE_CLICK_PREFIX = "DEVICE_"
LIGHT = "light"
OUTLET = "outlet"

# Сообщения управления устройствами
DEVICE_INFO_TEMPLATE = """{name}
Текущее состояние: 

Основной переключатель: {status}
{additional_info}"""

STATUS_ON = "Включено ✅"
STATUS_OFF = "Выключено ❌"
STATUS_UNKNOWN = "Неизвестно ❓"

# Кнопки управления
TURN_ON_TEXT = "🔘 Включить"
TURN_OFF_TEXT = "🔘 Выключить"

SET_TIMER_TEXT = "⏱ Установить таймер"
BACK_TO_DEVICES_TEXT = "⬅️ К списку устройств"


# Статус устройства
DEVICE_STATUS_HEADER = "💡 {name}\n━━━━━━━━━━━━"
MAIN_SWITCH_STATUS = "🔘 Основной: {status}"
EXTRA_SWITCH_STATUS = "🔘 Дополнительный: {status}"

# Текст кнопок
MAIN_SWITCH_BUTTON = "🔄 Основной: {state}"
EXTRA_SWITCH_BUTTON = "🔄 Дополнительный: {state}"