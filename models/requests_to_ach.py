import os
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from models.create_db import Achievements, LogOfAch
from models.exceptions import AchNotFoundError
from models.requests_to_users import get_user_id_by_tg_id


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_description_about_ach(ach_id: int):
    with Session() as session:
        print(ach_id)
        ach = session.query(Achievements).filter(Achievements.id == ach_id).first()
        img = ach.img
        description = ach.description
        return img, description


def get_all_ach() -> list:
    with Session() as session:
        ach = session.query(Achievements).all()
        return ach

def award_achievement(user_id: int, achievement_id: int) -> bool:
    with Session() as session:
        existing = session.query(LogOfAch).filter(and_(LogOfAch.user_id == user_id, LogOfAch.ach_id == achievement_id)).first()
        if existing:
            return False

        new_log = LogOfAch(
            user_id = user_id,
            ach_id = achievement_id
        )

        session.add(new_log)
        session.commit()
        return True

def get_achievement_by_id(achievement_id: int) -> Achievements:
    with Session() as session:
        achievement = session.query(Achievements).filter(Achievements.id == achievement_id).first()
        return achievement