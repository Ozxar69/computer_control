import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import register_handlers
from data import TELEGRAM_BOT_TOKEN
from system.power_management import cancel_shutdown_timer

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv(TELEGRAM_BOT_TOKEN)


bot = Bot(token=TOKEN)
dp = Dispatcher()


register_handlers(dp)


async def main():
    cancel_shutdown_timer()

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
