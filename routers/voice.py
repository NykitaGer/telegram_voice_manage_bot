from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db.manager import DatabaseManager
from utils.permissions import is_user_admin

router = Router()
db = DatabaseManager()

@router.message(F.text, Command("add_voice"))
async def add_voice(message: Message):
    # if not is_user_admin(db, message.from_user.id):
    #     await message.answer("❌You don't have permissions for this command!")
    #     return
    db.set_voice_pending(message.chat.id, True)
    await message.answer("✅Send your voice messages")

@router.message(F.text, Command("stop_voice"))
async def stop_adding_voice(message: Message):
    db.set_voice_pending(message.chat.id, False)
    await message.answer("⚠️Future voice messages won't be saved!")

@router.message(F.text, Command("get_voices"))
async def get_voices(message: Message):
    voices = db.get_voices()
    result = "Voices:\n" + "\n".join(f"{index+1}. {voice[1]}" for index, voice in enumerate(voices))
    await message.answer(result)

@router.message(F.text, Command("delete_voice"))
async def delete_voice(message: Message):
    if not is_user_admin(db, message.from_user.id):
        await message.answer("❌You don't have permissions for this command!")
        return
    
    _, voice_name = message.text.split(maxsplit=1)
    db.delete_voice(voice_name)
    await message.answer("✅Voice was deleted successfully")

@router.message(F.voice)
async def voice_handler(message: Message):
    if not db.is_voice_pending(message.chat.id):
        return
    db.add_voice(message.voice.file_id, message.caption or "Unnamed Voice")
    await message.answer("✅Voice message was added!")
