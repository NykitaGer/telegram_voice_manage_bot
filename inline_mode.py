from aiogram import Router, F
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle
)

from aiogram.fsm.context import FSMContext

router = Router()


def get_voice_messages() -> list[str] | None:
    
    return 


@router.inline_query()
async def inline_voice_message(inline_query: InlineQuery):
    return
