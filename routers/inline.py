from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultVoice
from db.manager import DatabaseManager

router = Router()
db = DatabaseManager()

@router.inline_query()
async def inline_voice_message(inline_query: InlineQuery):
    user_query = inline_query.query.strip()

    voices = db.get_voices()

    filtered_voices = [
        (file_id, name) for file_id, name in voices if user_query.lower() in name.lower()
    ] if user_query else voices

    results = [
        InlineQueryResultVoice(
            id=(f"{index}-{file_id}")[:64],  # Tetegram's limit of 64 characters
            voice_url=file_id,
            title=name,
            #caption=name
        )
        for index, (file_id, name) in enumerate(filtered_voices)
    ]

    await inline_query.answer(results, cache_time=0, is_personal=True)
