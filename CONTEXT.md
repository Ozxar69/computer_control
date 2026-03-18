# computer_control — контекст проекта

## Архитектура

Проект разделён на два независимых сервиса:

### 1. FastAPI (нативный Windows-сервис)
- Запускается напрямую на Windows через `python fastapi_main.py`
- Автозапуск через ярлык `run.vbs` → `run.bat`
- Управляет железом: громкость (`pycaw`), яркость (`screen_brightness_control`), клавиатура (`pynput`/`PyAutoGUI`), питание (`os.system shutdown`), умный дом (`tinytuya`)
- Слушает на порту из `FASTAPI_PORT` (.env)
- Защищён API-ключом: каждый запрос должен содержать заголовок `X-API-Key`
- Логи шлёт напрямую в Seq через кастомный `SeqHandler` (CLEF-формат, `/api/events/raw`)

### 2. Telegram Bot (Docker-контейнер)
- Запускается через `docker compose up -d`
- Не имеет доступа к железу — только кнопки и вызовы FastAPI через `httpx`
- Логи уходят через Docker GELF log driver → sqelf → Seq

### 3. sqelf (Docker-контейнер)
- Официальный Seq-коллектор для Docker (`datalust/sqelf`)
- Принимает GELF-логи от Docker-демона на порту `12201/udp`
- Пробрасывает их в Seq

### 4. Seq (Docker-контейнер)
- Централизованный лог-сервер (`datalust/seq`)
- Доступен на `http://localhost:{SEQ_PORT}` (значение из `.env`)
- Аутентификация отключена (`SEQ_FIRSTRUN_NOAUTHENTICATION=true`)

---

## Структура файлов

```
computer_control/
├── fastapi_main.py          # Точка входа FastAPI. SeqHandler, ApiKeyMiddleware, роутеры
├── run.bat                  # python fastapi_main.py
├── run.vbs                  # Запускает run.bat без окна (автозапуск)
├── requirements.txt         # Зависимости FastAPI-сервиса
├── .env                     # Секреты (не в git)
├── .env.example             # Шаблон переменных
│
├── routes/
│   ├── volume.py            # GET/POST /volume/
│   ├── brightness.py        # GET/POST /brightness/  (WMI-safe через _safe_get_brightness)
│   ├── keyboard.py          # POST /keyboard/play-pause
│   ├── power.py             # GET /power/, POST /power/shutdown, DELETE /power/shutdown
│   └── home.py              # GET /home/devices, GET/POST /home/devices/{id}/toggle
│
├── system/
│   └── power_management.py  # Таймер выключения (_flag, _end_time, московское время)
│
├── devices/                 # Tuya-устройства (tinytuya)
├── volume/                  # pycaw
├── screen/                  # screen_brightness_control
├── keyboard/                # pynput / PyAutoGUI
│
├── docker-compose.yml       # telegram_bot + sqelf + seq
│
└── telegram_bot/
    ├── Dockerfile           # python:3.13-slim, PYTHONUNBUFFERED=1
    ├── requirements.txt     # aiogram, httpx, python-dotenv, pytz
    ├── .env                 # Секреты бота (не в git)
    ├── .env.example         # Шаблон
    ├── main.py              # Запуск бота, retry-цикл с exponential backoff
    ├── client.py            # httpx.AsyncClient, X-API-Key заголовок, follow_redirects=True
    ├── admin.py             # Декоратор @access (проверка ADMIN_IDS)
    ├── data.py              # Все строковые константы и LOG_* константы
    └── bot/
        ├── handlers.py      # Все callback и command хендлеры
        └── buttons.py       # Инлайн-клавиатуры
```

---

## Переменные окружения

### `D:\Dev\computer_control\.env` (FastAPI)
```
CC_API_KEY=        # Статический ключ защиты API (совпадает с ботом)
FASTAPI_PORT=      # Порт FastAPI, например 8765
SEQ_URL=           # http://localhost:{SEQ_PORT}
SEQ_PORT=          # Порт Seq, например 5341

DEVICE_1_NAME=
DEVICE_1_TYPE=     # light | outlet
DEVICE_1_ID=
DEVICE_1_IP=
DEVICE_1_KEY=
DEVICE_1_VERSION=  # 3.4
# ... DEVICE_2_*, DEVICE_3_* и т.д.
```

### `D:\Dev\computer_control\telegram_bot\.env` (бот)
```
TELEGRAM_BOT_TOKEN=
ADMIN_IDS=          # Через запятую, например 792230644
CC_API_KEY=         # Тот же ключ что в FastAPI .env
FASTAPI_URL=        # http://host.docker.internal:{FASTAPI_PORT}
```

---

## Запуск

### Первый запуск / после изменений в боте
```powershell
cd D:\Dev\computer_control
docker compose down
docker compose up -d --build
```

### Перезапуск только бота
```powershell
docker compose up -d --build telegram_bot
```

### Запуск FastAPI (нативно)
```powershell
cd D:\Dev\computer_control
python fastapi_main.py
```

### Проверка статуса
```powershell
docker compose ps
docker compose logs telegram_bot
docker compose logs sqelf
```

---

## Логирование

### Бот (Docker)
- Пишет в stdout через стандартный `logging.basicConfig`
- Docker GELF log driver захватывает stdout и шлёт в sqelf на `host.docker.internal:12201`
- В Seq события имеют свойства: `tag = 'cc.telegram_bot'`, `container_name = 'cc_telegram_bot'`
- Заглушены шумные логгеры: `httpx`, `httpcore`, `aiogram.event`

### FastAPI (нативный)
- Кастомный `SeqHandler` в `fastapi_main.py` — фоновый поток, очередь, POST на `/api/events/raw` с `Content-Type: application/vnd.serilog.clef`
- В Seq события имеют свойство `Application = 'cc.fastapi'`
- Заглушен `screen_brightness_control` (WMI-ошибки внешнего монитора)
- uvicorn запущен с `access_log=False` и `disable_existing_loggers=False` чтобы не сбрасывать SeqHandler

### Фильтрация в Seq
- Бот: `tag = 'cc.telegram_bot'`
- FastAPI: `Application = 'cc.fastapi'`

---

## Известные особенности

1. **Внешний монитор и яркость**: `get_brightness()` бросает WMI-исключение на внешних мониторах. Решено через `_safe_get_brightness()` в `routes/brightness.py` — возвращает запрошенное значение как fallback.

2. **FastAPI redirect**: роуты FastAPI без слеша (`/volume`) редиректят на `/volume/`. Бот использует `follow_redirects=True` в httpx.

3. **SEQ_PORT**: должен быть явно задан в `.env`. Если пустой — Docker назначит случайный порт. SEQ_URL для FastAPI должен совпадать: `http://localhost:{SEQ_PORT}`.

4. **seqlog не используется**: библиотека `seqlog` несовместима с uvicorn (сбрасывает логгеры) и слала логи в устаревшем формате. Заменена на кастомный `SeqHandler`.

5. **Fluent Bit не используется**: заменён на `sqelf` (официальный Docker→Seq коллектор), т.к. Fluent Bit не мог корректно выставить `Content-Type: application/vnd.serilog.clef`.
