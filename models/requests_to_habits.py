import os
from sqlalchemy import create_engine, func, or_, and_
from sqlalchemy.orm import sessionmaker
from models.create_db import Habits
from .requests_to_users import get_user_id_by_tg_id
from sqlalchemy.sql.operators import ilike_op,like_op


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




