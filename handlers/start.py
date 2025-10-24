from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from decouple import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.start_kb import start_kb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.session_local import Session
from models.create_db import *


bot = Bot(token = config('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

router = Router()

@router.message(Command("start"))
async def get_start(message: Message):
    await message.answer('Укажите свой пол', reply_markup=start_kb())


@router.message(F.text == 'Мужчина')
async def handle_man(message: Message):
    with Session() as session:
        new_user = User(
            sex='M',
            tg_id=message.from_user.id,
        )
        session.add(new_user)
        session.commit()

        all_users = session.query(User).all()
        for user in all_users:
            print(user.id, user.sex, user.tg_id, user.date_of_reg, user.num_friends)
    await message.answer('...')


@router.message(F.text == 'Женщина')
async def handle_man(message: Message):
    with Session() as session:
        new_user = User(
            sex='F',
            tg_id=message.from_user.id,
        )
        session.add(new_user)
        session.commit()

        all_users = session.query(User).all()
        for user in all_users:
            print(user.id, user.sex, user.tg_id, user.date_of_reg, user.num_friends)
    await message.answer('...')
