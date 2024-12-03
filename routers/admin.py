from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.permissions import is_user_admin
from db.manager import DatabaseManager

router = Router()
db = DatabaseManager()

@router.message(F.text, Command("get_users"))
async def get_users(message: Message):
    if not is_user_admin(db, message.from_user.id):
        await message.answer("❌You don't have permissions for this command!")
        return
    
    users = db.get_users()
    result = "Users:\n" + "\n".join(f"{user[1]} - {user[0]} | {user[2]}" for user in users)
    await message.answer(result)

@router.message(F.text, Command("make_admin"))
async def make_admin(message: Message):
    if not is_user_admin(db, message.from_user.id):
        await message.answer("❌You don't have permissions for this command!")
        return

    _, user_id = message.text.split(maxsplit=1)
    db.change_user_permission(int(user_id), True)
    await message.answer("✅This user is now an admin!")
