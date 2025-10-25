from aiogram import Router
from .start import router as start_router
from .admin import router as admin_router
from .profile import router as profile_router
from .scrolling_habits import router as scroll_habit_router


router = Router()

router.include_routers(
    start_router,
    admin_router,
    profile_router,
    scroll_habit_router
)