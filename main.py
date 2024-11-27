import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram import F
from dotenv import load_dotenv

from db import create_tables
from commands import router as command_router
from inline_mode import router as inline_router

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, prase_mode=ParseMode.HTML)

MEDIA_DIR = "saved_media"
os.makedirs(MEDIA_DIR, exist_ok=True)

async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(command_router, inline_router)

    create_tables()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
