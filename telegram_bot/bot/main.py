import asyncio
import logging
import os
from aiogram import Bot, Dispatcher


# Настройки логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения.")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def on_startup():
    """Действия при старте бота."""
    logging.info("Бот запускается...")

    logging.info("Бот успешно запущен!")


async def on_shutdown():
    """Действия при остановке бота."""
    logging.info("Бот останавливается...")


async def main():
    """Точка входа в приложение."""
    # Регистрация функций запуска и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
