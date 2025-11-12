import asyncio
from datetime import datetime, timedelta, date, time
from aiogram import Bot
from fontTools.misc.plistlib import end_date
from models.requests_to_habits import get_expired_habits, get_first_mark_date, get_all_habits
from models.requests_to_log_habits import get_habit_marks_count, delete_habit
from models.requests_to_users import get_tg_id_by_id

class HabitCleanupService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running = False

    async def check_and_cleanup_expired_habits(self):
        """Проверяет и удаляет истекшие привычки"""
        print(f"🧹 Проверка истекших привычек в {datetime.now()}")

        expired_habits = get_expired_habits()
        print(f"Найдено {len(expired_habits)} истекших привычек")

        # ОТЛАДКА: выводим информацию о каждой привычке
        all_habits = get_all_habits()  # нужно создать эту функцию
        print(f"Всего привычек в БД: {len(all_habits)}")

        for habit in all_habits:
            first_mark = get_first_mark_date(habit.id)
            if first_mark:
                end_date = first_mark + timedelta(days=habit.day_len)
                print(f"Привычка {habit.id}: {habit.name}")
                print(f"  Первая отметка: {first_mark}")
                print(f"  Длительность: {habit.day_len} дней")
                print(f"  Конец срока: {end_date}")
                print(f"  Истекла: {datetime.now() >= end_date}")

        for habit in expired_habits:
            try:
                tg_id = get_tg_id_by_id(habit.user_id)
                marks_count = get_habit_marks_count(habit.id)
                first_mark_date = get_first_mark_date(habit.id)

                start_date_str = first_mark_date.strftime("%d.%m.%Y")
                end_date = first_mark_date + timedelta(days=habit.day_len)
                end_date_str = end_date.strftime("%d.%m.%Y")

                if marks_count >= habit.day_len:
                    await self.bot.send_message(
                        tg_id,
                        f"🎉 Поздравляем! Вы успешно выполнили привычку:\n"
                        f"\"{habit.name}\"\n"
                        f"Привычка завершена и удалена."
                    )
                else:
                    await self.bot.send_message(
                        tg_id,
                        f"Привычка \"{habit.name}\" истекла.\n"
                        f"За {habit.day_len} дней вы сделали только {marks_count} из {habit.day_len} отметок.\n"
                        f"Привычка удалена. Попробуйте снова!"
                    )

                delete_habit(habit.id)
            except Exception as e:
                print(f"Ошибка боработки привычки {habit.id}: {e}")

    async def schedule_cleanup(self):
        self.is_running = True
        while self.is_running:
            now = datetime.now()
            target_time = time(11, 49)  # Время проверки

            next_run = datetime.combine(now.date(), target_time)
            if now >= next_run:
                next_run += timedelta(days=1)

            wait_seconds = (next_run - now).total_seconds()
            print(f"Следующая проверка привычек через {wait_seconds:.0f} секунд")

            await asyncio.sleep(wait_seconds)
            if self.is_running:
                await self.check_and_cleanup_expired_habits()

    def stop(self):
        self.is_running = False


