from aiogram import Router
from .start import router as start_router
from .admin import router as admin_router

router = Router()

router.include_routers(
    start_router,
    admin_router
)