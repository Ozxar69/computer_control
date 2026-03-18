import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import register_handlers
from data import TELEGRAM_BOT_TOKEN

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("aiogram.event").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv(TELEGRAM_BOT_TOKEN))
dp = Dispatcher()

register_handlers(dp)


async def main():
    logger.info("ComputerControl Bot starting...")
    retry_count = 0

    while True:
        try:
            logger.info("Starting polling (attempt %d)", retry_count + 1)
            await dp.start_polling(bot)
            retry_count = 0
        except Exception as e:
            retry_count += 1
            logger.error(
                "Polling error #%d [%s]: %s",
                retry_count,
                type(e).__name__,
                str(e),
            )
            wait_sec = min(5 * retry_count, 60)
            logger.info("Reconnecting in %ds...", wait_sec)
            await asyncio.sleep(wait_sec)


if __name__ == "__main__":
    asyncio.run(main())
