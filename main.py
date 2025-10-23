import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher
from handlers import router as main_router


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token = config('TOKEN'))
    dp = Dispatcher()
    dp.include_router(main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())