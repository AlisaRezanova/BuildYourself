import os
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from models.create_db import User, Habits, LogOfHabits, Achievements, LogOfAch
from datetime import date


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def deeleetee():
    with Session() as session:
        stmt = (delete(User).where(User.id == 2))
        session.execute(
            stmt)
        session.commit()
        all_users = session.query(User).all()
        for user in all_users:
            print(user.id, user.sex, user.tg_id, user.date_of_reg, user.num_friends)


def show():
    with Session() as session:
        current_user = session.query(User).filter(User.tg_id == 000).first()
        print(current_user)


def filling_habits():
    with Session() as session:
        hab1 = Habits(
            user_id = 1,
            name = 'Бег по утрам'
        )

        hab2 = Habits(
            user_id=1,
            name='Бег по вечерам'
        )

        hab3 = Habits(
            user_id=1,
            name='Не есть сладкое'
        )

        session.add_all([hab1, hab2, hab3])
        session.commit()

        all_habits = session.query(Habits).all()
        for habit in all_habits:
            print(habit.id, habit.user_id, habit.name)


def filling_log_of_habits():
    with Session() as session:
        log1 = LogOfHabits(
            habit_id=1,
            date_of_mark=date(2025, 10, 22)
        )
        log2 = LogOfHabits(
            habit_id=1,
            date_of_mark=date(2025, 10, 24)
        )
        session.add_all([log1, log2])
        session.commit()


def filling_ach():
    with Session() as session:
        ach1 = Achievements(
            name='Первый пользователь',
            description='Первый пользователь нашего ТГ бота!!!'
        )
        ach2 = Achievements(
            name='Первооткрыватель',
            description='Добавление своей первой привычки!!!'
        )
        session.add_all([ach1, ach2])
        session.commit()
        ach = session.query(Achievements).all()
        print([i.name for i in ach])


def filling_log_ach():
    with Session() as session:
        log1 = LogOfAch(
            ach_id=1,
            user_id=1
        )
        log2 = LogOfAch(
            ach_id=2,
            user_id=1
        )
        session.add_all([log1, log2])
        session.commit()

filling_log_ach()
