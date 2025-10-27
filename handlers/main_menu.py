from aiogram import F, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.main_menu_kb import main_menu_kb
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(F.text == 'Главное меню')
async def get_main_menu(message:Message, state: FSMContext):
    await message.answer('...', reply_markup=main_menu_kb())


@router.callback_query(F.data == 'main menu')
async def get_main_menu_inline(callback_query: CallbackQuery):
    await callback_query.message.reply('...', reply_markup=main_menu_kb())


