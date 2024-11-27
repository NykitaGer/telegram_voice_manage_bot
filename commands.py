from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from db import add_voice_to_db


router = Router()

@router.message(F.text, Command("start"))
async def start_function(message: Message):
    await message.answer("Welcome to VoiceManager!")


@router.message(F.text, Command("add_voice"))
async def add_voice(message: Message):
    add_voice_to_db(message.message_id, "name can be the same") # this doesn't work in this way, just for testing
    await message.answer("Voice message was added!")
