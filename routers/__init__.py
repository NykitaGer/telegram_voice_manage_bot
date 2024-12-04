from .general import router as general_router
from .admin import router as admin_router
from .voice import router as voice_router
from .inline import router as inline_router
from .video import router as video_router

__all__ = [
    "general_router",
    "admin_router",
    "voice_router",
    "inline_router",
    "video_router"
]
