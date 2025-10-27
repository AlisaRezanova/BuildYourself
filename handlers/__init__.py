from aiogram import Router
from .start import router as start_router
from .admin import router as admin_router
from .profile import router as profile_router
from .scrolling import router as scroll_router
from .main_menu import router as main_menu_router
from .achievements import router as achievements_router
from .friends import router as friends_router
from .requests_in_friends import router as req_router


router = Router()

router.include_routers(
    start_router,
    admin_router,
    profile_router,
    scroll_router,
    main_menu_router,
    achievements_router,
    friends_router,
    req_router
)