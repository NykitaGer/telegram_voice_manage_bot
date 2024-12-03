from .general import router as general_router
from .admin import router as admin_router
from .voice import router as voice_router

__all__ = [
    "general_router",
    "admin_router",
    "voice_router"
]
