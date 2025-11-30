import os
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from create_db.create_db import Achievements, LogOfAch
from .session import session


def get_description_about_ach(ach_id: int):
    print(ach_id)
    ach = session.query(Achievements).filter(Achievements.id == ach_id).first()
    img = ach.img
    description = ach.description
    return img, description


def get_all_ach() -> list:
    ach = session.query(Achievements).all()
    return ach

def award_achievement(user_id: int, achievement_id: int) -> bool:
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
    achievement = session.query(Achievements).filter(Achievements.id == achievement_id).first()
    return achievement