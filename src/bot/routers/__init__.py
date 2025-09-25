__all__ = "router"

from aiogram import Router

from .user_commands import router as user_commands_router

router = Router(name=__name__)

router.include_routers(
    user_commands_router,
)
