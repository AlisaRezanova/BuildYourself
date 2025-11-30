import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db.create_db import Habits, User
from models.requests_to_log_habits import get_first_mark_date
from models.requests_to_users import get_user_id_by_tg_id
from models.requests_to_friendshabits import create_coop_habit_invite
from datetime import datetime, timedelta
from .session import session



def get_all_habits_by_user_id(tg_id: int) -> list:
    user_id = get_user_id_by_tg_id(tg_id)
    all_habits = session.query(Habits).filter(Habits.user_id==user_id).all()
    return all_habits


def get_habit_by_name(name: str, tg_id: int):
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
    habit = session.query(Habits).filter(Habits.id==habit_id).first()
    if not habit:
        raise ValueError('Error')
    return habit.name

def create_new_habit(tg_id: int,  sender_id, receiver_id, habit_name: str, duration_days: int = 14, notification: bool = True, habit_type='ordinary',
                     friendship_id=None) -> int:
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        raise ValueError('Error: User not found')

    new_habit = Habits(
        user_id = user.id,
        name = habit_name,
        day_len = duration_days,
        notification = notification,
        is_coop='yes' if habit_type == 'cooperative' else 'no'
    )

    session.add(new_habit)
    session.commit()

    if habit_type == 'cooperative' and friendship_id:
            create_coop_habit_invite(new_habit.id, friendship_id, receiver_id, sender_id)

    return new_habit.id



def get_habit_by_id(habit_id: int) -> Habits:
    habit = session.query(Habits).filter(Habits.id == habit_id).first()
    if not habit:
        raise ValueError('Error: Habit not found')
    return habit

def update_habit_duration(habit_id: int, duration_days: int) -> None:
    habit = session.query(Habits).filter(Habits.id == habit_id).first()
    if habit:
        habit.day_len = duration_days
        session.commit()

def update_habit_notification(habit_id: int, notification: bool) -> None:
    habit = session.query(Habits).filter(Habits.id == habit_id).first()
    if habit:
        habit.notification = notification
        session.commit()


def get_count_habit_by_id(user_id: int) -> int:
    habits = session.query(Habits).filter(Habits.user_id==user_id).all()
    return len(habits)


def get_habits_with_notifications() -> list:
    habits = session.query(Habits).filter(Habits.notification == True).all()
    return habits


def get_expired_habits() -> list:
    now = datetime.now()
    habits = session.query(Habits).all()
    expired_habits = []

    for habit in habits:
        first_mark_date = get_first_mark_date(habit.id)

        if first_mark_date:
            end_date = first_mark_date + timedelta (days=habit.day_len)
            if now >= end_date:
                expired_habits.append(habit)

    return expired_habits


def get_all_habits() -> list:
    habits = session.query(Habits).all()
    return habits

