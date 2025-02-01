# Телеграм-бот для управления системными параметрами


Этот телеграм-бот позволяет управлять различными системными параметрами, такими как громкость звука, яркость монитора, выключение компьютера и управление медиаплеером. Бот предоставляет интерактивные кнопки для удобного управления.

## Возможности бота


### Активация бота:
* Бот отправляет сообщение о том, что он активирован, с кнопками для дальнейших действий.
### Управление громкостью:
* Изменение уровня громкости (от 0% до 100% с шагом 5%).
* Возможность включения/выключения звука (Mute).
### Управление яркостью монитора:
* Изменение уровня яркости (25%, 50%, 75%, 100%).
* Включение ночного режима (0% яркости).
### Управление питанием:
* Запуск таймера выключения компьютера (от 10 минут до 3 часов).
* Отмена запланированного выключения.
### Подтверждение и отмена бронирования:
* Запуск таймера выключения компьютера (от 10 минут до 3 часов).
* Отмена запланированного выключения.
### Управление медиаплеером:
* Воспроизведение/пауза медиа (пробел).
### Интерактивные кнопки:
* Удобное управление через кнопки в Telegram.
* Возможность отмены действий.
## Используемые технологии
#### Языки программирования:
* Python 3.12.0
#### Библиотеки:
* [aiogram  3.17.0](https://docs.aiogram.dev/en/latest/) — асинхронный фреймворк для создания Telegram-ботов.
* [pycaw](https://github.com/AndreMiras/pycaw) — библиотека для управления громкостью звука в Windows.
* [screen-brightness-control](https://pypi.org/project/screen-brightness-control/) — библиотека для управления яркостью монитора.
* [os](https://docs.python.org/3/library/os.html) — стандартная библиотека Python для работы с системными командами (например, выключение компьютера).
* [time](https://docs.python.org/3/library/time.html) — стандартная библиотека Python для работы с временем (например, таймеры).
#### Стиль кода
Проект использует стиль кодирования Black для обеспечения единообразия и читаемости кода.
#### Теги
🐍 Python
📦 pycaw
📱 aiogram
⚙️ os
🎨 Black Style

## Установка

1. Клонируйте репозиторий:
``` bash
git clone <URL_репозитория>
```
2. Перейдите в директорию проекта:
``` bash
cd <имя_директории>
```
3. Создайте и активируйте виртуальное окружение:
``` bash
python -m venv venv 
``` 
* Если у вас Linux/macOS:
``` bash
source venv/bin/activate
```
* Если у вас Windows:
``` bash
. venv/Scripts/activate 
```
4. Установите зависимости:
``` bash
pip install -r requirements.txt
```
## Запуск
На основе файла example_env создайте файл .env и заполните его

Для запуска бота выполните следующую команду:
``` bash
python main.py
```
## Команды бота
* /start — запуск бота и отображение главного меню с кнопками.
* Громкость — управление уровнем громкости.
* Яркость — управление уровнем яркости монитора.
* Питание — управление выключением компьютера.
* Клавиатура — управление медиаплеером (пробел для воспроизведения/паузы).

## Структура проекта
``` bash
bot/
├── main.py              # Основной файл с логикой бота
├── buttons.py           # Функции для создания кнопок
├── volume_control.py    # Логика управления громкостью
├── brightness_control.py # Логика управления яркостью
├── power_control.py     # Логика управления питанием
├── media_control.py     # Логика управления медиаплеером
├── README.md            # Документация
```


## Вклад
Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест с вашими изменениями.

Автор: [Ozxar69](https://github.com/Ozxar69)