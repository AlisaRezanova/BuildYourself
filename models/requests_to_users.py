import os
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from create_db.User import User
from models.exceptions import UserNotFoundError
from datetime import date, timedelta
from .session import session


def get_user_id_by_tg_id(tg_id: int) -> int:
    print(tg_id)
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        raise UserNotFoundError
    user_id = user.id
    return user_id


def get_tg_id_by_id(us_id: int) -> int:
    user = session.query(User).filter(User.id==us_id).first()
    if not user:
        raise UserNotFoundError
    return user.tg_id


def get_all_users_to_admin() -> list:
    users = session.query(User).all()
    return users


def get_short_info_about_user_by_id(user_id: id) -> User:
    user = session.query(User).filter(User.id==user_id).first()
    return user


def get_more_information_about_user_by_id(user_id:int) -> dict:
    from models.requests_to_habits import get_count_habit_by_id
    from models.requests_to_log_ach import get_count_ach_by_id
    count_ach = get_count_ach_by_id(user_id)
    count_hab = get_count_habit_by_id(user_id)
    info = {'count_ach': count_ach, 'count_hab': count_hab}
    return info


def delete_user_by_id(user_id: int) -> bool:
    try:
        stmt = (delete(User).where(User.id==user_id))
        session.execute(
            stmt)
        session.commit()
        return True
    except:
        return False


def get_count_new_users_by_week() -> int:
    recent_week = date.today() - timedelta(days=7)
    users = session.query(User).filter(User.date_of_reg >= recent_week).all()
    return len(users)


def get_count_new_users_by_month() -> int:
    recent_week = date.today() - timedelta(days=30)
    users = session.query(User).filter(User.date_of_reg >= recent_week).all()
    return len(users)


def get_count_new_users_by_year() -> int:
    recent_week = date.today() - timedelta(days=365)
    users = session.query(User).filter(User.date_of_reg >= recent_week).all()
    return len(users)


def get_user_by_id(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user