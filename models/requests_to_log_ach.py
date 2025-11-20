import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import Achievements, LogOfAch
from models.exceptions import AchNotFoundError
from models.requests_to_users import get_user_id_by_tg_id


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_ach_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = get_user_id_by_tg_id(tg_id)
        achievements = session.query(LogOfAch).filter(LogOfAch.user_id==user_id).all()
        return achievements


def get_ach_by_id(ach_id: int) -> Achievements:
    with Session() as session:
        ach = session.query(Achievements).filter(Achievements.id==ach_id).first()
        if ach:
            return ach
        else:
            raise AchNotFoundError('Achievement Not Found')


def get_count_ach_by_id(user_id: int) -> int:
    with Session() as session:
        ach = session.query(LogOfAch).filter(LogOfAch.user_id==user_id).all()
        return len(ach)
