import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram import F
from dotenv import load_dotenv

from db import create_tables
from inline_mode import router as inline_router
from commands import router as command_router

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)

# MEDIA_DIR = "../saved_media"
# os.makedirs(MEDIA_DIR, exist_ok=True)

async def main() -> None:
    dp = Dispatcher()

    dp.include_router(inline_router)
    dp.include_router(command_router)

    create_tables()

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
