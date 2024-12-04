from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db import DatabaseManager
from utils import is_user_admin, VideoSave

router = Router()
db = DatabaseManager()


@router.message(F.text, Command("add_video"))
async def add_voice(message: Message, state: FSMContext):
    if not is_user_admin(db, message.from_user.id):
        await message.answer("❌You don't have permissions for this command!")
        return
    db.set_video_pending(message.chat.id, True)
    await state.set_state(VideoSave.waiting_for_name)
    await message.answer("✅Send your video messages")

@router.message(F.text, Command("stop_video"), VideoSave.waiting_for_name)
async def stop_adding_voice(message: Message, state: FSMContext):
    db.set_video_pending(message.chat.id, False)
    await message.answer("⚠️Future video messages won't be saved!")
    await state.clear()

@router.message(F.text, Command("get_videos"))
async def get_videos(message: Message):
    videos = db.get_videos()
    result = "Videos:\n" + "\n".join(f"{index+1}. {voice[1]}" for index, voice in enumerate(videos))
    await message.answer(result)

@router.message(F.video_note, VideoSave.waiting_for_name)
async def video_handler(message: Message, state: FSMContext):
    if not db.is_video_pending(message.chat.id):
        return

    await state.update_data(video_note_file_id=message.video_note.file_id)
    await message.answer("Send a name for video")
    await state.set_state(VideoSave.waiting_for_name)

@router.message(F.text, VideoSave.waiting_for_name)
async def video_name_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    video_file_id = data.get("video_note_file_id")

    video_name = message.text.strip()

    db.add_video(video_file_id, video_name or "Unnamed video")
    await message.answer("✅Video was added!")
    await state.clear()
