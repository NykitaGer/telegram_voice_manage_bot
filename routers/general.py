from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db.manager import DatabaseManager

router = Router()
db = DatabaseManager()

@router.message(F.text, Command("start"))
async def start_function(message: Message):
    db.add_chat(message.chat.id)
    db.add_user(message.from_user.id, message.from_user.username, False)
    await message.answer("Welcome to VoiceManager!")
