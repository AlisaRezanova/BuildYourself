import os
from itertools import count

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import Habits, User
from models.requests_to_users import get_user_id_by_tg_id


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_all_habits_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        all_habits = session.query(Habits).filter(Habits.user_id==user_id).all()
        return all_habits


def get_habit_by_name(name: str, tg_id: int):
    with Session() as session:

        user_id = get_user_id_by_tg_id(tg_id)
        habit = session.query(Habits).filter(Habits.user_id==user_id).filter(Habits.name.ilike(f"%{name}%")).first()
        if habit:
            return habit
        return None


def get_index_habit(habit, habits):
    for h in range(len(habits)):
        if habits[h].name == habit.name:
            return h
    return 0


def get_name_habit_by_id(habit_id: int) -> str:
    with Session() as session:
        habit = session.query(Habits).filter(Habits.id==habit_id).first()
        if not habit:
            raise ValueError('Error')
        return habit.name

def create_new_habit(tg_id: int, habit_name: str) -> int:
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).first()
        if not user:
            raise ValueError('Error: User not found')

        new_habit = Habits(
            user_id = user.id,
            name = habit_name,
            day_len = 14,
            notification = True,
            is_coop = 'no'
        )

        session.add(new_habit)
        session.commit()

        return new_habit.id

def get_habit_by_id(habit_id: int) -> Habits:
    with Session() as session:
        habit = session.query(Habits).filter(Habits.id == habit_id).first()
        if not habit:
            raise ValueError('Error: Habit not found')
        return habit

def update_habit_duration(habit_id: int, duration_days: int) -> None:
    with Session() as session:
        habit = session.query(Habits).filter(Habits.id == habit_id).first()
        if habit:
            habit.day_len = duration_days
            session.commit()

def update_habit_notification(habit_id: int, notification: bool) -> None:
    with Session() as session:
        habit = session.query(Habits).filter(Habits.id == habit_id).first()
        if habit:
            habit.notification = notification
            session.commit()


def get_count_habit_by_id(user_id: int) -> int:
    with Session() as session:
        habits = session.query(Habits).filter(Habits.user_id==user_id).all()
        return len(habits)

def get_habits_with_notifications() -> list:
    with Session() as session:
        habits = session.query(Habits).filter(Habits.notification == True).all()
        return habits





