import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token = config('TOKEN'))
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())