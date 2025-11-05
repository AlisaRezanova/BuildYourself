import os
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from models.create_db import User
from models.exceptions import UserNotFoundError
from datetime import date, timedelta


db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def get_user_id_by_tg_id(tg_id: int) -> int:
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).first()
        if not user:
            raise UserNotFoundError
        user_id = user.id
        return user_id


def get_tg_id_by_id(us_id: int) -> int:
    with Session() as session:
        user = session.query(User).filter(User.id==us_id).first()
        if not user:
            raise UserNotFoundError
        return user.tg_id


def get_all_users_to_admin() -> list:
    with Session() as session:
        users = session.query(User).all()
        return users


def get_short_info_about_user_by_id(user_id: id) -> User:
    with Session() as session:
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
    with Session() as session:
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
    with Session() as session:
        users = session.query(User).filter(User.date_of_reg >= recent_week).all()
        return len(users)


def get_count_new_users_by_month() -> int:
    recent_week = date.today() - timedelta(days=30)
    with Session() as session:
        users = session.query(User).filter(User.date_of_reg >= recent_week).all()
        return len(users)


def get_count_new_users_by_year() -> int:
    recent_week = date.today() - timedelta(days=365)
    with Session() as session:
        users = session.query(User).filter(User.date_of_reg >= recent_week).all()
        return len(users)



