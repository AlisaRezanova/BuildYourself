from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards.main_menu_kb import main_menu_kb
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(F.text == 'Главное меню')
async def get_main_menu(message: Message, state: FSMContext):
    await state.clear()
    photo = FSInputFile("img/main_menu.png")
    await message.answer_photo(photo, caption="Главное меню", reply_markup=main_menu_kb())



@router.callback_query(F.data == 'main menu')
async def get_main_menu_inline(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.reply('...', reply_markup=main_menu_kb())


