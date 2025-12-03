import asyncio
from datetime import datetime, time, timedelta
from aiogram import Bot
from models.requests_to_habits import get_habits_with_notifications
from models.requests_to_users import get_tg_id_by_id

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running = False

    async def send_daily_notifications(self):
        try:
            print(f"Отправка уведомлений в {datetime.now()}")
            habits = get_habits_with_notifications()
            print(f"Найдено {len(habits)} привычек с уведомленимяи")

            for habit in habits:
                try:
                    tg_id = get_tg_id_by_id(habit.user_id)
                    await self.bot.send_message(
                        tg_id,
                        f"Напоминание о привычке: {habit.name}\n"
                        f"Не забудьте выполнить привычку сегодня! "
                    )
                    print(f"Уведомление отправлено пользователю {tg_id}")
                except Exception as e:
                    print(f" Ошибка отправки пользователю {habit.user_id}: {e}")
        except Exception as e:
            print(f" Ошибка в send_daily_notifications: {e}")

    async def schedule_daily_notifications(self):
        self.is_running = True
        print("Сервис уведомлений запущен")

        while self.is_running:
            try:
                now = datetime.now()
                target_time = time(9, 59)  # натсройка времени

                next_run = datetime.combine(now.date(), target_time)
                if now >= next_run:
                    next_run += timedelta(days=1)

                wait_seconds = (next_run - now).total_seconds()
                print(f"Следующее уведомление через {wait_seconds:.0f} секунд")

                await asyncio.sleep(wait_seconds)

                if self.is_running:
                    await self.send_daily_notifications()

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Ошибка в планировщике: {e}")
                await asyncio.sleep(60)

    def stop(self):
        self.is_running = False
        print("Сервис уведомлений остановлен")

