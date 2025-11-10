import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher
from handlers import router as main_router
from handlers.notification import NotificationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token = config('TOKEN'))
    dp = Dispatcher()
    dp.include_router(main_router)

    notification_service = NotificationService(bot)
    notification_task = asyncio.create_task(notification_service.schedule_daily_notifications())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    notification_service.stop()
    notification_task.cancel()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())