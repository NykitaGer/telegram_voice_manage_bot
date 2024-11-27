from aiogram import Router, F
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultAudio
)

from aiogram.fsm.context import FSMContext
from db import get_voices_from_db

router = Router()


@router.inline_query()
async def inline_voice_message(inline_query: InlineQuery):
    voices = get_voices_from_db()

    results = []
    
    for index, file_id, name in enumerate(voices):
        result_id = f"{index}-{inline_query.from_user.id}"
        results.append(InlineQueryResultAudio(
            id=result_id, title=name ,audio_url=file_id
        ))

    await inline_query.answer(results, cache_time=0, is_personal=True)


@router.inline_query()
async def inline_video_message(inline_query: InlineQuery):
    videos = 0 # TODO: create a function to get viodes from database

    results = []

    for index, file_id, name in enumerate(videos):
        result_id = f"{index}-{inline_query.from_user.id}"
        results.append(InlineQueryResultAudio(
            id=result_id, title=name ,audio_url=file_id
        ))

    await inline_query.answer(results, cache_time=0, is_personal=True)
