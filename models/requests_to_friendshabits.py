import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import Habits, FriendsHabits
from .requests_to_friends import get_all_friends_by_user_id
from .requests_to_users import get_user_id_by_tg_id


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_all_requests_in_habits(tg_id: int):
    friends = get_all_friends_by_user_id(tg_id)
    friends_id = [fr.id for fr in friends]
    with Session() as session:
        list_coop_habits = session.query(FriendsHabits).filter(FriendsHabits.friend_id.in_(friends_id)).filter(FriendsHabits.status=='waiting_habit').all()
        return list_coop_habits


def update_status_coop_habit(habit_id: int, new_status: str) -> bool:
    with Session() as session:
        try:
            coop_habit = session.query(FriendsHabits).filter(FriendsHabits.id==habit_id).first()
            coop_habit.status = new_status
            session.commit()
            return True
        except Exception as e:
            raise ValueError(e)

