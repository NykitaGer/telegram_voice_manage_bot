from aiogram import Router, F
from aiogram.types import (
    InlineQuery,
    InlineQueryResultVoice,
    InputTextMessageContent,
    InputInvoiceMessageContent
)

from aiogram.fsm.context import FSMContext
from db import (
    get_voices_from_db
)

router = Router()


@router.inline_query()
async def inline_voice_message(inline_query: InlineQuery):
    user_query = inline_query.query.strip()
    voices = get_voices_from_db()
    
    filtered_voices = [
        (file_id, name) for file_id, name in voices if user_query.lower() in name.lower()
    ] if user_query else voices

    results = [
        InlineQueryResultVoice(
            id=(f"{index}-{file_id}")[:64],
            voice_url=file_id,
            title=name,
            caption=name
        )
        for index, (file_id, name) in enumerate(filtered_voices)
    ]

    await inline_query.answer(results, cache_time=0, is_personal=True)
