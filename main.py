import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher
from handlers import router as main_router
from handlers.notification import NotificationService
from handlers.habit_cleanup import HabitCleanupService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token = config('TOKEN'))
    dp = Dispatcher()
    dp.include_router(main_router)

    notification_service = NotificationService(bot)
    notification_task = asyncio.create_task(notification_service.schedule_daily_notifications())
    cleanup_service = HabitCleanupService(bot)
    cleanup_task = asyncio.create_task(cleanup_service.schedule_cleanup())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    notification_service.stop()
    cleanup_service.stop()
    notification_task.cancel()
    cleanup_task.cancel()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())