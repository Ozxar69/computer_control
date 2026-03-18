START_BUTTON = "start"
START_REPLAY = "Привет!\nЯ помогу тебе управлять твоим компьютером.\nВыбери функцию:\n"
VOLUME = "🔉Громкость"
VOLUME_BUTTON_CLICK = "volume_click"
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

HOME_BUTTON_CLICK = "HOME_CLICK"
HOME_BUTTON = "🏠 Дом"
SMART_HOME_MANAGEMENT = "Главное меню управления устройствами\n\nВыбери категорию:"
LIGHTS_MENU_TITLE = "💡 Управление освещением:"
OUTLETS_MENU_TITLE = "🔌 Управление розетками:"
LOADING_LIGHTS_MSG = "🔍 Загружаю список света..."
LOADING_OUTLETS_MSG = "🔍 Загружаю список розеток..."
NO_LIGHTS_MSG = "⚠️ Нет доступных устройств освещения"
NO_OUTLETS_MSG = "⚠️ Нет доступных розеток"
ERROR_MSG_TEMPLATE = "⚠️ Ошибка: {error}"

HOME_BUTTON_TEXT = "🏠 Дом"
LIGHTS_BUTTON_TEXT = "💡 Свет"
OUTLETS_BUTTON_TEXT = "🔌 Розетки"
BACK_BUTTON_TEXT = "🔙 Назад"
ONLINE_ICON = "🟢"
OFFLINE_ICON = "🔴"
DEVICE_BUTTON_TEXT = "{status} {name}"

LIGHTS_MENU_CLICK = "LIGHTS_MENU"
OUTLETS_MENU_CLICK = "OUTLETS_MENU"
BACK_TO_MAIN_CLICK = "SMART_HOME_MAIN"
DEVICE_CLICK_PREFIX = "DEVICE_"
LIGHT = "light"
OUTLET = "outlet"

DEVICE_INFO_TEMPLATE = """{name}
Текущее состояние:

Основной переключатель: {status}
{additional_info}"""

STATUS_ON = "Включено ✅"
STATUS_OFF = "Выключено ❌"

TURN_ON_TEXT = "🔘 Включить"
TURN_OFF_TEXT = "🔘 Выключить"
BACK_TO_DEVICES_TEXT = "⬅️ К списку устройств"

DEVICE_STATUS_HEADER = "💡 {name}\n━━━━━━━━━━━━"
MAIN_SWITCH_STATUS = "🔘 Основной: {status}"
EXTRA_SWITCH_STATUS = "🔘 Дополнительный: {status}"

MAIN_SWITCH_BUTTON = "🔄 Основной: {state}"
EXTRA_SWITCH_BUTTON = "🔄 Дополнительный: {state}"

TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
ADMIN_IDS = "ADMIN_IDS"
ACCESS_DENIED = "Access denied."

# Logging messages
LOG_START_COMMAND = "Start command from user %d"
LOG_VOLUME_GET_ERROR = "Failed to get volume from API: %s"
LOG_VOLUME_SET = "Volume set to %d%% by user %d"
LOG_VOLUME_SET_ERROR = "Failed to set volume: %s"
LOG_BRIGHTNESS_GET_ERROR = "Failed to get brightness from API: %s"
LOG_BRIGHTNESS_SET = "Brightness set to %d%% by user %d"
LOG_BRIGHTNESS_SET_ERROR = "Failed to set brightness: %s"
LOG_POWER_GET_ERROR = "Failed to get power status: %s"
LOG_SHUTDOWN_SET = "Shutdown timer set to %d min by user %d"
LOG_SHUTDOWN_SET_ERROR = "Failed to set shutdown timer: %s"
LOG_SHUTDOWN_CANCEL = "Shutdown cancelled by user %d"
LOG_SHUTDOWN_CANCEL_ERROR = "Failed to cancel shutdown: %s"
LOG_PLAY_PAUSE = "Play/Pause by user %d"
LOG_PLAY_PAUSE_ERROR = "Failed to trigger play/pause: %s"
LOG_LIGHTS_LOAD_ERROR = "Failed to load lights: %s"
LOG_OUTLETS_LOAD_ERROR = "Failed to load outlets: %s"
LOG_DEVICE_TOGGLE_ERROR = "Device toggle error for %s: %s"
LOG_DEVICE_INFO_ERROR = "Device info error for %s: %s"
