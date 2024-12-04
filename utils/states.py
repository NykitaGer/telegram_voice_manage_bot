from aiogram.fsm.state import StatesGroup, State


class VideoSave(StatesGroup):
    waiting_for_name = State()
