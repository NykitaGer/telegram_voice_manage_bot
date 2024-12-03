import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv

from db import DatabaseManager
from routers import admin, voice, general, inline


load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)

db_manager = DatabaseManager()

# MEDIA_DIR = "../saved_media"
# os.makedirs(MEDIA_DIR, exist_ok=True)

async def main() -> None:
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(voice.router)
    dp.include_router(general.router)
    dp.include_router(inline.router)

    db_manager._create_tables()

    bot_commands = [
        BotCommand(command="/get_voices", description="Get available voices"),
        BotCommand(command="/get_users", description="Get all users"),
        BotCommand(command="/add_voice", description="All voice messages below will be automatically added"),
        BotCommand(command="/stop_voice", description="Stops adding voice messages")
    ]

    await bot.set_my_commands(commands=bot_commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
