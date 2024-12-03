from aiogram import Router, F
from aiogram.types import Message, Voice
from aiogram.filters import Command
from aiogram.enums import ParseMode

from db import *


router = Router()


@router.message(F.text, Command("start"))
async def start_function(message: Message):
    add_chat_id(message.chat.id)
    add_user(message.from_user.id, message.from_user.username, False)
    await message.answer("Welcome to VoiceManager!")


@router.message(F.text, Command("get_users"))
async def get_users(message: Message):
    is_admin = is_user_admin(message.from_user.id)
    if not is_admin:
        await message.answer("❌You don't have permissions for this command!")
        return
    
    users = get_users_from_db()
    result = "Users:\n"
    for user_id, username, is_admin in users:
        result += f"{username} - {user_id} | {is_admin}\n"
    await message.answer(result)


@router.message(F.text, Command("make_admin"))
async def make_admin(message: Message):
    is_admin = is_user_admin(message.from_user.id)
    if not is_admin:
        if message.from_user.id == 517842442:
            pass
        else:
            await message.answer("❌You don't have permissions for this command!")
            return
    
    splitted_mesage = message.text.split()
    user_id = splitted_mesage[1]
    change_user_permission(user_id, True) # to make user an admin
    await message.answer("✅This user is now an admin!")


@router.message(F.text, Command("add_voice"))
async def add_voice(message: Message):
    is_admin = is_user_admin(message.from_user.id)
    if not is_admin:
        await message.answer("❌You don't have permissions for this command!")
        return
    change_voice_pending(message.chat.id, True)
    await message.answer("✅Send your voice messages")


@router.message(F.text, Command("stop_voice"))
async def stop_adding_voice(message: Message):
    change_voice_pending(message.chat.id, False)
    await message.answer("⚠️Future voice messages won't be saved!")


@router.message(F.text, Command("get_voices"))
async def get_voices(message: Message):
    data = get_voices_from_db()

    result = "Voices:\n"
    for index, (id, name) in enumerate(data):
        result += f"{index+1}. {name}\n"

    await message.answer(result)


@router.message(F.text, Command("delete_voice"))
async def delete_voice(message: Message):
    is_admin = is_user_admin(message.from_user.id)
    if not is_admin:
        await message.answer("❌You don't have permissions for this command!")
        return
    
    splitted_message = message.text.split()
    voice_name = splitted_message[1]
    delete_voice_from_db(voice_name)
    await message.answer("✅Voice was deleted successfully")


@router.message(F.voice)
async def voice_handler(message: Message):
    check = check_voice_pending(message.chat.id)
    if (check == False):
        return
    add_voice_to_db(message.voice.file_id, message.caption)
    await message.answer("Voice message was added!")