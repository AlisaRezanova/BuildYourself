import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.create_db import Achievements, User, LogOfAch
from models.exceptions import UserNotFoundError

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_ach_by_user_id(tg_id: int) -> list:
    with Session() as session:
        user_id = session.query(User).filter(User.tg_id==tg_id).first().id
        if not user_id:
            raise UserNotFoundError
        achievements = session.query(LogOfAch).filter(LogOfAch.user_id==user_id).all()
        return achievements


def get_ach_by_id(ach_id: int):
    with Session() as session:
        ach = session.query(Achievements).filter(Achievements.id==ach_id).first()
        if ach:
            return ach
        else:
            raise ValueError('Achievement Not Found')