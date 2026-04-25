import asyncio
import sys
from loguru import logger
from src.config import Config
from src.db import init_db
from src.scheduler import start_scheduler

logger.remove()
logger.add(sys.stderr, level=Config.LOG_LEVEL, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.add("logs/parser_{time:YYYY-MM-DD}.log", rotation="10 MB", retention="30 days", level="INFO")


async def main():
    logger.info("🔌 Инициализация БД...")
    await init_db()

    scheduler = start_scheduler()
    logger.info("🏁 Парсер запущен. Ожидание задач...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Остановка по сигналу...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())