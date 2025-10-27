import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import Habits
from .requests_to_users import get_user_id_by_tg_id

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_all_habits_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        all_habits = session.query(Habits).filter(Habits.user_id==user_id).all()
        return all_habits



