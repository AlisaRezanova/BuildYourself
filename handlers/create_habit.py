from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.main_menu_kb import main_menu_kb
from keyboards.duration_choice_kb import duration_choice_kb
from keyboards.notification_need_kb import notification_choice_kb
from keyboards.confirm_habit_kb import confirm_habit_kb
from keyboards.habit_type_kb import habit_type_kb
from keyboards.friends_choice_kb import friends_choice_kb
from models.requests_to_habits import create_new_habit, get_all_habits_by_user_id, update_habit_duration, update_habit_notification
from models.requests_to_friends import get_friends_list_with_names
from models.requests_to_friendshabits import create_coop_habit_invite
from handlers.earn_achievement import EarnAchievement
from models.requests_to_users import get_user_id_by_tg_id

router = Router()


class HabitStates:
    waiting_for_habit_name = "waiting_for_habit_name"
    waiting_for_habit_type = "waiting_for_habit_type"
    waiting_for_friend_choice = "waiting_for_friend_choice"
    waiting_for_duration_choice = "waiting_for_duration_choice"
    waiting_for_notification_choice = "waiting_for_notification_choice"
    waiting_for_confirmation = "waiting_for_confirmation"

@router.message(F.text == 'Создание новой привычки')
async def create_new_habit_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(HabitStates.waiting_for_habit_name)
    await message.answer('Введите название привычки:', reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(HabitStates.waiting_for_habit_name))
async def process_habit_name(message: Message, state: FSMContext):
    habit_name = message.text.strip()

    if not habit_name:
        await message.answer('Название привычки не может быть пустым')
        return

    if len(habit_name) > 100:
        await message.answer('Название привычки слишком длинное (максимум 100 символов)')
        return

    await state.update_data(habit_name=habit_name)

    data = await state.get_data()
    if data.get('duration_text') and data.get('notification_text'):
        await show_summary(message, state, data)
    elif data.get('duration_text'):
        await state.set_state(HabitStates.waiting_for_notification_choice)
        await message.answer('Нужны ли уведомления?', reply_markup=notification_choice_kb())
    else:
        await state.set_state(HabitStates.waiting_for_habit_type)
        await message.answer('Выберите тип привычки:', reply_markup=habit_type_kb())


@router.message(StateFilter(HabitStates.waiting_for_habit_type))
async def process_habit_type(message: Message, state: FSMContext):
    if message.text not in ["Обычная привычка", "Совместная привычка"]:
        await message.answer('Пожалуйста, выберите тип привычки из предложенных вариантов')
        return

    data = await state.get_data()

    if message.text == "Обычная привычка":
        await state.update_data(habit_type="ordinary", friend_id=None, friend_name=None)
        await state.set_state(HabitStates.waiting_for_duration_choice)
        await message.answer('Выберите длительность привычки:', reply_markup=duration_choice_kb())

    else:
        friends = await get_friends_list_with_names(message.from_user.id)
        if not friends:
            await message.answer('У вас пока нет друзей для создания совместной привычки. Сначала добавьте друзей!',
                                 reply_markup=main_menu_kb())
            await state.clear()
            return

        await state.update_data(habit_type="cooperative", friends_list=friends)
        await state.set_state(HabitStates.waiting_for_friend_choice)
        await message.answer('Выберите друга для совместной привычки:', reply_markup=friends_choice_kb(friends))


@router.callback_query(StateFilter(HabitStates.waiting_for_friend_choice), F.data.startswith('friend_'))
async def process_friend_choice(callback_query: CallbackQuery, state: FSMContext):
    friend_id = int(callback_query.data.split('_')[1])

    data = await state.get_data()
    friends_list = data.get('friends_list', [])

    # Находим выбранного друга
    selected_friend = next((f for f in friends_list if f['id'] == friend_id), None)

    if not selected_friend:
        await callback_query.answer('Друг не найден')
        return

    await state.update_data(
        my_id=get_user_id_by_tg_id(callback_query.from_user.id),
        receiver_id=selected_friend['tg_id'],
        friend_id=friend_id,
        friend_name=selected_friend['name']
    )

    await callback_query.message.edit_text(f'Выбран друг: {selected_friend["name"]}')

    data = await state.get_data()
    if data.get('duration_text') and data.get('notification_text'):
        await show_summary(callback_query.message, state, data)
    elif data.get('duration_text'):
        await state.set_state(HabitStates.waiting_for_notification_choice)
        await callback_query.message.answer('Нужны ли уведомления?', reply_markup=notification_choice_kb())
    else:
        await state.set_state(HabitStates.waiting_for_duration_choice)
        await callback_query.message.answer('Выберите длительность привычки:', reply_markup=duration_choice_kb())

@router.callback_query(StateFilter(HabitStates.waiting_for_friend_choice), F.data == 'cancel_coop')
async def cancel_coop_habit(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text('Создание совместной привычки отменено')
    await callback_query.message.answer('Главное меню:', reply_markup=main_menu_kb())

@router.message(StateFilter(HabitStates.waiting_for_duration_choice), F.text.in_(['1 неделя', '2 месяца', '6 месяцев', '1 год']))
async def process_duration_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('habit_id')
    habit_name = data.get('habit_name')

    duration_map = {
        '1 неделя': 7,
        '2 месяца': 60,
        '6 месяцев': 180,
        '1 год': 365
    }

    duration_days = duration_map[message.text]

    await state.update_data(duration_days=duration_days, duration_text=message.text)
    data = await state.get_data()
    if data.get('notification_text'):
        await show_summary(message, state, data)
    else:
        await state.set_state(HabitStates.waiting_for_notification_choice)
        await message.answer(f'Длительность привычки установлена: {message.text}')
        await message.answer('Нужны ли уведомления?', reply_markup=notification_choice_kb())

@router.message(StateFilter(HabitStates.waiting_for_notification_choice), F.text.in_(['Уведомления нужны', 'Уведомления не нужны']))
async def process_notification_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('habit_id')
    habit_name = data.get('habit_name')
    duration_text = data.get('duration_text')

    notification = True if message.text == 'Уведомления нужны' else False
    update_habit_notification(habit_id, notification)

    notification_text = 'включены' if notification else 'выключены'
    await state.update_data(
        notification=notification,
        notification_text=notification_text
    )

    data = await state.get_data()
    await show_summary(message, state, data)

@router.message(StateFilter(HabitStates.waiting_for_confirmation))
async def process_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text == "Все правильно":


        habit_id = create_new_habit(
            message.from_user.id,
            data.get('my_id'),
            get_user_id_by_tg_id(data.get('receiver_id')),
            data.get('habit_name'),
            data.get('duration_days'),
            data.get('notification'),
            data.get('habit_type'),
            data.get('friend_id')
        )

        if data.get('habit_type') == 'cooperative' and data.get('friend_id'):
            rec_id = get_user_id_by_tg_id(data.get('receiver_id'))
            create_coop_habit_invite(habit_id, data.get('friend_id'), rec_id, data.get('my_id'))

            await message.answer(
                f"✅ Приглашение на совместную привычку отправлено {data.get('friend_name')}!",
                reply_markup=main_menu_kb()
            )
        else:
            await message.answer(
                f"Привычка \"{data.get('habit_name')}\" успешно создана!",
                reply_markup=main_menu_kb()
            )

        awarded_achievements = EarnAchievement.check_habit_achievements(message.from_user.id)

        for achievement_id in awarded_achievements:
            achievement = EarnAchievement.get_achievement_by_id(achievement_id)
            achievement_image = EarnAchievement.get_achievement_image(achievement)

            if achievement_image:
                await message.answer_photo(
                    achievement_image,
                    caption=f'🎉 Вы получили награду "{achievement.name}"!\n📝 {achievement.description}'
                )
            else:
                await message.answer(f'🎉 Вы получили награду "{achievement.name}"!')
                await message.answer(f'{achievement.description}')

        await message.answer(
            f"Привычка \"{data.get('habit_name')}\" успешно создана!",
            reply_markup=main_menu_kb()
        )
        await state.clear()

    elif message.text == "Изменить название":
        await state.set_state(HabitStates.waiting_for_habit_name)
        await message.answer("Введите новое название привычки:", reply_markup=ReplyKeyboardRemove())

    elif message.text == "Изменить длительность":
        await state.set_state(HabitStates.waiting_for_duration_choice)
        await message.answer("Выберите длительность привычки:", reply_markup=duration_choice_kb())

    elif message.text == "Изменить статус уведомлений":
        await state.set_state(HabitStates.waiting_for_notification_choice)
        await message.answer("Нужны ли уведомления?", reply_markup=notification_choice_kb())


async def show_summary(message: Message, state: FSMContext, data: dict):
    habit_type = data.get('habit_type', 'ordinary')

    if habit_type == 'ordinary':
        type_text = "Обычная привычка"
    else:
        friend_name = data.get('friend_name')
        type_text = f"Совместная с {friend_name}"

    summary_message = (
        f"Проверьте информацию о привычке:\n\n"
        f"Название: {data.get('habit_name')}\n"
        f"Тип: {type_text}\n"
        f"Длительность: {data.get('duration_text')}\n"
        f"Уведомления: {data.get('notification_text')}\n\n"
        f"Всё правильно?"
    )

    await message.answer(summary_message, reply_markup=confirm_habit_kb())
    await state.set_state(HabitStates.waiting_for_confirmation)