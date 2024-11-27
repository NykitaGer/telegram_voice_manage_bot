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
    inline_query
    for index, file_id, name in enumerate(voices):
        # message_content = InputTextMessageContent(
        #     message_text="" # TODO: here needs to send a voice message by its id
        # )
        result_id = f"{index}-{inline_query.from_user.id}"
        results.append(InlineQueryResultAudio(
            id=result_id, audio_url=file_id
        ))
        # results.append(InlineQueryResultArticle(
        #     id=result_id, title=name, input_message_content=message_content
        # ))

    await inline_query.answer(results, cache_time=0, is_personal=True)
