import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import router as handlers
import database

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6272985102:AAETERKA6BaQjdE_yemA3iytIAFfubX2TMU")

dp = Dispatcher()


async def main():
    dp.include_routers(handlers)
    await dp.start_polling(bot)

if __name__ == "__main__":
    database.create_database_and_table()
    asyncio.run(main())