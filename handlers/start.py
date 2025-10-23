from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from decouple import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery


bot = Bot(token = config('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

router = Router()

@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer('Встречающая надпись!')

