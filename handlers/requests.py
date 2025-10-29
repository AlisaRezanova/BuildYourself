from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import Message

from keyboards.all_requests_kb import all_requests_kb

router = Router()


@router.message(F.text=='Запросы')
async def get_all_requests(message: Message):
    await message.answer('...', reply_markup=all_requests_kb())