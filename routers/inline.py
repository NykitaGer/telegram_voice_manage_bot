from aiogram import Router
from aiogram.types import (
    InlineQuery, 
    InlineQueryResultVoice, 
    InlineQueryResultCachedVideo
)

from db import DatabaseManager

router = Router()
db = DatabaseManager()

@router.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    user_query = inline_query.query.strip()

    # Fetch voices and videos from the database
    voices = db.get_voices()
    videos = db.get_videos()

    # Filter by user query
    filtered_voices = [
        (file_id, name) for file_id, name in voices if user_query.lower() in name.lower()
    ] if user_query else voices

    filtered_videos = [
        (file_id, name) for file_id, name in videos if user_query.lower() in name.lower()
    ] if user_query else videos

    # Prepare results for inline query
    voice_results = [
        InlineQueryResultVoice(
            id=f"voice-{index}-{file_id}"[:64],
            voice_url=file_id,
            title=name
        )
        for index, (file_id, name) in enumerate(filtered_voices)
    ]

    video_results = [
        InlineQueryResultCachedVideo(
            id=f"video-{index}-{file_id}"[:64],
            video_file_id=file_id,
            title=name
        )
        for index, (file_id, name) in enumerate(filtered_videos)
    ]

    # Combine results and respond
    results = voice_results + video_results

    await inline_query.answer(results, cache_time=0, is_personal=True)
