from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from decouple import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.admin_kb import admin_kb


bot = Bot(token = config('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

router = Router()

ADMIN = [int(x) for x in config('ADMIN').split(',')]

@router.message(Command('admin'))
async def get_admin(message: Message):
    print(message.from_user.id)
    if message.from_user.id in ADMIN:
        await message.answer('Надпись для админа', reply_markup=admin_kb())