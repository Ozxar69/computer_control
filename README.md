# Computer Control

Проект для удаленного управления Windows-компьютером через Telegram.

Система разделена на две части:

- `FastAPI` сервис на хосте Windows (доступ к железу и ОС).
- `telegram_bot` в Docker (UI и команды в Telegram).

## Что умеет

- Управление громкостью (0-100, шаг 5, mute).
- Переключение устройства вывода звука.
- Показ текущего устройства в меню громкости.
- Управление яркостью монитора.
- Таймер выключения ПК и отмена.
- Кнопка Play/Pause (эмуляция пробела).

## Актуальная архитектура

`telegram_bot` не управляет системой напрямую.
Он вызывает HTTP API по адресу `FASTAPI_URL`.

```text
Telegram -> telegram_bot (Docker) -> FastAPI (Windows host) -> ОС/устройства
```

Важно:

- в `docker-compose.yml` запускаются только `telegram_bot`, `seq`, `sqelf`;
- `FastAPI` нужно запускать отдельно на хосте Windows.

## Структура проекта

```text
.
├── fastapi_main.py
├── routes/
│   ├── volume.py
│   ├── brightness.py
│   ├── power.py
│   └── keyboard.py
├── volume/volume_control.py
├── screen/screen_control.py
├── system/power_management.py
├── keyboard/
├── telegram_bot/
│   ├── main.py
│   ├── client.py
│   ├── data.py
│   ├── .env.example
│   ├── Dockerfile
│   └── bot/
│       ├── handlers.py
│       └── buttons.py
└── docker-compose.yml
```

## Настройка окружения

### 1) FastAPI (.env в корне)

Скопируй `.env.example` в `.env` и заполни:

- `CC_API_KEY`
- `FASTAPI_PORT`
- `SEQ_URL`
- `SEQ_PORT`
- параметры устройств Tuya (если нужны)

### 2) Telegram bot (`telegram_bot/.env`)

Скопируй `telegram_bot/.env.example` в `telegram_bot/.env` и заполни:

- `TELEGRAM_BOT_TOKEN`
- `ADMIN_IDS`
- `CC_API_KEY` (должен совпадать с корневым `.env`)
- `FASTAPI_URL` (например `http://host.docker.internal:8765`)
- `SEQ_URL` (обычно `http://seq:80`)

## Запуск

### Запуск FastAPI на хосте Windows

Из корня проекта:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python fastapi_main.py
```

### Запуск Telegram bot + Seq в Docker

Из корня проекта:

```bash
docker compose up -d --build
```

## Полезные команды

Перезапуск только бота:

```bash
docker compose restart telegram_bot
```

Логи бота:

```bash
docker compose logs -f --tail=200 telegram_bot
```

Проверка API с хоста:

```bash
curl -H "X-API-Key: <CC_API_KEY>" http://127.0.0.1:8765/volume/
```

## API (основное)

- `GET /volume/` -> текущая громкость и устройство.
- `POST /volume/` -> установка громкости.
- `POST /volume/switch-output` -> переключение output-устройства.
- `GET /brightness/`, `POST /brightness/`
- `GET /power/`, `POST /power/shutdown`, `DELETE /power/shutdown`
- `POST /keyboard/play-pause`

## Особенности по звуку

- Переключение устройства вывода реализовано через Windows COM.
- В `volume/volume_control.py` задан список приоритетных устройств:
  `PRIMARY_OUTPUT_DEVICE_IDS`.
- В меню бота отображается имя текущего устройства и отдельная кнопка
  переключения.

## Troubleshooting

`Unknown device` и `Громкость сейчас: ?%` в боте:

- обычно это ошибка API `/volume`;
- проверь, что FastAPI реально запущен на `FASTAPI_PORT`;
- проверь логи FastAPI и `CC_API_KEY`.

`404` на `/volume/switch-output`:

- запущен старый процесс FastAPI без нового роута;
- перезапусти `python fastapi_main.py`.

Бот не достучался до API:

- проверь `FASTAPI_URL` в `telegram_bot/.env`;
- из контейнера используется `host.docker.internal`.
